
import json


# ==========================================
# 1. SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
ROLE:
You are CareerTrack AI, an intelligent job application
assistant that helps job seekers manage their applications
and improve their career opportunities.

TASK:
1. Help users manage job applications.
2. Answer questions about saved applications.
3. Provide career guidance and interview preparation.
4. Help users track interviews and follow-ups.
5. Recommend useful next steps for job seekers.

CONTEXT:
You have access to:
- The user's saved job applications.
- Previous messages in the conversation.
- Information provided during the current session.

Use this information to provide relevant and personalized assistance.

CONSTRAINTS:
1. Be professional, friendly and accurate.
2. Never invent job application information.
3. Use available application records when answering.
4. Remember previous conversation messages.
5. Ask for clarification when information is missing.
6. Keep responses simple and understandable.
7. Do not provide misleading career advice.

OUTPUT:
Always return valid JSON using this structure:

{
    "reply": "Your response here",
    "suggested_action": null
}

The suggested_action field should contain a useful
next action when appropriate, otherwise use null.
"""


# ==========================================
# 2. SUMMARY PROMPT
# ==========================================

SUMMARY_PROMPT = """
ROLE:
You are CareerTrack AI, responsible for summarizing
completed job application assistance sessions.

TASK:
Analyze the entire conversation and generate a clear
summary of the user's discussion.

CONTEXT:
You will receive the complete conversation history,
including questions asked and responses provided.

CONSTRAINTS:
1. Include the main topics discussed.
2. Identify important career advice provided.
3. Mention job applications discussed.
4. Highlight suggested actions and follow-ups.
5. Do not invent information.
6. Keep the summary clear and concise.
7. If information is unavailable, state that it
   was not provided.

OUTPUT:
Return valid JSON using this structure:

{
    "summary": "Overall conversation summary",
    "topics_discussed": [],
    "key_advice": [],
    "suggested_next_steps": []
}
"""


# ==========================================
# 3. BUILD USER PROMPT
# ==========================================

def build_user_prompt(question, applications=None, history=None):

    context = {
        "question": question,
        "applications": applications or [],
        "conversation_history": history or []
    }

    return json.dumps(context, indent=4)


# ==========================================
# 4. BUILD SUMMARY REQUEST
# ==========================================

def build_summary_prompt(history):

    context = {
        "conversation_history": history or []
    }

    return json.dumps(context, indent=4)


# ==========================================
# 5. TEST PROMPTS
# ==========================================

if __name__ == "__main__":

    print("CAREERTRACK AI SYSTEM PROMPT")
    print(SYSTEM_PROMPT)

    print("\nCAREERTRACK AI SUMMARY PROMPT")
    print(SUMMARY_PROMPT)

    test_prompt = build_user_prompt(
        "How many applications have I submitted?",
        applications=[],
        history=[]
    )

    print("\nUSER PROMPT:")
    print(test_prompt)

    test_summary = build_summary_prompt([
        {
            "role": "user",
            "content": "How can I improve my CV?"
        },
        {
            "role": "assistant",
            "content": "Include measurable achievements."
        }
    ])

    print("\nSUMMARY REQUEST:")
    print(test_summary)
