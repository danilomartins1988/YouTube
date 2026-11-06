"""Automated animation QA for the animation-engine demo (or any engine preview).

    python tools/engine_qa.py [video] [out_dir]
      default video: output/engine/engine_demo_30s.mp4, out_dir: docs/engine/qa

Checks (all measured from the rendered file or from the engine's own maths, never assumed):
  1. file exists, exact duration, 1920x1080, 30 fps, frame count
  2. blank/black frames (ffmpeg blackdetect) and frozen picture (freezedetect)
  3. motion energy: mean absolute frame difference at 10 fps, per 0.5 s window and per scene; flags windows
     with almost no change (static) and reports the quietest window of every scene
  4. clipping: bright content touching the frame edge outside map/full-bleed scenes
  5. readability: WCAG contrast of the palette's text colours on the background; minimum font size in code
  6. SVG errors: renders sample stills with verbose logs and scans for NaN / invalid attribute / errors
  7. motion probe (tools: esbuild + node): presenter joints and travel, marker tip vs active stroke distance,
     reveal monotonicity, pointing accuracy, map camera movement
  8. filmstrips: 8 consecutive frames (0.1 s apart) per scene, so motion can be inspected, plus a contact sheet
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REM = ROOT / "remotion"
SCENES = [("1 presenter draws", 0, 6), ("2 economic flow", 6, 12), ("3 world map", 12, 18), ("4 exploded chip", 18, 24), ("5 network -> chart -> title", 24, 30)]
FULL_BLEED = [(11.8, 18.5)]          # the map is intentionally full-bleed


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe(video: Path) -> dict:
    out = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                          "stream=width,height,r_frame_rate,nb_read_frames,codec_name:format=duration", "-of", "json", str(video)]).stdout)
    s = out["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return {"width": s["width"], "height": s["height"], "fps": float(num) / float(den), "frames": int(s["nb_read_frames"]),
            "duration_s": float(out["format"]["duration"]), "codec": s["codec_name"]}


def detect(video: Path, filt: str, key: str) -> list[str]:
    err = run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", filt, "-an", "-f", "null", "-"]).stderr
    return [ln.strip() for ln in err.splitlines() if key in ln]


def frames_gray(video: Path, fps: int = 10, w: int = 480, h: int = 270) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", f"fps={fps},scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w).astype(np.float32)


def contrast(c1: str, c2: str) -> float:
    def lum(h):
        r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
    a, b = sorted([lum(c1), lum(c2)], reverse=True)
    return (a + 0.05) / (b + 0.05)


def main() -> None:
    video = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "output/engine/engine_demo_30s.mp4"
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "docs/engine/qa"
    out_dir.mkdir(parents=True, exist_ok=True)
    R: dict = {"video": str(video.relative_to(ROOT)) if video.is_relative_to(ROOT) else str(video), "exists": video.exists()}
    if not video.exists():
        print(json.dumps(R)); sys.exit(1)
    R["probe"] = probe(video)
    p = R["probe"]
    R["checks"] = {}
    C = R["checks"]
    C["duration_30s"] = abs(p["duration_s"] - 30.0) < 0.05 and p["frames"] == 900
    C["resolution_1920x1080"] = (p["width"], p["height"]) == (1920, 1080)
    C["fps_30"] = abs(p["fps"] - 30) < 1e-6
    # 2. black / frozen
    black = detect(video, "blackdetect=d=0.1:pix_th=0.06", "black_start")
    R["black_segments"] = black
    # the film opens with an iris and ends with an intentional fade to black in the last ~0.45 s
    bad_black = [b for b in black if not re.search(r"black_start:(29\.[5-9]|30)", b) and not re.search(r"black_start:0(\.0+)?\b", b)]
    C["no_unexpected_black"] = not bad_black
    frozen = detect(video, "freezedetect=n=0.0015:d=1.0", "freeze_start")
    R["frozen_segments"] = frozen
    C["no_frozen_over_1s"] = not frozen
    # 3. motion energy
    g = frames_gray(video)
    diff = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))          # per 0.1 s
    win = [float(diff[i:i + 5].mean()) for i in range(0, len(diff) - 4, 5)]   # 0.5 s windows
    R["motion_energy_windows"] = [round(v, 3) for v in win]
    static = [i * 0.5 for i, v in enumerate(win) if v < 0.15 and i * 0.5 < 29.4]
    R["static_windows_s"] = static
    C["no_static_half_seconds"] = not static
    R["scene_motion"] = {}
    for name, a, b in SCENES:
        seg = win[int(a * 2): int(b * 2)]
        R["scene_motion"][name] = {"mean": round(float(np.mean(seg)), 3), "quietest_window": round(float(np.min(seg)), 3)}
    # 4. clipping at edges (bright pixels in a 6 px border, outside full-bleed scenes)
    clip = []
    for i, fr in enumerate(g):
        t = i / 10
        if any(a <= t <= b for a, b in FULL_BLEED):
            continue
        border = np.concatenate([fr[:3].ravel(), fr[-3:].ravel(), fr[:, :3].ravel(), fr[:, -3:].ravel()])
        if (border > 200).mean() > 0.01:
            clip.append(round(t, 1))
    R["edge_bright_times_s"] = clip
    C["no_edge_clipping"] = not clip
    # 5. readability
    pal = {"bg": "#07111F", "panel": "#101B2E", "ink": "#F4F1EA", "muted": "#8B98AA", "gold": "#D4AF5A", "blue": "#5EA8E6", "teal": "#7FC8B8"}
    R["contrast_on_bg"] = {k: round(contrast(v, pal["bg"]), 2) for k, v in pal.items() if k not in ("bg",)}
    R["contrast_on_panel"] = {k: round(contrast(v, pal["panel"]), 2) for k, v in pal.items() if k in ("ink", "muted", "gold")}
    sizes = []
    for f in (REM / "src/animation-engine").rglob("*.tsx"):
        sizes += [int(x) for x in re.findall(r"fontSize=\{(\d+)", f.read_text())]
    R["min_font_px_in_code"] = min(sizes)
    C["text_contrast_AA"] = min(R["contrast_on_bg"][k] for k in ("ink", "muted", "gold", "blue", "teal")) >= 4.5
    C["min_font_18px"] = R["min_font_px_in_code"] >= 18
    # 6. SVG / runtime errors on sample stills
    props = ROOT / "output/engine/props.json"
    logs = ""
    for fr in [60, 120, 250, 330, 420, 500, 600, 660, 760, 840]:
        r = run(["npx", "remotion", "still", "src/index.ts", "EngineDemo", f"/tmp/engine_qa_{fr}.png", f"--frame={fr}", "--scale=0.25",
                 f"--props={props}", "--log=verbose", "--gl=angle", "--browser-executable=/opt/pw-browsers/chromium"], cwd=REM)
        logs += r.stdout + r.stderr
    errs = sorted(set(m for m in re.findall(r"[^\n]*(?:NaN|is not a valid|Invalid|TypeError|ReferenceError|Error:)[^\n]*", logs)))
    R["svg_runtime_errors"] = errs[:20]
    C["no_svg_runtime_errors"] = not errs
    # 7. motion probe (engine maths)
    pj = out_dir / "probe.cjs"
    subprocess.run(["npx", "esbuild", "src/animation-engine/qa/probe.ts", "--bundle", "--platform=node", "--format=cjs", "--jsx=automatic",
                    f"--outfile={pj}", "--log-level=warning"], cwd=REM, check=True)
    pr = json.loads(run(["node", str(pj)]).stdout)
    pj.unlink()
    R["motion_probe"] = pr
    C["presenter_walks"] = max(pr["presenter_walk_x"]) - min(pr["presenter_walk_x"]) > 500
    C["presenter_anticipation_lean"] = min(pr["presenter_lean_deg"]) < -2 and max(pr["presenter_lean_deg"]) > 2
    C["marker_tip_on_path"] = pr["draw_tip_error_px"]["mean"] < 2 and pr["draw_tip_error_px"]["max"] < 12
    C["arm_moves_while_drawing"] = pr["draw_elbow_range_px"]["x"] > 200 and pr["draw_elbow_range_px"]["y"] > 100
    C["body_follows_pen"] = pr["draw_body_range_px"] > 300
    C["drawing_reveals_progressively"] = pr["draw_reveal_monotonic"]
    C["pointing_reaches_target"] = pr["point_state_active"] and pr["point_hand_to_target_px"] < 4
    cams = pr["map_camera"]
    C["map_camera_moves"] = len({tuple(c) for c in cams}) >= 3
    # 8. filmstrips + contact sheet
    big = frames_gray  # noqa
    strip_dir = out_dir / "filmstrips"
    strip_dir.mkdir(exist_ok=True)
    picks = {"1_presenter_walk": 0.9, "1_presenter_draws": 3.3, "1_presenter_points": 5.2, "2_chart_to_flow": 6.3, "2_flow_processing": 9.0,
             "2_payments": 11.1, "3_flow_to_map": 12.2, "3_routes": 13.6, "3_camera_pan": 15.2, "4_dive": 17.7, "4_explode": 19.2,
             "4_reassemble": 22.3, "5_network": 24.5, "5_bars": 26.2, "5_title": 28.1}
    for name, t0 in picks.items():
        ims = []
        for k in range(8):
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0 + k * 0.1:.2f}", "-i", str(video), "-frames:v", "1", "-vf", "scale=480:270",
                                  "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True).stdout
            ims.append(Image.open(__import__("io").BytesIO(raw)).convert("RGB"))
        sheet = Image.new("RGB", (480 * 4, 270 * 2))
        for k, im in enumerate(ims):
            sheet.paste(im, ((k % 4) * 480, (k // 4) * 270))
        sheet.save(strip_dir / f"{name}.jpg", quality=82)
    R["filmstrips"] = sorted(str(p.relative_to(ROOT)) for p in strip_dir.glob("*.jpg"))
    R["passed"] = all(C.values())
    (out_dir / "engine_qa.json").write_text(json.dumps(R, indent=1))
    print(json.dumps({"checks": C, "passed": R["passed"], "static_windows_s": static, "black": black, "frozen": frozen,
                      "edge": clip[:20], "svg_errors": errs[:5], "scene_motion": R["scene_motion"]}, indent=1))


if __name__ == "__main__":
    main()
