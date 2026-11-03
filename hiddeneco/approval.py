"""Human approval checkpoint. Nothing is published without a named reviewer approving the exact
video file that passed QC. Even then, this MVP only assembles an upload package - it never
calls the YouTube API."""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone

from hiddeneco.config import ProjectPaths


class ApprovalError(RuntimeError):
    pass


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _qc(paths: ProjectPaths) -> dict:
    p = paths.out / "qc" / "qc_report.json"
    if not p.exists():
        raise ApprovalError("No QC report. Run the build first.")
    return json.loads(p.read_text())


def approve(paths: ProjectPaths, reviewer: str, notes: str = "") -> dict:
    if not reviewer.strip():
        raise ApprovalError("A named reviewer is required.")
    qc = _qc(paths)
    if not qc["passed"]:
        raise ApprovalError(f"QC has {qc['errors']} error(s). Fix them before approval.")
    if qc["publish_blockers"]:
        ids = ", ".join(b["claim"] for b in qc["publish_blockers"])
        raise ApprovalError(f"Unverified claims block approval: {ids}. Verify them in sources.yaml "
                            "(status: human_verified, verified_by: <name>) and rebuild.")
    if not paths.final_video.exists():
        raise ApprovalError("Final video missing.")
    record = {"decision": "approved", "reviewer": reviewer, "notes": notes,
              "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "video_sha256": sha256(paths.final_video),
              "qc_sha256": sha256(paths.out / "qc" / "qc_report.json")}
    (paths.out / "approval.json").write_text(json.dumps(record, indent=2))
    return record


def check_approved(paths: ProjectPaths) -> dict:
    p = paths.out / "approval.json"
    if not p.exists():
        raise ApprovalError("Not approved. Run: python -m hiddeneco approve <slug> --reviewer 'Name'")
    rec = json.loads(p.read_text())
    if rec.get("decision") != "approved":
        raise ApprovalError("Latest decision is not 'approved'.")
    if rec["video_sha256"] != sha256(paths.final_video):
        raise ApprovalError("Video changed since approval. Re-run QC and approval.")
    return rec


def package_for_upload(paths: ProjectPaths) -> str:
    rec = check_approved(paths)
    drafts = paths.out / "exports_draft"
    if not drafts.exists():
        raise ApprovalError("No export drafts found. Rebuild first.")
    pkg = paths.out / "publish_package"
    if pkg.exists():
        shutil.rmtree(pkg)
    shutil.copytree(drafts, pkg)
    for platform_dir in pkg.iterdir():
        shutil.copy2(paths.out / "approval.json", platform_dir / "approval.json")
        cl = platform_dir / "CHECKLIST.md"
        if cl.exists():
            cl.write_text(cl.read_text().replace("DRAFT (not approved)", f"APPROVED by {rec['reviewer']}"))
    return (f"Approved by {rec['reviewer']} at {rec['at']}. Packages ready at {pkg} "
            f"({', '.join(sorted(p.name for p in pkg.iterdir()))}). Automatic upload is intentionally "
            "not implemented; upload manually after re-checking each CHECKLIST.md.")
