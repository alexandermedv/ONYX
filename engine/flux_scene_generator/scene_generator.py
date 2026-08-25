from __future__ import annotations

import argparse
import copy
import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path

PROMPT_NODE = "56:51"
SAMPLER_NODE = "56:58"
LATENT_NODE = "56:50"
SAVE_NODE = "9"

GENDER_ALIASES = {
    "male": "male", "man": "male", "мужчина": "male", "мужской": "male",
    "female": "female", "woman": "female", "женщина": "female", "женский": "female",
}


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as stream:
        return json.load(stream)


def load_session_spec(session_path: Path) -> dict:
    session = read_json(session_path)

    if session.get("schema") != "onyx.session_spec":
        raise ValueError(
            'Session schema must be "onyx.session_spec"'
        )

    if session.get("schema_version") != "1.0":
        raise ValueError(
            'Session schema_version must be "1.0"'
        )

    if session.get("status") != "ready":
        raise ValueError(
            "Session must have status 'ready' before generation"
        )

    profile_value = session.get("client_profile")
    if not isinstance(profile_value, str) or not profile_value.strip():
        raise ValueError(
            "Session must contain client_profile"
        )

    profile_path = Path(profile_value)

    if not profile_path.is_absolute():
        profile_path = session_path.parent / profile_path

    if not profile_path.is_file():
        raise FileNotFoundError(
            f"Client profile not found: {profile_path}"
        )

    profile = read_json(profile_path)

    session_client_id = session.get("client_id")
    profile_client_id = profile.get("client_id")

    if session_client_id != profile_client_id:
        raise ValueError(
            "client_id mismatch: "
            f"session={session_client_id!r}, "
            f"profile={profile_client_id!r}"
        )

    generation = session.get("generation", {})

    candidate_count = generation.get("candidate_count")
    if type(candidate_count) is not int or candidate_count < 1:
        raise ValueError(
            "generation.candidate_count must be a positive integer"
        )

    collection = (
        session.get("creative_direction", {})
        .get("collection")
    )

    if not isinstance(collection, str) or not collection.strip():
        raise ValueError(
            "creative_direction.collection is required"
        )

    return {
        "session": session,
        "session_path": session_path,
        "profile_path": profile_path,
        "count": candidate_count,
        "collection": collection,
    }


def choose_block(name: str, spec: dict, rng: random.Random) -> str:
    mode = spec.get("mode", "fixed")
    if mode == "fixed":
        return spec["fixed"]
    if mode == "random":
        choices = spec.get("choices", [])
        if not choices:
            raise ValueError(f"Parameter '{name}' has random mode but no choices")
        return rng.choice(choices)
    raise ValueError(f"Parameter '{name}' has unsupported mode: {mode}")


def cycled_values(values: list, count: int, rng: random.Random) -> list:
    if not values:
        return []
    result = []
    while len(result) < count:
        cycle = copy.deepcopy(values)
        rng.shuffle(cycle)
        # A fresh cycle may start with the same value that ended the previous
        # one.  The pool has already been exhausted at that point, but an
        # immediate duplicate still looks like poor diversity in a series.
        if result and len(cycle) > 1 and cycle[0] == result[-1]:
            swap_index = next(
                (index for index, value in enumerate(cycle[1:], start=1)
                 if value != result[-1]),
                None,
            )
            if swap_index is not None:
                cycle[0], cycle[swap_index] = cycle[swap_index], cycle[0]
        result.extend(cycle)
    return result[:count]


def field_value(profile: dict, name: str, default=None):
    value = profile.get(name, default)
    if isinstance(value, dict):
        return value.get("value", default)
    return value


def normalize_gender(value) -> str:
    normalized = GENDER_ALIASES.get(str(value).strip().lower())
    if not normalized:
        raise ValueError(f"Unsupported gender in client profile: {value!r}")
    return normalized


def legacy_profile_character(profile: dict) -> dict:
    character = {}

    for name in (
        "gender",
        "age_range",
        "body_type",
        "hair",
        "facial_hair",
        "eye_color",
        "glasses",
        "face_shape",
        "ethnicity",
    ):
        value = field_value(profile, name)
        if value is not None:
            character[name] = value

    character.update(profile.get("manual_overrides", {}))
    return character


