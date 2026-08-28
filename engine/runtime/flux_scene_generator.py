from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.parse
import uuid
from pathlib import Path
from typing import Any

from .comfyui_client import (
    ComfyUIClient,
    ComfyUIClientError,
    ComfyUIExecutionFailed,
    ComfyUIHTTPError,
    ComfyUIImageOutput,
    ComfyUIMalformedResponse,
    ComfyUITimeout,
    ComfyUIUnavailable,
    WorkflowRejected,
)
from .providers import ProviderArtifact, ProviderExecutionResult, SceneGeneratorRequest


NODE_SPEC = {
    "56:51": ("CLIPTextEncode", ("text",)),
    "56:58": (
        "KSampler",
        ("seed", "steps", "cfg", "sampler_name", "scheduler", "denoise"),
    ),
    "56:50": ("EmptySD3LatentImage", ("width", "height", "batch_size")),
    "9": ("SaveImage", ("filename_prefix", "images")),
    "56:48": ("UNETLoader", ("unet_name",)),
}
PROMPT_NODE = "56:51"
SAMPLER_NODE = "56:58"
LATENT_NODE = "56:50"
SAVE_NODE = "9"
MODEL_NODE = "56:48"
SAFE_RESULT_ID = re.compile(r"^[A-Za-z0-9_-]+$")
IMAGE_SUFFIXES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


class FluxInputError(ValueError):
    pass


class FluxWorkflowError(ValueError):
    pass


class FluxOutputSafetyError(ValueError):
    pass


def _number(value: object, name: str, minimum: float, maximum: float) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FluxInputError(f"{name} must be numeric")
    if not minimum <= value <= maximum:
        raise FluxInputError(f"{name} must be between {minimum:g} and {maximum:g}")
    return value


