"""Local, mapping-safe P01 blind-review web application."""
from __future__ import annotations

import argparse
import csv
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, abort, jsonify, render_template_string, request, send_file


SCORE_COLUMNS = ("review_id", "scene", "candidate_id", "identity_score", "realism_score", "scene_score", "commercial_score", "verdict", "comment", "reviewed_at")
SCORE_FIELDS = ("identity_score", "realism_score", "scene_score", "commercial_score")
VERDICTS = {"PASS", "REPAIR", "REGENERATE", "REJECT"}


HTML = r"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><title>ONYX Blind Review</title><style>
:root { color-scheme: dark; } body { margin:0; font:15px system-ui,sans-serif; background:#101216; color:#eef1f6; }
header { display:flex; justify-content:space-between; align-items:center; padding:14px 20px; background:#181c23; border-bottom:1px solid #343b48; }
main { display:grid; grid-template-columns:minmax(220px,28vw) 1fr; min-height:calc(100vh - 62px); }
aside { padding:16px; background:#171b22; border-right:1px solid #343b48; overflow:auto; } h2 { font-size:14px; text-transform:uppercase; letter-spacing:.08em; color:#aeb7c7; }
.master { width:100%; max-height:40vh; object-fit:contain; background:#0c0e12; cursor:zoom-in; } .refs { display:grid; grid-template-columns:repeat(3,1fr); gap:7px; } .refs img { width:100%; height:115px; object-fit:contain; background:#0c0e12; cursor:zoom-in; }
section { display:flex; flex-direction:column; min-width:0; } .candidate-meta { padding:14px 20px; display:flex; gap:22px; font-weight:700; } .candidate-wrap { flex:1; min-height:35vh; padding:6px 20px; display:flex; align-items:center; justify-content:center; }
#candidate { max-width:100%; max-height:calc(100vh - 410px); object-fit:contain; cursor:zoom-in; } .controls { padding:15px 20px; border-top:1px solid #343b48; background:#181c23; }
.metric { display:grid; grid-template-columns:145px repeat(5,minmax(40px,1fr)); gap:5px; align-items:center; margin:6px 0; } .metric strong { color:#cdd5e1; } button { border:1px solid #465065; border-radius:5px; background:#272e3a; color:#f4f6fa; padding:8px 10px; cursor:pointer; } button:hover { background:#39445a; } button.selected { background:#266f59; outline:2px solid #78dfbc; } button.active { border-color:#80a8ff; } button:disabled { opacity:.45; cursor:default; }
.actions { display:flex; align-items:center; gap:8px; margin-top:12px; } .primary { background:#236747; font-weight:700; } textarea { width:100%; box-sizing:border-box; margin-top:10px; background:#11151d; color:#eef1f6; border:1px solid #465065; border-radius:5px; padding:8px; min-height:55px; } #status { margin-left:auto; color:#aeb7c7; } .help { color:#aeb7c7; font-size:12px; margin-top:8px; }
#modal { display:none; position:fixed; inset:0; background:#000d; z-index:10; align-items:center; justify-content:center; padding:24px; } #modal img { max-width:96vw; max-height:94vh; object-fit:contain; } .complete { display:none; text-align:center; margin:auto; font-size:20px; }
</style></head><body><header><strong>ONYX — Blind Review v1</strong><span id="progress">Reviewed: 0 / 36</span></header><main>
<aside><h2>Identity reference</h2><p>Master</p><img id="master" class="master" src="/api/reference/master" alt="P01 master" onclick="zoom(this.src)"><p>References</p><div class="refs">{% for index in range(3) %}<img src="/api/reference/ref/{{index}}" alt="P01 reference {{index + 1}}" onclick="zoom(this.src)">{% endfor %}</div></aside>
<section><div id="review"><div class="candidate-meta"><span id="scene">Scene: —</span><span id="label">Candidate: —</span></div><div class="candidate-wrap"><img id="candidate" alt="Blind candidate" onclick="zoom(this.src)"></div><div class="controls"><div id="metrics"></div><textarea id="comment" maxlength="2000" placeholder="Comment (optional)"></textarea><div class="actions"><button onclick="previous()">← Previous</button><button onclick="skip()">Skip</button><button class="primary" id="save" onclick="saveNext()">Save &amp; Next</button><span id="status"></span></div><div class="help">Выберите метрику кликом по её строке, затем 1–5. I/R/S/C выбирают Identity/Realism/Scene/Commercial. Enter = Save &amp; Next.</div></div></div>
<div id="complete" class="complete"><p>Blind review complete: 36 / 36</p><p>Mapping остаётся скрытым.</p><button class="primary" onclick="finishReview()">Finish review</button><p id="finish-status" class="help"></p></div></section></main><div id="modal" onclick="this.style.display='none'"><img id="modal-image" alt="Enlarged image"></div>
<script>
const metrics = [{key:'identity_score',label:'Identity'},{key:'realism_score',label:'Realism'},{key:'scene_score',label:'Scene / Anatomy'},{key:'commercial_score',label:'Commercial Quality'}];
const verdicts=['PASS','REPAIR','REGENERATE','REJECT']; let position=0, item=null, active='identity_score';
function zoom(src){ document.getElementById('modal-image').src=src; document.getElementById('modal').style.display='flex'; }
function renderMetrics(){ const root=document.getElementById('metrics'); root.innerHTML=''; for(const metric of metrics){const row=document.createElement('div');row.className='metric'; const title=document.createElement('strong');title.textContent=metric.label; title.onclick=()=>{active=metric.key;renderMetrics()}; row.append(title); for(let value=1;value<=5;value++){const b=document.createElement('button');b.textContent=value;b.className=(item.scores[metric.key]===value?'selected ':'')+(active===metric.key?'active':'');b.onclick=()=>{item.scores[metric.key]=value;active=metric.key;renderMetrics()};row.append(b)}root.append(row)} const verdict=document.createElement('div'); verdict.className='metric';const label=document.createElement('strong');label.textContent='Overall verdict';verdict.append(label);for(const value of verdicts){const b=document.createElement('button');b.textContent=value;b.className=item.verdict===value?'selected':'';b.onclick=()=>{item.verdict=value;renderMetrics()};verdict.append(b)}root.append(verdict) }
async function load(pos){const response=await fetch('/api/item/'+pos);const data=await response.json(); if(data.finished){document.getElementById('review').style.display='none';document.getElementById('complete').style.display='block';await progress();return}position=data.position;item=data;document.getElementById('review').style.display='block';document.getElementById('complete').style.display='none';document.getElementById('scene').textContent='Scene: '+item.scene;document.getElementById('label').textContent='Candidate: '+item.candidate_label;document.getElementById('candidate').src='/api/candidate/'+encodeURIComponent(item.candidate_id)+'?v='+Date.now();document.getElementById('comment').value=item.comment||'';renderMetrics();await progress()}
async function progress(){const data=await (await fetch('/api/progress')).json();document.getElementById('progress').textContent='Reviewed: '+data.reviewed+' / '+data.total}
function previous(){if(position>0)load(position-1)} function skip(){load(position+1)}
async function saveNext(){if(!metrics.every(metric=>Number.isInteger(item.scores[metric.key]))||!item.verdict){document.getElementById('status').textContent='Заполните четыре оценки и verdict.';return}const response=await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({candidate_id:item.candidate_id,...item.scores,verdict:item.verdict,comment:document.getElementById('comment').value})});const data=await response.json();document.getElementById('status').textContent=data.ok?'Сохранено.':data.error||'Ошибка сохранения.';if(data.ok)load(position+1)}
async function finishReview(){const response=await fetch('/api/finish',{method:'POST'});const data=await response.json();document.getElementById('finish-status').textContent=data.ok?'Review marked finished. Mapping не раскрыт.':data.error}
document.addEventListener('keydown',event=>{if(event.target.tagName==='TEXTAREA')return;const key=event.key.toLowerCase();const selectors={i:'identity_score',r:'realism_score',s:'scene_score',c:'commercial_score'};if(selectors[key]){active=selectors[key];renderMetrics()}else if(/^[1-5]$/.test(key)&&item){item.scores[active]=Number(key);renderMetrics()}else if(event.key==='Enter'){event.preventDefault();saveNext()}else if(event.key==='ArrowLeft'){previous()}});load(0);
</script></body></html>"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReviewStore:
    def __init__(self, root: Path):
        self.root, self.lock = root, threading.Lock()
        self.config = json.loads((root / "review_config.json").read_text(encoding="utf-8-sig"))
        self.mapping = json.loads((root / "blind_mapping.json").read_text(encoding="utf-8-sig"))
        self.scores_path, self.state_path = root / "blind_review_scores.csv", root / "review_state.json"
        self.order = self.config["review_order"]
        self.public = {record["candidate_id"]: record for record in self.order}
        if len(self.public) != 36:
            raise ValueError("review order must contain 36 unique candidate IDs")
        self.rows = self._read_rows()
        if set(self.rows) != set(self.public):
            raise ValueError("scores do not match the immutable review order")

    def _read_rows(self) -> dict[str, dict[str, str]]:
        with self.scores_path.open(encoding="utf-8-sig", newline="") as stream:
            return {row["candidate_id"]: row for row in csv.DictReader(stream)}

    def _write_rows(self) -> None:
        temporary = self.scores_path.with_suffix(".writing.csv")
        with temporary.open("w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.DictWriter(stream, fieldnames=SCORE_COLUMNS)
            writer.writeheader()
            for candidate in self.order:
                writer.writerow(self.rows[candidate["candidate_id"]])
        os.replace(temporary, self.scores_path)

    @staticmethod
    def complete(row: dict[str, str]) -> bool:
        return all(str(row.get(key, "")).strip() for key in (*SCORE_FIELDS, "verdict", "reviewed_at"))

    def asset(self, candidate_id: str) -> Path:
        record = self.public[candidate_id]
        letter = candidate_id.rsplit("-", 1)[1]
        participant = self.mapping["mapping"][record["scene"]][letter]
        return Path(self.mapping["participants"][participant]["source"][record["scene"]])

    def item(self, position: int) -> dict[str, Any]:
        if position >= len(self.order):
            return {"finished": True}
        position = max(0, position)
        public = self.order[position]
        row = self.rows[public["candidate_id"]]
        scores = {key: int(row[key]) if row.get(key, "").strip() else None for key in SCORE_FIELDS}
        return {"finished": False, "position": position, "scene": public["scene"], "candidate_id": public["candidate_id"], "candidate_label": public["candidate_id"].rsplit("-", 1)[1], "scores": scores, "verdict": row.get("verdict") or None, "comment": row.get("comment") or "", "complete": self.complete(row)}

    def progress(self) -> dict[str, int]:
        return {"reviewed": sum(self.complete(row) for row in self.rows.values()), "total": len(self.order)}

    def save(self, payload: dict[str, Any]) -> None:
        candidate_id = str(payload.get("candidate_id", ""))
        if candidate_id not in self.public:
            raise ValueError("unknown candidate")
        if self.finished():
            raise ValueError("review is already finished")
        values = {key: int(payload[key]) for key in SCORE_FIELDS}
        if any(value not in {1, 2, 3, 4, 5} for value in values.values()):
            raise ValueError("scores must be integers from 1 to 5")
        verdict = str(payload.get("verdict", "")).upper()
        if verdict not in VERDICTS:
            raise ValueError("invalid verdict")
        comment = str(payload.get("comment", "")).strip()
        if len(comment) > 2000:
            raise ValueError("comment is too long")
        with self.lock:
            row = self.rows[candidate_id]
            row.update({key: str(value) for key, value in values.items()})
            row.update({"verdict": verdict, "comment": comment, "reviewed_at": now()})
            self._write_rows()
            self.rows = self._read_rows()

    def finished(self) -> bool:
        return self.state_path.is_file() and bool(json.loads(self.state_path.read_text(encoding="utf-8-sig")).get("finished_at"))

    def finish(self) -> None:
        if self.progress()["reviewed"] != len(self.order):
            raise ValueError("all 36 candidates must be reviewed before finish")
        temporary = self.state_path.with_suffix(".writing.json")
        temporary.write_text(json.dumps({"review_id": self.config["review_id"], "finished_at": now()}, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, self.state_path)


def create_app(root: Path) -> Flask:
    store = ReviewStore(root)
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        return render_template_string(HTML)

    @app.get("/api/reference/master")
    def master():
        return send_file(store.config["references"]["master"])

    @app.get("/api/reference/ref/<int:index>")
    def reference(index: int):
        references = store.config["references"]["references"]
        if index not in range(len(references)):
            abort(404)
        return send_file(references[index])

    @app.get("/api/candidate/<candidate_id>")
    def candidate(candidate_id: str):
        if candidate_id not in store.public:
            abort(404)
        return send_file(store.asset(candidate_id))

    @app.get("/api/item/<int:position>")
    def item(position: int):
        return jsonify(store.item(position))

    @app.get("/api/progress")
    def progress():
        return jsonify(store.progress())

    @app.post("/api/save")
    def save():
        try:
            store.save(request.get_json(force=True))
            return jsonify({"ok": True, **store.progress()})
        except Exception as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400

    @app.post("/api/finish")
    def finish():
        try:
            store.finish()
            return jsonify({"ok": True})
        except Exception as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400

    return app


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    create_app(args.root.resolve()).run(host=args.host, port=args.port, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
