def build_summary_prompt(conversation_history):
    """
    Builds a prompt for summarising a conversation.
    """

    if not conversation_history:
        return None

    conversation = ""

    for message in conversation_history:
        role = message.get("role", "user")
        content = message.get("content", "")

        conversation += f"{role}: {content}\n"

    prompt = f"""
You are an assistant that summarises conversations.

Create a concise summary of the conversation below.

Preserve important information:
- Job preferences
- Skills and qualifications
- Career goals
- Job application details
- Important decisions

Do not invent information.

Conversation:
{conversation}

Provide a clear, organised summary.
"""

    return prompt


if __name__ == "__main__":

    sample_conversation = [
        {
            "role": "user",
            "content": "I am looking for a remote software internship."
        },
        {
            "role": "assistant",
            "content": "What programming skills do you have?"
        },
        {
            "role": "user",
            "content": "I know Python and JavaScript."
        }
    ]

    result = build_summary_prompt(sample_conversation)

    print(result)