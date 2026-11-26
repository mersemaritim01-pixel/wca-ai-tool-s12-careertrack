
import json
import re
import os
from pathlib import Path
from datetime import datetime

from prompts import (
    SYSTEM_PROMPT,
    SUMMARY_PROMPT,
    build_user_prompt,
    build_summary_prompt
)

from memory import ConversationMemory
from anthropic import Anthropic
from dotenv import load_dotenv


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=API_KEY) if API_KEY else None

MODEL = "claude-sonnet-4-6"


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

    for message in reversed(messages):

        pattern = (
            r"\b(?:at|with|to)\s+"
            r"([A-Za-z0-9][A-Za-z0-9&.'’ -]{0,60}?)"
            r"(?=\s*[,.!?;]|\s+(?:for|as|and)\s+|$)"
        )

        matches = re.findall(pattern, message, re.IGNORECASE)

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
# 3. SIMULATE CLAUDE RESPONSE
# ==========================================

def simulate_claude_response(question, history=None):

    history = history or []

    company = identify_company(question, history)

    question_lower = question.lower()

    interview_keywords = [
        "interview",
        "prepare for",
        "interview questions",
        "expect for this position",
        "expect in the interview"
    ]

    if any(word in question_lower for word in interview_keywords):

        if company:

            reply = (
                f"Let's prepare you for your opportunity at "
                f"{company}.\n\n"
                "Here are some interview questions to practise:\n\n"
                "1. Tell us about yourself.\n"
                f"2. Why do you want to work at {company}?\n"
                "3. What relevant skills and experience do you have?\n"
                "4. What do you know about our company?\n"
                "5. How would you handle a challenging situation?\n"
                "6. What are your strengths and weaknesses?\n"
                "7. Where do you see yourself in five years?\n\n"
                "Preparation tips:\n"
                "- Research the company's products and services.\n"
                "- Understand the responsibilities of the position.\n"
                "- Practise answering questions confidently.\n"
                "- Prepare examples from your previous experience."
            )

        else:

            reply = (
                "Here are some common interview questions to practise:\n\n"
                "1. Tell us about yourself.\n"
                "2. Why should we hire you?\n"
                "3. What are your strengths and weaknesses?\n"
                "4. What relevant experience do you have?\n"
                "5. Where do you see yourself in five years?\n\n"
                "Research the employer and position before your interview."
            )

    else:

        reply = (
            "This is a simulated CareerTrack AI response. "
            f"You asked: {question}. "
            "I can help you manage and improve your job applications."
        )

    return json.dumps({
        "reply": reply,
        "suggested_action": None
    })


# ==========================================
# 4. VALIDATE AI RESPONSE
# ==========================================

def validate_response(response):

    try:

        data = json.loads(response)

        if not isinstance(data, dict):
            return None

        if not isinstance(data.get("reply"), str):
            return None

        if not data["reply"].strip():
            return None

        if "suggested_action" not in data:
            return None

        return data

    except (json.JSONDecodeError, TypeError):

        return None


# ==========================================
# 5. ASK CLAUDE
# ==========================================

