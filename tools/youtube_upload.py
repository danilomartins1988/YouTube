"""Upload a finished episode (or its Short) to YouTube as PRIVATE, using the YouTube Data API v3.

Safety rules (channel policy: nothing is published without the owner's explicit authorization):
- Default is a DRY RUN: it only prints what would be sent. Add --confirm to really upload.
- Privacy is always "private" unless --privacy is given explicitly; "public" also needs --i-am-the-owner-and-approve-public.
- Credentials are read from environment variables only and are never printed or written to disk:
    YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN   (OAuth client of the owner's own Google Cloud project)
- Every real upload is logged (no secrets) to docs/YOUTUBE_UPLOADS.md; an episode already in that log is refused unless --again.

Usage:
  python tools/youtube_upload.py check                         # verifies the credentials and shows the channel name
  python tools/youtube_upload.py episode 38-airports           # dry run of the long video
  python tools/youtube_upload.py episode 38-airports --confirm # private upload + thumbnail + English captions
  python tools/youtube_upload.py short 38-airports --confirm   # private upload of the Short
Standard library only (urllib), resumable upload in 8 MB chunks.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "docs/YOUTUBE_UPLOADS.md"
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
CHUNK = 8 * 1024 * 1024
CATEGORY_EDUCATION = "27"


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def access_token() -> str:
    need = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        die("missing environment variables: " + ", ".join(missing) + " (add them in the cloud environment settings)")
    body = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                   "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=60) as r:
            return json.load(r)["access_token"]
    except urllib.error.HTTPError as e:
        die(f"token refresh failed: HTTP {e.code} {e.read().decode(errors='replace')[:300]}")
    return ""


def call(method: str, url: str, tok: str, data: bytes | None = None, headers: dict | None = None, raw: bool = False):
    h = {"Authorization": f"Bearer {tok}", **(headers or {})}
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r if raw else json.load(r)
    except urllib.error.HTTPError as e:
        if raw and e.code == 308:
            return e
        die(f"{method} {url.split('?')[0]} failed: HTTP {e.code} {e.read().decode(errors='replace')[:500]}")


def episode_files(ep: str, kind: str) -> dict:
    d = ROOT / "docs/episodes" / ep
    if not d.is_dir():
        die(f"no folder docs/episodes/{ep}")
    if kind == "episode":
        pkg = d / "youtube-package"
        status = json.loads((pkg / "PACKAGE_STATUS.json").read_text())
        if not status.get("package_ready"):
            die("package not ready (PACKAGE_STATUS.json package_ready=false)")
        video = ROOT / (pkg / "video.txt").read_text().splitlines()[0].strip()
        title = (pkg / "title.txt").read_text().strip().splitlines()[0]
        desc = (pkg / "description.txt").read_text().strip()
        tags = [t.strip() for t in (pkg / "tags.txt").read_text().split(",") if t.strip()]
        return {"video": video, "title": title, "description": desc, "tags": tags, "thumb": pkg / "thumbnail.png",
                "srt": d / "subtitles_en.srt"}
    md = (d / "youtube-short/short_package.md").read_text()
    blocks = dict(re.findall(r"## (Title|Description|Tags)\s*\n+```\n(.*?)\n```", md, re.S))
    m = re.search(r"File: `([^`]+\.mp4)`", md)
    if not (m and "Title" in blocks):
        die("could not read the Short package")
    return {"video": ROOT / m.group(1), "title": blocks["Title"].strip(), "description": blocks.get("Description", "").strip(),
            "tags": [t.strip() for t in blocks.get("Tags", "").split(",") if t.strip()], "thumb": None, "srt": None}


def already_logged(key: str) -> bool:
    return LOG.exists() and f"| {key} |" in LOG.read_text()


def log(key: str, vid: str, title: str, privacy: str) -> None:
    if not LOG.exists():
        LOG.write_text("# YouTube uploads (made by tools/youtube_upload.py)\n\n| Key | Video ID | Privacy | Uploaded (UTC) | Title |\n|---|---|---|---|---|\n")
    with LOG.open("a") as f:
        f.write(f"| {key} | {vid} | {privacy} | {dt.datetime.utcnow():%Y-%m-%d %H:%M} | {title} |\n")


def upload(args) -> None:
    f = episode_files(args.ep, args.cmd)
    key = f"{args.ep}:{args.cmd}"
    if args.privacy == "public" and not args.i_am_the_owner_and_approve_public:
        die("public needs --i-am-the-owner-and-approve-public (owner's explicit authorization)")
    if not Path(f["video"]).exists():
        die(f"video file not found: {f['video']}")
    meta = {"snippet": {"title": f["title"][:100], "description": f["description"][:5000], "tags": f["tags"],
                        "categoryId": CATEGORY_EDUCATION, "defaultLanguage": "en", "defaultAudioLanguage": "en"},
            "status": {"privacyStatus": args.privacy, "selfDeclaredMadeForKids": False}}
    size = Path(f["video"]).stat().st_size
    print(f"{key}: {Path(f['video']).name} ({size / 1e6:.1f} MB) as {args.privacy.upper()}")
    print(f"  title: {meta['snippet']['title']}")
    print(f"  tags: {len(f['tags'])}, description: {len(meta['snippet']['description'])} chars, "
          f"thumbnail: {bool(f['thumb'] and f['thumb'].exists())}, captions: {bool(f['srt'] and f['srt'].exists())}")
    if not args.confirm:
        print("DRY RUN: nothing sent. Add --confirm to upload.")
        return
    if already_logged(key) and not args.again:
        die(f"{key} is already in docs/YOUTUBE_UPLOADS.md (use --again to upload a second copy)")
    tok = access_token()
    r = call("POST", f"{UPLOAD}/videos?uploadType=resumable&part=snippet,status", tok, json.dumps(meta).encode(),
             {"Content-Type": "application/json; charset=UTF-8", "X-Upload-Content-Type": "video/mp4",
              "X-Upload-Content-Length": str(size)}, raw=True)
    loc = r.headers["Location"]
    sent, res = 0, None
    with open(f["video"], "rb") as fh:
        while sent < size:
            chunk = fh.read(CHUNK)
            end = sent + len(chunk) - 1
            r = call("PUT", loc, tok, chunk, {"Content-Length": str(len(chunk)), "Content-Range": f"bytes {sent}-{end}/{size}"}, raw=True)
            sent = end + 1
            print(f"  uploaded {sent / size:5.1%}", end="\r")
            if getattr(r, "status", None) in (200, 201):
                res = json.load(r)
    print()
    if not res:
        die("upload finished without a video resource")
    vid = res["id"]
    print(f"  video id {vid} ({res['status']['privacyStatus']})")
    if f["thumb"] and f["thumb"].exists():
        call("POST", f"{UPLOAD}/thumbnails/set?videoId={vid}", tok, f["thumb"].read_bytes(), {"Content-Type": "image/png"})
        print("  thumbnail set")
    if f["srt"] and f["srt"].exists() and not args.no_captions:
        boundary = "hiddeneco-boundary"
        cap = json.dumps({"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}})
        body = (f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{cap}\r\n--{boundary}\r\n"
                f"Content-Type: application/octet-stream\r\n\r\n").encode() + f["srt"].read_bytes() + f"\r\n--{boundary}--".encode()
        call("POST", f"{UPLOAD}/captions?uploadType=multipart&part=snippet", tok, body, {"Content-Type": f"multipart/related; boundary={boundary}"})
        print("  English captions added")
    log(key, vid, f["title"], res["status"]["privacyStatus"])
    print(f"  logged in {LOG.relative_to(ROOT)}; open https://studio.youtube.com/video/{vid}/edit")


def check(_args) -> None:
    tok = access_token()
    me = call("GET", f"{API}/channels?part=snippet&mine=true", tok)
    items = me.get("items", [])
    print("channel:", items[0]["snippet"]["title"] if items else "(no channel on this account)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    for k in ("episode", "short"):
        p = sub.add_parser(k)
        p.add_argument("ep", help="docs/episodes folder, e.g. 38-airports")
        p.add_argument("--confirm", action="store_true", help="really upload (default: dry run)")
        p.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
        p.add_argument("--i-am-the-owner-and-approve-public", action="store_true")
        p.add_argument("--again", action="store_true")
        p.add_argument("--no-captions", action="store_true")
    a = ap.parse_args()
    check(a) if a.cmd == "check" else upload(a)


if __name__ == "__main__":
    main()
