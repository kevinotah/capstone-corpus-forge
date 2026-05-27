from __future__ import annotations

import os
from typing import Any

from application.rag.retriever import BaseRetriever, NoRetriever
from application.rag.prompt_manager import compose_prompt


class RAGEngine:
    def __init__(
        self,
        retriever: BaseRetriever,
        api_key: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> None:
        self.retriever = retriever
        self.config = config or {}
        self._api_key = api_key or os.environ.get("GOOGLE_API_KEY", "")
        self._client = self._build_client()

    def answer(
        self,
        mode: str,
        query: str,
        selected_docs: list[dict[str, Any]],
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run the full pipeline and return {"answer": str, "usage": dict}."""
        passages = self.retriever.retrieve(query, selected_docs)
        prompt = compose_prompt(mode, query, passages, params)
        return self._call_llm(prompt)

    def _build_client(self):
        if not self._api_key:
            return None
        try:
            from google import genai
            return genai.Client(api_key=self._api_key)
        except ImportError:
            return None

    def _call_llm(self, prompt: str) -> dict[str, Any]:
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
    """Always uses NoRetriever — dumps full document text into the prompt."""

    def __init__(self, api_key: str | None = None, config: dict[str, Any] | None = None) -> None:
        super().__init__(retriever=NoRetriever(), api_key=api_key, config=config)