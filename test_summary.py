import unittest
from summary import build_summary_prompt


class TestSummary(unittest.TestCase):

    def test_empty_conversation(self):
        result = build_summary_prompt([])
        self.assertIsNone(result)

    def test_summary_prompt_contains_messages(self):
        conversation = [
            {
                "role": "user",
                "content": "I am looking for a remote job."
            },
            {
                "role": "assistant",
                "content": "What skills do you have?"
            }
        ]

        result = build_summary_prompt(conversation)

        self.assertIn("remote job", result)
        self.assertIn("What skills do you have?", result)

    def test_summary_prompt_contains_instructions(self):
        conversation = [
            {
                "role": "user",
                "content": "I know Python."
            }
        ]

        result = build_summary_prompt(conversation)

        self.assertIn("Do not invent information", result)
        self.assertIn("Python", result)


if __name__ == "__main__":
    unittest.main()

from summary import generate_summary, display_summary

applications = [
    {"company": "NCBA Bank", "status": "Interview"},
    {"company": "Britam", "status": "Applied"},
    {"company": "Jubilee", "status": "Offer"},
    {"company": "Co-op Bank", "status": "Rejected"}
]

# Generate summary
result = generate_summary(applications)

print(result)

# Display summary
display_summary(applications)
