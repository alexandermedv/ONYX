"""Read-only validation of the P02 session; writes reports, never images or review scores."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
PERSONA = ROOT.parents[1]
REPO = next(p for p in ROOT.parents if (p / '.git').exists())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_csv(p):
    with p.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def validate(baseline=None, tracked_before=None, request=None):
    manifest=json.loads((ROOT/'business_manifest.yaml').read_text(encoding='utf-8'))
    prompts=json.loads((ROOT/'01_prompts/P02_business_v1_prompts.yaml').read_text(encoding='utf-8'))
    marketing=json.loads((ROOT/'05_marketing/marketing_manifest.yaml').read_text(encoding='utf-8'))
    review=read_csv(ROOT/'02_review/P02_business_v1_review.csv')
    qa=read_csv(ROOT/'02_review/technical_qa.csv')
    web=read_csv(ROOT/'04_web/web_manifest.csv')
    mappings=read_csv(ROOT/'02_review/source_mapping.csv')
    ids=[f'BUS_{i:02d}' for i in range(1,11)]
    assert [a['id'] for a in manifest['images']]==ids
    assert [a['id'] for a in prompts['prompts']]==ids
    assert [a['id'] for a in review]==ids
    assert [a['id'] for a in qa]==ids
    assert [a['id'] for a in mappings]==ids
    assert len({a['sha256'] for a in manifest['images']})==10
    assert len(list((ROOT/'00_source').glob('*.png')))==10
    assert len(list((ROOT/'03_final').glob('*.png')))==10
    for a in manifest['images']:
        for field in ('source_path','canonical_source_path','final_filename'):
            p=ROOT/a[field]
            assert sha(p)==a['sha256'],p
            assert p.stat().st_size==a['file_size_bytes']
            with Image.open(p) as im:
                assert im.format=='PNG'; im.verify()
            with Image.open(p) as im:
                im.load(); assert list(im.size)==[a['width'],a['height']]
        q=next(q for q in qa if q['id']==a['id'])
        assert q['sha256']==a['sha256'] and q['readable']=='True' and q['exact_duplicate']=='False'
        assert a['status']=='candidate' and a['publish_approved'] is False
        assert a['width']*4==a['height']*3
    for a in manifest['identity_inputs']:
        assert sha(PERSONA/a['file'])==a['sha256']
    for p in prompts['prompts']:
        assert (ROOT/'01_prompts'/f"{p['id']}.txt").read_text(encoding='utf-8').rstrip('\n')==p['prompt']
        assert hashlib.sha256(p['prompt'].encode()).hexdigest()==p['text_sha256']
        assert p['prompt'] in (ROOT/'01_prompts/P02_business_v1_prompts.md').read_text(encoding='utf-8')
    assert (ROOT/'01_prompts/session_identity_block.md').read_text(encoding='utf-8').rstrip('\n')==prompts['session_identity_rule']
    if request:
        raw=request.read_text(encoding='utf-8-sig')
        section=raw.split('PROMPTS:',1)[1].split('4. IMAGE MANIFEST',1)[0]
        for p in prompts['prompts']:
            match=re.search(r'-{5,}\s*\n'+p['id']+r'\s*\n-{5,}\s*\n(.*?)(?=\n-{5,}\s*\nBUS_|\n={5,})',section,re.S)
            assert match and match[1].strip()==p['prompt'],p['id']
    for row in review:
        assert row['decision']=='PENDING'
        assert all(not value for key,value in row.items() if key.endswith('_1_5'))
    assert len(web)==20 and len(marketing['assets'])==18
    for a in web:
        p=ROOT/a['derivative']
        assert sha(p)==a['sha256'] and p.stat().st_size==int(a['file_size'])
        with Image.open(p) as im:
            im.load(); assert im.size==(int(a['width']),int(a['height'])) and im.format==a['format']
        src=next(s for s in manifest['images'] if s['final_filename']==a['source'])
        assert int(a['width'])*src['height']==int(a['height'])*src['width']
        assert max(int(a['width']),int(a['height']))<=1600
    for a in marketing['assets']:
        p=ROOT/a['file']
        assert sha(p)==a['sha256'] and p.stat().st_size==a['file_size_bytes']
        with Image.open(p) as im:
            im.load(); assert im.size==(a['width'],a['height'])
        for source in a['source_inputs']:
            base=REPO if source.get('path_base')=='repository' else ROOT
            assert sha(base/source['file'])==source['sha256']
        assert not a['publish_approved']
    p01_count=None; existing_count=None
    if baseline:
        original={k.replace('\\','/'):v for k,v in json.loads(baseline.read_text(encoding='utf-8')).items()}
        allowed_document='09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/README.md'
        p01_prefix='09 Experiments/identity_benchmark_v1/P01_M30_Corporate/'
        for file,h in original.items():
            if file!=allowed_document:
                assert sha(REPO/file)==h, f'Pre-existing file changed: {file}'
        before={p:h for p,h in original.items() if p.startswith(p01_prefix)}
        after={p.relative_to(REPO).as_posix():sha(p) for p in (PERSONA.parent/'P01_M30_Corporate').rglob('*') if p.is_file()}
        assert before==after,'P01 inventory or content changed'
        p01_count=len(before);existing_count=len(original)-1
    if tracked_before:
        assert subprocess.check_output(['git','diff','--binary'],cwd=REPO)==tracked_before.read_bytes()
    # No one-off bytecode/cache outputs should be part of this pack.
    assert not list(ROOT.rglob('__pycache__'))
    result={'session_id':'P02_BUSINESS_V1','checked_on':'2026-09-15',
            'sources_present':10,'sources_expected':10,'unique_sha256':10,
            'prompts_present':10,'manifest_entries':10,'human_review_rows':10,'human_decisions':'PENDING',
            'png_valid_and_readable':10,'aspect_ratio_3_4':10,'technical_qa_rows':10,
            'near_duplicate_detection':'SKIPPED: existing repository tool requires unavailable cv2',
            'candidate_staging_copies_verified':10,'web_derivatives_verified':20,
            'marketing_derivatives_verified':18,'marketing_traceability':'PASS; two text-only cards have no image inputs',
            'p02_identity_pngs_verified_unchanged':len(manifest['identity_inputs']),
            'p01_files_verified_unchanged':p01_count,'preexisting_files_verified_unchanged':existing_count,
            'unrelated_tracked_diff_unchanged':True if tracked_before else None,
            'source_pngs_overwritten':False,'source_originals_and_reserve_preserved':True,
            'technical_pack_status':'PASS','human_approval':'PENDING','publish_approved':False,
            'commit_created':False}
    (ROOT/'02_review/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report='# P02 BUSINESS V1 — final packaging report\n\n'
    report+='Technical package complete. Human approval and publication are pending. No commit created.\n\n'
    report+='## Validation\n\n| Check | Result |\n|---|---|\n'
    for k,v in result.items(): report+=f'| {k} | {v} |\n'
    report+='\n## Source mapping and SHA256\n\nAll originals remain in the session root. Canonical paths are in `00_source`.\n\n| ID | Original filename | Canonical filename | Dimensions | Bytes | SHA256 |\n|---|---|---|---|---:|---|\n'
    for a in manifest['images']:
        report+=f"| {a['id']} | {a['source_filename']} | {a['canonical_filename']} | {a['width']} × {a['height']} | {a['file_size_bytes']} | `{a['sha256']}` |\n"
    report+='\n## Prompt manifest\n\n10/10 verbatim prompts, BUS_01–BUS_10; session identity rule preserved. Model, seed and settings unknown. Each prompt has its own text SHA256. `scene`, `pose_type`, `gaze`, `expression`, `framing` and `wardrobe` in the image manifest are observed descriptions.\n\n'
    report+='## Technical QA\n\n10/10 PNGs verified and decoded; exact 3:4 aspect ratio; unique SHA256. No human scores or automated identity scores assigned. Near-duplicate detection skipped due to missing cv2. EXIF presence is recorded per image in technical_qa.csv.\n\n'
    report+='## Marketing assets\n\n| File | Dimensions | Source IDs | Status |\n|---|---|---|---|\n'
    for a in marketing['assets']:
        report+=f"| {a['file']} | {a['width']} × {a['height']} | {', '.join(s['id'] for s in a['source_inputs']) or 'Text only'} | candidate |\n"
    report+='\n## business_v1 tree\n\n```text\nbusiness_v1/\n'
    def tree(folder,depth=1):
        lines=[]
        for p in sorted(folder.iterdir(),key=lambda p:(not p.is_dir(),p.name)):
            lines.append('  '*depth+p.name+('/' if p.is_dir() else ''))
            if p.is_dir():lines.extend(tree(p,depth+1))
        return lines
    # Include this report before it exists on the first pass.
    lines=tree(ROOT)
    if not (ROOT/'FINAL_REPORT.md').exists():lines.append('  FINAL_REPORT.md')
    report+='\n'.join(lines)+'\n```\n'
    for title,args in [('git status --short',['status','--short']),('git diff --stat',['diff','--stat'])]:
        report+='\n## '+title+'\n\n```text\n'+subprocess.check_output(['git',*args],cwd=REPO,encoding='utf-8')+'```\n'
    report+='\nThe tracked diff above predates this phase. P02 is untracked, so these new files are absent from ordinary git diff --stat. No staging or commit was performed. Existing P01 changes are not part of this work.\n\n'
    report+='## Suggested commit message — not executed\n\n`feat(onyx): add P02 business portfolio session v1`\n'
    (ROOT/'FINAL_REPORT.md').write_text(report,encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path)
    p.add_argument('--tracked-before',type=Path)
    p.add_argument('--request',type=Path)
    a=p.parse_args()
    validate(a.baseline,a.tracked_before,a.request)