def profile_v2_character(profile: dict) -> dict:
    build = field_value(profile.get("body", {}), "build")
    if build == "average":
        build = "average build"

    character = {
        "gender": field_value(profile.get("identity", {}), "gender"),
        "age_range": field_value(profile.get("identity", {}), "exact_age"),
        "body_type": build,
        "face_shape": field_value(profile.get("face", {}), "shape"),
        "hair": (
            profile.get("hair", {})
            .get("scalp_hair", {})
            .get("type")
        ),
        "facial_hair": (
            profile.get("face", {})
            .get("facial_hair", {})
            .get("type")
        ),
        "eye_color": field_value(profile.get("eyes", {}), "color"),
        "glasses": field_value(
            profile.get("accessories", {}),
            "glasses",
            False,
        ),
    }

    facial_hair_aliases = {
        "clean_shaven": "clean-shaven",
        "no_facial_hair": "no facial hair",
    }
    character["facial_hair"] = facial_hair_aliases.get(
        character["facial_hair"],
        character["facial_hair"],
    )

    eye_color = character.get("eye_color")
    if eye_color and not str(eye_color).lower().endswith("eyes"):
        character["eye_color"] = f"{eye_color} eyes"

    return {
        key: value
        for key, value in character.items()
        if value is not None
    }


def load_client_character(
    profile_path: Path,
    overrides_path: Path | None,
) -> dict:
    profile = read_json(profile_path)

    if (
        profile.get("schema") == "onyx.client_profile"
        and profile.get("schema_version") == "2.0"
    ):
        merged = profile_v2_character(profile)
    else:
        merged = legacy_profile_character(profile)

    if overrides_path:
        merged.update(read_json(overrides_path))

    if "gender" not in merged:
        raise ValueError("Client profile must contain gender")

    merged["gender"] = normalize_gender(merged["gender"])
    merged.setdefault("age_range", "adult")
    merged.setdefault("body_type", "average build")
    merged.setdefault("hair", "natural hair")
    merged.setdefault(
        "facial_hair",
        "clean-shaven"
        if merged["gender"] == "male"
        else "no facial hair",
    )
    merged.setdefault("eye_color", "natural eye color")
    merged.setdefault("glasses", False)
    merged["source"] = "client_profile"
    merged["profile_file"] = str(profile_path)
    merged["overrides_file"] = (
        str(overrides_path)
        if overrides_path
        else None
    )

    return merged


def portfolio_characters(config: dict, count: int, rng: random.Random) -> list[dict]:
    presets = config.get("portfolio_characters", [])
    if not presets:
        raise ValueError("Config has no portfolio_characters")
    characters = cycled_values(presets, count, rng)
    for character in characters:
        character["gender"] = normalize_gender(character["gender"])
        character["source"] = "portfolio_preset"
    return characters


def clothing_values(config: dict, characters: list[dict], rng: random.Random) -> list[str]:
    pools = config.get("clothing_by_gender", {})
    spec = config.get("parameters", {}).get("clothing", {"mode": "random"})
    mode = spec.get("mode", "random")
    used: dict[str, list[str]] = {}
    last_by_gender: dict[str, str] = {}
    result = []
    for character in characters:
        gender = character["gender"]
        if mode == "fixed":
            fixed_by_gender = spec.get("fixed_by_gender", {})
            value = fixed_by_gender.get(gender) or fixed_by_gender.get("unisex")
            if not value:
                raise ValueError(
                    f"Parameter 'clothing' has fixed mode but no fixed value "
                    f"for gender '{gender}'"
                )
            result.append(value)
            continue
        if mode != "random":
            raise ValueError(f"Parameter 'clothing' has unsupported mode: {mode}")
        choices = pools.get(gender) or pools.get("unisex")
        if not choices:
            raise ValueError(f"No clothing choices configured for gender '{gender}'")
        if not used.get(gender):
            used[gender] = list(choices)
            rng.shuffle(used[gender])
            previous = last_by_gender.get(gender)
            if previous is not None and len(used[gender]) > 1 and used[gender][-1] == previous:
                swap_index = next(
                    (index for index, value in enumerate(used[gender][:-1])
                     if value != previous),
                    None,
                )
                if swap_index is not None:
                    used[gender][-1], used[gender][swap_index] = (
                        used[gender][swap_index],
                        used[gender][-1],
                    )
        value = used[gender].pop()
        result.append(value)
        last_by_gender[gender] = value
    return result


