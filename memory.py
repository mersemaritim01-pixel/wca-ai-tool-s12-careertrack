
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone


# Folder for storing conversation sessions
SESSION_DIR = Path("sessions")
SESSION_DIR.mkdir(exist_ok=True)


class ConversationMemory:

    def __init__(self, session_id=None, max_turns=4):
        self.session_id = session_id or str(uuid.uuid4())
        self.max_turns = max_turns
        self.history = []

    def add_message(self, role, content):
        """Store a user or assistant message."""

        if role not in ("user", "assistant"):
            raise ValueError("Role must be user or assistant.")

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Message content cannot be empty.")

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.history.append(message)

        # Keep the latest four conversation turns
        self.history = self.history[-(self.max_turns * 2):]

    def get_history(self):
        """Retrieve conversation history."""

        return [
            {"role": message["role"], "content": message["content"]}
            for message in self.history
        ]

    def save(self):
        """Save conversation history to a JSON file."""

        file_path = SESSION_DIR / f"{self.session_id}.json"

        data = {
            "session_id": self.session_id,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "conversation_history": self.history
        }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return file_path

    def load(self):
        """Load a previously saved conversation."""

        file_path = SESSION_DIR / f"{self.session_id}.json"

        if not file_path.exists():
            return False

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid conversation file.")

        messages = data.get("conversation_history")

        if not isinstance(messages, list):
            raise ValueError("Invalid conversation history.")

        for message in messages:
            if (
                not isinstance(message, dict)
                or message.get("role") not in ("user", "assistant")
                or not isinstance(message.get("content"), str)
            ):
                raise ValueError("Invalid message in conversation history.")

        self.history = messages[-(self.max_turns * 2):]

        return True

    def clear_history(self):
        """Clear conversation history."""

        self.history = []
