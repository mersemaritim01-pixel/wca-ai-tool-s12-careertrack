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

def generate_summary(applications):
    """
    Generate statistics for job applications.
    """

    total = len(applications)

    statuses = {
        "Applied": 0,
        "Under Review": 0,
        "Interview": 0,
        "Rejected": 0,
        "Offer": 0,
        "Withdrawn": 0
    }

    for application in applications:
        status = application.get("status", "Applied")

        if status in statuses:
            statuses[status] += 1

    active = total - statuses["Withdrawn"]

    return {
        "total_applications": total,
        "active_applications": active,
        "under_review": statuses["Under Review"],
        "interviews": statuses["Interview"],
        "rejections": statuses["Rejected"],
        "offers": statuses["Offer"],
        "withdrawn": statuses["Withdrawn"],
        "status_breakdown": statuses
    }


def display_summary(applications):
    """
    Display application statistics.
    """

    summary = generate_summary(applications)

    print("\n========== CAREERTRACK SUMMARY ==========")

    print("Total Applications:", summary["total_applications"])
    print("Active Applications:", summary["active_applications"])
    print("Under Review:", summary["under_review"])
    print("Interviews:", summary["interviews"])
    print("Rejections:", summary["rejections"])
    print("Job Offers:", summary["offers"])
    print("Withdrawn:", summary["withdrawn"])

    print("\nStatus Breakdown:")

    for status, count in summary["status_breakdown"].items():
        print(f"{status}: {count}")

    print("=========================================")
