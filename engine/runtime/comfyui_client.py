from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable


class ComfyUIClientError(RuntimeError):
    """Base error raised by the transport-neutral ComfyUI boundary."""


class ComfyUIUnavailable(ComfyUIClientError):
    def __init__(self, message: str, *, operation: str) -> None:
        super().__init__(message)
        self.operation = operation


class ComfyUIHTTPError(ComfyUIClientError):
    def __init__(self, status: int, message: str, *, operation: str) -> None:
        super().__init__(message)
        self.status = status
        self.operation = operation


class WorkflowRejected(ComfyUIClientError):
    pass


class ComfyUIExecutionFailed(ComfyUIClientError):
    pass


class ComfyUIMalformedResponse(ComfyUIClientError):
    pass


class ComfyUITimeout(ComfyUIClientError):
    def __init__(self, prompt_id: str, timeout_seconds: float) -> None:
        super().__init__(
            f"ComfyUI prompt {prompt_id} did not finish within {timeout_seconds:g} seconds"
        )
        self.prompt_id = prompt_id


@dataclass(frozen=True)
class ComfyUIImageOutput:
    node_id: str
    filename: str
    subfolder: str
    output_type: str


Opener = Callable[..., Any]
Clock = Callable[[], float]
Sleeper = Callable[[float], None]


class ComfyUIClient:
    """Minimal synchronous client for one submitted ComfyUI API workflow."""

    def __init__(
        self,
        endpoint: str,
        *,
        opener: Opener = urllib.request.urlopen,
        clock: Clock = time.monotonic,
        sleeper: Sleeper = time.sleep,
        request_timeout_seconds: float = 30,
        poll_interval_seconds: float = 1,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.opener = opener
        self.clock = clock
        self.sleeper = sleeper
        self.request_timeout_seconds = request_timeout_seconds
        self.poll_interval_seconds = poll_interval_seconds

    def _open(self, request: urllib.request.Request, *, operation: str) -> bytes:
        try:
            with self.opener(request, timeout=self.request_timeout_seconds) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            message = f"HTTP {exc.code} during {operation}: {body or exc.reason}"
            raise ComfyUIHTTPError(exc.code, message, operation=operation) from exc
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
            raise ComfyUIUnavailable(
                f"ComfyUI unavailable during {operation}: {exc}",
                operation=operation,
            ) from exc

    def _json(
        self,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        operation: str,
    ) -> dict[str, Any]:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(f"{self.endpoint}{path}", data=data)
        request.add_header("Connection", "close")
        if data is not None:
            request.add_header("Content-Type", "application/json")
        raw = self._open(request, operation=operation)
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ComfyUIMalformedResponse(
                f"ComfyUI returned malformed JSON during {operation}"
            ) from exc
        if not isinstance(parsed, dict):
            raise ComfyUIMalformedResponse(
                f"ComfyUI returned a non-object response during {operation}"
            )
        return parsed

    def submit(self, workflow: dict[str, Any], client_id: str) -> str:
        """Submit exactly once. The caller must not retry an ambiguous POST."""
        try:
            response = self._json(
                "/prompt",
                payload={"prompt": workflow, "client_id": client_id},
                operation="prompt submission",
            )
        except ComfyUIHTTPError as exc:
            if 400 <= exc.status < 500:
                raise WorkflowRejected(str(exc)) from exc
            raise
        prompt_id = response.get("prompt_id")
        if not isinstance(prompt_id, str) or not prompt_id.strip():
            raise WorkflowRejected("ComfyUI /prompt response has no valid prompt_id")
        return prompt_id

    def _history_record(self, prompt_id: str) -> dict[str, Any] | None:
        encoded = urllib.parse.quote(prompt_id, safe="")
        history = self._json(
            f"/history/{encoded}", operation=f"history polling for {prompt_id}"
        )
        if prompt_id not in history:
            return None
        record = history[prompt_id]
        if not isinstance(record, dict):
            raise ComfyUIMalformedResponse("ComfyUI history record must be an object")
        status = record.get("status")
        if not isinstance(status, dict):
            raise ComfyUIMalformedResponse("ComfyUI history record has no valid status")
        status_str = status.get("status_str")
        completed = status.get("completed")
        if status_str == "error":
            raise ComfyUIExecutionFailed(
                "ComfyUI execution failed: "
                + json.dumps(status, ensure_ascii=False, sort_keys=True)
            )
        if completed is True or status_str == "success":
            return record
        return None

    def wait_for_history(self, prompt_id: str, timeout_seconds: float) -> dict[str, Any]:
        deadline = self.clock() + timeout_seconds
        while True:
            record = self._history_record(prompt_id)
            if record is not None:
                return record
            if self.clock() >= deadline:
                raise ComfyUITimeout(prompt_id, timeout_seconds)
            self.sleeper(self.poll_interval_seconds)

    @staticmethod
    def one_image(record: dict[str, Any]) -> ComfyUIImageOutput:
        outputs = record.get("outputs")
        if not isinstance(outputs, dict):
            raise ComfyUIMalformedResponse("Successful history has no outputs object")
        images: list[ComfyUIImageOutput] = []
        for node_id, node_output in outputs.items():
            if not isinstance(node_output, dict):
                raise ComfyUIMalformedResponse("History node output must be an object")
            node_images = node_output.get("images", [])
            if not isinstance(node_images, list):
                raise ComfyUIMalformedResponse("History images must be an array")
            for image in node_images:
                if not isinstance(image, dict):
                    raise ComfyUIMalformedResponse("History image descriptor must be an object")
                filename = image.get("filename")
                subfolder = image.get("subfolder", "")
                output_type = image.get("type", "output")
                if not all(isinstance(value, str) for value in (filename, subfolder, output_type)):
                    raise ComfyUIMalformedResponse("History image descriptor is malformed")
                images.append(ComfyUIImageOutput(str(node_id), filename, subfolder, output_type))
        if not images:
            raise LookupError("Successful ComfyUI history contains no image output")
        if len(images) != 1:
            raise ValueError(
                f"Phase 1B.3 requires exactly one image output, received {len(images)}"
            )
        return images[0]

    def download(self, image: ComfyUIImageOutput) -> bytes:
        query = urllib.parse.urlencode(
            {
                "filename": image.filename,
                "subfolder": image.subfolder,
                "type": image.output_type,
            }
        )
        request = urllib.request.Request(f"{self.endpoint}/view?{query}")
        request.add_header("Connection", "close")
        payload = self._open(request, operation="output download")
        if not payload:
            raise ComfyUIMalformedResponse("ComfyUI /view returned an empty output")
        return payload
