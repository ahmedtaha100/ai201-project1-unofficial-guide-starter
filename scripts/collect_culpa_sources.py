#!/usr/bin/env python3
"""Collect Columbia CS course/professor review text from CULPA's public API."""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path


BASE_URL = "https://culpa.info"
OUTPUT_DIR = Path("documents")
MAX_REVIEWS_PER_COURSE = 15

COURSES = [
    {
        "slug": "coms-w1004-intro-java",
        "course_id": 3807,
        "source_url": "https://culpa.info/course/3807",
        "subtopic": "introductory programming",
    },
    {
        "slug": "coms-w3134-data-structures",
        "course_id": 4,
        "source_url": "https://culpa.info/course/4",
        "subtopic": "core data structures",
    },
    {
        "slug": "coms-w3157-advanced-programming",
        "course_id": 4758,
        "source_url": "https://culpa.info/course/4758",
        "subtopic": "advanced programming in C/C++",
    },
    {
        "slug": "coms-w3203-discrete-math",
        "course_id": 397,
        "source_url": "https://culpa.info/course/397",
        "subtopic": "proofs and discrete mathematics",
    },
    {
        "slug": "coms-w4111-databases",
        "course_id": 664,
        "source_url": "https://culpa.info/course/664",
        "subtopic": "databases",
    },
    {
        "slug": "coms-w4115-plt",
        "course_id": 3105,
        "source_url": "https://culpa.info/course/3105",
        "subtopic": "programming languages and translators",
    },
    {
        "slug": "coms-w4156-advanced-software-engineering",
        "course_id": 1616,
        "source_url": "https://culpa.info/course/1616",
        "subtopic": "advanced software engineering",
    },
    {
        "slug": "coms-w4701-artificial-intelligence",
        "course_id": 26,
        "source_url": "https://culpa.info/course/26",
        "subtopic": "artificial intelligence",
    },
    {
        "slug": "coms-w4771-machine-learning",
        "course_id": 1921,
        "source_url": "https://culpa.info/course/1921",
        "subtopic": "machine learning",
    },
    {
        "slug": "coms-e6111-advanced-database-systems",
        "course_id": 4956,
        "source_url": "https://culpa.info/course/4956",
        "subtopic": "graduate database systems",
    },
]


def fetch_json(path: str, params: dict[str, object] | None = None) -> dict | list:
    query = ""
    if params:
        query = "?" + urllib.parse.urlencode(params)
    url = f"{BASE_URL}/{path}{query}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "CodePath-AI201-course-project/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = unescape(str(value))
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def professor_name(header: dict | None) -> str:
    if not header:
        return "Unknown professor"
    first = clean_text(header.get("first_name"))
    last = clean_text(header.get("last_name"))
    return " ".join(part for part in [first, last] if part).strip() or "Unknown professor"


def collect_reviews(course_id: int) -> tuple[int, list[dict]]:
    reviews: list[dict] = []
    total = 0
    page = 1
    while len(reviews) < MAX_REVIEWS_PER_COURSE:
        payload = fetch_json(f"api/review/course/{course_id}", {"page": page})
        page_reviews = payload.get("reviews", [])
        total = payload.get("number_of_reviews", total)
        if not page_reviews:
            break
        reviews.extend(page_reviews)
        page += 1
        time.sleep(0.15)
    return total, reviews[:MAX_REVIEWS_PER_COURSE]


def render_document(course: dict, card: dict, total_reviews: int, reviews: list[dict]) -> str:
    summary = card.get("course_summary", {})
    header = summary.get("course_header", {})
    professors = card.get("professors_that_taught", [])

    lines = [
        f"Source title: {header.get('course_code')} {header.get('course_name')} CULPA reviews",
        f"Source URL: {course['source_url']}",
        f"Source type: Public CULPA course review page / API",
        f"Domain subtopic: {course['subtopic']}",
        f"Course code: {header.get('course_code')}",
        f"Course name: {header.get('course_name')}",
        f"Course ID: {course['course_id']}",
        f"Total CULPA reviews reported: {total_reviews}",
        f"Reviews collected in this document: {len(reviews)}",
        "",
        "Professors listed on course page:",
    ]
    for professor in professors:
        lines.append(f"- {professor_name(professor)}")

    lines.extend(["", "Student reviews:"])

    for index, review in enumerate(reviews, start=1):
        review_header = review.get("course_header", header)
        lines.extend([
            "",
            f"Review {index}",
            f"Review ID: {review.get('review_id')}",
            f"Submission date: {review.get('submission_date')}",
            f"Course: {review_header.get('course_code')} {review_header.get('course_name')}",
            f"Professor: {professor_name(review.get('professor_header'))}",
            f"Rating: {review.get('rating')}",
            f"Agree/disagree/funny counts: {review.get('agree_count')}/{review.get('disagree_count')}/{review.get('funny_count')}",
            "Review text:",
            clean_text(review.get("content")),
            "Workload notes:",
            clean_text(review.get("workload")),
        ])

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    manifest = []

    for course in COURSES:
        card = fetch_json(f"api/course_page/card/{course['course_id']}")
        total_reviews, reviews = collect_reviews(course["course_id"])
        text = render_document(course, card, total_reviews, reviews)
        output_path = OUTPUT_DIR / f"{course['slug']}.txt"
        output_path.write_text(text, encoding="utf-8")
        manifest.append({
            **course,
            "file": str(output_path),
            "total_reviews_reported": total_reviews,
            "reviews_collected": len(reviews),
        })
        print(f"Wrote {output_path} ({len(reviews)} reviews, {len(text)} chars)")

    (OUTPUT_DIR / "sources_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_DIR / 'sources_manifest.json'}")


if __name__ == "__main__":
    main()
