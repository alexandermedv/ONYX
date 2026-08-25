from __future__ import annotations

import argparse
import hashlib
import shutil
import threading
from pathlib import Path

import pandas as pd
from flask import Flask, Response, jsonify, render_template_string, request


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

app = Flask(__name__)

df: pd.DataFrame
csv_path: Path
backup_path: Path
reference_images: list[Path]
review_order: list[int]

save_lock = threading.Lock()


HTML = r"""
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>ONYX QA Reviewer v0.2</title>

<style>
body {
    margin: 0;
    background: #111;
    color: #eee;
    font-family: Arial, sans-serif;
}

.header {
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    background: #1b1b1b;
    border-bottom: 1px solid #333;
}

.references {
    display: flex;
    justify-content: center;
    gap: 8px;
    padding: 8px;
    height: 125px;
    background: #181818;
}

.references img {
    max-height: 115px;
    max-width: 170px;
    object-fit: contain;
    border: 1px solid #444;
}

.candidate-container {
    height: calc(100vh - 355px);
    min-height: 320px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
}

.candidate {
    max-height: 100%;
    max-width: 92%;
    object-fit: contain;
}

.controls {
    background: #181818;
    border-top: 1px solid #333;
    padding: 10px 20px;
}

.row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 7px;
    margin: 6px;
}

.label {
    width: 120px;
    text-align: right;
    margin-right: 10px;
    font-weight: bold;
}

button {
    padding: 8px 14px;
    border: 1px solid #555;
    background: #292929;
    color: white;
    cursor: pointer;
    border-radius: 5px;
}

button:hover {
    background: #444;
}

button.selected {
    outline: 3px solid white;
    background: #555;
}

.save {
    background: #315b38;
    min-width: 180px;
    font-weight: bold;
}

.save:disabled {
    background: #333;
    color: #777;
    cursor: default;
}

.status {
    color: #aaa;
    min-height: 18px;
}

.error {
    color: #ff7777;
    font-weight: bold;
}

.success {
    color: #79d987;
}

.help {
    color: #888;
    font-size: 12px;
}
</style>
</head>

<body>

<div class="header">
    <div><strong>ONYX QA Reviewer v0.2 — Blind Review</strong></div>
    <div id="progress">Loading...</div>
</div>

<div class="references">
{% for i in range(reference_count) %}
    <img src="/reference/{{ i }}">
{% endfor %}
</div>

<div class="candidate-container">
    <img id="candidate" class="candidate">
</div>

<div class="controls">

    <div class="row">
        <span class="label">Identity</span>
        <button id="i0" onclick="chooseIdentity(0)">1 — другой</button>
        <button id="i1" onclick="chooseIdentity(1)">2 — слабо</button>
        <button id="i2" onclick="chooseIdentity(2)">3 — похож</button>
        <button id="i3" onclick="chooseIdentity(3)">4 — очень похож</button>
    </div>

    <div class="row">
        <span class="label">Quality</span>
        <button id="q0" onclick="chooseQuality(0)">Q — брак</button>
        <button id="q1" onclick="chooseQuality(1)">W — плохо</button>
        <button id="q2" onclick="chooseQuality(2)">E — нормально</button>
        <button id="q3" onclick="chooseQuality(3)">R — готово</button>
    </div>

    <div class="row">
        <span class="label">Client-ready</span>
        <button id="rY" onclick="chooseReady('Y')">Y — да</button>
        <button id="rN" onclick="chooseReady('N')">N — нет</button>
    </div>

    <div class="row">
        <button onclick="previous()">← Previous</button>
        <button id="saveButton" class="save" onclick="saveAndNext()" disabled>
            SAVE & NEXT
        </button>
        <button onclick="nextWithoutSave()">Next →</button>
    </div>

    <div class="row">
        <span id="status" class="status"></span>
    </div>

    <div class="row help">
        Identity 1–4 · Quality Q/W/E/R · Ready Y/N · Enter = SAVE & NEXT
    </div>

</div>

<script>

let position = {{ start_position }};
let identity = null;
let quality = null;
let ready = null;
let saving = false;


function mark(group, selectedId) {
    group.forEach(id =>
        document.getElementById(id).classList.remove("selected")
    );

    if (selectedId !== null) {
        document.getElementById(selectedId).classList.add("selected");
    }
}


function updateSaveButton() {
    document.getElementById("saveButton").disabled =
        identity === null ||
        quality === null ||
        ready === null ||
        saving;
}


function chooseIdentity(value) {
    identity = value;
    mark(["i0","i1","i2","i3"], "i" + value);
    updateSaveButton();
}


function chooseQuality(value) {
    quality = value;
    mark(["q0","q1","q2","q3"], "q" + value);
    updateSaveButton();
}


function chooseReady(value) {
    ready = value;
    mark(["rY","rN"], value === "Y" ? "rY" : "rN");
    updateSaveButton();
}


async function load(pos) {

    const response = await fetch("/item/" + pos);
    const item = await response.json();

    if (item.finished) {
        document.getElementById("candidate").style.display = "none";
        document.getElementById("progress").innerText =
            item.total + " / " + item.total;

        document.getElementById("status").className = "success";
        document.getElementById("status").innerText =
            "Все 120 изображений сохранены.";

        return;
    }

    position = item.position;

    identity = item.identity;
    quality = item.quality;
    ready = item.ready;

    document.getElementById("candidate").style.display = "block";
    document.getElementById("candidate").src =
        "/candidate/" + position + "?v=" + Date.now();

    document.getElementById("progress").innerText =
        (position + 1) + " / " + item.total;

    mark(
        ["i0","i1","i2","i3"],
        identity === null ? null : "i" + identity
    );

    mark(
        ["q0","q1","q2","q3"],
        quality === null ? null : "q" + quality
    );

    mark(
        ["rY","rN"],
        ready === null ? null : (ready === "Y" ? "rY" : "rN")
    );

    document.getElementById("status").className = "status";

    document.getElementById("status").innerText =
        item.complete
        ? "Эта оценка уже сохранена."
        : "Выбери все 3 оценки.";

    updateSaveButton();
}


async function saveAndNext() {

    if (
        saving ||
        identity === null ||
        quality === null ||
        ready === null
    ) {
        return;
    }

    saving = true;
    updateSaveButton();

    const status = document.getElementById("status");
    status.className = "status";
    status.innerText = "Сохраняю и проверяю...";

    try {

        const response = await fetch("/save-rating", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                position: position,
                human_identity: identity,
                human_quality: quality,
                client_ready: ready
            })
        });

        const result = await response.json();

        if (!response.ok || !result.ok || !result.verified) {
            throw new Error(
                result.error || "Verification failed"
            );
        }

        status.className = "success";
        status.innerText =
            "СОХРАНЕНО ✓  " +
            "Identity=" + result.saved.human_identity +
            " Quality=" + result.saved.human_quality +
            " Ready=" + result.saved.client_ready;

        await new Promise(resolve => setTimeout(resolve, 120));

        saving = false;
        await load(position + 1);

    } catch (error) {

        saving = false;
        updateSaveButton();

        status.className = "error";
        status.innerText =
            "НЕ СОХРАНЕНО: " + error.message;
    }
}


function previous() {
    if (!saving && position > 0) {
        load(position - 1);
    }
}


function nextWithoutSave() {
    if (!saving) {
        load(position + 1);
    }
}


document.addEventListener("keydown", async event => {

    if (saving) return;

    if (event.key === "1") chooseIdentity(0);
    if (event.key === "2") chooseIdentity(1);
    if (event.key === "3") chooseIdentity(2);
    if (event.key === "4") chooseIdentity(3);

    if (event.key.toLowerCase() === "q") chooseQuality(0);
    if (event.key.toLowerCase() === "w") chooseQuality(1);
    if (event.key.toLowerCase() === "e") chooseQuality(2);
    if (event.key.toLowerCase() === "r") chooseQuality(3);

    if (event.key.toLowerCase() === "y") chooseReady("Y");
    if (event.key.toLowerCase() === "n") chooseReady("N");

    if (event.key === "Enter") {
        event.preventDefault();
        await saveAndNext();
    }

    if (event.key === "ArrowLeft") previous();
});


load(position);

</script>
</body>
</html>
"""


