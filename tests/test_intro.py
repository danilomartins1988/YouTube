import numpy as np

from hiddeneco.intro import INTRO_SECONDS, insert_intro, signature
from hiddeneco.models import Scene, Script, Segment, Storyboard


def _fixture():
    segs = [Segment(id="hook", narration="x" * 200), Segment(id="more", narration="y" * 200),
            Segment(id="card", narration=""), Segment(id="body", narration="z" * 300)]
    scenes = [Scene(id=f"s{i}", segment=s.id, type="kinetic_text") for i, s in enumerate(segs)]
    return Script(title="t", segments=segs), Storyboard(scenes=scenes)


def test_intro_goes_after_the_hook_and_only_once():
    sc, sb = _fixture()
    proj = {"renderer": "remotion"}
    sc2, sb2, after = insert_intro(proj, sc, sb, render=lambda x: x)
    assert after == "hook"                                  # 200 chars ~ 14.6 s >= 10 s: the natural end of the hook
    assert [s.type for s in sb2.scenes][1] == "channel_intro"
    assert [s.id for s in sc2.segments][1] == "channel_intro"
    sc3, sb3, again = insert_intro(proj, sc2, sb2, render=lambda x: x)
    assert again is None and len(sb3.scenes) == len(sb2.scenes)   # no duplicates


def test_intro_can_be_disabled_or_placed_explicitly():
    sc, sb = _fixture()
    assert insert_intro({"renderer": "remotion", "intro": {"enabled": False}}, sc, sb, render=lambda x: x)[2] is None
    assert insert_intro({"renderer": "ffmpeg"}, sc, sb, render=lambda x: x)[2] is None
    assert insert_intro({"renderer": "remotion", "intro": {"after_segment": "more"}}, sc, sb, render=lambda x: x)[2] == "more"


def test_signature_is_five_seconds_and_does_not_clip():
    x = signature()
    assert abs(len(x) / 48000 - INTRO_SECONDS) < 1e-6
    assert 0.8 < np.max(np.abs(x)) < 0.95
