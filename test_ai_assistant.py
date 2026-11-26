
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from ai_assistant import validate_response, ask_claude


def mock_claude_response(text):
    """Create a response with the same structure as Claude's API response."""
    return SimpleNamespace(
        content=[
            SimpleNamespace(
                type="text",
                text=text
            )
        ]
    )


class TestAIResponse(unittest.TestCase):

    def test_valid_response(self):
        response = '{"reply": "Good job", "suggested_action": null}'
        self.assertIsNotNone(validate_response(response))

    def test_invalid_json(self):
        response = '{"reply": "Good job"'
        self.assertIsNone(validate_response(response))

    def test_missing_reply(self):
        response = '{"suggested_action": null}'
        self.assertIsNone(validate_response(response))

    def test_missing_action(self):
        response = '{"reply": "Good job"}'
        self.assertIsNone(validate_response(response))

    @patch("ai_assistant.client.messages.create")
    def test_retry_success(self, mock_create):

        mock_create.side_effect = [
            mock_claude_response("invalid response"),
            mock_claude_response(
                '{"reply": "Success", "suggested_action": null}'
            )
        ]

        result = ask_claude("Help me find a job")

        self.assertEqual(result["reply"], "Success")
        self.assertEqual(mock_create.call_count, 2)

    @patch("ai_assistant.client.messages.create")
    def test_retry_failure(self, mock_create):

        mock_create.return_value = mock_claude_response(
            "invalid response"
        )

        result = ask_claude("Help me find a job")

        self.assertEqual(
            result["reply"],
            "Unable to generate a valid response."
        )

        self.assertEqual(mock_create.call_count, 2)


if __name__ == "__main__":
    unittest.main()