def image_bytes(path: Path) -> bytes:
    return path.read_bytes()


def mime_type(path: Path) -> str:
    ext = path.suffix.lower()

    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"

    return "application/octet-stream"


def complete(row: pd.Series) -> bool:
    for column in [
        "human_identity",
        "human_quality",
        "client_ready",
    ]:
        value = row.get(column)

        if pd.isna(value) or str(value).strip() == "":
            return False

    return True


def save_and_verify(
    row_index: int,
    human_identity: int,
    human_quality: int,
    client_ready: str,
) -> dict:

    global df

    with save_lock:

        # Backup BEFORE changing the master CSV.
        if csv_path.exists():
            shutil.copy2(csv_path, backup_path)

        df.loc[row_index, "human_identity"] = human_identity
        df.loc[row_index, "human_quality"] = human_quality
        df.loc[row_index, "client_ready"] = client_ready

        temp_path = csv_path.with_name(
            csv_path.stem + ".writing.csv"
        )

        df.to_csv(
            temp_path,
            index=False,
            encoding="utf-8-sig",
        )

        temp_path.replace(csv_path)

        # CRITICAL:
        # Read the file back from disk.
        verification = pd.read_csv(
            csv_path,
            encoding="utf-8-sig",
        )

        verification["human_identity"] = pd.to_numeric(
            verification["human_identity"],
            errors="coerce",
        ).astype("Int64")

        verification["human_quality"] = pd.to_numeric(
            verification["human_quality"],
            errors="coerce",
        ).astype("Int64")

        verification["client_ready"] = (
            verification["client_ready"].astype("string")
        )

        saved_identity = verification.loc[
            row_index,
            "human_identity"
        ]

        saved_quality = verification.loc[
            row_index,
            "human_quality"
        ]

        saved_ready = str(
            verification.loc[
                row_index,
                "client_ready"
            ]
        ).strip().upper()

        verified = (
            int(saved_identity) == int(human_identity)
            and int(saved_quality) == int(human_quality)
            and saved_ready == client_ready
        )

        if not verified:
            raise RuntimeError(
                "CSV read-back verification failed"
            )

        # Keep RAM state identical to disk.
        df = verification

        return {
            "human_identity": int(saved_identity),
            "human_quality": int(saved_quality),
            "client_ready": saved_ready,
        }


