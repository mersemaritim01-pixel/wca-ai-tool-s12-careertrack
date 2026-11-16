

import json

# System instructions for the AI assistant
SYSTEM_PROMPT = """
You are CareerTrack AI, an intelligent job application assistant.

Your responsibilities:
1. Help users manage their job applications.
2. Answer questions about saved applications.
3. Provide career guidance and interview preparation.
4. Help users track interviews and follow-ups.
5. Generate clear and helpful responses.

Rules:
- Be professional, friendly, and accurate.
- Do not invent job application information.
- Use the available application records when answering.
- If information is missing, ask the user for clarification.
- Keep responses simple and understandable.

Always return your response in valid JSON format:

{
    "reply": "Your response here",
    "suggested_action": null
}
"""


# Prepare the user's message for the AI
def build_user_prompt(question, applications=None, history=None):

    context = {
        "question": question,
        "applications": applications or [],
        "conversation_history": history or []
    }

    return json.dumps(context, indent=4)


# Test the prompt
if __name__ == "__main__":
    print(SYSTEM_PROMPT)

    test_prompt = build_user_prompt(
        "How many applications have I submitted?"
    )

    print("\nUser Prompt:")
    print(test_prompt)
