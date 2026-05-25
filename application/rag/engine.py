"""RAG engine wrapper

Expose `RAGEngine` which orchestrates retrieving relevant text and calling an LLM client.
Keep the LLM call abstracted so tests can mock it.

TODOs:
- Implement `RAGEngine.__init__(retriever, llm_client, config)`
- Implement `RAGEngine.answer(query, selected_docs)` that:
  1. asks retriever for relevant passages
  2. composes a prompt + context
  3. calls `llm_client` and returns the output + usage data
- Add error handling and token accounting hooks.
"""
from typing import Any, Dict, List


class RAGEngine:
    def __init__(self, retriever: Any, llm_client: Any, config: Dict | None = None) -> None:
        self.retriever = retriever
        self.llm = llm_client
        self.config = config or {}

    def answer(self, query: str, selected_docs: List[Dict]) -> Dict:
        """Return dict {"answer": str, "usage": {...}}.

        TODO: implement retrieval, prompt composition, LLM call, and token usage parsing.
        """
        # 1) retrieve
        passages = self.retriever.retrieve(query, selected_docs)

        # 2) TODO: compose prompt using `passages` and `query`
        prompt = """
        TODO: compose prompt here by combining passages and the user query.
        """

        # 3) TODO: call self.llm(prompt) and parse response
        # return structure should include answer and usage info
        return {"answer": "TODO: implement", "usage": {}}


class NoRAGEngine(RAGEngine):
    """Simple engine that dumps selected docs into the prompt (no retrieval).

    TODO: implement a minimal safe prompt composition that respects token limits.
    """
    pass