def build_selection_plan(config: dict, count: int, rng: random.Random, characters: list[dict]) -> list[dict]:
    """Build a series while avoiding repeats until each random pool is exhausted."""
    plan = [{} for _ in range(count)]
    scene_presets = config.get("scene_presets", [])
    if scene_presets:
        scene_spec = config.get("parameters", {}).get(
            "scene_preset", {"mode": "random"}
        )
        scene_mode = scene_spec.get("mode", "random")
        if scene_mode == "fixed":
            fixed_id = scene_spec.get("fixed")
            fixed_preset = next(
                (preset for preset in scene_presets if preset.get("id") == fixed_id),
                None,
            )
            if fixed_preset is None:
                raise ValueError(
                    f"Parameter 'scene_preset' refers to unknown preset: {fixed_id!r}"
                )
            preset_values = [fixed_preset] * count
        elif scene_mode == "random":
            preset_values = cycled_values(scene_presets, count, rng)
        else:
            raise ValueError(
                f"Parameter 'scene_preset' has unsupported mode: {scene_mode}"
            )
        for index, preset in enumerate(preset_values[:count]):
            plan[index]["scene_preset_id"] = preset["id"]
            for key in ("scene_blueprint", "environment", "lighting", "camera"):
                plan[index][key] = preset[key]

    for name, spec in config["parameters"].items():
        if scene_presets and name in {"scene_blueprint", "environment", "lighting", "camera"}:
            continue
        if name in {"hairstyle", "clothing", "scene_preset"}:
            continue
        mode = spec.get("mode", "fixed")
        if mode == "fixed":
            values = [spec["fixed"]] * count
        elif mode == "random":
            choices = spec.get("choices", [])
            if not choices:
                raise ValueError(f"Parameter '{name}' has random mode but no choices")
            values = cycled_values(choices, count, rng)
        else:
            raise ValueError(f"Parameter '{name}' has unsupported mode: {mode}")
        for index, value in enumerate(values):
            plan[index][name] = value
    clothes = clothing_values(config, characters, rng)
    for index in range(count):
        plan[index]["character"] = characters[index]
        plan[index]["clothing"] = clothes[index]
    return plan


def character_description(character: dict) -> str:
    subject = "man" if character["gender"] == "male" else "woman"
    age = str(character.get("age_range", "adult")).strip()
    if age.isdigit():
        age = f"{age}-year-old"
    elif age.replace("–", "-").replace("-", "").isdigit():
        age = f"{age} years old"
    identity = " ".join(part for part in (age, str(character.get("ethnicity", "")).strip(), subject) if part)
    parts = [identity]
    for key in ("body_type", "face_shape", "hair"):
        value = character.get(key)
        if value and str(value).lower() not in {"none", "not detected", "unknown"}:
            parts.append(str(value))
    facial_hair = str(character.get("facial_hair", "")).strip()
    if facial_hair.lower().replace("_", "-") in {"clean-shaven", "clean shaven", "no facial hair"}:
        parts.append(
            "a freshly razor-shaved face with smooth bare cheeks, "
            "a smooth upper lip and a smooth bare jawline"
        )
    elif facial_hair.lower() not in {"", "none", "not detected", "unknown"}:
        parts.append(facial_hair)
    eye_color = character.get("eye_color")
    if eye_color and str(eye_color).lower() not in {"none", "not detected", "unknown"}:
        parts.append(str(eye_color))
    glasses = character.get("glasses")
    parts.append("wearing glasses" if glasses is True else "without glasses")
    return ", ".join(part for part in parts if part)


def is_clean_shaven(character: dict) -> bool:
    facial_hair = str(character.get("facial_hair", "")).strip().lower()
    normalized = facial_hair.replace("_", "-")
    return normalized in {"clean-shaven", "clean shaven", "no facial hair"}


