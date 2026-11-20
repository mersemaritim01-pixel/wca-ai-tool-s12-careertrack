
import json
from prompts import SYSTEM_PROMPT, build_user_prompt
from memory import ConversationMemory


def simulate_claude_response(question):
    """
    Simulates a Claude AI response while we develop
    the project without an API key.
    """

    response = {
        "reply": (
            "This is a simulated CareerTrack AI response. "
            f"You asked: {question}. "
            "I can help you manage and improve your job applications."
        ),
        "suggested_action": None
    }

    return json.dumps(response)


def validate_response(response):
    """
    Checks whether the AI response contains valid JSON
    and the required fields.
    """

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


def ask_claude(question, applications=None, history=None):
    """
    Sends a question to simulated Claude AI
    and validates the response.
    """

    user_prompt = build_user_prompt(
        question,
        applications,
        history
    )

    for attempt in range(2):

        response = simulate_claude_response(question)

        result = validate_response(response)

        if result is not None:
            return result

        print(f"Invalid response. Retry {attempt + 1}...")

    return {
        "reply": "Unable to generate a valid response.",
        "suggested_action": None
    }


def ask_with_memory(question, memory, applications=None):
    """
    Connects AI responses with conversation memory.
    """

    # Retrieve previous conversation
    history = memory.get_history()

    # Store the current question
    memory.add_message("user", question)

    # Generate AI response using previous history
    result = ask_claude(
        question,
        applications,
        history
    )

    # Store AI response
    memory.add_message("assistant", result["reply"])

    # Save conversation
    memory.save()

    return result


if __name__ == "__main__":

    memory = ConversationMemory(
        session_id="careertrack_default"
    )

    # Load previous conversations
    memory.load()

    print("Welcome to CareerTrack AI!")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            print("Conversation saved. Goodbye!")
            break

        result = ask_with_memory(question, memory)

        print("\nCareerTrack AI:")
        print(result["reply"])
        print()

