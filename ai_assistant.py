
import json
import os
import re
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from anthropic import Anthropic

from prompts import (
    SYSTEM_PROMPT,
    SUMMARY_PROMPT,
    build_user_prompt,
    build_summary_prompt
)

from memory import ConversationMemory
from rag import retrieve_knowledge


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=API_KEY) if API_KEY else None

CLAUDE_MODEL = "claude-sonnet-4-6"


# ==========================================
# 2. IDENTIFY COMPANY FROM CONVERSATION
# ==========================================

def identify_company(question, history=None):

    history = history or []

    messages = [
        message["content"]
        for message in history
        if message["role"] == "user"
    ]

    messages.append(question)

    pattern = (
        r"\b(?:at|with|to)\s+"
        r"([A-Za-z0-9][A-Za-z0-9&.'’ -]{0,60}?)"
        r"(?=\s*[,.!?;]|\s+(?:for|as|and)\s+|$)"
    )

    for message in reversed(messages):

        matches = re.findall(
            pattern,
            message,
            re.IGNORECASE
        )

        if matches:

            company = matches[-1].strip()

            ignored = [
                "the company",
                "this company",
                "an interview",
                "the interview"
            ]

            if company.lower() not in ignored:
                return company

    return None


# ==========================================
# 3. EXTRACT JSON FROM CLAUDE RESPONSE
# ==========================================

def extract_json(response_text):

    if not isinstance(response_text, str):
        return None

    response_text = response_text.strip()

    # Remove Markdown code fences
    response_text = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response_text,
        flags=re.IGNORECASE
    )

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:

        # Attempt to extract a JSON object
        start = response_text.find("{")
        end = response_text.rfind("}")

        if start != -1 and end != -1 and end > start:

            try:
                return json.loads(
                    response_text[start:end + 1]
                )

            except json.JSONDecodeError:
                return None

    return None


# ==========================================
# 4. VALIDATE CLAUDE RESPONSE
# ==========================================

def validate_response(response):

    data = extract_json(response)

    if not isinstance(data, dict):
        return None

    if not isinstance(data.get("reply"), str):
        return None

    if not data["reply"].strip():
        return None

    if "suggested_action" not in data:
        return None

    return data


# ==========================================
# 5. ASK CLAUDE USING REAL API AND RAG
# ==========================================

def ask_claude(question, applications=None, history=None):

    if client is None:

        return {
            "reply": (
                "Claude API key is missing. "
                "Please check your .env file and ensure "
                "ANTHROPIC_API_KEY is configured."
            ),
            "suggested_action": None
        }

    history = history or []

    try:

        # Retrieve relevant information from knowledge base
        try:
            relevant_knowledge = retrieve_knowledge(question)

        except Exception as rag_error:

            print("Knowledge retrieval error:", rag_error)
            relevant_knowledge = ""

        # Retrieve relevant information from knowledge.txt
        relevant_knowledge = retrieve_knowledge(question)

        # Build the user's prompt, including application information
        user_prompt = build_user_prompt(
            question,
            applications,
            None
        )

        complete_prompt = f"""
{user_prompt}
# ==========================================
# 5. CONNECT AI WITH MEMORY
# ==========================================

RELEVANT KNOWLEDGE RETRIEVED FROM CAREERTRACK AI:

{relevant_knowledge}

Use the retrieved knowledge when it is relevant.
Use conversation history to understand previous questions.
Do not invent job applications or personal information.

Return ONLY valid JSON in this exact format:

{{
    "reply": "Your helpful answer here",
    "suggested_action": null
}}
"""

        # Include previous conversation messages
        messages = []

        for message in history:

            if message["role"] in ("user", "assistant"):

                messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })

        # Add the current question
        messages.append({
            "role": "user",
            "content": complete_prompt
        })

        # Retry invalid responses
        for attempt in range(2):

            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                messages=messages
            )

            # Extract Claude's text response
            response_text = "\n".join(
                block.text
                for block in response.content
                if block.type == "text"
            )

            result = validate_response(response_text)

            if result is not None:
                return result

            print(
                f"Invalid Claude response. "
                f"Retry {attempt + 1}..."
            )

        return {
            "reply": (
                "Unable to generate a valid response. "
                "Please try asking your question again."
            ),
            "suggested_action": None
        }

    except Exception as error:

        print("Claude API error:", error)

        return {
            "reply": (
                "Sorry, I could not connect to Claude. "
                "Please check your API key, internet connection, "
                "model access and available API credits."
            ),
            "suggested_action": None
        }


