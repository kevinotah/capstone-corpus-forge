"""RAG/No-RAG integration module (Stage 2 skeleton)

TODOs:
- Provide a single entrypoint class (RAGEngine) that the web app can import.
- Keep implementations pluggable: a "no-rag" simple dumper and a "rag" retriever-backed path.
"""

# TODO: implement RAGEngine, NoRAGEngine, and hooks for configuration

__all__ = ["RAGEngine", "NoRAGEngine"]
