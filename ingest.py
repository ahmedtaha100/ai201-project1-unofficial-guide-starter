"""Load, clean, and chunk CULPA course-review documents."""

from __future__ import annotations

import html
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from config import (
    CHUNK_MAX_CHARS,
    CHUNK_OVERLAP_CHARS,
    CHUNKS_PATH,
    CLEANED_DIR,
    DOCUMENTS_DIR,
)


REVIEW_HEADING_RE = re.compile(r"^Review (\d+)\s*$", re.MULTILINE)
NOISE_RE = re.compile(r"\b(read more|show less|cookie policy|advertisement)\b", re.IGNORECASE)


@dataclass(frozen=True)
class ReviewRecord:
    review_number: str
    review_id: str
    submitted_at: str
    course: str
    professor: str
    rating: str
    review_text: str
    workload_notes: str


@dataclass(frozen=True)
class SourceDocument:
    source_file: str
    source_title: str
    source_url: str
    source_type: str
    subtopic: str
    course_code: str
    course_name: str
    course_id: str
    total_reviews_reported: str
    reviews_collected: str
    professors: tuple[str, ...]
    reviews: tuple[ReviewRecord, ...]


def clean_text(value: str) -> str:
    """Normalize review text while preserving sentence order and useful line breaks."""
    value = html.unescape(value)
    value = value.replace("\xa0", " ")
    value = NOISE_RE.sub("", value)
    lines = []
    for line in value.splitlines():
        compact = re.sub(r"\s+", " ", line).strip()
        if compact:
            lines.append(compact)
    return "\n".join(lines).strip()


def _field(block: str, name: str, default: str = "") -> str:
    match = re.search(rf"^{re.escape(name)}:\s*(.*)$", block, re.MULTILINE)
    return clean_text(match.group(1)) if match else default


def _section(block: str, start_marker: str, end_marker: str | None = None) -> str:
    start = block.find(start_marker)
    if start == -1:
        return ""
    start += len(start_marker)
    if end_marker:
        end = block.find(end_marker, start)
        if end == -1:
            end = len(block)
    else:
        end = len(block)
    return clean_text(block[start:end])


def parse_source_document(path: Path) -> SourceDocument:
    raw = path.read_text(encoding="utf-8")
    header, _, review_region = raw.partition("Student reviews:")

    professors_region = ""
    header_without_professors = header
    if "Professors listed on course page:" in header:
        header_without_professors, _, professors_region = header.partition(
            "Professors listed on course page:"
        )

    professor_lines = [
        clean_text(line.removeprefix("- "))
        for line in professors_region.splitlines()
        if line.strip().startswith("- ")
    ]

    reviews: list[ReviewRecord] = []
    matches = list(REVIEW_HEADING_RE.finditer(review_region))
    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(review_region)
        block = review_region[match.start() : next_start]
        reviews.append(
            ReviewRecord(
                review_number=match.group(1),
                review_id=_field(block, "Review ID", f"unknown-{match.group(1)}"),
                submitted_at=_field(block, "Submission date"),
                course=_field(block, "Course"),
                professor=_field(block, "Professor", "Unknown"),
                rating=_field(block, "Rating", "None"),
                review_text=_section(block, "Review text:", "Workload notes:"),
                workload_notes=_section(block, "Workload notes:"),
            )
        )

    return SourceDocument(
        source_file=str(path.relative_to(path.parent.parent)),
        source_title=_field(header_without_professors, "Source title"),
        source_url=_field(header_without_professors, "Source URL"),
        source_type=_field(header_without_professors, "Source type"),
        subtopic=_field(header_without_professors, "Domain subtopic"),
        course_code=_field(header_without_professors, "Course code"),
        course_name=_field(header_without_professors, "Course name"),
        course_id=_field(header_without_professors, "Course ID"),
        total_reviews_reported=_field(header_without_professors, "Total CULPA reviews reported"),
        reviews_collected=_field(header_without_professors, "Reviews collected in this document"),
        professors=tuple(professor_lines),
        reviews=tuple(reviews),
    )


