
from memory import ConversationMemory

# Create memory
memory = ConversationMemory()

# Add conversation messages
memory.add_message("user", "How can I improve my CV?")
memory.add_message("assistant", "Use measurable achievements.")
memory.add_message("user", "How do I prepare for interviews?")
memory.add_message("assistant", "Practice common interview questions.")

# Display history
print("Conversation History:")
print(memory.get_history())

# Save conversation
saved_file = memory.save()
print("\nConversation saved to:", saved_file)

# Test loading
new_memory = ConversationMemory(memory.session_id)

if new_memory.load():
    print("\nConversation loaded successfully!")
    print(new_memory.get_history())
else:
    print("\nNo saved conversation found.")
