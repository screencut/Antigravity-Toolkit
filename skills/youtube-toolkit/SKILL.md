---
name: youtube-toolkit
description: Fetch transcripts and comprehensive metadata (title, channel, channel URL, video URL, publish date, duration) for any YouTube video, Short, or livestream without using a browser.
---

# YouTube Toolkit

Modular skill for extracting YouTube transcripts and comprehensive video metadata via direct HTTP endpoints without launching a web browser.

## Capabilities

- **Zero-Browser Operation**: Lightweight HTTP requests and YouTube internal endpoints; no Chromium/Playwright instance needed.
- **Universal URL Parsing**: Supports standard watch links (`youtube.com/watch?v=`), Shorts (`youtube.com/shorts/`), shortened links (`youtu.be/`), embed links (`youtube.com/embed/`), and live stream links (`youtube.com/live/`).
- **Transcript Extraction**: Fetches manual or auto-generated captions (defaults to Polish and English priority).
- **Metadata Fields Extracted**:
  1. `title`: Video title
  2. `channel_name`: Channel / author name
  3. `channel_url`: Direct URL to the creator channel
  4. `video_url`: Canonical video URL
  5. `published_date`: ISO publication date (`YYYY-MM-DD`)
  6. `duration`: Human-readable formatted duration (`MM:SS` or `HH:MM:SS`)
- **Self-Contained (Lean)**: Bundled with pure Python dependencies in `lib/` (`youtube_transcript_api` and `defusedxml`). Zero `pip install` required.

## Execution

Run the Python CLI script using the `run_command` tool (as **regular user**):

```powershell
python "skills/youtube-toolkit/get_transcript.py" "<YOUTUBE_URL_OR_VIDEO_ID>" [OPTIONS]
```

### CLI Modes & Flags:

- **Default (clean text)**: Outputs formatted metadata header followed by full clean transcript text.
  ```powershell
  python "skills/youtube-toolkit/get_transcript.py" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  ```

- `--timestamps`: Prepend timecodes `[MM:SS]` before each transcript segment.
  ```powershell
  python "skills/youtube-toolkit/get_transcript.py" "dQw4w9WgXcQ" --timestamps
  ```

- `--metadata-only`: Fast sub-second retrieval of the 6 metadata fields without transcript fetching.
  ```powershell
  python "skills/youtube-toolkit/get_transcript.py" "dQw4w9WgXcQ" --metadata-only
  ```

- `--json`: Structured JSON dump of metadata and transcript snippets for programmatic pipeline consumption.
  ```powershell
  python "skills/youtube-toolkit/get_transcript.py" "dQw4w9WgXcQ" --json
  ```