# ==========================================
# 6. CONNECT CLAUDE WITH CONVERSATION MEMORY
# ==========================================

def ask_with_memory(question, memory, applications=None):

    # Retrieve previous conversation
    history = memory.get_history()

    # Save the current user question
    memory.add_message("user", question)

    # Send question, applications and history to Claude
    result = ask_claude(
        question,
        applications,
        history
    )

    # Save Claude's response
    memory.add_message(
        "assistant",
        result["reply"]
    )

    # Save conversation to JSON
    memory.save()

    return result


# ==========================================
# 7. VALIDATE SESSION SUMMARY
# ==========================================

def validate_summary(response):

    data = extract_json(response)

    if not isinstance(data, dict):
        return None

    if not isinstance(data.get("summary"), str):
        return None

    if not data["summary"].strip():
        return None

    required_lists = [
        "companies_discussed",
        "positions_discussed",
        "topics_discussed",
        "key_advice",
        "suggested_next_steps"
    ]

    for field in required_lists:

        if not isinstance(data.get(field), list):
            return None

        if not all(
            isinstance(item, str)
            for item in data[field]
        ):
            return None

    return data


# ==========================================
# 8. GENERATE REAL CLAUDE SESSION SUMMARY
# ==========================================

def generate_session_summary(history):

    if client is None:

        print("Claude API key is missing.")
        return None

    try:

        summary_prompt = build_summary_prompt(history)

        complete_summary_prompt = f"""
{summary_prompt}

Return ONLY valid JSON using this structure:

{{
    "summary": "A short summary of the conversation",
    "companies_discussed": [],
    "positions_discussed": [],
    "topics_discussed": [],
    "key_advice": [],
    "suggested_next_steps": []
}}

Do not invent information that was not discussed.
"""

        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1500,
            system=SUMMARY_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": complete_summary_prompt
                }
            ]
        )

        response_text = "".join(
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SUMMARY_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": summary_prompt
                }
            ]
        )

        summary_prompt = build_summary_prompt(history)

        complete_summary_prompt = f"""
{summary_prompt}

Return ONLY valid JSON using this structure:

{{
    "summary": "A short summary of the conversation",
    "companies_discussed": [],
    "positions_discussed": [],
    "topics_discussed": [],
    "key_advice": [],
    "suggested_next_steps": []
}}

Do not invent information that was not discussed.
"""

        for attempt in range(2):

            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=2048,
                system=SUMMARY_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": complete_summary_prompt
                    }
                ]
            )

            response_text = "\n".join(
                block.text
                for block in response.content
                if block.type == "text"
            )

            result = validate_summary(response_text)

            if result is not None:
                return result

            print(
                f"Invalid summary response. "
                f"Retry {attempt + 1}..."
            )

        print("Claude returned an invalid summary format.")
        return None

    except Exception as error:

        print("Summary API error:", error)
        return None

        print("Claude returned an invalid summary format.")
        return None

    except Exception as error:

        print("Summary API error:", error)
        return None


# ==========================================
# 9. SAVE COMPLETE SESSION
# ==========================================

def finalize_session(memory):

    history = memory.get_history()

    if not history:

        print("No conversation available to summarize.")
        return None

    print("\nGenerating final conversation summary...")

    summary = generate_session_summary(history)

    if summary is None:

        print("Unable to generate a valid summary.")
        return None

    # Create sessions folder
    session_folder = (
        Path(__file__).resolve().parent / "sessions"
    )

    session_folder.mkdir(exist_ok=True)

    # Generate dated filename
    current_date = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    filename = (
        f"session_{current_date}_{memory.session_id}.json"
    )

    file_path = session_folder / filename

    session_data = {
        "session_id": memory.session_id,
        "date": current_date,
        "conversation_history": history,
        "summary": summary
    }

    with open(file_path, "w", encoding="utf-8") as file:

        json.dump(
            session_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nSESSION SUMMARY")

    print(
        json.dumps(summary, indent=4)
    )

    print("\nSession saved successfully!")
    print("File:", file_path)

    return file_path


# ==========================================
# 10. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    memory = ConversationMemory(
        session_id="careertrack_default"
    )

    memory.load()

    print("\nWelcome to CareerTrack AI!")
    print("Type 'exit' to end your session.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() == "exit":

            finalize_session(memory)

            print("\nThank you for using CareerTrack AI!")

            break

        if not question:

            print("Please enter a question.")
            continue

        result = ask_with_memory(
            question,
            memory
        )

        print("\nCareerTrack AI:")
        print(result["reply"])
        print()
