#!/usr/bin/env python3
"""
YouTube Transcript & Comprehensive Metadata Extractor (Portable & Self-Contained)
"""

import sys
import os

# Prevent bytecode generation to preserve lean, zero-bloat portable runtime
sys.dont_write_bytecode = True
import re
import json
import argparse
import urllib.request

# Ensure UTF-8 output on Windows consoles to prevent charmap encoding errors
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 1. Vendor/lib support: Load bundled dependencies from local 'lib' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
bundled_lib = os.path.join(current_dir, "lib")
if os.path.exists(bundled_lib):
    sys.path.insert(0, bundled_lib)

# 2. Auto-bootstrap fallback: If running on a new machine without dependencies, auto-install
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "youtube-transcript-api", "--quiet"])
        from youtube_transcript_api import YouTubeTranscriptApi
    except Exception as e:
        sys.stderr.write(f"Error: Missing youtube_transcript_api and could not auto-install: {e}\n")
        sys.exit(1)

def extract_video_id(url_or_id: str) -> str:
    url_or_id = url_or_id.strip()
    patterns = [
        r'(?:v=|/shorts/|youtu\.be/|/embed/|/live/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return url_or_id

def parse_iso_duration(dur_str: str) -> str:
    if not dur_str:
        return "Nieznana"
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", dur_str)
    if not m:
        if dur_str.isdigit():
            total = int(dur_str)
            h = total // 3600
            rem = total % 3600
            m_ = rem // 60
            s = rem % 60
            return f"{h}:{m_:02d}:{s:02d}" if h > 0 else f"{m_:02d}:{s:02d}"
        return dur_str
    h = int(m.group(1) or 0)
    m_ = int(m.group(2) or 0)
    s = int(m.group(3) or 0)
    if h > 0:
        return f"{h}:{m_:02d}:{s:02d}"
    return f"{m_:02d}:{s:02d}"

def get_video_metadata(video_id: str) -> dict:
    meta = {
        "id": video_id,
        "video_url": f"https://www.youtube.com/watch?v={video_id}",
        "title": "Nieznany tytuł",
        "channel_name": "Nieznany kanał",
        "channel_url": "",
        "published_date": "Nieznana data",
        "duration": "Nieznana"
    }
    # 1. oEmbed for title, author, author_url
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        req = urllib.request.Request(oembed_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            meta["title"] = data.get("title", meta["title"])
            meta["channel_name"] = data.get("author_name", meta["channel_name"])
            meta["channel_url"] = data.get("author_url", meta["channel_url"])
    except Exception:
        pass

    # 2. Page HTML for datePublished and duration
    try:
        page_url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(page_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        pub_match = re.search(r'itemprop="datePublished" content="([^"]+)"', html)
        if not pub_match:
            pub_match = re.search(r'"publishDate":\s*"([^"]+)"', html)
        if pub_match:
            meta["published_date"] = pub_match.group(1).split("T")[0]

        dur_match = re.search(r'itemprop="duration" content="([^"]+)"', html)
        if not dur_match:
            dur_match = re.search(r'"lengthSeconds":\s*"([^"]+)"', html)
        if dur_match:
            meta["duration"] = parse_iso_duration(dur_match.group(1))
    except Exception:
        pass

    return meta

def get_transcript(video_id: str, languages=('pl', 'en')):
    ytt = YouTubeTranscriptApi()
    return ytt.fetch(video_id, languages=languages)

def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcript and metadata")
    parser.add_argument("url", help="YouTube video URL, Short URL, or 11-char Video ID")
    parser.add_argument("--timestamps", action="store_true", help="Include timestamps [MM:SS] in output")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--metadata-only", action="store_true", help="Only output video metadata without transcript")
    
    args = parser.parse_args()
    video_id = extract_video_id(args.url)
    meta = get_video_metadata(video_id)
    
    if args.metadata_only:
        if args.json:
            print(json.dumps(meta, ensure_ascii=False, indent=2))
        else:
            print(f"Tytuł filmu:     {meta['title']}")
            print(f"Kanał:           {meta['channel_name']}")
            print(f"Link do kanału:  {meta['channel_url']}")
            print(f"Link do filmu:   {meta['video_url']}")
            print(f"Data publikacji: {meta['published_date']}")
            print(f"Długość filmu:   {meta['duration']}")
        return

    try:
        transcript_data = get_transcript(video_id)
    except Exception as e:
        sys.stderr.write(f"Błąd pobierania transkrypcji dla {video_id}: {e}\n")
        sys.exit(1)

    snippets = transcript_data.snippets
    
    if args.json:
        result = {
            "metadata": meta,
            "transcript": [
                {
                    "start": s.start,
                    "duration": s.duration,
                    "text": s.text
                } for s in snippets
            ]
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("=== METADANE FILMU ===")
    print(f"Tytuł:           {meta['title']}")
    print(f"Kanał:           {meta['channel_name']}")
    print(f"Link do kanału:  {meta['channel_url']}")
    print(f"Link do filmu:   {meta['video_url']}")
    print(f"Data publikacji: {meta['published_date']}")
    print(f"Długość:         {meta['duration']}")
    print("-" * 50)
    print("=== TRANSKRYPCJA ===")
    
    for s in snippets:
        if args.timestamps:
            sec = int(s.start)
            ts = f"[{sec // 60:02d}:{sec % 60:02d}]"
            print(f"{ts} {s.text}")
        else:
            print(s.text)

if __name__ == "__main__":
    main()
