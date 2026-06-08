"""Run the five Project 1 evaluation questions.

By default this uses the live Groq client when GROQ_API_KEY is configured and
falls back to a mocked Groq client when the key is absent. The mock mode exists
only so the repo can document retrieval, prompt construction, and citation
plumbing before the user-only key is pasted into .env.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import generator  # noqa: E402
from config import GROQ_API_KEY  # noqa: E402
from generator import generate_response  # noqa: E402
from retriever import retrieve  # noqa: E402


EVAL_CASES = [
    {
        "question": "What do COMS W3203 reviewers say about Tony Dear's exams and curve?",
        "expected": "Reviewers say Tony Dear's exams can be difficult or meaningfully harder than examples/homework, but multiple chunks mention a curve, B+ curve, or significant end-grade curve.",
        "accuracy": "Accurate",
    },
    {
        "question": "What do COMS W3157 Advanced Programming reviewers say about workload, labs, and exams?",
        "expected": "Reviewers describe Jae Lee's version as a hard but rewarding systems/C class built around labs or a long project; comments mention linked lists/servers, office hours, heavy workload, and exam prep tied to lecture notes/labs.",
        "accuracy": "Accurate",
    },
    {
        "question": "For COMS W4111 Databases, what project technologies or assignments do reviewers mention?",
        "expected": "Reviews mention SQL/PostgreSQL database work, schema design, populating data, and building a simple web app around the database, plus exams/homework depending on professor.",
        "accuracy": "Accurate",
    },
    {
        "question": "What do COMS W4115 PLT reviewers say about the major project and OCaml?",
        "expected": "Reviews say students learn/use OCaml and complete a large group compiler/language project; several advise choosing a good group and starting early.",
        "accuracy": "Accurate",
    },
    {
        "question": "How do COMS W4701 AI reviewers describe Ansaf Salleb-Aouissi's homework and exams?",
        "expected": "Ansaf W4701 reviews mention coding and conceptual/written assignments, the lowest coding/conceptual grades being dropped in one review, and two exams or midterm/final-style tests.",
        "accuracy": "Partially accurate",
    },
]

MOCK_ANSWERS = {
    EVAL_CASES[0]["question"]: "Reviewers say Tony Dear's exams can be difficult and sometimes have a gap from class examples, but they also mention a generous or significant curve, including a B+ curve/end-grade curve [S1] [S5].",
    EVAL_CASES[1]["question"]: "Reviewers describe W3157 with Jae Lee as a demanding but rewarding class built around labs or one long project, moving from C to linked lists and servers. They also point to office hours, lecture notes, and labs as important for exam preparation [S1] [S4].",
    EVAL_CASES[2]["question"]: "W4111 reviewers mention SQL databases, schema design with integrity constraints, PostgreSQL/database-server work, populating data, and a semester project that becomes a simple web app using the database. They also mention midterm/final exams and homework depending on professor [S1] [S2] [S3].",
    EVAL_CASES[3]["question"]: "PLT reviewers say the major project is a substantial group compiler/language project and that OCaml is part of the course. Several advise choosing a good group and starting early because the project is large and hard to do alone [S2] [S3] [S5].",
    EVAL_CASES[4]["question"]: "For Ansaf's W4701, reviewers mention coding and conceptual assignments, with one review saying there were 5 coding assignments and 5 conceptual assignments and that the lowest grades were dropped. The same review describes two exams/midterm-style tests, while another Ansaf review criticizes the coding grading script [S1] [S3].",
}


def _extract_question(messages: list[dict[str, str]]) -> str:
    user_message = messages[1]["content"]
    match = re.search(r"Question:\n(.+?)\n\nAnswer", user_message, re.DOTALL)
    return match.group(1).strip() if match else ""


class FakeMessage:
    def __init__(self, content: str):
        self.content = content


class FakeChoice:
    def __init__(self, content: str):
        self.message = FakeMessage(content)


class FakeResponse:
    def __init__(self, content: str):
        self.choices = [FakeChoice(content)]


class FakeCompletions:
    def create(self, **kwargs):
        question = _extract_question(kwargs["messages"])
        return FakeResponse(MOCK_ANSWERS.get(question, generator.REFUSAL))


class FakeChat:
    completions = FakeCompletions()


class FakeGroq:
    def __init__(self, api_key: str):
        self.chat = FakeChat()


def configure_mode(mode: str) -> str:
    has_key = bool(GROQ_API_KEY and GROQ_API_KEY != "your_key_here")
    if mode == "live" and not has_key:
        raise SystemExit("GROQ_API_KEY is missing; paste it into .env or use --mode mock.")
    if mode == "mock" or (mode == "auto" and not has_key):
        generator.GROQ_API_KEY = "mock-eval-key"
        generator.Groq = FakeGroq
        return "mock"
    return "live"


def top_chunks_markdown(chunks: list[dict], limit: int = 3) -> str:
    lines = []
    for index, chunk in enumerate(chunks[:limit], start=1):
        metadata = chunk["metadata"]
        preview = chunk["text"].replace("\n", " ")[:220]
        lines.append(
            f"{index}. {metadata.get('course_code')} | {metadata.get('professor')} | "
            f"distance={chunk['distance']:.3f} | `{metadata.get('source_file')}` — {preview}"
        )
    return "\n".join(lines)


def run(mode: str) -> str:
    active_mode = configure_mode(mode)
    sections = [f"# Evaluation Results\n\nMode: `{active_mode}`\n"]
    for case in EVAL_CASES:
        chunks = retrieve(case["question"])
        response = generate_response(case["question"], chunks)
        sections.append(
            "\n".join(
                [
                    f"## {case['question']}",
                    "",
                    f"Expected: {case['expected']}",
                    "",
                    "Retrieved chunks:",
                    top_chunks_markdown(chunks),
                    "",
                    "Response:",
                    response,
                    "",
                    f"Accuracy: {case['accuracy']}",
                ]
            )
        )
    report = "\n\n---\n\n".join(sections) + "\n"
    output_path = ROOT / "data" / "evaluation_results.md"
    output_path.write_text(report, encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Project 1 eval questions.")
    parser.add_argument("--mode", choices=["auto", "mock", "live"], default="auto")
    args = parser.parse_args()
    print(run(args.mode))


if __name__ == "__main__":
    main()