def age_identity_requirement(character: dict) -> str:
    """Turn exact client age into a high-priority positive identity anchor."""
    raw_age = str(character.get("age_range", "")).strip()
    if not raw_age.isdigit():
        return ""
    age = int(raw_age)
    decade = (age // 10) * 10
    possessive = "his" if character["gender"] == "male" else "her"
    return (
        f"Age-critical identity requirement: the subject is exactly {age} years old, "
        f"clearly an adult in {possessive} {decade}s, with age-appropriate youthful "
        "adult facial proportions, firm natural skin and only subtle natural expression lines.\n\n"
    )


def build_prompt(config: dict, selected: dict) -> str:
    character = selected["character"]
    pronoun = "He" if character["gender"] == "male" else "She"
    identity_requirement = ""
    if character["gender"] == "male" and is_clean_shaven(character):
        identity_requirement = (
            "Identity-critical grooming requirement: the face is freshly razor-shaved, "
            "with smooth bare cheeks, a smooth upper lip and a smooth bare jawline.\n\n"
        )
    age_requirement = age_identity_requirement(character)
    prompt = (
        f"A natural, highly realistic editorial business photograph of a single {character_description(character)}.\n\n"
        f"{age_requirement}"
        f"{identity_requirement}"
        f"{pronoun} is wearing {selected['clothing']}.\n\n"
        f"{pronoun} is {selected['scene_blueprint']}. The posture is confident but unposed, "
        f"as if photographed during a real working day. The subject has {selected['expression']}.\n\n"
        f"{selected.get('environment', config.get('environment', 'The setting is functional, inhabited and realistic rather than staged like a showroom.'))}\n\n"
        f"Lighting: {selected['lighting']}. Neutral color grading with charcoal, navy and warm brown tones.\n\n"
        f"Photographed on {selected['camera']}. Natural depth of field, realistic optical rendering, "
        "fine fabric texture, visible skin pores, subtle under-eye detail, natural body proportions "
        "and anatomically correct hands. Authentic corporate editorial photography, restrained "
        "retouching, slight photographic grain, subtle lens softness, realistic exposure, "
        "no artificial glamour, no glossy advertising look."
    )
    return prompt


def generation_seed(generation: dict, rng: random.Random) -> int:
    mode = generation.get("seed_mode", "random")
    if mode == "fixed":
        return int(generation["fixed_seed"])
    if mode == "random":
        return rng.randrange(0, 2**63)
    raise ValueError(f"Unsupported seed_mode: {mode}")


def prepare_workflow(
    base: dict, config: dict, prompt: str, seed: int, run_id: str, scene_id: str
) -> dict:
    workflow = copy.deepcopy(base)
    generation = config["generation"]
    workflow[PROMPT_NODE]["inputs"]["text"] = prompt
    sampler = workflow[SAMPLER_NODE]["inputs"]
    for key in ("steps", "cfg", "sampler_name", "scheduler", "denoise"):
        sampler[key] = generation[key]
    sampler["seed"] = seed
    latent = workflow[LATENT_NODE]["inputs"]
    for key in ("width", "height", "batch_size"):
        latent[key] = generation[key]
    workflow[SAVE_NODE]["inputs"]["filename_prefix"] = f"ONYX/{run_id}/{scene_id}"
    return workflow


def api_json(url: str, payload: dict | None = None, attempts: int = 8) -> dict:
    """Call ComfyUI and tolerate temporary Windows socket exhaustion."""
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    retry_delays = (2, 4, 8, 15, 15, 15, 15)

    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(url, data=data)
        request.add_header("Connection", "close")
        if data is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as error:
            if attempt == attempts:
                raise RuntimeError(
                    f"ComfyUI API is unavailable after {attempts} attempts: {url}"
                ) from error
            delay = retry_delays[min(attempt - 1, len(retry_delays) - 1)]
            print(
                f"ComfyUI connection error ({error}). "
                f"Retry {attempt}/{attempts - 1} in {delay} s..."
            )
            time.sleep(delay)

    raise RuntimeError("Unreachable retry state")


def run_workflow(
    server: str, workflow: dict, client_id: str, wait_timeout: int = 1800
) -> tuple[str, dict]:
    queued = api_json(f"{server}/prompt", {"prompt": workflow, "client_id": client_id})
    prompt_id = queued["prompt_id"]
    deadline = time.monotonic() + wait_timeout
    while True:
        history = api_json(f"{server}/history/{prompt_id}")
        if prompt_id in history:
            return prompt_id, history[prompt_id]
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"ComfyUI did not finish prompt {prompt_id} within {wait_timeout} seconds"
            )
        time.sleep(2)


def download_outputs(
    server: str, history: dict, output_dir: Path, scene_id: str
) -> list[str]:
    saved = []
    image_number = 0
    for node_output in history.get("outputs", {}).values():
        for image in node_output.get("images", []):
            image_number += 1
            query = urllib.parse.urlencode({
                "filename": image["filename"],
                "subfolder": image.get("subfolder", ""),
                "type": image.get("type", "output"),
            })
            source_suffix = Path(image["filename"]).suffix or ".png"
            local_name = (
                f"{scene_id}{source_suffix}"
                if image_number == 1
                else f"{scene_id}_{image_number:02d}{source_suffix}"
            )
            destination = output_dir / local_name
            request = urllib.request.Request(f"{server}/view?{query}")
            request.add_header("Connection", "close")
            with urllib.request.urlopen(request, timeout=120) as response:
                destination.write_bytes(response.read())
            saved.append(destination.name)
    return saved


