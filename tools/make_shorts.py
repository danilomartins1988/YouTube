"""Builds a vertical YouTube Short (1080x1920) for each finished episode from its own opening hook.

The Short reuses the episode's already-narrated, fact-checked opening segments (everything before the first act card,
skipping the channel intro), cut from the final MP4 with the timings in timeline.json. Layout, inside the 9:16 safe
zone (top 250, bottom 480, right 140): a big two-line hook headline on top, the 16:9 picture in the middle, burned-in
word captions (from the timeline's word timings) below, and a 2.5 s end card pointing to the full episode.
No new narration, no new figures: every word and number comes from the published episode.

Run: python tools/make_shorts.py [episode-id ...]   (default: every entry in SHORTS)
Writes output/shorts/<ep>_short.mp4 and docs/episodes/<ep>/youtube-short/{short_package.md,cover.png}.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_B = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
FONT_M = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"
W, H = 1080, 1920
VID_Y, VID_H = 600, 767
CROP_W = 1520  # centre crop of the 1920x1080 picture (keeps the centred callouts), scaled to 1080 wide
LEAD_IN = 0.35
MAX_SECONDS = 58.0
BG = (11, 15, 26)
GOLD = (255, 194, 26)

# ep id: (slug, deliverable, video name, hook line 1, hook line 2 (accent), short title, hashtags)
SHORTS = {
    "01-switzerland": ("why-switzerland-is-so-rich", "documentary", "switzerland_documentary", "HOW DID THIS TINY COUNTRY", "GET SO RICH?", "How Did Switzerland Get So Rich?", "#switzerland #economics"),
    "02-dubai": ("how-dubai-really-makes-money", "documentary", "dubai_documentary", "DUBAI ISN'T RICH", "BECAUSE OF OIL", "Dubai Doesn't Make Its Money the Way You Think", "#dubai #economics"),
    "03-formula1": ("the-hidden-business-of-formula-1", "documentary", "formula1_documentary", "WHO REALLY GETS RICH", "FROM FORMULA 1?", "Who Really Gets Rich From Formula 1?", "#formula1 #f1 #business"),
    "04-norway": ("why-norway-is-so-rich", "documentary", "norway_documentary", "NORWAY FOUND OIL.", "THEN IT DID THIS", "How Norway Turned Oil Into a Fortune", "#norway #oil #economics"),
    "06-nvidia": ("how-nvidia-took-over-the-ai-economy", "documentary_presenter", "nvidia_documentary_presenter", "ONE CHIP COMPANY", "TOOK OVER AI", "How Nvidia Took Over the AI Economy", "#nvidia #ai #chips"),
    "07-taiwan-v2": ("why-taiwan-matters-cartoon", "documentary", "taiwan_v2_documentary", "THE ISLAND THE WORLD", "CAN'T AFFORD TO LOSE", "Why Taiwan Matters So Much", "#taiwan #chips #economics"),
    "08-asml": ("the-machine-only-one-company-can-build", "documentary", "asml_documentary", "ONLY ONE COMPANY", "CAN BUILD THIS MACHINE", "The Machine Only One Company on Earth Can Build", "#asml #chips #technology"),
    "09-cables": ("the-cables-at-the-bottom-of-the-ocean", "documentary", "cables_documentary", "YOUR INTERNET RUNS", "UNDER THE OCEAN", "The Internet Runs Under the Ocean", "#internet #cables #technology"),
    "10-anguilla": ("the-island-getting-rich-from-ai", "documentary", "anguilla_documentary", "A TINY ISLAND IS", "GETTING RICH FROM .AI", "The Tiny Island Getting Rich From AI", "#ai #anguilla #economics"),
    "11-flags": ("why-ships-fly-foreign-flags", "documentary", "flags_documentary", "WHY SHIPS FLY FLAGS", "OF TINY COUNTRIES", "Why Almost Half the World's Ships Fly Three Small Flags", "#shipping #economics"),
    "12-wirecard": ("the-2-billion-that-never-existed", "documentary", "wirecard_documentary", "$2 BILLION", "THAT NEVER EXISTED", "The $2 Billion That Never Existed", "#wirecard #fraud #finance"),
    "13-volkswagen": ("the-day-volkswagen-became-the-most-valuable-company", "documentary", "volkswagen_documentary", "THE DAY VOLKSWAGEN", "WAS WORTH THE MOST", "The Day Volkswagen Became the World's Most Valuable Company", "#volkswagen #stocks #finance"),
    "14-memory": ("the-three-companies-that-decide-memory-prices", "documentary", "memory_documentary", "3 COMPANIES DECIDE", "WHAT YOUR MEMORY COSTS", "Three Companies Decide What Your Memory Costs", "#chips #memory #economics"),
    "15-nanoimprint": ("the-stamp-that-could-break-asmls-monopoly", "documentary", "nanoimprint_documentary", "CAN A STAMP BEAT", "A $400 MILLION MACHINE?", "Can a Stamp Beat a $400 Million Machine?", "#asml #canon #chips"),
    "16-terafab": ("why-elon-musk-wants-his-own-chip-factory", "documentary", "terafab_documentary", "WHY ELON MUSK WANTS", "HIS OWN CHIP FACTORY", "Why Elon Musk Wants His Own Chip Factory", "#elonmusk #tesla #chips"),
    "17-india-chips": ("indias-chip-plants-dont-make-chips", "documentary", "india_chips_documentary", "INDIA'S CHIP PLANTS", "DON'T MAKE CHIPS", "India's Chip Plants Don't Make Chips. That's the Plan", "#india #chips #economics"),
    "18-chip-chemicals": ("the-chemicals-that-decide-who-makes-chips", "documentary", "chip_chemicals_documentary", "NO CHEMICALS,", "NO CHIPS", "The Chemicals That Decide Who Makes Chips", "#chips #chemicals #economics"),
    "19-quibi": ("the-175-billion-app-that-lasted-six-months", "documentary", "quibi_documentary", "$1.75 BILLION APP.", "GONE IN 6 MONTHS", "The $1.75 Billion App That Lasted Six Months", "#quibi #streaming #business"),
    "20-notpetya": ("the-10-billion-cyberattack-that-froze-maersk", "documentary", "notpetya_documentary", "ONE SOFTWARE UPDATE.", "$10 BILLION IN DAMAGE", "One Software Update Froze the World's Biggest Shipping Company", "#cybersecurity #maersk #shipping"),
    "22-iceland": ("how-three-banks-nearly-destroyed-an-entire-country", "documentary", "iceland_documentary", "3 BANKS GREW ~9X", "BIGGER THAN THEIR COUNTRY", "How Three Banks Nearly Destroyed an Entire Country", "#iceland #banking #economics"),
    "21-citibank": ("the-bank-that-accidentally-sent-900-million", "documentary", "citibank_documentary", "A BANK SENT $900M", "BY MISTAKE", "The Bank That Accidentally Sent $900 Million", "#citibank #banking #finance"),
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"command failed: {' '.join(cmd[:6])}…\n{r.stderr[-1500:]}")
    return r.stdout


def fit(draw, text, font_path, max_w, start):
    size = start
    while size > 40:
        f = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(font_path, size)


def headline_layer(l1, l2, path, end=False):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    maxw = W - 60 - 140
    cx = 60 + maxw / 2
    f1 = fit(d, l1, FONT_B, maxw, 104)
    f2 = fit(d, l2, FONT_B, maxw, 120)
    y = 290
    d.text((cx, y), l1, font=f1, fill=(255, 255, 255), anchor="ma", stroke_width=6, stroke_fill=(0, 0, 0))
    y2 = y + f1.size + 26
    bw = d.textlength(l2, font=f2) + 56
    d.rounded_rectangle([cx - bw / 2, y2 - 14, cx + bw / 2, y2 + f2.size + 22], radius=22, fill=GOLD)
    d.text((cx, y2), l2, font=f2, fill=(12, 12, 12), anchor="ma")
    fb = ImageFont.truetype(FONT_M, 34)
    d.text((cx, 262), "THE HIDDEN ECONOMICS", font=fb, fill=(170, 180, 200), anchor="ma")
    if end:
        fe = ImageFont.truetype(FONT_B, 66)
        d.rounded_rectangle([90, 820, W - 150, 1160], radius=36, fill=(255, 255, 255))
        d.text((cx, 880), "FULL STORY", font=fe, fill=(12, 12, 12), anchor="ma")
        d.text((cx, 970), "ON THE CHANNEL", font=fe, fill=(12, 12, 12), anchor="ma")
        d.text((cx, 1070), "every figure sourced", font=ImageFont.truetype(FONT_M, 40), fill=(90, 90, 90), anchor="ma")
    im.save(path)


def ass_time(t):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def captions(segs, path):
    lines = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "", "[V4+ Styles]",
             "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
             "Style: Cap,Inter Display ExtraBold,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,7,2,8,60,140,0,1",
             "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for off, words in segs:
        chunk = []
        for k, w in enumerate(words):
            chunk.append(w)
            last = k == len(words) - 1
            if len(chunk) == 3 or last or w["word"].endswith((".", ",", "?", "!")):
                a, b = off + chunk[0]["start"], off + chunk[-1]["end"] + 0.08
                if not last:
                    b = min(b, off + words[k + 1]["start"])
                txt = " ".join(c["word"] for c in chunk).upper()
                lines.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,1395,,{{\\fad(40,0)}}{txt}")
                chunk = []
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def build(ep):
    slug, dv, vname, l1, l2, title, tags = SHORTS[ep]
    video = ROOT / "output" / f"{vname}.mp4"
    tl = json.loads((ROOT / "output" / slug / dv / "timeline.json").read_text())
    picks, total = [], 0.0
    for x in tl:
        seg, typ = x["scene"]["segment"], x["scene"]["type"]
        if typ == "act_title" or seg.endswith("_card"):
            break
        if seg == "channel_intro" or typ == "channel_intro":
            continue
        if picks and total + x["duration"] > MAX_SECONDS:
            break
        picks.append(x)
        total += x["duration"]
    work = ROOT / "output" / "shorts" / ep
    work.mkdir(parents=True, exist_ok=True)
    headline_layer(l1, l2, work / "top.png")
    headline_layer(l1, l2, work / "end.png", end=True)
    segs, off = [], 0.0
    for x in picks:
        segs.append((off + LEAD_IN, x.get("words") or []))
        off += x["duration"]
    captions(segs, work / "caps.ass")
    # 1) cut + join the opening segments
    parts = "".join(f"[0:v]trim={x['start']}:{x['start'] + x['duration']},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={x['start']}:{x['start'] + x['duration']},asetpts=PTS-STARTPTS[a{i}];" for i, x in enumerate(picks))
    cat = "".join(f"[v{i}][a{i}]" for i in range(len(picks))) + f"concat=n={len(picks)}:v=1:a=1[cv][ca]"
    fc = (parts + cat + f";[cv]crop={CROP_W}:1080,scale={W}:{VID_H}:flags=lanczos[sv];color=c=0x0B0F1A:s={W}x{H}:d={total}[bg];[bg][sv]overlay=0:{VID_Y}:shortest=1[b1];"
          f"[b1][1:v]overlay=0:0[b2];[b2]ass={work / 'caps.ass'}[outv];[ca]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[outa]")
    body = work / "body.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video), "-loop", "1", "-i", str(work / "top.png"),
         "-filter_complex", fc, "-map", "[outv]", "-map", "[outa]", "-t", f"{total:.3f}", "-r", "30",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(body)])
    # 2) end card (2.5 s) with the last frame of the picture underneath
    endc = work / "end.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-sseof", "-0.1", "-i", str(body), "-loop", "1", "-i", str(work / "end.png"),
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
         "-filter_complex", "[0:v]trim=end_frame=1,loop=loop=-1:size=1,setpts=N/30/TB,boxblur=8[b];[b][1:v]overlay=0:0[v]",
         "-map", "[v]", "-map", "2:a", "-t", "2.5", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(endc)])
    out = ROOT / "output" / "shorts" / f"{ep}_short.mp4"
    lst = work / "list.txt"
    lst.write_text(f"file '{body}'\nfile '{endc}'\n")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(out)])
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)]).strip())
    # cover frame + package
    pkg = ROOT / "docs" / "episodes" / ep / "youtube-short"
    pkg.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", "1.2", "-i", str(out), "-frames:v", "1", str(pkg / "cover.png")])
    long_title = (ROOT / "docs" / "episodes" / ep / "youtube-package" / "title.txt")
    lt = long_title.read_text().strip() if long_title.exists() else ""
    narration = " ".join(" ".join(w["word"] for w in (x.get("words") or [])) for x in picks)
    (pkg / "short_package.md").write_text(
        f"# YouTube Short: \"{title}\" ({ep})\n\nPrepared for manual publishing. Nothing has been uploaded. "
        f"File: `output/shorts/{ep}_short.mp4` ({dur:.0f} s, 1080x1920, captions burned in). Not committed (MP4).\n\n"
        f"Built by `tools/make_shorts.py` from the episode's own opening ({len(picks)} narrated segments, same audio and "
        f"sources as the full episode; no new figures).\n\n## Title\n\n```\n{title} #shorts\n```\n\n## Description\n\n```\n"
        f"{title}. The full story, with every figure sourced, is in the long video on the channel: \"{lt}\".\n\n"
        f"{tags} #shorts #economics\n```\n\n## On-screen hook\n\n```\n{l1}\n{l2}\n```\n\n## Narration in the Short\n\n> {narration}\n\n"
        f"## Publishing note\n\nLink the Short to the full video with YouTube's \"Related video\" field after both are uploaded.\n",
        encoding="utf-8")
    return out, dur, len(picks)


if __name__ == "__main__":
    eps = sys.argv[1:] or list(SHORTS)
    for ep in eps:
        if not (ROOT / "output" / f"{SHORTS[ep][2]}.mp4").exists():
            print(f"{ep}: SKIP (no final video yet)")
            continue
        out, dur, n = build(ep)
        print(f"{ep}: {out.relative_to(ROOT)} {dur:.1f}s ({n} segments)")
