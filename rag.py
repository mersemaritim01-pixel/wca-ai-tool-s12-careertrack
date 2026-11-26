import re
from pathlib import Path

# Locate knowledge.txt
KNOWLEDGE_FILE = Path(__file__).resolve().parent / "knowledge.txt"


def load_knowledge():
    """Read the knowledge file."""

    if not KNOWLEDGE_FILE.exists():
        return ""

    return KNOWLEDGE_FILE.read_text(encoding="utf-8")


def retrieve_knowledge(question, top_k=3):
    """Find knowledge sections relevant to a question."""

    knowledge = load_knowledge()

    if not knowledge.strip():
        return "Knowledge file is empty or missing."

    sections = re.split(r"\n(?=## )", knowledge)

    question_words = set(
        re.findall(r"\b[a-zA-Z]{3,}\b", question.lower())
    )

    scored_sections = []

    for section in sections:

        section_words = set(
            re.findall(r"\b[a-zA-Z]{3,}\b", section.lower())
        )

        score = len(question_words.intersection(section_words))

        if score > 0:
            scored_sections.append((score, section.strip()))

    scored_sections.sort(key=lambda item: item[0], reverse=True)

    results = [
        section
        for score, section in scored_sections[:top_k]
    ]

    if not results:
        return "No directly relevant information found."

    return "\n\n".join(results)


# Test the RAG system
if __name__ == "__main__":

    question = input("Ask a career question: ")

    results = retrieve_knowledge(question)

    print("\nRetrieved Knowledge:")
    print(results)
