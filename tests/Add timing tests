"""Tests for reel_splitter.splitter."""
from reel_splitter.splitter import (
    build_clips,
    break_long_sentence,
    max_words_for,
    split_sentences,
)
from reel_splitter.timing import count_words


def test_split_sentences_on_period_and_question() -> None:
    text = "First one. Second one? Third one!"
    assert split_sentences(text) == ["First one.", "Second one?", "Third one!"]


def test_split_sentences_on_devanagari_danda() -> None:
    text = "पहला वाक्य। दूसरा वाक्य।"
    assert split_sentences(text) == ["पहला वाक्य।", "दूसरा वाक्य।"]


def test_split_sentences_on_newlines() -> None:
    text = "Line one\nLine two"
    assert split_sentences(text) == ["Line one", "Line two"]


def test_split_sentences_empty_input() -> None:
    assert split_sentences("") == []
    assert split_sentences("   \n\n  ") == []


def test_max_words_for_default() -> None:
    # 15 seconds * 2.5 words per second = 37 words
    assert max_words_for(15.0, 2.5) == 37


def test_max_words_for_rejects_non_positive() -> None:
    import pytest

    with pytest.raises(ValueError):
        max_words_for(0, 2.5)


def test_break_long_sentence_prefers_comma() -> None:
    sentence = "one two three four, five six seven eight nine"
    pieces = break_long_sentence(sentence, max_words=6)
    assert pieces[0] == "one two three four,"
    assert pieces[1] == "five six seven eight nine"


def test_break_long_sentence_hard_cut_without_comma() -> None:
    sentence = "a b c d e f g h i j"
    pieces = break_long_sentence(sentence, max_words=4)
    assert pieces == ["a b c d", "e f g h", "i j"]


def test_no_clip_exceeds_max_seconds() -> None:
    text = " ".join(["word"] * 200) + "."
    clips = build_clips(text, max_seconds=15.0, wps=2.5)
    limit = max_words_for(15.0, 2.5)
    for clip in clips:
        assert clip.word_count <= limit
        assert count_words(clip.text) <= limit


def test_short_sentences_are_grouped_into_one_clip() -> None:
    text = "One two. Three four. Five six."
    clips = build_clips(text, max_seconds=15.0, wps=2.5)
    assert len(clips) == 1
    assert clips[0].text == "One two. Three four. Five six."
    assert clips[0].flagged is False


def test_long_sentence_is_split_and_flagged() -> None:
    text = " ".join(["word"] * 80) + "."
    clips = build_clips(text, max_seconds=15.0, wps=2.5)
    assert len(clips) > 1
    assert all(clip.flagged for clip in clips)


def test_sentence_is_never_split_in_the_middle_when_it_fits() -> None:
    text = "Short one. " + " ".join(["word"] * 30) + ". Another short one."
    clips = build_clips(text, max_seconds=15.0, wps=2.5)
    all_text = " ".join(clip.text for clip in clips)
    assert "Short one." in all_text
    assert "Another short one." in all_text
    for clip in clips:
        assert clip.flagged is False or clip.word_count <= 37


def test_start_and_end_times_are_cumulative() -> None:
    text = "One two three four five. Six seven eight nine ten. " \
           "Eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty."
    clips = build_clips(text, max_seconds=5.0, wps=2.5)
    assert clips[0].start_sec == 0.0
    for prev, nxt in zip(clips, clips[1:]):
        assert nxt.start_sec == prev.end_sec


def test_empty_input_gives_no_clips() -> None:
    assert build_clips("") == []
    assert build_clips("   ") == []


def test_hindi_text_is_grouped() -> None:
    text = "यह एक टेस्ट है। यह दूसरा वाक्य है।"
    clips = build_clips(text, max_seconds=15.0, wps=2.5)
    assert len(clips) == 1
    assert clips[0].word_count == count_words(text)
