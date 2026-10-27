"""Write clip text files and the timeline CSV."""
from __future__ import annotations

import csv
from pathlib import Path

from .splitter import Clip

TIMELINE_FIELDS = ["clip_number", "start_sec", "end_sec", "word_count", "text"]


def write_clips(clips: list[Clip], out_dir: str | Path) -> list[Path]:
    """Write clip_NN.txt files and timeline.csv into out_dir."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for clip in clips:
        path = out / f"clip_{clip.number:02d}.txt"
        body = clip.text + "\n"
        if clip.flagged:
            body += "\n[NOTE: a sentence here was longer than the limit and was split by word count.]\n"
        path.write_text(body, encoding="utf-8")
        written.append(path)

    csv_path = out / "timeline.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TIMELINE_FIELDS)
        writer.writeheader()
        for clip in clips:
            writer.writerow(
                {
                    "clip_number": clip.number,
                    "start_sec": clip.start_sec,
                    "end_sec": clip.end_sec,
                    "word_count": clip.word_count,
                    "text": clip.text,
                }
            )
    written.append(csv_path)
    return written
