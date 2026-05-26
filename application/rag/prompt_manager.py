from __future__ import annotations

from typing import Any


def _format_passages(passages: list[dict[str, Any]]) -> str:
    parts = []
    for p in passages:
        name = p.get("name", "document")
        text = p.get("text", "").strip()
        parts.append(f"--- {name} ---\n{text}")
    return "\n\n".join(parts) if parts else "[No documents provided]"


def compose_prompt(
    mode: str,
    query: str,
    passages: list[dict[str, Any]],
    params: dict[str, Any] | None = None,
) -> str:
    params = params or {}
    context = _format_passages(passages)

    if mode == "chat":
        tone = params.get("tone", "helpful and clear")
        return f"""You are a {tone} assistant. Answer the user's question using ONLY the documents below.
If the answer is not in the documents, say so — do not make things up.

DOCUMENTS:
{context}

USER QUESTION:
{query}
"""

    if mode == "flashcards":
        num = params.get("num_cards", 10)
        return f"""You are an expert educator. Based on the documents below, generate exactly {num} flashcards.

Format your response as a JSON array like this (and nothing else):
[
  {{"front": "Question or term", "back": "Answer or definition"}},
  ...
]

DOCUMENTS:
{context}
"""

    if mode == "quiz":
        num = params.get("num_questions", 5)
        difficulty = params.get("difficulty", "medium")
        return f"""You are an expert educator. Based on the documents below, generate exactly {num} multiple-choice quiz questions at {difficulty} difficulty.

Format your response as a JSON array like this (and nothing else):
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A",
    "explanation": "..."
  }},
  ...
]

DOCUMENTS:
{context}
"""

    if mode == "code_review":
        return f"""You are a senior software engineer doing a code review.
Analyze the code below and provide:
1. A brief summary of what the code does
2. Up to 3 strengths
3. Up to 3 issues or improvements (with specific line references if possible)
4. An overall quality rating out of 5

CODE:
{context}

FOCUS:
{query if query else "General review"}
"""

    # Fallback: treat as chat
    return compose_prompt("chat", query, passages, params)