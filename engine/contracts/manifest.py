from __future__ import annotations

import json

from .models import Manifest
from .validation import validate_manifest


def loads_manifest(text: str, *, validate: bool = True) -> Manifest:
    manifest = Manifest.from_dict(json.loads(text))
    if validate:
        validate_manifest(manifest)
    return manifest


def dumps_manifest(manifest: Manifest, *, indent: int = 2) -> str:
    validate_manifest(manifest)
    return json.dumps(manifest.to_dict(), ensure_ascii=False, indent=indent) + "\n"