def ask_claude(question, applications=None, history=None):

    if client is None:

        return {
            "reply": (
                "Claude API key is missing. Please check your "
                ".env file and ensure ANTHROPIC_API_KEY is configured."
            ),
            "suggested_action": None
        }

    user_prompt = build_user_prompt(
        question,
        applications,
        history
    )

    for attempt in range(2):

        try:

            response = client.messages.create(
                model=MODEL,
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            response_text = "\n".join(
                block.text
                for block in response.content
                if block.type == "text"
            )

            response_text = re.sub(
                r"^```(?:json)?\s*|\s*```$",
                "",
                response_text.strip(),
                flags=re.IGNORECASE
            )

            result = validate_response(response_text)

            if result is not None:
                return result

            print(f"Invalid response. Retry {attempt + 1}...")

        except Exception as error:

            print("Claude API error:", error)

            return {
                "reply": (
                    "Unable to connect to Claude AI. "
                    "Please check your internet connection, "
                    "API key and API account."
                ),
                "suggested_action": None
            }

    return {
        "reply": "Unable to generate a valid response.",
        "suggested_action": None
    }


# ==========================================
# 6. CONNECT AI WITH MEMORY
# ==========================================

def ask_with_memory(question, memory, applications=None):

    history = memory.get_history()

    memory.add_message("user", question)

    result = ask_claude(
        question,
        applications,
        history
    )

    memory.add_message("assistant", result["reply"])

    memory.save()

    return result


# ==========================================
# 7. SIMULATE FINAL AI SUMMARY
# ==========================================

def simulate_claude_summary(history):

    user_questions = [
        message["content"]
        for message in history
        if message["role"] == "user"
    ]

    companies = []
    positions = []

    for question in user_questions:

        # Identify employers mentioned in the conversation
        company = identify_company(question, [])

        if company and company.lower() not in [
            item.lower() for item in companies
        ]:
            companies.append(company)

        # Identify job positions mentioned by the user
        match = re.search(
            r"\b(?:applied|applying|apply)\s+for\s+"
            r"(?:an?\s+)?(.+?)\s+"
            r"(?:position|role|job)\b",
            question,
            re.IGNORECASE
        )

        if match:

            position = match.group(1).strip()

            if position.lower() not in [
                item.lower() for item in positions
            ]:
                positions.append(position)

    # Identify the main discussion topics
    all_questions = " ".join(user_questions).lower()

    topics = []

    if "interview" in all_questions:
        topics.append("Interview preparation")

    if any(
        word in all_questions
        for word in ["application", "applied", "job"]
    ):
        topics.append("Job application management")

    if any(
        word in all_questions
        for word in ["career", "experience", "skills"]
    ):
        topics.append("Career development")

    if not topics:
        topics = ["General career assistance"]

    # Generate a relevant summary
    summary_parts = []

    if positions:

        summary_parts.append(
            "job positions including " + ", ".join(positions)
        )

    if companies:

        summary_parts.append(
            "employers including " + ", ".join(companies)
        )

    if summary_parts:

        summary = (
            "The user discussed "
            + " and ".join(summary_parts)
            + ". The main focus was "
            + ", ".join(topics).lower()
            + "."
        )

    else:

        summary = (
            "The user discussed career development and job application "
            "management with CareerTrack AI."
        )

    # Provide useful key advice
    key_advice = []

    if "Interview preparation" in topics:

        key_advice.extend([
            "Prepare answers to common interview questions.",
            "Research each employer before attending an interview.",
            "Use examples from previous work experience to demonstrate skills."
        ])

    if "Job application management" in topics:

        key_advice.extend([
            "Keep application records updated.",
            "Monitor application progress and follow up when appropriate."
        ])

    if not key_advice:

        key_advice.append(
            "Continue using CareerTrack AI to support career development."
        )

    # Suggested next steps
    suggested_next_steps = [
        "Continue monitoring job application progress.",
        "Prepare for upcoming interviews.",
        "Research employers and position requirements."
    ]

    response = {
        "summary": summary,
        "companies_discussed": companies,
        "positions_discussed": positions,
        "topics_discussed": topics,
        "key_advice": key_advice,
        "suggested_next_steps": suggested_next_steps
    }

    return json.dumps(response, indent=4)


# ==========================================
# 8. VALIDATE SUMMARY RESPONSE
# ==========================================

def validate_summary(response):

    try:

        data = json.loads(response)

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

    except (json.JSONDecodeError, TypeError):

        return None


# ==========================================
# 9. GENERATE FINAL SESSION SUMMARY
# ==========================================

def generate_session_summary(history):

    if client is None:

        print("Claude API key is missing.")
        return None

    summary_prompt = build_summary_prompt(history)

    for attempt in range(2):

        try:

            response = client.messages.create(
                model=MODEL,
                max_tokens=2048,
                system=SUMMARY_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": summary_prompt
                    }
                ]
            )

            response_text = "\n".join(
                block.text
                for block in response.content
                if block.type == "text"
            )

            response_text = re.sub(
                r"^```(?:json)?\s*|\s*```$",
                "",
                response_text.strip(),
                flags=re.IGNORECASE
            )

            result = validate_summary(response_text)

            if result is not None:
                return result

            print(f"Invalid summary. Retry {attempt + 1}...")

        except Exception as error:

            print("Summary generation error:", error)
            return None

    return None


# ==========================================
# 10. SAVE COMPLETE SESSION
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
    session_folder = Path(__file__).resolve().parent / "sessions"

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

    print(json.dumps(summary, indent=4))

    print("\nSession saved successfully!")
    print("File:", file_path)

    return file_path


# ==========================================
# 11. MAIN PROGRAM
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

        result = ask_with_memory(question, memory)

        print("\nCareerTrack AI:")
        print(result["reply"])
        print()