def create_run_directory(output_root: Path) -> tuple[str, Path]:
    """Create a unique folder so results from separate launches never mix."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_id = f"run_{timestamp}"
    run_dir = output_root / run_id
    suffix = 2
    while run_dir.exists():
        run_id = f"run_{timestamp}_{suffix:02d}"
        run_dir = output_root / run_id
        suffix += 1
    run_dir.mkdir(parents=True)
    return run_id, run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="ONYX Flux scene generator 0.7.1")
    parser.add_argument("--workflow", type=Path, default=Path("ONYX_Flux_Scene_Generator_0.3_API.json"))
    parser.add_argument("--config", type=Path, default=Path("scene_config.json"))
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--count", type=int)
    parser.add_argument("--mode", choices=("portfolio", "client"), default="portfolio")
    parser.add_argument("--collection", default="executive")
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--overrides", type=Path)
    parser.add_argument(
        "--session",
        type=Path,
        help="Path to ONYX Session Spec 1.0",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    session_context = None

    if args.session:
        if args.profile:
            parser.error(
                "--profile cannot be combined with --session; "
                "the profile is defined inside the session"
            )

        if args.overrides:
            parser.error(
                "--overrides cannot be combined with --session"
            )

        session_context = load_session_spec(args.session)
        args.mode = "client"
        args.profile = session_context["profile_path"]

        if args.count is None:
            args.count = session_context["count"]

        args.collection = session_context["collection"]

    base_workflow = read_json(args.workflow)
    config = read_json(args.config)

    if args.collection != config.get("collection_id", "executive"):
        raise ValueError(
            f"Config contains collection "
            f"'{config.get('collection_id', 'executive')}', "
            f"not '{args.collection}'"
        )

    count = args.count or int(config.get("count", 1))

    args.output.mkdir(parents=True, exist_ok=True)

    if args.mode == "client":
        # В Job Engine output уже является каталогом конкретной стадии.
        # Дополнительный run_<timestamp> здесь не создаём.
        run_id = args.output.parent.name
        run_dir = args.output
    else:
        run_id, run_dir = create_run_directory(args.output)

    rng = random.SystemRandom()
    client_id = str(uuid.uuid4())
    if args.mode == "client":
        if not args.profile:
            parser.error("--profile is required in client mode")
        character = load_client_character(args.profile, args.overrides)
        characters = [copy.deepcopy(character) for _ in range(count)]
    else:
        if args.profile or args.overrides:
            parser.error("--profile/--overrides can only be used in client mode")
        characters = portfolio_characters(config, count, rng)
    selection_plan = build_selection_plan(config, count, rng, characters)

    for index in range(1, count + 1):
        scene_id = f"scene_{index:03d}"
        selected = selection_plan[index - 1]
        prompt = build_prompt(config, selected)
        seed = generation_seed(config["generation"], rng)
        workflow = prepare_workflow(base_workflow, config, prompt, seed, run_id, scene_id)
        metadata = {
            "run_id": run_id,
            "scene_id": scene_id,
            "collection": config["collection"],
            "collection_id": config.get("collection_id", "executive"),
            "mode": args.mode,
            "session": (
                {
                    "session_id": session_context["session"].get("session_id"),
                    "session_file": str(session_context["session_path"]),
                    "status": session_context["session"].get("status"),
                }
                if session_context
                else None
            ),
            "character": selected["character"],
            "character_prompt": character_description(selected["character"]),
            "parameter_sources": {
                "character": selected["character"]["source"],
                "clothing": (
                    "collection_"
                    + config.get("parameters", {})
                    .get("clothing", {})
                    .get("mode", "random")
                ),
                "scene": (
                    "collection_scene_library_"
                    + config.get("parameters", {})
                    .get("scene_preset", {})
                    .get("mode", "random")
                ),
                "expression": (
                    "collection_"
                    + config.get("parameters", {})
                    .get("expression", {})
                    .get("mode", "fixed")
                ),
            },
            "generation_seed": seed,
            "selected_parameters": selected,
            "prompt": prompt,
            "generation": config["generation"],
            "workflow_file": str(args.workflow),
            "local_output_directory": str(run_dir),
            "output_images": [],
        }
        if not args.dry_run:
            prompt_id, history = run_workflow(config["server"].rstrip("/"), workflow, client_id)
            metadata["prompt_id"] = prompt_id
            metadata["output_images"] = download_outputs(
                config["server"].rstrip("/"), history, run_dir, scene_id
            )
        with (run_dir / f"{scene_id}.json").open("w", encoding="utf-8") as stream:
            json.dump(metadata, stream, ensure_ascii=False, indent=2)
        print(f"{scene_id}: seed={seed}, mode={'dry-run' if args.dry_run else 'generated'}")
    print(f"Results: {run_dir.resolve()}")


if __name__ == "__main__":
    main()