@app.route("/")
def index():
    return render_template_string(
        HTML,
        reference_count=len(reference_images),
        start_position=find_resume_position(),
    )


@app.route("/reference/<int:index>")
def reference(index: int):
    path = reference_images[index]

    return Response(
        image_bytes(path),
        mimetype=mime_type(path),
    )


@app.route("/candidate/<int:position>")
def candidate(position: int):

    if position < 0 or position >= len(review_order):
        return Response(status=404)

    row_index = review_order[position]
    path = Path(df.loc[row_index, "source"])

    return Response(
        image_bytes(path),
        mimetype=mime_type(path),
    )


@app.route("/item/<int:position>")
def item(position: int):

    if position >= len(review_order):
        return jsonify({
            "finished": True,
            "total": len(review_order),
        })

    if position < 0:
        position = 0

    row_index = review_order[position]
    row = df.loc[row_index]

    def get_value(column):
        value = row.get(column)

        if pd.isna(value) or str(value).strip() == "":
            return None

        return value

    identity = get_value("human_identity")
    quality = get_value("human_quality")
    ready = get_value("client_ready")

    return jsonify({
        "finished": False,
        "position": position,
        "total": len(review_order),
        "identity": (
            int(float(identity))
            if identity is not None
            else None
        ),
        "quality": (
            int(float(quality))
            if quality is not None
            else None
        ),
        "ready": (
            str(ready).strip().upper()
            if ready is not None
            else None
        ),
        "complete": complete(row),
    })


