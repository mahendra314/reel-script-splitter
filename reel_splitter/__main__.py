"""CLI entry point.

Usage:
    python -m reel_splitter input/script.txt --max-seconds 15 --wps 2.5 --out clips/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .splitter import build_clips
from .writer import write_clips


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="reel_splitter",
        description="Split a short-form video script into timed clips.",
    )
    parser.add_argument("input", type=Path, help="UTF-8 .txt script file")
    parser.add_argument("--max-seconds", type=float, default=15.0,
                        help="maximum estimated seconds per clip (default: 15)")
    parser.add_argument("--wps", type=float, default=2.5,
                        help="estimated words per second (default: 2.5)")
    parser.add_argument("--out", type=Path, default=Path("clips"),
                        help="output directory (default: clips/)")
    args = parser.parse_args(argv)

    if args.max_seconds <= 0 or args.wps <= 0:
        parser.error("--max-seconds and --wps must be positive")
    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")

    # utf-8-sig also accepts files saved with a BOM (common with Windows Notepad).
    text = args.input.read_text(encoding="utf-8-sig")
    clips = build_clips(text, max_seconds=args.max_seconds, wps=args.wps)
    if not clips:
        print("No text found in input. Nothing written.")
        return 0

    write_clips(clips, args.out)
    print(f"Wrote {len(clips)} clip(s) to {args.out}/")

    flagged = [c.number for c in clips if c.flagged]
    if flagged:
        print(f"Warning: clip(s) {flagged} contain a sentence split by word count.",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
