"""Run ONYX upscale, then build all client-delivery tiers."""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("package", type=Path)
    p.add_argument("--workflow", type=Path, required=True)
    p.add_argument("--comfy-input", type=Path, required=True)
    p.add_argument("--comfy-output", type=Path, required=True)
    p.add_argument("--font", type=Path, required=True)
    p.add_argument("--order-id", default="<ID>")
    p.add_argument("--server", default="http://127.0.0.1:8188")
    args = p.parse_args()
    package = args.package
    name = package.parent.name.lower().replace("_v1", "")
    source = package / "final_source_resolution"
    input_dir = package / f"upscale_{name}_v1_input"
    output_dir = package / f"upscale_{name}_v1"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in source.glob("*.jpg"):
        target = input_dir / item.name
        if not target.exists(): target.write_bytes(item.read_bytes())
    generator = Path(__file__).parents[1] / "scene_generator" / "generator.py"
    subprocess.run([sys.executable, str(generator), "--server", args.server, "--comfy-output", str(args.comfy_output), "--timeout", "1800", "postprocess", "--workflow", str(args.workflow), "--input-dir", str(input_dir), "--output-dir", str(output_dir), "--comfy-input", str(args.comfy_input)], check=True)
    delivery = Path(__file__).with_name("onyx_delivery.py")
    subprocess.run([sys.executable, str(delivery), str(package), "--font", str(args.font), "--order-id", args.order_id], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
