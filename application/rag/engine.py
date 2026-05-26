"""RAG engine — orchestrates retrieval, prompt composition, and LLM calls.

Usage:
    from application.rag.engine import NoRAGEngine
    from application.rag.retriever import NoRetriever

    engine = NoRAGEngine(retriever=NoRetriever(), api_key="YOUR_KEY")
    result = engine.answer("chat", "What is this document about?", selected_docs)
    print(result["answer"])
    print(result["usage"])  # {"input_tokens": N, "output_tokens": N}
"""
from __future__ import annotations

import os
from typing import Any

from application.rag.retriever import BaseRetriever, NoRetriever
from application.rag.prompt_manager import compose_prompt


class RAGEngine:
    """Base engine — subclasses provide a retriever and call the LLM."""

    def __init__(
        self,
        retriever: BaseRetriever,
        api_key: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> None:
        self.retriever = retriever
        self.config = config or {}

        # Resolve API key: argument > env var
        self._api_key = api_key or os.environ.get("GOOGLE_API_KEY", "")
        self._client = self._build_client()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def answer(
        self,
        mode: str,
        query: str,
        selected_docs: list[dict[str, Any]],
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run the full pipeline and return {"answer": str, "usage": dict}.

        Args:
            mode: "chat" | "flashcards" | "quiz" | "code_review"
            query: the user's question or instruction
            selected_docs: list of document dicts from DocumentStore
            params: optional overrides (tone, num_cards, difficulty, …)
        """
        passages = self.retriever.retrieve(query, selected_docs)
        prompt = compose_prompt(mode, query, passages, params)
        return self._call_llm(prompt)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_client(self):
        """Return a Gemini client, or None if the library is not installed."""
        if not self._api_key:
            return None
        try:
            from google import genai
            return genai.Client(api_key=self._api_key)
        except ImportError:
            return None

    def _call_llm(self, prompt: str) -> dict[str, Any]:
        """Send prompt to Gemini and return answer + token usage."""
        if self._client is None:
            return {
                "answer": "AI is not configured. Please set the GOOGLE_API_KEY environment variable.",
                "usage": {},
            }

        model = self.config.get("model", "gemini-2.5-flash-lite")

        try:
            response = self._client.models.generate_content(
                model=model,
                contents=prompt,
            )

            answer = response.text or ""

            # Extract token usage if available
            usage = {}
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                meta = response.usage_metadata
                usage = {
                    "input_tokens": getattr(meta, "prompt_token_count", 0),
                    "output_tokens": getattr(meta, "candidates_token_count", 0),
                }

            return {"answer": answer, "usage": usage}

        except Exception as exc:
            return {"answer": f"Error calling AI: {exc}", "usage": {}}


class NoRAGEngine(RAGEngine):
    """Convenience subclass that always uses NoRetriever (full-document dump)."""

    def __init__(self, api_key: str | None = None, config: dict[str, Any] | None = None) -> None:
        super().__init__(retriever=NoRetriever(), api_key=api_key, config=config)