"""Retriever interface and implementations.

NoRetriever  — returns the full text of each selected document (NoRAG path).
SimpleRetriever — vector-store backed retriever (RAG path, Stage 2 extension).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


class BaseRetriever:
    def retrieve(self, query: str, docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Return a list of passages relevant to `query`.

        Each item must have at least {"id": str, "text": str}.
        """
        raise NotImplementedError


class NoRetriever(BaseRetriever):
    """Dumps the full text of every selected document — no retrieval logic."""

    def retrieve(self, query: str, docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        passages = []
        for doc in docs:
            path = Path(doc.get("path", ""))
            try:
                if path.suffix.lower() == ".pdf":
                    from pypdf import PdfReader
                    reader = PdfReader(str(path))
                    text = "\n".join(page.extract_text() or "" for page in reader.pages)
                else:
                    text = path.read_text(encoding="utf-8", errors="replace")
            except (OSError, ImportError):
                text = f"[Could not read file: {path.name}]"

            passages.append({
                "id": doc.get("id", ""),
                "name": doc.get("name", path.name),
                "text": text,
            })
        return passages


class SimpleRetriever(BaseRetriever):
    """Chunk-and-embed retriever backed by ChromaDB (RAG path).

    Install extras to use:
        pip install chromadb sentence-transformers
    """

    def __init__(self, collection_name: str = "corpus_forge", db_path: str = "./chroma_db") -> None:
        try:
            import chromadb
            from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

            self._ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            self._client = chromadb.PersistentClient(path=db_path)
            self._collection = self._client.get_or_create_collection(
                name=collection_name,
                embedding_function=self._ef,
            )
            self._available = True
        except ImportError:
            self._available = False

    def index_document(self, doc: dict[str, Any]) -> None:
        """Index a single document into ChromaDB (idempotent — skips if already indexed)."""
        if not self._available:
            return

        doc_id = doc.get("id", "")
        path = Path(doc.get("path", ""))

        # Check if already indexed by querying for a known id prefix
        existing = self._collection.get(where={"doc_id": doc_id}, limit=1)
        if existing["ids"]:
            return

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return

        # Split into paragraphs, keep chunks with enough content
        chunks = [c.strip() for c in text.split("\n\n") if len(c.strip()) > 80]
        if not chunks:
            return

        self._collection.add(
            documents=chunks,
            ids=[f"{doc_id}_{i}" for i in range(len(chunks))],
            metadatas=[{"doc_id": doc_id, "name": doc.get("name", "")} for _ in chunks],
        )

    def retrieve(self, query: str, docs: list[dict[str, Any]], n_results: int = 5) -> list[dict[str, Any]]:
        if not self._available or not docs:
            return []

        # Ensure all docs are indexed
        for doc in docs:
            self.index_document(doc)

        doc_ids = [doc["id"] for doc in docs]

        results = self._collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"doc_id": {"$in": doc_ids}},
        )

        passages = []
        for text, meta in zip(results["documents"][0], results["metadatas"][0]):
            passages.append({
                "id": meta.get("doc_id", ""),
                "name": meta.get("name", ""),
                "text": text,
            })
        return passages