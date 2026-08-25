import argparse
import json
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "schema": str,
    "schema_version": str,
    "session_id": str,
    "client_id": str,
    "client_profile": str,
    "status": str,
    "creative_direction.collection": str,
    "generation.scene_mode": str,
    "generation.candidate_count": int,
    "generation.target_final_count": int,
    "generation.orientation": str,
    "generation.aspect_ratio": str,
    "generation.scene_generator_version": str,
}


def get_nested(data, path):
    current = data

    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]

    return current


def load_json(path, label, errors):
    try:
        with path.open("r", encoding="utf-8-sig") as file:
            return json.load(file)
    except FileNotFoundError:
        errors.append(f"{label} not found: {path}")
    except json.JSONDecodeError as error:
        errors.append(f"{label} contains invalid JSON: {error}")

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Validate ONYX Session Spec 1.0"
    )
    parser.add_argument(
        "session_spec",
        help="Path to session_spec.json"
    )
    args = parser.parse_args()

    session_path = Path(args.session_spec)
    errors = []
    warnings = []

    session = load_json(session_path, "session spec", errors)

    if session is None:
        for error in errors:
            print(f"ERROR: {error}")
        return 2

    if session.get("schema") != "onyx.session_spec":
        errors.append('schema must be "onyx.session_spec"')

    if session.get("schema_version") != "1.0":
        errors.append('schema_version must be "1.0"')

    for field, expected_type in REQUIRED_FIELDS.items():
        value = get_nested(session, field)

        if value is None:
            errors.append(f"required field is missing: {field}")
        elif type(value) is not expected_type:
            errors.append(
                f"{field} must be {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        elif isinstance(value, str) and not value.strip():
            errors.append(f"required field is empty: {field}")

    allowed_statuses = {
        "draft",
        "ready",
        "running",
        "review",
        "completed",
        "cancelled",
    }

    status = session.get("status")

    if isinstance(status, str) and status not in allowed_statuses:
        errors.append(
            f"status must be one of: {', '.join(sorted(allowed_statuses))}"
        )

    if status == "draft":
        warnings.append(
            'session status is "draft"; change it to "ready" '
            "before production generation"
        )

    candidate_count = get_nested(
        session,
        "generation.candidate_count"
    )
    target_final_count = get_nested(
        session,
        "generation.target_final_count"
    )

    if type(candidate_count) is int and candidate_count < 1:
        errors.append(
            "generation.candidate_count must be at least 1"
        )

    if type(target_final_count) is int and target_final_count < 1:
        errors.append(
            "generation.target_final_count must be at least 1"
        )

    if (
        type(candidate_count) is int
        and type(target_final_count) is int
        and target_final_count > candidate_count
    ):
        errors.append(
            "generation.target_final_count cannot be greater than "
            "generation.candidate_count"
        )

    profile_value = session.get("client_profile")
    profile = None
    profile_path = None

    if isinstance(profile_value, str) and profile_value.strip():
        profile_path = Path(profile_value)
        profile = load_json(profile_path, "client profile", errors)

    if profile is not None:
        if profile.get("schema") != "onyx.client_profile":
            errors.append(
                'linked profile schema must be "onyx.client_profile"'
            )

        if profile.get("schema_version") != "2.0":
            errors.append(
                'linked profile schema_version must be "2.0"'
            )

        session_client_id = session.get("client_id")
        profile_client_id = profile.get("client_id")

        if session_client_id != profile_client_id:
            errors.append(
                "client_id mismatch: "
                f"session={session_client_id!r}, "
                f"profile={profile_client_id!r}"
            )

    if errors:
        validation_status = "NOT_READY"
    elif warnings:
        validation_status = "READY_WITH_WARNINGS"
    else:
        validation_status = "READY"

    print(f"Session: {session_path}")
    print(f"Session ID: {session.get('session_id', 'unknown')}")
    print(f"Client: {session.get('client_id', 'unknown')}")
    print(f"Schema: {session.get('schema', 'missing')}")
    print(f"Version: {session.get('schema_version', 'missing')}")
    print(f"Session status: {session.get('status', 'missing')}")

    if profile_path is not None:
        print(f"Client profile: {profile_path}")

    print(f"Validation status: {validation_status}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if not errors and not warnings:
        print("\nNo validation issues found.")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())