from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def project_root() -> Path:
    """
    Возвращает корневую папку репозитория ONYX.

    Текущий файл:
    ONYX/engine/jobs/create_job.py

    parents[0] -> jobs
    parents[1] -> engine
    parents[2] -> ONYX
    """
    return Path(__file__).resolve().parents[2]


def load_settings() -> dict[str, Any]:
    """Загружает глобальные настройки ONYX из config/settings.yaml."""
    settings_path = project_root() / "config" / "settings.yaml"

    if not settings_path.exists():
        raise FileNotFoundError(
            f"Не найден файл настроек:\n{settings_path}"
        )

    with settings_path.open("r", encoding="utf-8") as file:
        settings = yaml.safe_load(file)

    if not isinstance(settings, dict):
        raise ValueError(
            f"Ожидался YAML-объект в файле:\n{settings_path}"
        )

    required_sections = (
        "clients_root",
        "comfyui",
        "facefusion",
        "generation",
    )

    missing = [
        section
        for section in required_sections
        if section not in settings
    ]

    if missing:
        raise ValueError(
            "В settings.yaml отсутствуют разделы: "
            + ", ".join(missing)
        )

    return settings


def count_source_images(source_dir: Path) -> int:
    """Считает пригодные исходные изображения клиента."""
    if not source_dir.exists():
        return 0

    return sum(
        path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        for path in source_dir.iterdir()
    )


def write_json(path: Path, data: dict[str, Any]) -> None:
    """Безопасно записывает JSON через временный файл."""
    temporary = path.with_suffix(path.suffix + ".tmp")

    with temporary.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    temporary.replace(path)


def create_job(client: str, job_name: str) -> Path:
    """
    Создает новое задание ONYX и формирует job.json.

    Исходные фотографии клиента не копируются в задание.
    Они постоянно хранятся в Clients/<Client>/source.
    """
    settings = load_settings()
    onyx_root = project_root()

    clients_root = Path(settings["clients_root"]).expanduser().resolve()
    client_root = clients_root / client

    profile_dir = client_root / "profile"
    source_dir = client_root / "source"
    jobs_dir = client_root / "jobs"
    job_dir = jobs_dir / job_name

    # Постоянная структура клиента.
    profile_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)
    jobs_dir.mkdir(parents=True, exist_ok=True)

    # Структура конкретного задания.
    for folder_name in (
        "02_scenes",
        "03_face_swapped",
        "04_final",
        "logs",
    ):
        (job_dir / folder_name).mkdir(parents=True, exist_ok=True)

    profile_path = profile_dir / "client_profile.json"

    generator_path = (
        onyx_root
        / "engine"
        / "scene_generator"
        / "generator.py"
    )

    facefusion_runner_path = (
        onyx_root
        / "engine"
        / "facefusion"
        / "runner.py"
    )

    scene_workflow_path = (
        onyx_root
        / "comfyui-workflows"
        / "Scene_Generator_Random_API.json"
    )

    postprocess_workflow_path = (
        onyx_root
        / "comfyui-workflows"
        / "Portrait_PostProcessor_1.0_API.json"
    )

    comfyui_root = Path(settings["comfyui"]["root"]).expanduser()
    comfyui_server = str(settings["comfyui"]["server"])
    comfyui_timeout = int(settings["comfyui"].get("timeout", 1800))

    facefusion_root = Path(
        settings["facefusion"]["root"]
    ).expanduser()

    facefusion_python = Path(
        settings["facefusion"]["python"]
    ).expanduser()

    scene_count = int(
        settings["generation"].get("scene_count", 8)
    )

    job: dict[str, Any] = {
        "schema_version": "1.0",
        "job_id": job_name,
        "client_id": client,
        "paths": {
            "client_profile": str(profile_path),
        },
        "pipeline": {
            "scene_generator": {
                "enabled": True,
                "command": [
                    "{python}",
                    str(generator_path),
                    "--server",
                    comfyui_server,
                    "--comfy-output",
                    str(comfyui_root / "output"),
                    "--timeout",
                    str(comfyui_timeout),
                    "scenes",
                    "--workflow",
                    str(scene_workflow_path),
                    "--profile",
                    "{client_profile}",
                    "--output-dir",
                    "{output_dir}",
                    "--count",
                    str(scene_count),
                ],
                "minimum_output_images": scene_count,
            },
            "facefusion": {
                "enabled": True,
                "command": [
                    "{python}",
                    str(facefusion_runner_path),
                    "--facefusion-folder",
                    str(facefusion_root),
                    "--python",
                    str(facefusion_python),
                    "--source-dir",
                    "{source_dir}",
                    "--target-dir",
                    "{input_dir}",
                    "--output-dir",
                    "{output_dir}",
                ],
                "minimum_output_images": 1,
            },
            "postprocessor": {
                "enabled": True,
                "command": [
                    "{python}",
                    str(generator_path),
                    "--server",
                    comfyui_server,
                    "--comfy-output",
                    str(comfyui_root / "output"),
                    "--timeout",
                    str(comfyui_timeout),
                    "postprocess",
                    "--workflow",
                    str(postprocess_workflow_path),
                    "--profile",
                    "{client_profile}",
                    "--input-dir",
                    "{input_dir}",
                    "--output-dir",
                    "{output_dir}",
                    "--comfy-input",
                    str(comfyui_root / "input"),
                ],
                "minimum_output_images": 1,
            },
        },
    }

    job_file = job_dir / "job.json"
    write_json(job_file, job)

    source_count = count_source_images(source_dir)

    print("=" * 70)
    print("ONYX JOB CREATED")
    print("=" * 70)
    print(f"Клиент:           {client}")
    print(f"Задание:          {job_name}")
    print(f"Папка задания:    {job_dir}")
    print(f"Профиль клиента:  {profile_path}")
    print(f"Исходные фото:    {source_dir}")
    print(f"Найдено фото:     {source_count}")
    print(f"Количество сцен:  {scene_count}")
    print(f"Job-файл:         {job_file}")

    if not profile_path.exists():
        print()
        print(
            "ПРЕДУПРЕЖДЕНИЕ: client_profile.json пока отсутствует."
        )

    if source_count == 0:
        print()
        print(
            "ПРЕДУПРЕЖДЕНИЕ: в постоянной папке source "
            "нет фотографий клиента."
        )
        print(
            "Генерация сцен возможна, но FaceFusion "
            "не сможет выполнить замену лица."
        )

    return job_dir