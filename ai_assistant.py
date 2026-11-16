

import json
from prompts import SYSTEM_PROMPT, build_user_prompt


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
    Sends a question to the simulated Claude AI
    and validates the response.

    Retries once if the response is invalid.
    """

    user_prompt = build_user_prompt(
        question,
        applications,
        history
    )

    for attempt in range(2):

        # Simulated Claude response
        response = simulate_claude_response(question)

        # Validate the response
        result = validate_response(response)

        if result is not None:
            return result

        print(f"Invalid response. Retry {attempt + 1}...")

    return {
        "reply": "Unable to generate a valid response.",
        "suggested_action": None
    }


if __name__ == "__main__":

    question = "How can I improve my job application?"

    result = ask_claude(question)

    print("\nCareerTrack AI Response:")
    print(json.dumps(result, indent=4))
