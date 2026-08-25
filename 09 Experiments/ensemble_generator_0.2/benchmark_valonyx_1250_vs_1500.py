import copy
import json
import time
import urllib.request
from pathlib import Path


COMFY_URL = "http://127.0.0.1:8188"

WORKFLOW_PATH = Path(
    r"D:\AI\ONYX\09 Experiments\ensemble_generator_0.2"
    r"\workflows\valonyx_lora_benchmark_api.json"
)

CHECKPOINTS = {
    "step1250": "valonyx_v1_step1250.safetensors",
    "step1500": "valonyx_v1_step1500.safetensors",
}

SCENES = [
    {
        "name": "closeup",
        "seed": 202608170101,
        "width": 768,
        "height": 1024,
        "prompt": (
            "A photorealistic close-up portrait photograph of valonyx woman, "
            "preserving her recognizable identity, natural facial proportions "
            "and real age, looking directly at the camera, calm natural expression, "
            "head and shoulders composition, soft natural window light, "
            "simple neutral indoor background, authentic skin texture, "
            "natural facial asymmetry, realistic hair texture, "
            "85mm lens, shallow depth of field, restrained photographic retouching."
        ),
    },

    {
        "name": "business",
        "seed": 202608170102,
        "width": 896,
        "height": 1152,
        "prompt": (
            "A photorealistic medium three-quarter corporate editorial portrait "
            "of valonyx woman, preserving her recognizable identity, natural facial "
            "proportions and real age. She is standing in a sophisticated modern "
            "executive office, body slightly angled toward the camera, looking at "
            "the camera with a calm confident natural expression. She is wearing "
            "a well-fitted dark navy business suit and a crisp white shirt. "
            "Both hands visible in a relaxed natural position. Soft daylight from "
            "a large side window, authentic skin texture, realistic body proportions, "
            "anatomically correct hands, 85mm lens, f/2.8, restrained retouching, "
            "authentic corporate editorial photography."
        ),
    },

    {
        "name": "outdoor",
        "seed": 202608170103,
        "width": 896,
        "height": 1152,
        "prompt": (
            "A photorealistic outdoor editorial portrait photograph of valonyx woman, "
            "preserving her recognizable identity, natural facial proportions and "
            "real age. She is standing on a modern European city street wearing "
            "elegant casual clothing, relaxed natural posture, looking toward the "
            "camera with a subtle natural expression. Both hands visible. "
            "Soft overcast daylight, realistic hair and authentic skin texture, "
            "natural body proportions, detailed urban environment, "
            "85mm photographic look, restrained professional retouching."
        ),
    },
]


def find_save_nodes(workflow):
    return [
        (node_id, node)
        for node_id, node in workflow.items()
        if node.get("class_type") == "SaveImage"
    ]


def queue_prompt(workflow):
    payload = json.dumps({"prompt": workflow}).encode("utf-8")

    request = urllib.request.Request(
        f"{COMFY_URL}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


with WORKFLOW_PATH.open("r", encoding="utf-8-sig") as f:
    base_workflow = json.load(f)


print("=" * 78)
print("ONYX — VALONYX CHECKPOINT BENCHMARK")
print("1250 vs 1500")
print("SaveImage will be added dynamically")
print("=" * 78)
print()


for scene in SCENES:

    print("=" * 78)
    print(
        f"SCENE: {scene['name']} | "
        f"seed={scene['seed']} | "
        f"{scene['width']}x{scene['height']}"
    )
    print("=" * 78)

    for checkpoint_label, checkpoint_file in CHECKPOINTS.items():

        workflow = copy.deepcopy(base_workflow)

        # ---------------------------------------------------------
        # LoRA
        # ---------------------------------------------------------

        workflow["76:59"]["inputs"]["lora_name"] = checkpoint_file
        workflow["76:59"]["inputs"]["strength_model"] = 1.0

        # ---------------------------------------------------------
        # Prompt
        # ---------------------------------------------------------

        workflow["76:74"]["inputs"]["text"] = scene["prompt"]

        # ---------------------------------------------------------
        # Seed
        # ---------------------------------------------------------

        workflow["76:75"]["inputs"]["seed"] = scene["seed"]

        # ---------------------------------------------------------
        # Resolution
        # ---------------------------------------------------------

        workflow["76:71"]["inputs"]["width"] = scene["width"]
        workflow["76:71"]["inputs"]["height"] = scene["height"]

                # ---------------------------------------------------------
        # Add SaveImage dynamically.
        #
        # 76:72 = VAEDecode
        # output 0 = final IMAGE
        # ---------------------------------------------------------

        filename_prefix = (
            f"ONYX_Valonyx_Checkpoint_Benchmark/"
            f"{scene['name']}_{checkpoint_label}"
        )

        workflow["benchmark_save"] = {
            "inputs": {
                "filename_prefix": filename_prefix,
                "images": ["76:72", 0],
            },
            "class_type": "SaveImage",
            "_meta": {
                "title": "Benchmark Save"
            },
        }

        print(
            f"{scene['name']:10} "
            f"{checkpoint_label:8} "
            f"LoRA={checkpoint_file}"
        )

        result = queue_prompt(workflow)

        print(
            f"  queued: {result.get('prompt_id')}"
        )

        time.sleep(0.5)


print()
print("=" * 78)
print("6 GENERATIONS QUEUED")
print("=" * 78)

print(
    r"Results: D:\AI\ComfyUI_Flux\ComfyUI\output"
    r"\ONYX_Valonyx_Checkpoint_Benchmark"
)