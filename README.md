# Antigravity Toolkit 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](#)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Agentic-orange.svg)](#)
[![Zero Browser](https://img.shields.io/badge/Browser-Zero%20Dependency-purple.svg)](#)
[![Brand](https://img.shields.io/badge/Created%20by-Pixel%20F-blueviolet.svg)](#)

An official, modular suite of production-grade agent skills, execution tools, and system rules engineered by **Pixel F** for **Google Antigravity**. Built from the ground up with clean, decoupled architecture to power autonomous agent workflows and pave the way for a universal **Agnostic Agent Toolkit**.

---

## 📂 Repository Structure

```text
Antigravity-Toolkit/
├── .gitignore              # Multi-runtime Git ignore configuration
├── LICENSE                 # Open-source MIT License (Pixel F)
├── README.md               # Repository documentation & module index
├── rules/                  # System prompts, behavioral guardrails & coding rules
│   └── .gitkeep
└── skills/                 # Standalone, zero-dependency agent skill packages
    └── youtube-toolkit/    # Production YouTube transcript & metadata extraction engine
        ├── SKILL.md        # Antigravity skill manifest & execution spec
        ├── get_transcript.py # High-performance, self-contained CLI runner
        └── lib/            # Lean vendored pure-Python dependencies (~91 KB)
            ├── defusedxml/
            └── youtube_transcript_api/
```

---

## 🛠 Featured Module: `youtube-toolkit`

The `youtube-toolkit` is an agent-centric skill designed to fetch transcripts and rich video metadata in milliseconds without launching or emulating a web browser.

### Key Capabilities

- **Zero-Browser Overhead**: Operates entirely over direct HTTP requests and internal YouTube endpoints. Zero Chromium, Puppeteer, or Playwright processes required.
- **Universal URL Parser**: Intelligently normalizes any YouTube link format:
  - Standard watch URLs: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
  - YouTube Shorts: `https://www.youtube.com/shorts/VIDEO_ID`
  - Shortened links: `https://youtu.be/VIDEO_ID`
  - Embed URLs: `https://www.youtube.com/embed/VIDEO_ID`
  - Live streams: `https://www.youtube.com/live/VIDEO_ID`
  - Raw 11-character Video IDs.
- **Caption Extraction**: Ingests official and auto-generated subtitles with automatic language negotiation (defaults to Polish and English priority).
- **Lean Zero-Bloat Packaging**:
  - Vendored pure-Python runtime libraries (`youtube_transcript_api` + `defusedxml`) located in `lib/`.
  - Zero initial `pip install` required.
  - Fully audited: stripped of test suites, demo fixtures, and cached bytecode (`*.pyc`), weighing just ~91 KB.
  - Built-in auto-bootstrap fallback if deployed on bare systems.

### Extracted Metadata Fields

| Field Name | JSON Key | Data Type | Description |
|---|---|---|---|
| **Video Title** | `title` | `string` | Full title of the video |
| **Channel Name** | `channel_name` | `string` | Author or publishing channel name |
| **Channel URL** | `channel_url` | `string` | Canonical link to creator's YouTube channel |
| **Video URL** | `video_url` | `string` | Canonical YouTube watch URL |
| **Published Date** | `published_date` | `string` | Publication date formatted as `YYYY-MM-DD` |
| **Duration** | `duration` | `string` | Human-readable duration (`MM:SS` or `HH:MM:SS`) |

---

## 💻 CLI Usage & Command Modes

The module can be invoked from any terminal or Antigravity agent process using standard Python as a **regular user**:

```powershell
python "skills/youtube-toolkit/get_transcript.py" "<YOUTUBE_URL_OR_ID>" [OPTIONS]
```

### 1. Default Mode (Formatted Text & Clean Transcript)
Prints the 6 metadata fields followed by continuous clean transcript text:
```powershell
python "skills/youtube-toolkit/get_transcript.py" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### 2. Timestamps Mode (`--timestamps`)
Prepends `[MM:SS]` time markers to every dialogue phrase:
```powershell
python "skills/youtube-toolkit/get_transcript.py" "dQw4w9WgXcQ" --timestamps
```

### 3. Metadata Only Mode (`--metadata-only`)
Executes an ultra-fast sub-second lookup of the 6 metadata properties without fetching or parsing transcripts:
```powershell
python "skills/youtube-toolkit/get_transcript.py" "dQw4w9WgXcQ" --metadata-only
```

### 4. Structured JSON Pipeline Mode (`--json`)
Outputs machine-parseable JSON containing structured metadata and an array of transcript segments with `start`, `duration`, and `text` properties:
```powershell
python "skills/youtube-toolkit/get_transcript.py" "dQw4w9WgXcQ" --json
```

Sample JSON Output:
```json
{
  "metadata": {
    "id": "dQw4w9WgXcQ",
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "title": "Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)",
    "channel_name": "Rick Astley",
    "channel_url": "https://www.youtube.com/@RickAstleyYT",
    "published_date": "2009-10-24",
    "duration": "03:34"
  },
  "transcript": [
    {
      "start": 18.2,
      "duration": 4.1,
      "text": "We're no strangers to love"
    }
  ]
}
```

---

## 🗺 Roadmap

### `youtube-toolkit`
- [ ] **Thumbnail Downloader**: Direct download and resolution selection (MaxRes, High, Medium) for multimodal visual analysis.
- [ ] **Comment Thread Extraction**: Retrieval of top comments and author replies for audience feedback and sentiment analysis.
- [ ] **Video Chapters & Sections**: Automated parsing of video chapters and time-bounded segment extraction.

### `Antigravity-Toolkit`
- [ ] **Rules Ecosystem (`rules/`)**: Reusable behavioral rulesets, code-quality gates, and deterministic anti-hallucination protocols.
- [ ] **Agnostic Agent Toolkit**: Cross-compatibility runtime adapters allowing these skills to seamlessly execute across Claude Code, Cursor, Copilot CLI, and custom LLM agent harnesses.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Developed with precision under the **Pixel F** banner.
