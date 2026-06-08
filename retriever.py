"""Embedding, vector storage, and retrieval for the Columbia CS review corpus."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_PATH, CHUNKS_PATH, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K
from ingest import build_corpus


_model: SentenceTransformer | None = None
_client: chromadb.ClientAPI | None = None
_collection: chromadb.Collection | None = None


EVAL_QUERIES = [
    "What do COMS W3203 reviewers say about Tony Dear's exams and curve?",
    "For COMS W4111 Databases, what project technologies or assignments do reviewers mention?",
    "What do COMS W3157 Advanced Programming reviewers say about workload, labs, and exams?",
]

COURSE_CODE_RE = re.compile(r"\b(?:COMS\s*)?([WE]\d{4})\b", re.IGNORECASE)


def load_chunks(chunks_path: Path = CHUNKS_PATH) -> list[dict[str, Any]]:
    if not chunks_path.exists():
        build_corpus()
    chunks: list[dict[str, Any]] = []
    with chunks_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                chunks.append(json.loads(line))
    return chunks


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def get_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return _client


def get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        _collection = get_client().get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def _as_chroma_metadata(metadata: dict[str, Any]) -> dict[str, str | int | float | bool]:
    output: dict[str, str | int | float | bool] = {}
    for key, value in metadata.items():
        if isinstance(value, (str, int, float, bool)):
            output[key] = value
        elif value is None:
            output[key] = ""
        else:
            output[key] = json.dumps(value, ensure_ascii=False)
    return output


def reset_collection() -> chromadb.Collection:
    global _collection
    client = get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    _collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return _collection


def build_vector_store(force: bool = False, batch_size: int = 64) -> chromadb.Collection:
    chunks = load_chunks()
    collection = reset_collection() if force else get_collection()
    if not force and collection.count() == len(chunks):
        return collection
    if collection.count():
        collection = reset_collection()

    model = get_model()
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        texts = [chunk["text"] for chunk in batch]
        embeddings = model.encode(texts, normalize_embeddings=True).tolist()
        collection.add(
            ids=[chunk["id"] for chunk in batch],
            documents=texts,
            metadatas=[_as_chroma_metadata(chunk["metadata"]) for chunk in batch],
            embeddings=embeddings,
        )
    return collection


def extract_course_code(query: str) -> str | None:
    match = COURSE_CODE_RE.search(query)
    if not match:
        return None
    return f"COMS {match.group(1).upper()}"


def _query_mentions_professor(query: str, result: dict[str, Any]) -> bool:
    professor = result["metadata"].get("professor", "")
    return bool(professor) and professor.lower() in query.lower()


def retrieve(query: str, top_k: int = TOP_K) -> list[dict[str, Any]]:
    collection = get_collection()
    if collection.count() == 0:
        collection = build_vector_store()

    query_top_k = max(top_k * 4, top_k)
    query_embedding = get_model().encode([query], normalize_embeddings=True)[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=query_top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved = []
    for text, metadata, distance in zip(documents, metadatas, distances, strict=True):
        retrieved.append(
            {
                "text": text,
                "metadata": dict(metadata),
                "source": metadata.get("source_label", metadata.get("source_file", "unknown")),
                "distance": float(distance),
            }
        )

    course_code = extract_course_code(query)

    def rank(result: dict[str, Any]) -> tuple[int, int, float]:
        metadata_course = result["metadata"].get("course_code", "").upper()
        course_rank = 0 if not course_code or metadata_course == course_code else 1
        professor_rank = 0 if _query_mentions_professor(query, result) else 1
        return course_rank, professor_rank, result["distance"]

    retrieved.sort(key=rank)
    return retrieved[:top_k]


def print_retrieval_report(queries: list[str], force_build: bool = True) -> None:
    if force_build:
        build_vector_store(force=True)
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Stored chunks: {get_collection().count()}")
    for query in queries:
        print(f"\n=== Query: {query}")
        for rank, result in enumerate(retrieve(query), start=1):
            metadata = result["metadata"]
            preview = result["text"].replace("\n", " ")[:360]
            print(
                f"{rank}. distance={result['distance']:.3f} "
                f"| {metadata.get('course_code')} | {metadata.get('professor')} "
                f"| {metadata.get('source_file')}"
            )
            print(f"   {preview}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and test the review retriever.")
    parser.add_argument("--query", action="append", help="Query to run. Repeatable.")
    parser.add_argument("--no-build", action="store_true", help="Reuse an existing Chroma index.")
    args = parser.parse_args()

    queries = args.query or EVAL_QUERIES
    print_retrieval_report(queries, force_build=not args.no_build)


if __name__ == "__main__":
    main()
