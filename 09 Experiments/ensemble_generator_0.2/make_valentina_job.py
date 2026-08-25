import json
from pathlib import Path

src = Path("job.20scenes.release.json")
dst = Path("job.20scenes.valentina.json")

with src.open("r", encoding="utf-8-sig") as f:
    d = json.load(f)

# ------------------------------------------------------------
# JOB
# ------------------------------------------------------------

d["job_id"] = "2026-08-17_valentina_full_pipeline_20"
d["base_seed"] = 202608170201
d["trigger_word"] = "valonyx"

# ------------------------------------------------------------
# IDENTITY
# ------------------------------------------------------------

d["identity"]["appearance"] = (
    "an adult Eastern European woman with a slim build, "
    "long natural brown hair, light eyes, natural facial proportions, "
    "subtle expression lines, slight natural facial asymmetry and "
    "authentic skin texture"
)

d["identity"]["dreamo_reference"] = "valentina_face.png"

d["identity"]["facefusion"]["source_dir"] = (
    r"D:\AI\Clients\Valentina\references"
)

# ------------------------------------------------------------
# SCENES
# Preserve scene/location/pose/camera structure,
# replace Alexander-specific subject constraints.
# ------------------------------------------------------------

for scene in d["scenes"]:

    scene["subject"] = (
        "one adult woman with long natural brown hair, "
        "realistic feminine facial features and natural proportions"
    )

    neg = scene.get("negative_prompt", "")

    # Remove Alexander-specific bald/hair prohibitions.
    banned = [
        "hair",
        "hairstyle",
        "haircut",
        "fringe",
        "bangs",
        "side hair",
        "temple hair",
        "long hair",
        "short hair",
        "receding hairline",
    ]

    parts = [x.strip() for x in neg.split(",") if x.strip()]
    parts = [x for x in parts if x.lower() not in banned]

    scene["negative_prompt"] = ", ".join(parts)

# ------------------------------------------------------------
# JUGGERNAUT
# ------------------------------------------------------------

jug = d.setdefault("renderer_settings", {}).setdefault(
    "juggernautxl", {}
)

jug["identity_prefix"] = (
    "adult woman, long natural brown hair, "
    "realistic feminine facial features, natural proportions"
)

jug["negative_prompt_suffix"] = (
    "deformed face, distorted anatomy, extra fingers, extra limbs, "
    "cgi, plastic skin, excessive beauty retouching"
)

# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

with dst.open("w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("Created:", dst.resolve())
print("Scenes:", len(d["scenes"]))
print("Trigger:", d["trigger_word"])
print("DreamO reference:", d["identity"]["dreamo_reference"])
print("FaceFusion:", d["identity"]["facefusion"]["source_dir"])
