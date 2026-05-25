"""Prompt templates and helpers for composing LLM prompts.

TODOs:
- Add template strings for chat, flashcards, and quiz generation.
- Provide a `compose_prompt(mode, query, passages, params)` helper.
"""
from typing import List, Dict


def compose_prompt(mode: str, query: str, passages: List[Dict], params: Dict | None = None) -> str:
    """Return a prompt string for the LLM based on `mode`.

    Modes: 'chat', 'flashcards', 'quiz', 'code_review'
    """
    params = params or {}
    # TODO: create clear, minimal templates for each mode
    return "TODO: composed prompt"
