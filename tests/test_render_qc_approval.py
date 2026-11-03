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
def style(paths):
    return Style(yaml.safe_load((paths.project_dir / "project.yaml").read_text())["style"])


def test_every_scene_type_renders(paths, dossier, style):
    board = sb.rendered(sb.load_storyboard(paths.project_dir), dossier)
    seen = set()
    for scene in board.scenes:
        r = SCENES[scene.type](style, scene.params, 6.0, narration="In 1815 chemical of young people",
                               lead=0.4, speech=5.0, credits=["Test"])
        for t in (0.0, 2.5, 5.9):
            img = r.frame(t, 0)
            assert img.size == (1920, 1080)
        seen.add(scene.type)
    assert {"map", "bar_chart", "kinetic_text", "ring_stat", "pictogram", "ranking", "end_card"} <= seen


@requires_ffmpeg
def test_render_scene_to_mp4(tmp_path, style):
    from hiddeneco.render.assemble import probe, render_scene
    scene = Scene(id="t", segment="x", type="title_card", params={"title": "Test"})
    ts = TimedScene(scene=scene, narration="", audio_path="", audio_seconds=0.5, start=0, duration=1.0)
    out = render_scene(ts, style, [], tmp_path / "t.mp4", settings()["video"], 0.2)
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
    paths.out.mkdir(parents=True, exist_ok=True)
    paths.final_video.write_bytes(b"video")
    (paths.out_sub("qc") / "qc_report.json").write_text(json.dumps(qc_report))


def test_approval_blocked_by_unverified_claims(paths):
    _fake_build(paths, {"passed": True, "errors": 0, "publish_blockers": [{"claim": "x"}]})
    with pytest.raises(approval.ApprovalError, match="Unverified"):
        approval.approve(paths, "Editor")


def test_approval_blocked_by_qc_errors(paths):
    _fake_build(paths, {"passed": False, "errors": 2, "publish_blockers": []})
    with pytest.raises(approval.ApprovalError, match="QC"):
        approval.approve(paths, "Editor")


def test_approval_and_tamper_detection(paths):
    _fake_build(paths, {"passed": True, "errors": 0, "publish_blockers": []})
    with pytest.raises(approval.ApprovalError):
        approval.approve(paths, "  ")
    approval.approve(paths, "Editor")
    assert "Upload package ready" in approval.package_for_upload(paths)
    paths.final_video.write_bytes(b"edited after approval")
    with pytest.raises(approval.ApprovalError, match="changed"):
        approval.package_for_upload(paths)
