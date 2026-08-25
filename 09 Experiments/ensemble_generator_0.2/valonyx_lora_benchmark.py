import copy
import json
import time
import urllib.request
from pathlib import Path


COMFY_URL = "http://127.0.0.1:8188"

WORKFLOW = Path(
    r"D:\AI\ONYX\09 Experiments\ensemble_generator_0.2"
    r"\workflows\valonyx_lora_benchmark_api.json"
)

CHECKPOINTS = [
    ("step750",  r"ONYX\valonyx_v1_step750.safetensors"),
    ("step1000", r"ONYX\valonyx_v1_step1000.safetensors"),
    ("step1250", r"ONYX\valonyx_v1_step1250.safetensors"),
    ("step1500", r"ONYX\valonyx_v1_step1500.safetensors"),
]

PROMPT = """
A photorealistic corporate editorial portrait of valonyx woman,
preserving her recognizable identity, natural facial proportions and real age.

She is standing beside a dark wooden executive desk in a sophisticated
modern office. Her body is turned slightly away from the camera while
her face is directed toward the camera.

She is wearing a well-fitted dark navy business suit and a white blouse.

Framed from mid-thigh upward, eye-level camera, balanced asymmetrical
composition.

Soft natural daylight from a large side window, authentic skin texture,
subtle expression lines, natural body proportions, 85mm full-frame lens
at f/2.8, natural depth of field, restrained retouching,
authentic corporate editorial photography.
""".strip()

SEED = 202608170001


def load_workflow():
    with WORKFLOW.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def queue_prompt(workflow):
    data = json.dumps({"prompt": workflow}).encode("utf-8")

    request = urllib.request.Request(
        f"{COMFY_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())


def wait_for_prompt(prompt_id):
    while True:
        with urllib.request.urlopen(
            f"{COMFY_URL}/history/{prompt_id}"
        ) as response:
            history = json.loads(response.read())

        if prompt_id in history:
            return history[prompt_id]

        time.sleep(2)


def main():

    base = load_workflow()

    print("=" * 72)
    print("ONYX LoRA Checkpoint Benchmark - Valentina")
    print("=" * 72)
    print("Seed      :", SEED)
    print("Checkpoints:", len(CHECKPOINTS))
    print()

    required = ["76:59", "76:74", "76:75", "76:72"]

    for node in required:
        if node not in base:
            raise RuntimeError(f"Required node missing: {node}")

    for label, checkpoint in CHECKPOINTS:

        workflow = copy.deepcopy(base)

        # ------------------------------------------------------------
        # Valentina LoRA
        # ------------------------------------------------------------

        workflow["76:59"]["inputs"]["lora_name"] = checkpoint
        workflow["76:59"]["inputs"]["strength_model"] = 1.0

        # ------------------------------------------------------------
        # Identical prompt
        # ------------------------------------------------------------

        workflow["76:74"]["inputs"]["text"] = PROMPT

        # ------------------------------------------------------------
        # Identical seed
        # ------------------------------------------------------------

        workflow["76:75"]["inputs"]["seed"] = SEED

        # ------------------------------------------------------------
        # Add dedicated output node.
        #
        # VAEDecode 76:72 produces IMAGE output #0.
        # ------------------------------------------------------------

        workflow["benchmark_save"] = {
            "inputs": {
                "filename_prefix":
                    f"ONYX_LoRA_Benchmark/Valentina/{label}/valonyx_{label}",
                "images": ["76:72", 0],
            },
            "class_type": "SaveImage",
            "_meta": {
                "title": "Benchmark Save"
            },
        }

        print("-" * 72)
        print("Variant   :", label)
        print("Checkpoint:", checkpoint)
        print("Seed      :", SEED)

        started = time.time()

        response = queue_prompt(workflow)

        if "prompt_id" not in response:
            raise RuntimeError(
                "ComfyUI rejected workflow:\n"
                + json.dumps(response, indent=2)
            )

        prompt_id = response["prompt_id"]

        print("Prompt ID :", prompt_id)

        wait_for_prompt(prompt_id)

        elapsed = time.time() - started

        print(f"Completed : {elapsed:.1f} sec")

    print()
    print("=" * 72)
    print("BENCHMARK COMPLETED")
    print("=" * 72)
    print(
        r"Results: D:\AI\ComfyUI_Flux\ComfyUI\output"
        r"\ONYX_LoRA_Benchmark\Valentina"
    )


if __name__ == "__main__":
    main()