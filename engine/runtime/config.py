from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


RUNTIME_CONFIG_SCHEMA = "onyx.runtime_config"
RUNTIME_CONFIG_VERSION = "1.0"
RUNTIME_CONFIG_ENV = "ONYX_RUNTIME_CONFIG"


class RuntimeConfigError(ValueError):
    """Raised when machine-local runtime configuration is invalid."""


def _optional_string(data: dict[str, Any], name: str) -> str | None:
    value = data.get(name)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise RuntimeConfigError(f"{name} must be a non-empty string when provided")
    return value


def _string_mapping(data: Any, label: str) -> dict[str, str]:
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise RuntimeConfigError(f"{label} must be an object")
    result: dict[str, str] = {}
    for key, value in data.items():
        if not isinstance(key, str) or not key or not isinstance(value, str) or not value:
            raise RuntimeConfigError(f"{label} must contain non-empty string keys and values")
        result[key] = value
    return result


@dataclass(frozen=True)
class ProviderRuntimeConfig:
    endpoint: str | None = None
    root: str | None = None
    python_executable: str | None = None
    input_root: str | None = None
    output_root: str | None = None
    workflow_root: str | None = None
    model_roots: dict[str, str] = field(default_factory=dict)
    models: dict[str, str] = field(default_factory=dict)
    capabilities: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProviderRuntimeConfig:
        if not isinstance(data, dict):
            raise RuntimeConfigError("Provider runtime configuration must be an object")
        known = {
            "endpoint", "root", "python_executable", "input_root", "output_root",
            "workflow_root", "model_roots", "models", "capabilities", "metadata",
        }
        unknown = set(data) - known
        if unknown:
            raise RuntimeConfigError(f"Unknown provider runtime fields: {sorted(unknown)}")
        capabilities = data.get("capabilities", [])
        if not isinstance(capabilities, list) or not all(isinstance(item, str) for item in capabilities):
            raise RuntimeConfigError("capabilities must be an array of strings")
        metadata = data.get("metadata", {})
        if not isinstance(metadata, dict):
            raise RuntimeConfigError("metadata must be an object")
        return cls(
            endpoint=_optional_string(data, "endpoint"),
            root=_optional_string(data, "root"),
            python_executable=_optional_string(data, "python_executable"),
            input_root=_optional_string(data, "input_root"),
            output_root=_optional_string(data, "output_root"),
            workflow_root=_optional_string(data, "workflow_root"),
            model_roots=_string_mapping(data.get("model_roots"), "model_roots"),
            models=_string_mapping(data.get("models"), "models"),
            capabilities=tuple(capabilities),
            metadata=dict(metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "model_roots": dict(self.model_roots),
            "models": dict(self.models),
            "capabilities": list(self.capabilities),
            "metadata": dict(self.metadata),
        }
        for name in ("endpoint", "root", "python_executable", "input_root", "output_root", "workflow_root"):
            value = getattr(self, name)
            if value is not None:
                result[name] = value
        return result


@dataclass(frozen=True)
class RuntimeConfig:
    schema: str
    schema_version: str
    machine_id: str
    repo_root: str
    workspace_root: str
    client_root: str
    providers: dict[str, ProviderRuntimeConfig]
    workflow_roots: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RuntimeConfig:
        if not isinstance(data, dict):
            raise RuntimeConfigError("Runtime configuration must be a JSON object")
        known = {
            "schema", "schema_version", "machine_id", "repo_root", "workspace_root",
            "client_root", "providers", "workflow_roots", "metadata",
        }
        unknown = set(data) - known
        if unknown:
            raise RuntimeConfigError(f"Unknown runtime configuration fields: {sorted(unknown)}")
        required = {"schema", "schema_version", "machine_id", "repo_root", "workspace_root", "client_root", "providers"}
        missing = required - set(data)
        if missing:
            raise RuntimeConfigError(f"Missing runtime configuration fields: {sorted(missing)}")
        if data["schema"] != RUNTIME_CONFIG_SCHEMA:
            raise RuntimeConfigError(f"Unsupported runtime config schema: {data['schema']}")
        if data["schema_version"] != RUNTIME_CONFIG_VERSION:
            raise RuntimeConfigError(f"Unsupported runtime config version: {data['schema_version']}")
        providers_data = data["providers"]
        if not isinstance(providers_data, dict):
            raise RuntimeConfigError("providers must be an object")
        providers = {
            provider_id: ProviderRuntimeConfig.from_dict(provider_data)
            for provider_id, provider_data in providers_data.items()
        }
        metadata = data.get("metadata", {})
        if not isinstance(metadata, dict):
            raise RuntimeConfigError("metadata must be an object")
        return cls(
            schema=str(data["schema"]),
            schema_version=str(data["schema_version"]),
            machine_id=str(data["machine_id"]),
            repo_root=str(data["repo_root"]),
            workspace_root=str(data["workspace_root"]),
            client_root=str(data["client_root"]),
            providers=providers,
            workflow_roots=_string_mapping(data.get("workflow_roots"), "workflow_roots"),
            metadata=dict(metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "schema_version": self.schema_version,
            "machine_id": self.machine_id,
            "repo_root": self.repo_root,
            "workspace_root": self.workspace_root,
            "client_root": self.client_root,
            "providers": {key: value.to_dict() for key, value in sorted(self.providers.items())},
            "workflow_roots": dict(sorted(self.workflow_roots.items())),
            "metadata": dict(self.metadata),
        }


def load_runtime_config(path: Path | str | None = None) -> RuntimeConfig:
    selected = path or os.environ.get(RUNTIME_CONFIG_ENV) or Path("config/runtime.local.json")
    config_path = Path(selected)
    try:
        data = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise RuntimeConfigError(f"Runtime configuration not found: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeConfigError(f"Invalid runtime configuration JSON: {config_path}: {exc}") from exc
    return RuntimeConfig.from_dict(data)


def dumps_runtime_config(config: RuntimeConfig, *, indent: int = 2) -> str:
    return json.dumps(config.to_dict(), ensure_ascii=False, indent=indent) + "\n"