@app.route("/save-rating", methods=["POST"])
def save_rating():

    try:
        payload = request.get_json(force=True)

        position = int(payload["position"])
        human_identity = int(payload["human_identity"])
        human_quality = int(payload["human_quality"])
        client_ready = str(
            payload["client_ready"]
        ).strip().upper()

        if position < 0 or position >= len(review_order):
            raise ValueError("Invalid position")

        if human_identity not in {0, 1, 2, 3}:
            raise ValueError("Invalid human_identity")

        if human_quality not in {0, 1, 2, 3}:
            raise ValueError("Invalid human_quality")

        if client_ready not in {"Y", "N"}:
            raise ValueError("Invalid client_ready")

        row_index = review_order[position]

        saved = save_and_verify(
            row_index,
            human_identity,
            human_quality,
            client_ready,
        )

        print(
            f"SAVED + VERIFIED "
            f"{position + 1:03d}/{len(review_order):03d} | "
            f"row={row_index} | "
            f"identity={saved['human_identity']} | "
            f"quality={saved['human_quality']} | "
            f"ready={saved['client_ready']}"
        )

        return jsonify({
            "ok": True,
            "verified": True,
            "saved": saved,
        })

    except Exception as exc:

        print(f"SAVE FAILED: {exc}")

        return jsonify({
            "ok": False,
            "verified": False,
            "error": str(exc),
        }), 500


def create_review_order(
    dataframe: pd.DataFrame,
) -> list[int]:

    items = []

    for index, row in dataframe.iterrows():

        blind_key = (
            str(row.get("scene_id", ""))
            + "|"
            + str(row.get("method", ""))
            + "|"
            + str(index)
        )

        digest = hashlib.sha256(
            blind_key.encode("utf-8")
        ).hexdigest()

        items.append((digest, index))

    items.sort()

    return [index for _, index in items]


def find_resume_position() -> int:

    for position, row_index in enumerate(review_order):
        if not complete(df.loc[row_index]):
            return position

    return len(review_order)


def main():

    global df
    global csv_path
    global backup_path
    global reference_images
    global review_order

    parser = argparse.ArgumentParser(
        description="ONYX blind QA reviewer v0.2"
    )

    parser.add_argument(
        "report",
        type=Path,
    )

    parser.add_argument(
        "reference_folder",
        type=Path,
    )

    parser.add_argument(
        "--port",
        type=int,
        default=5050,
    )

    args = parser.parse_args()

    csv_path = args.report.resolve()

    backup_path = csv_path.with_name(
        csv_path.stem + ".backup.csv"
    )

    df = pd.read_csv(
        csv_path,
        encoding="utf-8-sig",
    )

    # Annotation columns must use explicit dtypes.
    # Pandas otherwise interprets completely empty CSV columns as float64,
    # which prevents storing string values such as "Y" / "N".

    if "human_identity" not in df.columns:
        df["human_identity"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
    else:
        df["human_identity"] = pd.to_numeric(
            df["human_identity"],
            errors="coerce",
        ).astype("Int64")

    if "human_quality" not in df.columns:
        df["human_quality"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
    else:
        df["human_quality"] = pd.to_numeric(
            df["human_quality"],
            errors="coerce",
        ).astype("Int64")

    if "client_ready" not in df.columns:
        df["client_ready"] = pd.Series(pd.NA, index=df.index, dtype="string")
    else:
        df["client_ready"] = df["client_ready"].astype("string")

    reference_images = sorted(
        p
        for p in args.reference_folder.iterdir()
        if p.is_file()
        and p.suffix.lower() in IMAGE_EXTENSIONS
    )

    review_order = create_review_order(df)

    resume = find_resume_position()

    print()
    print("ONYX QA Reviewer v0.2")
    print("=" * 65)
    print(f"Dataset    : {csv_path}")
    print(f"Backup     : {backup_path}")
    print(f"Candidates : {len(df)}")
    print(f"References : {len(reference_images)}")
    print(
        f"Resume     : "
        f"{min(resume + 1, len(df))}/{len(df)}"
    )
    print()
    print(f"Open http://127.0.0.1:{args.port}")
    print()
    print("SAVE MODE:")
    print("  3 ratings -> one request -> CSV -> read-back verification")
    print("=" * 65)

    app.run(
        host="127.0.0.1",
        port=args.port,
        debug=False,
        threaded=True,
    )


if __name__ == "__main__":
    main()