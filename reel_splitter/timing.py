"""Duration estimation from a words-per-second rate.

This is an estimate. It does not measure real audio.
"""
from __future__ import annotations

DEFAULT_WPS = 2.5


def count_words(text: str) -> int:
    """Count words by splitting on whitespace.

    This works for Hindi (Devanagari), Hinglish, and English because
    words in all three are separated by spaces.
    """
    return len(text.split())


def estimate_seconds(text: str, wps: float = DEFAULT_WPS) -> float:
    """Return the estimated speaking time of text in seconds."""
    if wps <= 0:
        raise ValueError("words per second must be positive")
    return count_words(text) / wps
