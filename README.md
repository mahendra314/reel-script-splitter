# reel-script-splitter

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Split a short-form video script (`.txt`) into numbered clips of 15 seconds or less, with a CSV timeline.

## Why this exists

If you make Instagram Reels or YouTube Shorts, you often write a full script and then have to cut it into parts that fit the time limit. This tool does the first pass for you. It groups whole sentences into clips, so you do not cut a sentence in the middle. It also gives you a CSV with the estimated start and end time of each clip.

## Installation

You need Python 3.10 or newer.

**Windows (PowerShell)**
```powershell
git clone https://github.com/mahendra314/reel-script-splitter.git
cd reel-script-splitter
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

**macOS / Linux**
```bash
git clone https://github.com/mahendra314/reel-script-splitter.git
cd reel-script-splitter
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

The `[dev]` part installs pytest, which you need only to run the tests. The tool itself has no other dependencies.

## Usage

Run the tool on one of the sample files:

```bash
python -m reel_splitter examples/sample_english.txt --max-seconds 15 --wps 2.5 --out clips/
```

Options:

| Option | Default | Meaning |
|---|---|---|
| `input` | (required) | UTF-8 `.txt` script file |
| `--max-seconds` | `15` | Maximum estimated seconds per clip |
| `--wps` | `2.5` | Estimated words per second |
| `--out` | `clips/` | Folder for the output files |

The same works with the Hinglish sample:

```bash
python -m reel_splitter examples/sample_hinglish.txt --out clips_hinglish/
```

### What you get

For each clip, the tool writes one text file:

```
clips/clip_01.txt
clips/clip_02.txt
...
```

It also writes `clips/timeline.csv` with these columns:

```
clip_number,start_sec,end_sec,word_count,text
```

If one sentence was longer than the limit, the tool splits it at a comma or by word count. That clip is marked: its `.txt` file gets a NOTE at the end, and the terminal shows a warning with the clip number.

## How timing works

The tool does not listen to audio. It counts words and divides by the words-per-second rate:

`estimated seconds = word count / words per second`

With the default rate of 2.5 words per second, a clip can hold at most 37 words (15 seconds).

This is an estimate. Real speaking speed changes with the speaker, pauses, emotion, and language. Use the times as a starting point, then check the clips by recording or reading them out loud.

## Limitations

- It does not analyse audio. Pauses, music, and actual speaking speed are not measured.
- It does not connect to Instagram, YouTube, or any other platform. It only reads local text files.
- Words are counted by spaces. Languages without spaces between words will be counted wrong.
- A single sentence longer than the limit is split by word count, which may cut its meaning.

## Running the tests

```bash
pytest
```

## Contributing

Bug reports and small improvements are welcome. Please open an issue first for bigger changes. Keep the code simple and standard-library only, and add a test for any new behaviour.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
