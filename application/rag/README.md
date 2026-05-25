RAG / NoRAG module (Stage 2)

Purpose
- Provide a pluggable RAG integration for Stage 2.

Structure
- `retriever.py`: retriever interfaces and placeholders.
- `engine.py`: RAG engine wrapper that composes prompts and calls LLM client.
- `prompt_manager.py`: prompt templates for chat/flashcards/quiz/code_review.

Next steps (TODO):
- Choose LLM provider and implement `llm_client` wrapper.
- Decide whether to use an embedding store (FAISS, Chroma) and add `SimpleRetriever`.
- Implement token usage tracking and expose via API.
