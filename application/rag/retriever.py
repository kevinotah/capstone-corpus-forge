from __future__ import annotations

from pathlib import Path
from typing import Any


class BaseRetriever:
    def retrieve(self, query: str, docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        raise NotImplementedError


class NoRetriever(BaseRetriever):
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

    def _read_file(self, path: Path) -> str:
        try:
            if path.suffix.lower() == ".pdf":
                from pypdf import PdfReader
                reader = PdfReader(str(path))
                return "\n".join(page.extract_text() or "" for page in reader.pages)
            return path.read_text(encoding="utf-8", errors="replace")
        except (OSError, ImportError):
            return ""

    def _is_indexed(self, doc_id: str) -> bool:
        try:
            # Get chunks whose ID starts with doc_id prefix
            existing = self._collection.get(ids=[f"{doc_id}_0"])
            return len(existing["ids"]) > 0
        except Exception:
            return False

    def index_document(self, doc: dict[str, Any]) -> None:
        if not self._available:
            return

        doc_id = doc.get("id", "")
        path = Path(doc.get("path", ""))

        if self._is_indexed(doc_id):
            return

        text = self._read_file(path)
        if not text.strip():
            return

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

        for doc in docs:
            self.index_document(doc)

        try:
            total = self._collection.count()
            safe_n = min(n_results * len(docs), max(1, total))

            results = self._collection.query(
                query_texts=[query],
                n_results=safe_n,
            )
        except Exception:
            return []

        doc_ids = {doc["id"] for doc in docs}
        passages = []
        for text, meta in zip(results["documents"][0], results["metadatas"][0]):
            if meta.get("doc_id") in doc_ids:
                passages.append({
                    "id": meta.get("doc_id", ""),
                    "name": meta.get("name", ""),
                    "text": text,
                })
            if len(passages) >= n_results:
                break

        return passages