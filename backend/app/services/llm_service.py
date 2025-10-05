import os
from ..config import settings
import requests

# NOTE: You need to set OPENAI_API_KEY in .env or use another LLM provider
OPENAI_API_KEY = settings.OPENAI_API_KEY

def generate_question(role="general"):
    # Simple prompt-based question generation - replace with LLM call
    return {
        "id": "q_1",
        "text": "Describe a challenging technical problem you solved and how you approached it.",
        "difficulty": "medium"
    }

def evaluate_answer(transcript: str) -> float:
    """
    Very simple evaluator using heuristics or a call to an LLM for grading.
    Returns 0-10 score.
    """
    # placeholder heuristic:
    words = transcript.split()
    length = len(words)
    score = min(10, max(0, length / 20 * 2))  # naive: more words => better (replace with LLM eval)
    return round(score, 2)

# TODO: implement LLM call to get semantic grading