def render_cleaned_document(document: SourceDocument) -> str:
    lines = [
        f"Source title: {document.source_title}",
        f"Source URL: {document.source_url}",
        f"Source type: {document.source_type}",
        f"Domain subtopic: {document.subtopic}",
        f"Course code: {document.course_code}",
        f"Course name: {document.course_name}",
        f"Course ID: {document.course_id}",
        f"Total CULPA reviews reported: {document.total_reviews_reported}",
        f"Reviews collected in this document: {document.reviews_collected}",
        "",
        "Professors listed on course page:",
    ]
    lines.extend(f"- {professor}" for professor in document.professors)
    lines.append("")
    lines.append("Student reviews:")
    for review in document.reviews:
        lines.extend(
            [
                "",
                f"Review {review.review_number}",
                f"Review ID: {review.review_id}",
                f"Submission date: {review.submitted_at}",
                f"Course: {review.course}",
                f"Professor: {review.professor}",
                f"Rating: {review.rating}",
                "Review text:",
                review.review_text or "(empty)",
                "Workload notes:",
                review.workload_notes or "(empty)",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def _split_with_overlap(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text.strip()]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            lower_bound = start + int(max_chars * 0.6)
            boundary = text.rfind(" ", lower_bound, end)
            if boundary > start:
                end = boundary
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        next_start = max(end - overlap_chars, start + 1)
        while next_start < len(text) and not text[next_start].isspace():
            next_start += 1
        while next_start < len(text) and text[next_start].isspace():
            next_start += 1
        start = next_start
    return chunks


def _review_prefix(document: SourceDocument, review: ReviewRecord) -> str:
    return "\n".join(
        [
            f"Source: {document.source_title}",
            f"Source URL: {document.source_url}",
            f"Course: {document.course_code} {document.course_name}",
            f"Professor: {review.professor}",
            f"Review ID: {review.review_id}",
            f"Submitted: {review.submitted_at}",
            f"Rating: {review.rating}",
        ]
    )


def chunk_review(document: SourceDocument, review: ReviewRecord) -> list[dict[str, object]]:
    prefix = _review_prefix(document, review)
    body = "\n".join(
        [
            "Review text:",
            review.review_text or "(empty)",
            "Workload notes:",
            review.workload_notes or "(empty)",
        ]
    )
    full_text = f"{prefix}\n{body}"
    max_body_chars = max(300, CHUNK_MAX_CHARS - len(prefix) - 40)
    body_parts = _split_with_overlap(body, max_body_chars, CHUNK_OVERLAP_CHARS)

    chunks = []
    for part_index, part in enumerate(body_parts, start=1):
        part_label = f"Part {part_index}/{len(body_parts)}"
        text = f"{prefix}\n{part_label}\n{part}"
        if len(text) > CHUNK_MAX_CHARS:
            text = f"{prefix}\n{part_label}\n{part[: CHUNK_MAX_CHARS - len(prefix) - len(part_label) - 4].strip()}"
        chunk_id = (
            f"{Path(document.source_file).stem}-review-{review.review_id}-part-{part_index}"
        )
        chunks.append(
            {
                "id": chunk_id,
                "text": text,
                "metadata": {
                    "source_file": document.source_file,
                    "source_title": document.source_title,
                    "source_url": document.source_url,
                    "course_code": document.course_code,
                    "course_name": document.course_name,
                    "course_id": document.course_id,
                    "subtopic": document.subtopic,
                    "professor": review.professor,
                    "review_number": review.review_number,
                    "review_id": review.review_id,
                    "submitted_at": review.submitted_at,
                    "rating": review.rating,
                    "chunk_part": part_index,
                    "chunk_parts_total": len(body_parts),
                    "source_label": (
                        f"{document.course_code} {document.course_name}, "
                        f"{review.professor}, review {review.review_id}"
                    ),
                },
            }
        )
    if not chunks and full_text.strip():
        return [
            {
                "id": f"{Path(document.source_file).stem}-review-{review.review_id}-part-1",
                "text": full_text[:CHUNK_MAX_CHARS],
                "metadata": {},
            }
        ]
    return chunks


def load_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[SourceDocument]:
    paths = sorted(documents_dir.glob("*.txt"))
    return [parse_source_document(path) for path in paths]


def build_chunks(documents: Iterable[SourceDocument]) -> list[dict[str, object]]:
    chunks: list[dict[str, object]] = []
    for document in documents:
        for review in document.reviews:
            chunks.extend(chunk_review(document, review))
    for position, chunk in enumerate(chunks):
        chunk["metadata"]["chunk_position"] = position
    return chunks


def write_outputs(
    documents: list[SourceDocument],
    chunks: list[dict[str, object]],
    cleaned_dir: Path = CLEANED_DIR,
    chunks_path: Path = CHUNKS_PATH,
) -> None:
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    chunks_path.parent.mkdir(parents=True, exist_ok=True)
    for document in documents:
        output_path = cleaned_dir / Path(document.source_file).name
        output_path.write_text(render_cleaned_document(document), encoding="utf-8")
    with chunks_path.open("w", encoding="utf-8") as handle:
        for chunk in chunks:
            handle.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def build_corpus() -> list[dict[str, object]]:
    documents = load_documents()
    chunks = build_chunks(documents)
    write_outputs(documents, chunks)
    return chunks


def _print_checkpoint(documents: list[SourceDocument], chunks: list[dict[str, object]]) -> None:
    print(f"Loaded documents: {len(documents)}")
    print(f"Total review records: {sum(len(document.reviews) for document in documents)}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Cleaned documents directory: {CLEANED_DIR}")
    print(f"Chunks JSONL: {CHUNKS_PATH}")

    cleaned_preview = render_cleaned_document(documents[0])[:1800]
    print("\n--- Cleaned document preview ---")
    print(cleaned_preview)

    print("\n--- Five random chunks ---")
    for chunk in random.Random(201).sample(chunks, min(5, len(chunks))):
        metadata = chunk["metadata"]
        print(
            f"\n[{chunk['id']}] {metadata['source_file']} "
            f"| {metadata['course_code']} | {metadata['professor']}"
        )
        print(chunk["text"][:900])


def main() -> None:
    documents = load_documents()
    chunks = build_chunks(documents)
    write_outputs(documents, chunks)
    _print_checkpoint(documents, chunks)


if __name__ == "__main__":
    main()
