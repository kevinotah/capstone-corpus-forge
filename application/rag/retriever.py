"""Retriever interface and placeholder implementations.

This file should expose an abstract `BaseRetriever` and one or two simple implementations:
- `NoRetriever`: returns full document text (simple dumper)
- `SimpleRetriever`: placeholder for a vector-store backed retriever (RAG)

TODOs:
- Define `BaseRetriever` API: `retrieve(query: str, docs: list[dict]) -> list[dict]`
- Implement `NoRetriever` that returns the full selected docs.
- Add TODO hooks to wire in FAISS / embeddings when chosen.
"""
from typing import List, Dict


class BaseRetriever:
    def retrieve(self, query: str, docs: List[Dict]) -> List[Dict]:
        """Return a list of document pieces relevant to `query`.
        Each returned item should be a dict with at least `id` and `text`.
        """
        raise NotImplementedError


class NoRetriever(BaseRetriever):
    def retrieve(self, query: str, docs: List[Dict]) -> List[Dict]:
        # TODO: simply return the full text of selected docs (placeholder)
        return [{"id": d.get("id"), "text": d.get("content", "")} for d in docs]


class SimpleRetriever(BaseRetriever):
    def __init__(self):
        # TODO: initialize vector store / embeddings here
        pass

    def retrieve(self, query: str, docs: List[Dict]) -> List[Dict]:
        # TODO: implement simple retrieval using embeddings/FAISS
        return []
