"""Tests for reel_splitter.writer."""
import csv
from pathlib import Path

from reel_splitter.splitter import Clip
from reel_splitter.writer import TIMELINE_FIELDS, write_clips


def make_clip(
    number: int,
    text: str,
    start: float = 0.0,
    end: float = 1.0,
    flagged: bool = False,
) -> Clip:
    return Clip(
        number=number,
        text=text,
        start_sec=start,
        end_sec=end,
        word_count=len(text.split()),
        flagged=flagged,
    )


def test_writes_numbered_txt_files(tmp_path: Path) -> None:
    clips = [make_clip(1, "First clip."), make_clip(2, "Second clip.")]
    write_clips(clips, tmp_path)
    assert (tmp_path / "clip_01.txt").read_text(encoding="utf-8") == "First clip.\n"
    assert (tmp_path / "clip_02.txt").read_text(encoding="utf-8") == "Second clip.\n"


def test_flagged_clip_gets_note(tmp_path: Path) -> None:
    write_clips([make_clip(1, "Long split piece.", flagged=True)], tmp_path)
    content = (tmp_path / "clip_01.txt").read_text(encoding="utf-8")
    assert "NOTE" in content


def test_unflagged_clip_has_no_note(tmp_path: Path) -> None:
    write_clips([make_clip(1, "Normal clip.", flagged=False)], tmp_path)
    content = (tmp_path / "clip_01.txt").read_text(encoding="utf-8")
    assert "NOTE" not in content


def test_csv_header_matches_fields(tmp_path: Path) -> None:
    write_clips([make_clip(1, "Hello there.")], tmp_path)
    with (tmp_path / "timeline.csv").open(newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    assert header == TIMELINE_FIELDS


def test_csv_row_values(tmp_path: Path) -> None:
    write_clips([make_clip(1, "One two three.", start=0.0, end=1.2)], tmp_path)
    with (tmp_path / "timeline.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["clip_number"] == "1"
    assert rows[0]["start_sec"] == "0.0"
    assert rows[0]["end_sec"] == "1.2"
    assert rows[0]["word_count"] == "3"
    assert rows[0]["text"] == "One two three."


def test_csv_quotes_commas_and_newlines(tmp_path: Path) -> None:
    text = "hello, world\nnext line"
    write_clips([make_clip(1, text)], tmp_path)
    with (tmp_path / "timeline.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["text"] == text


def test_hindi_text_round_trip(tmp_path: Path) -> None:
    text = "यह एक टेस्ट है।"
    write_clips([make_clip(1, text)], tmp_path)
    assert (tmp_path / "clip_01.txt").read_text(encoding="utf-8").strip() == text
    with (tmp_path / "timeline.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["text"] == text


def test_creates_missing_output_dir(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "clips"
    write_clips([make_clip(1, "Hello.")], out)
    assert (out / "clip_01.txt").exists()
    assert (out / "timeline.csv").exists()


def test_returns_all_written_paths(tmp_path: Path) -> None:
    written = write_clips([make_clip(1, "A."), make_clip(2, "B.")], tmp_path)
    assert len(written) == 3
    assert written[-1].name == "timeline.csv"
