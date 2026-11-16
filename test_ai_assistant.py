
import unittest
from unittest.mock import patch

from ai_assistant import validate_response, ask_claude


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

    @patch("ai_assistant.simulate_claude_response")
    def test_retry_success(self, mock_response):
        mock_response.side_effect = [
            "invalid response",
            '{"reply": "Success", "suggested_action": null}'
        ]

        result = ask_claude("Help me find a job")

        self.assertEqual(result["reply"], "Success")
        self.assertEqual(mock_response.call_count, 2)

    @patch("ai_assistant.simulate_claude_response")
    def test_retry_failure(self, mock_response):
        mock_response.return_value = "invalid response"

        result = ask_claude("Help me find a job")

        self.assertEqual(
            result["reply"],
            "Unable to generate a valid response."
        )
        self.assertEqual(mock_response.call_count, 2)


if __name__ == "__main__":
    unittest.main()
