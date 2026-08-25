from __future__ import annotations

import json
import os
from pathlib import Path

from .models import Manifest
from .validation import validate_manifest


def save_manifest_atomic(path: Path, manifest: Manifest) -> None:
    """Validate and atomically replace manifest.json on the same filesystem."""
    validate_manifest(manifest)
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".writing")
    payload = json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2) + "\n"
    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def load_manifest(path: Path, *, validate: bool = True) -> Manifest:
    manifest = Manifest.from_dict(json.loads(path.read_text(encoding="utf-8-sig")))
    if validate:
        validate_manifest(manifest)
    return manifest

