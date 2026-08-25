from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd


IMAGE_COLUMNS = (
    "postprocessed_output",
    "source",
)


def find_image(row: pd.Series) -> Path | None:
    for column in IMAGE_COLUMNS:
        value = row.get(column)

        if pd.isna(value) or not str(value).strip():
            continue

        path = Path(str(value))

        if path.is_file():
            return path

    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ONYX Quality Gate v1.0 — finalize reviewed client set"
    )

    parser.add_argument("report", type=Path)
    parser.add_argument("--client", required=True)
    parser.add_argument("--delivery", type=Path, required=True)

    args = parser.parse_args()

    report_path = args.report.resolve()
    delivery_root = args.delivery.resolve()

    df = pd.read_csv(report_path, encoding="utf-8-sig")

    required = [
        "scene_id",
        "method",
        "human_identity",
        "human_quality",
        "client_ready",
    ]

    missing = [c for c in required if c not in df.columns]

    if missing:
        raise RuntimeError(
            "Missing required columns: " + ", ".join(missing)
        )

    # ---------------------------------------------------------
    # Verify manual QA is complete
    # ---------------------------------------------------------

    incomplete = (
        df["human_identity"].isna()
        | df["human_quality"].isna()
        | df["client_ready"].isna()
        | df["client_ready"].astype(str).str.strip().eq("")
    )

    if incomplete.any():
        raise RuntimeError(
            f"Manual review incomplete: "
            f"{int(incomplete.sum())}/{len(df)} rows are not rated."
        )

    df["client_ready"] = (
        df["client_ready"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    invalid_ready = ~df["client_ready"].isin(["Y", "N"])

    if invalid_ready.any():
        values = sorted(
            df.loc[invalid_ready, "client_ready"]
            .astype(str)
            .unique()
        )

        raise RuntimeError(
            f"Invalid client_ready values: {values}"
        )

    # ---------------------------------------------------------
    # Selection
    # Human decision is authoritative.
    # ---------------------------------------------------------

    accepted = df["client_ready"].eq("Y")

    df["qa_accepted"] = accepted

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    methods = {}

    for method, group in df.groupby("method"):

        accepted_group = group["client_ready"].eq("Y")

        identity = pd.to_numeric(
            group["human_identity"],
            errors="coerce",
        )

        quality = pd.to_numeric(
            group["human_quality"],
            errors="coerce",
        )

        methods[str(method)] = {
            "candidates": int(len(group)),
            "client_ready": int(accepted_group.sum()),
            "yield": round(
                float(accepted_group.mean()),
                4,
            ),
            "identity_mean": round(
                float(identity.mean()),
                3,
            ),
            "identity_median": round(
                float(identity.median()),
                3,
            ),
            "quality_mean": round(
                float(quality.mean()),
                3,
            ),
            "quality_median": round(
                float(quality.median()),
                3,
            ),
        }

    stats = {
        "quality_gate_version": "1.0",
        "client": args.client,
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "candidates": int(len(df)),
        "accepted": int(accepted.sum()),
        "rejected": int((~accepted).sum()),
        "yield": round(float(accepted.mean()), 4),
        "methods": methods,
    }

    # ---------------------------------------------------------
    # Create clean delivery
    # ---------------------------------------------------------

    delivery_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Safety:
    # remove only files previously created by this finalizer.
    for old in delivery_root.glob("ONYX_*.*"):
        if old.is_file():
            old.unlink()

    manifest_rows = []

    accepted_df = df[accepted].copy()

    for number, (_, row) in enumerate(
        accepted_df.iterrows(),
        start=1,
    ):
        source = find_image(row)

        if source is None:
            raise RuntimeError(
                "Image not found for "
                f"{row['scene_id']} / {row['method']}"
            )

        customer_name = (
            f"ONYX_{number:03d}{source.suffix.lower()}"
        )

        destination = (
            delivery_root / customer_name
        )

        shutil.copy2(
            source,
            destination,
        )

        manifest_rows.append({
            "customer_filename": customer_name,
            "scene_id": row["scene_id"],
            "method": row["method"],
            "human_identity": row["human_identity"],
            "human_quality": row["human_quality"],
            "client_ready": row["client_ready"],
            "source": str(source),
        })

    # ---------------------------------------------------------
    # Save QA artifacts
    # ---------------------------------------------------------

    qa_root = delivery_root / "_qa"

    qa_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    pd.DataFrame(manifest_rows).to_csv(
        qa_root / "delivery_manifest.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df.to_csv(
        qa_root / "quality_report.csv",
        index=False,
        encoding="utf-8-sig",
    )

    (qa_root / "qa_statistics.json").write_text(
        json.dumps(
            stats,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # ---------------------------------------------------------
    # Console report
    # ---------------------------------------------------------

    print()
    print("=" * 78)
    print("ONYX QUALITY GATE v1.0")
    print("=" * 78)

    print(f"Client     : {args.client}")
    print(f"Candidates : {len(df)}")
    print(f"Accepted   : {int(accepted.sum())}")
    print(f"Rejected   : {int((~accepted).sum())}")
    print(
        f"Yield      : "
        f"{accepted.mean() * 100:.1f}%"
    )

    print()
    print("METHOD PERFORMANCE")
    print("-" * 78)

    ranking = sorted(
        methods.items(),
        key=lambda x: (
            x[1]["yield"],
            x[1]["identity_mean"],
            x[1]["quality_mean"],
        ),
        reverse=True,
    )

    for method, data in ranking:
        print(
            f"{method:32} "
            f"{data['client_ready']:2}/"
            f"{data['candidates']:2}  "
            f"{data['yield'] * 100:5.1f}%  "
            f"ID={data['identity_mean']:.2f}  "
            f"Q={data['quality_mean']:.2f}"
        )

    print("-" * 78)
    print(f"Delivery   : {delivery_root}")
    print(f"Copied     : {len(manifest_rows)}")
    print("=" * 78)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())