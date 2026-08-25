from __future__ import annotations

import json
from pathlib import Path

from .models import JobSpec
from .validation import validate_job_spec


def loads_job_spec(text: str, *, validate: bool = True) -> JobSpec:
    job = JobSpec.from_dict(json.loads(text))
    if validate:
        validate_job_spec(job)
    return job


def load_job_spec(path: Path, *, validate: bool = True) -> JobSpec:
    return loads_job_spec(path.read_text(encoding="utf-8-sig"), validate=validate)


def dumps_job_spec(job: JobSpec, *, indent: int = 2) -> str:
    validate_job_spec(job)
    return json.dumps(job.to_dict(), ensure_ascii=False, indent=indent) + "\n"

