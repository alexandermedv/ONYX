import argparse
import json
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "schema": str,
    "schema_version": str,
    "client_id": str,
    "identity.gender.value": str,
    "identity.exact_age.value": int,
    "body.build.value": str,
    "face.facial_hair.type": str,
    "hair.scalp_hair.type": str,
    "eyes.color.value": str,
    "accessories.glasses.value": bool,
}

OPTIONAL_FIELDS = [
    "body.height.value",
    "face.shape.value",
    "face.skin_tone.value",
]

CONFIRMATION_FIELDS = [
    "identity.gender",
    "identity.exact_age",
    "identity.apparent_age_range",
    "body.build",
    "face.facial_hair",
    "hair.scalp_hair",
    "eyes.color",
    "accessories.glasses",
]


def get_nested(data, path):
    current = data

    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None

        current = current[part]

    return current


def main():
    parser = argparse.ArgumentParser(
        description="Validate ONYX Client Profile 2.0"
    )
    parser.add_argument("profile", help="Path to client_profile_v2.json")
    args = parser.parse_args()

    profile_path = Path(args.profile)

    if not profile_path.is_file():
        print(f"ERROR: profile not found: {profile_path}")
        return 2

    try:
        with profile_path.open("r", encoding="utf-8-sig") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        print(f"ERROR: invalid JSON: {error}")
        return 2

    errors = []
    warnings = []

    if data.get("schema") != "onyx.client_profile":
        errors.append(
            'schema must be "onyx.client_profile"'
        )

    if data.get("schema_version") != "2.0":
        errors.append(
            'schema_version must be "2.0"'
        )

    for field, expected_type in REQUIRED_FIELDS.items():
        value = get_nested(data, field)

        if value is None:
            errors.append(f"required field is missing: {field}")
        elif type(value) is not expected_type:
            errors.append(
                f"{field} must be {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        elif isinstance(value, str) and not value.strip():
            errors.append(f"required field is empty: {field}")

    exact_age = get_nested(data, "identity.exact_age.value")

    if type(exact_age) is int and not 1 <= exact_age <= 120:
        errors.append("identity.exact_age.value must be between 1 and 120")

    for field in OPTIONAL_FIELDS:
        if get_nested(data, field) is None:
            warnings.append(f"optional field is not filled: {field}")

    for field in CONFIRMATION_FIELDS:
        confirmed = get_nested(data, f"{field}.confirmed")

        if confirmed is not True:
            warnings.append(f"characteristic is not confirmed: {field}")

    if errors:
        status = "NOT_READY"
    elif warnings:
        status = "READY_WITH_WARNINGS"
    else:
        status = "READY"

    print(f"Profile: {profile_path}")
    print(f"Client: {data.get('client_id', 'unknown')}")
    print(f"Schema: {data.get('schema', 'missing')}")
    print(f"Version: {data.get('schema_version', 'missing')}")
    print(f"Status: {status}")

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