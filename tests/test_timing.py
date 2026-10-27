"""Tests for reel_splitter.timing."""
import pytest

from reel_splitter.timing import count_words, estimate_seconds


def test_count_words_english() -> None:
    assert count_words("Hello there my friend") == 4


def test_count_words_hindi() -> None:
    assert count_words("नमस्ते आप कैसे हैं") == 4


def test_count_words_hinglish() -> None:
    assert count_words("Ye video bahut useful hai") == 5


def test_count_words_empty() -> None:
    assert count_words("") == 0
    assert count_words("   \n\t  ") == 0


def test_estimate_seconds_default_rate() -> None:
    # 5 words at 2.5 words per second = 2 seconds
    assert estimate_seconds("one two three four five") == pytest.approx(2.0)


def test_estimate_seconds_custom_rate() -> None:
    # 5 words at 5 words per second = 1 second
    assert estimate_seconds("one two three four five", wps=5.0) == pytest.approx(1.0)


def test_estimate_seconds_rejects_zero_rate() -> None:
    with pytest.raises(ValueError):
        estimate_seconds("hello", wps=0)


def test_estimate_seconds_rejects_negative_rate() -> None:
    with pytest.raises(ValueError):
        estimate_seconds("hello", wps=-1.0)