def _positive_int(value: object, name: str, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise FluxInputError(f"{name} must be an integer between 1 and {maximum}")
    return value


def _prompt(scene_inputs: dict[str, object]) -> str:
    explicit = scene_inputs.get("explicit_prompts")
    value: object | None = None
    if isinstance(explicit, dict):
        value = explicit.get("scene.flux")
    if value is None:
        prompt = scene_inputs.get("prompt")
        if isinstance(prompt, dict):
            value = prompt.get("text")
    if not isinstance(value, str) or not value.strip():
        raise FluxInputError(
            'FLUX requires explicit_prompts["scene.flux"] or prompt["text"]'
        )
    return value.strip()


def _validated_parameters(parameters: dict[str, object]) -> dict[str, object]:
    allowed = {"width", "height", "steps", "cfg", "sampler_name", "scheduler", "denoise"}
    unknown = set(parameters) - allowed
    if unknown:
        raise FluxInputError(f"Unsupported FLUX parameters: {sorted(unknown)}")
    result: dict[str, object] = {}
    for name in ("width", "height"):
        if name in parameters:
            value = _positive_int(parameters[name], name, 4096)
            if value < 64 or value % 8:
                raise FluxInputError(f"{name} must be at least 64 and divisible by 8")
            result[name] = value
    if "steps" in parameters:
        result["steps"] = _positive_int(parameters["steps"], "steps", 200)
    if "cfg" in parameters:
        result["cfg"] = _number(parameters["cfg"], "cfg", 0, 100)
    if "denoise" in parameters:
        result["denoise"] = _number(parameters["denoise"], "denoise", 0, 1)
    for name in ("sampler_name", "scheduler"):
        if name in parameters:
            value = parameters[name]
            if not isinstance(value, str) or not value.strip():
                raise FluxInputError(f"{name} must be a non-empty string")
            result[name] = value
    return result


def _validate_workflow(workflow: dict[str, Any]) -> None:
    for node_id, (class_type, required_inputs) in NODE_SPEC.items():
        node = workflow.get(node_id)
        if not isinstance(node, dict):
            raise FluxWorkflowError(f"Workflow is missing node {node_id}")
        if node.get("class_type") != class_type:
            raise FluxWorkflowError(
                f"Workflow node {node_id} must be {class_type}, got {node.get('class_type')!r}"
            )
        inputs = node.get("inputs")
        if not isinstance(inputs, dict):
            raise FluxWorkflowError(f"Workflow node {node_id} has no inputs object")
        missing = [name for name in required_inputs if name not in inputs]
        if missing:
            raise FluxWorkflowError(f"Workflow node {node_id} is missing inputs {missing}")


def _normalized_subfolder(subfolder: str) -> str:
    if re.search(r"%(?:2f|5c)", subfolder, flags=re.IGNORECASE):
        raise FluxOutputSafetyError("ComfyUI subfolder is unsafe")
    decoded = urllib.parse.unquote(subfolder)
    normalized = decoded.replace("\\", "/")
    if normalized.startswith("/"):
        raise FluxOutputSafetyError("ComfyUI subfolder is unsafe")
    if normalized:
        parts = normalized.split("/")
        if any(part in {"", ".", ".."} for part in parts) or any(
            len(part) >= 2 and part[0].isalpha() and part[1] == ":" for part in parts
        ):
            raise FluxOutputSafetyError("ComfyUI subfolder is unsafe")
    return normalized


def _safe_descriptor(image: ComfyUIImageOutput) -> str:
    decoded_filename = urllib.parse.unquote(image.filename)
    if not decoded_filename or Path(decoded_filename).name != decoded_filename:
        raise FluxOutputSafetyError("ComfyUI filename must be a plain filename")
    if image.output_type != "output":
        raise FluxOutputSafetyError("ComfyUI image type must be 'output'")
    _normalized_subfolder(image.subfolder)
    suffix = Path(image.filename).suffix.lower()
    if suffix not in IMAGE_SUFFIXES:
        raise FluxOutputSafetyError(f"Unsupported ComfyUI image suffix: {suffix or '<none>'}")
    return suffix


def _atomic_write(path: Path, payload: bytes) -> None:
    temporary = path.with_name(path.name + ".writing")
    try:
        with temporary.open("wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


class FluxSceneGenerator:
    """Non-identity-aware FLUX adapter for one canonical ComfyUI candidate."""

    def __init__(self, *, opener=None, clock=None, sleeper=None) -> None:
        self.opener = opener
        self.clock = clock
        self.sleeper = sleeper

    @staticmethod
    def _failure(
        code: str,
        category: str,
        message: str,
        *,
        retryable: bool = False,
        metadata: dict[str, object] | None = None,
    ) -> ProviderExecutionResult:
        return ProviderExecutionResult.failure(
            code, category, message, retryable=retryable, metadata=metadata
        )

    def execute(self, request: SceneGeneratorRequest) -> ProviderExecutionResult:
        prompt_id: str | None = None
        actual_hash: str | None = None

        def failure_metadata(*, operation: str | None = None) -> dict[str, object]:
            metadata: dict[str, object] = {
                "endpoint": request.provider.endpoint,
                "submitted_seed": request.seed,
            }
            if actual_hash is not None:
                metadata["actual_workflow_sha256"] = actual_hash
            if prompt_id is not None:
                metadata["comfyui_prompt_id"] = prompt_id
            if operation is not None:
                metadata["operation"] = operation
            return metadata

        try:
            provider = request.provider
            if request.provider_id != "scene.flux" or provider.provider_id != request.provider_id:
                return self._failure(
                    "INVALID_PROVIDER_CONFIG", "configuration", "FLUX provider ID must be scene.flux"
                )
            if provider.identity_aware:
                return self._failure(
                    "INVALID_PROVIDER_CONFIG", "configuration", "Phase 1B.3 FLUX must be non-identity-aware"
                )
            if not provider.endpoint or not provider.workflow_path or not provider.model_path:
                return self._failure(
                    "INVALID_PROVIDER_CONFIG",
                    "configuration",
                    "FLUX requires endpoint, workflow_path and model_path",
                )

            workflow_path = Path(provider.workflow_path)
            if not workflow_path.is_file():
                return self._failure(
                    "WORKFLOW_NOT_FOUND", "configuration", f"Workflow not found: {workflow_path}"
                )
            model_path = Path(provider.model_path)
            if not model_path.is_file():
                return self._failure(
                    "INVALID_PROVIDER_CONFIG", "configuration", f"FLUX model not found: {model_path}"
                )

            try:
                raw_workflow = workflow_path.read_bytes()
            except OSError as exc:
                return self._failure("WORKFLOW_INVALID", "workflow", str(exc))
            actual_hash = hashlib.sha256(raw_workflow).hexdigest()
            if provider.workflow_hash and provider.workflow_hash.lower() != actual_hash:
                return self._failure(
                    "WORKFLOW_INVALID",
                    "workflow",
                    "Declared workflow hash does not match the resolved workflow file",
                    metadata={"actual_workflow_sha256": actual_hash},
                )
            try:
                workflow = json.loads(raw_workflow.decode("utf-8-sig"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise FluxWorkflowError("Workflow is not valid UTF-8 JSON") from exc
            if not isinstance(workflow, dict):
                raise FluxWorkflowError("Workflow root must be an object")
            _validate_workflow(workflow)

            try:
                scene_inputs = request.scene_inputs()
                raw_parameters = request.provider_parameters()
            except json.JSONDecodeError as exc:
                raise FluxInputError("Scene inputs and provider parameters must be valid JSON") from exc
            if not isinstance(scene_inputs, dict) or not isinstance(raw_parameters, dict):
                raise FluxInputError("Scene inputs and provider parameters must be JSON objects")
            parameters = _validated_parameters(raw_parameters)
            prompt = _prompt(scene_inputs)
            workflow[PROMPT_NODE]["inputs"]["text"] = prompt
            workflow[SAMPLER_NODE]["inputs"]["seed"] = request.seed
            for name in ("steps", "cfg", "sampler_name", "scheduler", "denoise"):
                if name in parameters:
                    workflow[SAMPLER_NODE]["inputs"][name] = parameters[name]
            for name in ("width", "height"):
                if name in parameters:
                    workflow[LATENT_NODE]["inputs"][name] = parameters[name]
            workflow[LATENT_NODE]["inputs"]["batch_size"] = 1
            workflow[MODEL_NODE]["inputs"]["unet_name"] = model_path.name
            workflow[SAVE_NODE]["inputs"]["filename_prefix"] = (
                f"ONYX_Canonical/{request.job_id}/{request.generation_result_id}"
            )

            runtime_metadata = json.loads(provider.runtime_metadata_json)
            if not isinstance(runtime_metadata, dict):
                return self._failure(
                    "INVALID_PROVIDER_CONFIG",
                    "configuration",
                    "Provider runtime metadata must be a JSON object",
                )
            request_timeout = _number(
                runtime_metadata.get("request_timeout_seconds", 30),
                "request_timeout_seconds",
                1,
                600,
            )
            generation_timeout = _number(
                runtime_metadata.get("generation_timeout_seconds", 1800),
                "generation_timeout_seconds",
                1,
                86400,
            )
            poll_interval = _number(
                runtime_metadata.get("poll_interval_seconds", 1),
                "poll_interval_seconds",
                0.01,
                60,
            )
            client_kwargs: dict[str, Any] = {
                "request_timeout_seconds": request_timeout,
                "poll_interval_seconds": poll_interval,
            }
            if self.opener is not None:
                client_kwargs["opener"] = self.opener
            if self.clock is not None:
                client_kwargs["clock"] = self.clock
            if self.sleeper is not None:
                client_kwargs["sleeper"] = self.sleeper
            client = ComfyUIClient(provider.endpoint, **client_kwargs)
            prompt_id = client.submit(workflow, uuid.uuid4().hex)
            history = client.wait_for_history(prompt_id, generation_timeout)
            try:
                image = client.one_image(history)
            except LookupError as exc:
                return self._failure(
                    "MISSING_OUTPUT",
                    "provider_output",
                    str(exc),
                    retryable=True,
                    metadata=failure_metadata(operation="history_output"),
                )
            except ValueError as exc:
                return self._failure(
                    "MISSING_OUTPUT",
                    "provider_output",
                    str(exc),
                    metadata=failure_metadata(operation="history_output"),
                )
            if image.node_id != SAVE_NODE:
                return self._failure(
                    "MISSING_OUTPUT",
                    "provider_output",
                    f"Expected image output from node {SAVE_NODE}, received node {image.node_id}",
                    metadata=failure_metadata(operation="history_output"),
                )
            suffix = _safe_descriptor(image)
            try:
                payload = client.download(image)
            except ComfyUIMalformedResponse as exc:
                return self._failure(
                    "OUTPUT_DOWNLOAD_FAILED",
                    "provider_output",
                    str(exc),
                    retryable=True,
                    metadata=failure_metadata(operation="output download"),
                )

            if not SAFE_RESULT_ID.fullmatch(request.generation_result_id):
                raise FluxOutputSafetyError("generation_result_id is unsafe for a local filename")
            output_dir = Path(request.output_path).resolve(strict=False)
            if not output_dir.is_absolute():
                raise FluxOutputSafetyError("request.output_path must be absolute")
            destination = output_dir / f"{request.generation_result_id}{suffix}"
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
                _atomic_write(destination, payload)
            except OSError as exc:
                return self._failure(
                    "ARTIFACT_WRITE_FAILED",
                    "filesystem",
                    str(exc),
                    metadata=failure_metadata(operation="artifact_write"),
                )
            return ProviderExecutionResult.success(
                ProviderArtifact(
                    resolved_path=str(destination),
                    kind="image",
                    role="generation_output",
                    mime_type=IMAGE_SUFFIXES[suffix],
                ),
                metadata={
                    "actual_workflow_sha256": actual_hash,
                    "comfyui_filename": image.filename,
                    "comfyui_prompt_id": prompt_id,
                    "comfyui_subfolder": image.subfolder,
                    "comfyui_type": image.output_type,
                    "output_node_id": image.node_id,
                    "submitted_seed": request.seed,
                },
            )
        except json.JSONDecodeError as exc:
            return self._failure("INVALID_PROVIDER_CONFIG", "configuration", str(exc))
        except FluxInputError as exc:
            return self._failure("INVALID_SCENE_INPUT", "input", str(exc))
        except FluxWorkflowError as exc:
            return self._failure("WORKFLOW_INVALID", "workflow", str(exc))
        except FluxOutputSafetyError as exc:
            return self._failure(
                "OUTPUT_PATH_UNSAFE",
                "security",
                str(exc),
                metadata=failure_metadata(operation="output_safety"),
            )
        except WorkflowRejected as exc:
            return self._failure("WORKFLOW_REJECTED", "workflow", str(exc))
        except ComfyUIExecutionFailed as exc:
            return self._failure(
                "EXECUTION_FAILED",
                "provider_execution",
                str(exc),
                metadata=failure_metadata(operation="history_poll"),
            )
        except ComfyUITimeout as exc:
            return self._failure(
                "GENERATION_TIMEOUT",
                "timeout",
                str(exc),
                metadata=failure_metadata(operation="history_poll"),
            )
        except ComfyUIHTTPError as exc:
            code = (
                "OUTPUT_DOWNLOAD_FAILED"
                if exc.operation == "output download"
                else "COMFYUI_HTTP_ERROR"
            )
            return self._failure(
                code,
                "transport",
                str(exc),
                retryable=exc.status == 429 or exc.status >= 500,
                metadata=failure_metadata(operation=exc.operation),
            )
        except ComfyUIUnavailable as exc:
            code = (
                "OUTPUT_DOWNLOAD_FAILED"
                if exc.operation == "output download"
                else "COMFYUI_UNAVAILABLE"
            )
            return self._failure(
                code,
                "transport",
                str(exc),
                retryable=True,
                metadata=failure_metadata(operation=exc.operation),
            )
        except ComfyUIMalformedResponse as exc:
            code = "MALFORMED_HISTORY" if prompt_id else "WORKFLOW_REJECTED"
            category = "protocol" if prompt_id else "workflow"
            return self._failure(
                code,
                category,
                str(exc),
                metadata=failure_metadata(operation="history_poll"),
            )
        except ComfyUIClientError as exc:
            return self._failure("COMFYUI_HTTP_ERROR", "transport", str(exc))
