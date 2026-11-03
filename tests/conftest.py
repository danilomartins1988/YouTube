import os
import shutil

import pytest

os.environ["HIDDENECO_OFFLINE"] = "1"   # tests never touch the network

SLUG = "why-switzerland-is-so-rich"


@pytest.fixture(scope="session")
def paths(tmp_path_factory):
    """A copy of the Switzerland project under a temp root so tests never write to output/."""
    from hiddeneco.config import REPO_ROOT, project_paths
    root = tmp_path_factory.mktemp("repo")
    shutil.copytree(REPO_ROOT / "projects" / SLUG, root / "projects" / SLUG)
    return project_paths(SLUG, root)


@pytest.fixture(scope="session")
def dossier(paths):
    from hiddeneco.research.dossier import build_dossier
    return build_dossier(paths)


requires_ffmpeg = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not installed")
