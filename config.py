"""Shared configuration for the Columbia CS review RAG project."""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
DATA_DIR = BASE_DIR / "data"
CLEANED_DIR = DATA_DIR / "cleaned_documents"
CHUNKS_PATH = DATA_DIR / "chunks.jsonl"
CHROMA_PATH = BASE_DIR / "chroma_db"

CHUNK_MAX_CHARS = 900
CHUNK_OVERLAP_CHARS = 150

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "columbia_cs_reviews"
TOP_K = 5
MAX_RELEVANT_DISTANCE = 0.65

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"
