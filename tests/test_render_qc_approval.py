import json

import pytest
import yaml

from hiddeneco import approval, qc
from hiddeneco import storyboard as sb
from hiddeneco.config import REPO_ROOT, settings
from hiddeneco.models import Scene, Storyboard, TimedScene
from hiddeneco.render.scenes import SCENES
from hiddeneco.render.style import Style

from .conftest import requires_ffmpeg


@pytest.fixture(scope="module")
def style_cfg(paths):
    return yaml.safe_load((paths.project_dir / "project.yaml").read_text())["style"]


@pytest.fixture(scope="module")
def style(style_cfg):
    return Style(style_cfg)


@pytest.mark.parametrize("deliv,size", [("documentary", (1920, 1080)), ("short_exports", (1080, 1920)),
                                        ("short_secrecy", (1080, 1920)), ("extended_franc", (1080, 1920))])
def test_every_scene_renders_in_its_format(paths, dossier, style_cfg, deliv, size):
    from hiddeneco import timing
    st = Style(style_cfg, *size)
    p = paths.for_deliverable(deliv)
    board = sb.rendered(sb.load_storyboard(p.deliverable_dir), dossier)
    words = timing.word_timings("In 1815 chemical of young people they made up drew a line", 0.4, 4.0)
    safe = settings()["formats"]["short_9x16"]["safe_zone"] if size[1] > size[0] else None
    for scene in board.scenes:
        r = SCENES[scene.type](st, scene.params, 6.0, narration="In 1815 chemical of young people",
                               lead=0.4, speech=5.0, credits=["Test"], words=words,
                               captions=timing.caption_chunks(words), safe=safe)
        for t in (0.0, 2.5, 5.9):
            assert r.frame(t, 0).size == size


def test_all_scene_types_covered(paths):
    used = set()
    for name in paths.deliverables():
        used |= {s.type for s in sb.load_storyboard(paths.for_deliverable(name).deliverable_dir).scenes}
    assert {"map", "bar_chart", "kinetic_text", "ring_stat", "pictogram", "ranking", "end_card",
            "big_number", "timeline", "line_chart", "split_compare", "act_title"} <= used


@requires_ffmpeg
def test_render_scene_to_mp4(tmp_path, style):
    from hiddeneco.render.assemble import probe, render_scene
    scene = Scene(id="t", segment="x", type="title_card", params={"title": "Test"})
    ts = TimedScene(scene=scene, narration="", audio_path="", audio_seconds=0.5, start=0, duration=1.0)
    fmt = settings()["formats"]["long_16x9"]
    out = render_scene(ts, style, [], tmp_path / "t.mp4", settings()["video"], fmt, captions=False)
    info = probe(out)
    v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    assert (v["width"], v["height"]) == (1920, 1080)


def test_licensing_rejects_unlisted_asset(dossier):
    board = Storyboard(scenes=[Scene(id="a", segment="hook", type="map", assets=["footage:random_clip"])])
    issues = qc.check_licensing(board, dossier)
    assert any(i["severity"] == "error" for i in issues)


def test_manifest_assets_are_allowlisted():
    manifest = yaml.safe_load((REPO_ROOT / "assets" / "manifest.yaml").read_text())["assets"]
    allow = settings()["licensing"]["allowlist"]
    assert all(a["license"] in allow for a in manifest.values())


def _fake_build(paths, qc_report):
    paths = paths
    paths.out.mkdir(parents=True, exist_ok=True)
    paths.final_video.write_bytes(b"video")
    (paths.out_sub("qc") / "qc_report.json").write_text(json.dumps(qc_report))


def test_approval_blocked_by_unverified_claims(vpaths):
    _fake_build(vpaths, {"passed": True, "errors": 0, "publish_blockers": [{"claim": "x"}]})
    with pytest.raises(approval.ApprovalError, match="Unverified"):
        approval.approve(vpaths, "Editor")


def test_approval_blocked_by_qc_errors(vpaths):
    _fake_build(vpaths, {"passed": False, "errors": 2, "publish_blockers": []})
    with pytest.raises(approval.ApprovalError, match="QC"):
        approval.approve(vpaths, "Editor")


def test_approval_exports_and_tamper_detection(vpaths):
    from hiddeneco import exports
    from hiddeneco.pipeline import load_deliverable
    _fake_build(vpaths, {"passed": True, "errors": 0, "publish_blockers": []})
    deliverable, _ = load_deliverable(vpaths)
    with pytest.raises(approval.ApprovalError, match="No export drafts"):
        approval.approve(vpaths, "Editor") and approval.package_for_upload(vpaths)
    drafts = exports.build_drafts(vpaths, deliverable)
    assert {d.name for d in drafts} == {"youtube_shorts", "instagram_reels"}
    assert "DRAFT" in (drafts[0] / "CHECKLIST.md").read_text()
    with pytest.raises(approval.ApprovalError):
        approval.approve(vpaths, "  ")
    approval.approve(vpaths, "Editor")
    msg = approval.package_for_upload(vpaths)
    assert "Packages ready" in msg
    assert "APPROVED by Editor" in (vpaths.out / "publish_package" / "youtube_shorts" / "CHECKLIST.md").read_text()
    vpaths.final_video.write_bytes(b"edited after approval")
    with pytest.raises(approval.ApprovalError, match="changed"):
        approval.package_for_upload(vpaths)
