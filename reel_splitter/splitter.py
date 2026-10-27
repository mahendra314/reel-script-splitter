"""Split a script into clips whose estimated duration is at most max_seconds."""
from __future__ import annotations

import math
import re
from dataclasses import dataclass

from .timing import count_words

# Break sentences after . ! ? or the Devanagari danda (।), and at line breaks.
_SENTENCE_END = re.compile(r"(?<=[.!?।])\s+|\n+")

# Words ending in these characters are good places to split a long sentence.
_SOFT_BREAKS = (",", ";", ":")


@dataclass
class Clip:
    number: int
    text: str
    start_sec: float
    end_sec: float
    word_count: int
    flagged: bool = False  # True if a long sentence had to be split by word count


def split_sentences(text: str) -> list[str]:
    """Split text into sentences, dropping empty pieces."""
    parts = _SENTENCE_END.split(text)
    return [part.strip() for part in parts if part and part.strip()]


def max_words_for(max_seconds: float, wps: float) -> int:
    """Convert a time limit into a word limit (always at least 1)."""
    if max_seconds <= 0:
        raise ValueError("max_seconds must be positive")
    return max(1, math.floor(max_seconds * wps))


def break_long_sentence(sentence: str, max_words: int) -> list[str]:
    """Split one long sentence into pieces of at most max_words words.

    Prefers to cut after a comma-like word in the second half of the window,
    so pieces are not tiny. Falls back to a hard cut at max_words.
    """
    words = sentence.split()
    pieces: list[str] = []
    while len(words) > max_words:
        window = words[:max_words]
        cut = max_words
        # Search backwards from the end of the window, stopping at the midpoint.
        for i in range(len(window) - 1, len(window) // 2 - 1, -1):
            if window[i].endswith(_SOFT_BREAKS):
                cut = i + 1
                break
        pieces.append(" ".join(words[:cut]))
        words = words[cut:]
    if words:
        pieces.append(" ".join(words))
    return pieces


def build_clips(text: str, max_seconds: float = 15.0, wps: float = 2.5) -> list[Clip]:
    """Group sentences into clips and estimate each clip's start and end time."""
    limit = max_words_for(max_seconds, wps)

    # Step 1: turn sentences into units. A unit is a whole sentence,
    # or a piece of a sentence that was too long for one clip.
    units: list[tuple[str, bool]] = []  # (text, was_forced_split)
    for sentence in split_sentences(text):
        if count_words(sentence) > limit:
            units.extend((piece, True) for piece in break_long_sentence(sentence, limit))
        else:
            units.append((sentence, False))

    # Step 2: greedily pack units into groups without exceeding the word limit.
    groups: list[list[tuple[str, bool]]] = []
    group: list[tuple[str, bool]] = []
    group_words = 0
    for unit_text, forced in units:
        n = count_words(unit_text)
        if group and group_words + n > limit:
            groups.append(group)
            group, group_words = [], 0
        group.append((unit_text, forced))
        group_words += n
    if group:
        groups.append(group)

    # Step 3: build Clip objects with times from cumulative word counts.
    clips: list[Clip] = []
    words_before = 0
    for number, grp in enumerate(groups, start=1):
        clip_text = " ".join(t for t, _ in grp)
        n = count_words(clip_text)
        clips.append(
            Clip(
                number=number,
                text=clip_text,
                start_sec=round(words_before / wps, 2),
                end_sec=round((words_before + n) / wps, 2),
                word_count=n,
                flagged=any(forced for _, forced in grp),
            )
        )
        words_before += n
    return clips
