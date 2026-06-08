"""Grounded answer generation over retrieved Columbia CS review chunks."""

from __future__ import annotations

from typing import Any

from groq import Groq

from config import GROQ_API_KEY, LLM_MODEL, MAX_RELEVANT_DISTANCE, TOP_K
from retriever import retrieve


REFUSAL = "I don't have enough information on that."
MISSING_KEY = (
    "Groq API key is not configured. Paste your key into .env, then restart the app "
    "to generate grounded answers."
)

GROUNDING_PROMPT = """You are a grounded RAG assistant for Columbia University CS course and professor reviews.
Answer only from the provided retrieved review chunks.
Do not use outside knowledge, guesses, or general Columbia knowledge.
If the chunks do not contain enough information to answer, say exactly: "I don't have enough information on that."
Use cautious language such as "reviewers say" because the sources are student opinions.
Every factual claim must be supported by the provided chunks and cited with bracketed source IDs like [S1].
Keep the answer concise and practical."""


def relevant_chunks(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [chunk for chunk in chunks if chunk["distance"] <= MAX_RELEVANT_DISTANCE]


def source_id(index: int) -> str:
    return f"S{index}"


def source_label(chunk: dict[str, Any]) -> str:
    metadata = chunk["metadata"]
    return (
        f"{metadata.get('course_code')} {metadata.get('course_name')} | "
        f"{metadata.get('professor')} | review {metadata.get('review_id')} | "
        f"{metadata.get('source_file')}"
    )


def format_context(chunks: list[dict[str, Any]]) -> str:
    blocks = []
    for index, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]
        blocks.append(
            "\n".join(
                [
                    f"[{source_id(index)}]",
                    f"Source label: {source_label(chunk)}",
                    f"Source URL: {metadata.get('source_url')}",
                    f"Distance: {chunk['distance']:.3f}",
                    "Chunk text:",
                    chunk["text"],
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)


def format_sources(chunks: list[dict[str, Any]]) -> str:
    if not chunks:
        return "Sources: none (no sufficiently relevant chunks retrieved)."
    lines = ["Sources:"]
    for index, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]
        lines.append(
            f"- [{source_id(index)}] {source_label(chunk)}; "
            f"distance={chunk['distance']:.3f}; {metadata.get('source_url')}"
        )
    return "\n".join(lines)


def build_messages(question: str, chunks: list[dict[str, Any]]) -> list[dict[str, str]]:
    context = format_context(chunks)
    user_prompt = (
        "Retrieved review chunks:\n"
        f"{context}\n\n"
        "Question:\n"
        f"{question}\n\n"
        "Answer using only the retrieved chunks."
    )
    return [
        {"role": "system", "content": GROUNDING_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def append_sources(answer: str, chunks: list[dict[str, Any]]) -> str:
    return f"{answer.strip()}\n\n{format_sources(chunks)}"


def generate_response(question: str, chunks: list[dict[str, Any]] | None = None) -> str:
    retrieved = chunks if chunks is not None else retrieve(question, top_k=TOP_K)
    grounded_chunks = relevant_chunks(retrieved)
    if not grounded_chunks:
        return append_sources(REFUSAL, [])

    if not GROQ_API_KEY or GROQ_API_KEY == "your_key_here":
        return append_sources(MISSING_KEY, grounded_chunks)

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=build_messages(question, grounded_chunks),
        temperature=0,
        max_tokens=700,
    )
    answer = response.choices[0].message.content.strip()
    if not answer:
        answer = REFUSAL
    return append_sources(answer, grounded_chunks)


def answer_question(question: str) -> tuple[str, list[dict[str, Any]]]:
    chunks = retrieve(question, top_k=TOP_K)
    return generate_response(question, chunks), chunks


def format_retrieval_details(chunks: list[dict[str, Any]]) -> str:
    lines = []
    for index, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]
        preview = chunk["text"].replace("\n", " ")[:500]
        lines.append(
            "\n".join(
                [
                    f"### {index}. {metadata.get('course_code')} | {metadata.get('professor')} | distance {chunk['distance']:.3f}",
                    f"`{metadata.get('source_file')}`",
                    preview,
                ]
            )
        )
    return "\n\n".join(lines)


if __name__ == "__main__":
    test_question = "What do COMS W3203 reviewers say about Tony Dear's exams and curve?"
    answer, retrieved_chunks = answer_question(test_question)
    print(answer)
    print("\n--- Retrieved chunks ---")
    print(format_retrieval_details(retrieved_chunks))
