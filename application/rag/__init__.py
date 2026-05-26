"""RAG / NoRAG integration module.

Quick start (NoRAG — no ChromaDB needed):

    from application.rag import NoRAGEngine

    engine = NoRAGEngine(api_key="YOUR_GOOGLE_API_KEY")
    result = engine.answer("chat", "Summarise these docs", selected_docs)
    print(result["answer"])

Quick start (RAG — requires chromadb + sentence-transformers):

    from application.rag import RAGEngine
    from application.rag.retriever import SimpleRetriever

    engine = RAGEngine(retriever=SimpleRetriever(), api_key="YOUR_GOOGLE_API_KEY")
    result = engine.answer("chat", "What does section 3 say?", selected_docs)
"""

from application.rag.engine import NoRAGEngine, RAGEngine

__all__ = ["RAGEngine", "NoRAGEngine"]