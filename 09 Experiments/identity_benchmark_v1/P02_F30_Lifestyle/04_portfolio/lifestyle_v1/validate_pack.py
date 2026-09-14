"""Validate lifestyle packaging and parallel business publishing exports.

Only writes lifestyle validation/final report. Does not modify historical business
reports, review decisions, sources or manifests.
"""
import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parent
BUSINESS=ROOT.parent/'business_v1'
PERSONA=ROOT.parents[1]
REPO=next(p for p in ROOT.parents if (p/'.git').exists())
FORBIDDEN=['test character','demo character','demonstration character','awaiting review',
           'pending review','candidate','review copy','internal review','review pending',
           'ожидает ревью','ожидает review','тестовый персонаж','демо-персонаж',
           'демонстрационный персонаж','внутренний макет','реальный клиент','real client']


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def rows(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))


def validate(baseline,tracked_before,request):
    manifest=load(ROOT/'lifestyle_manifest.yaml');images=manifest['images']
    prompts=load(ROOT/'01_prompts/P02_lifestyle_v1_prompts.yaml')
    review=rows(ROOT/'02_review/P02_lifestyle_v1_review.csv')
    qa=rows(ROOT/'02_review/technical_qa.csv');web=rows(ROOT/'04_web/web_manifest.csv')
    mapping=rows(ROOT/'02_review/source_mapping.csv')
    ids=[f'LIFE_{i:02d}' for i in range(1,11)]
    for sequence in (images,prompts['prompts'],review,qa,mapping):assert [a['id'] for a in sequence]==ids
    assert len({a['sha256'] for a in images})==10
    assert len(list((ROOT/'00_source').glob('*.png')))==10
    assert len(list((ROOT/'03_final').glob('*.png')))==10
    for a,q in zip(images,qa):
        for key in ('source_path','canonical_source_path','final_filename'):
            p=ROOT/a[key];assert sha(p)==a['sha256'];assert p.stat().st_size==a['file_size_bytes']
            with Image.open(p) as im:assert im.format=='PNG';im.verify()
            with Image.open(p) as im:
                im.load();assert im.size==(a['width'],a['height'])
                assert str(bool(im.getexif()))==q['exif_present']
        assert a['width']*4==a['height']*3
        assert q['sha256']==a['sha256'] and q['readable']=='True' and q['png_valid']=='True' and q['exact_duplicate']=='False'
        assert a['status']=='finalized_candidate_set' and a['human_decision']=='PENDING'
    assert manifest['portfolio_status']=='finalized_candidate_set' and manifest['human_review_status']=='PENDING'
    assert images[9]['source_filename']=='10.png' and images[9]['canonical_filename']=='P02_LIFE_10_evening_city.png'
    assert manifest['noncanonical'][0]['reason']=='superseded_by_evening_city_replacement'
    assert manifest['noncanonical'][0]['file'] is None
    for a in manifest['identity_inputs']:assert sha(PERSONA/a['path'])==a['sha256']
    supplied=request.read_text(encoding='utf-8-sig')
    rule=supplied.split('Сохранить session-level rule:',1)[1].split('Сохранить все 10 prompts.',1)[0].strip()
    assert rule==prompts['session_identity_rule']
    assert (ROOT/'01_prompts/session_identity_block.md').read_text(encoding='utf-8').rstrip('\n')==rule
    md=(ROOT/'01_prompts/P02_lifestyle_v1_prompts.md').read_text(encoding='utf-8')
    for a in prompts['prompts']:
        assert a['prompt'] in supplied and a['prompt'] in md
        assert (ROOT/'01_prompts'/f"{a['id']}.txt").read_text(encoding='utf-8').rstrip('\n')==a['prompt']
        assert hashlib.sha256(a['prompt'].encode()).hexdigest()==a['text_sha256']
    for a in review:
        assert a['decision']=='PENDING'
        assert all(not value for key,value in a.items() if key not in ('id','filename','decision'))
    assert len(web)==20
    for a in web:
        p=ROOT/a['derivative'];assert sha(p)==a['sha256'] and p.stat().st_size==int(a['file_size'])
        with Image.open(p) as im:
            im.load();assert im.size==(int(a['width']),int(a['height'])) and im.format==a['format']
        src=next(s for s in images if s['final_filename']==a['source'])
        assert int(a['width'])*src['height']==int(a['height'])*src['width']
        assert max(int(a['width']),int(a['height']))<=1600
    public={}
    for root,filename in [(ROOT,'marketing_manifest.yaml'),(BUSINESS,'publishing_manifest.yaml')]:
        pack=load(root/'05_marketing'/filename);assert len(pack['assets'])==18 and len(pack['copy'])==4
        for a in pack['assets']:
            p=root/a['file'];assert sha(p)==a['sha256'] and p.stat().st_size==a['file_size_bytes']
            with Image.open(p) as im:im.load();assert im.size==(a['width'],a['height'])
            for source in a['source_inputs']:
                base=REPO if source['path_base']=='repository' else root
                assert sha(base/source['path'])==source['sha256']
            public_text='\n'.join(a['rendered_text']).casefold()
            assert not any(term in public_text for term in FORBIDDEN),a['file']
            if root==BUSINESS:assert p.stem.endswith('_publish')
        for a in pack['copy']:
            p=root/a['file'];assert sha(p)==a['sha256']
            value=p.read_text(encoding='utf-8');assert value==a['text']
            assert not any(term in value.casefold() for term in FORBIDDEN),a['file']
        public[root.name]=pack
    old={k.replace('\\','/'):v for k,v in load(baseline).items()}
    allowed=(PERSONA/'README.md').relative_to(REPO).as_posix()
    for name,h in old.items():
        if name!=allowed:assert sha(REPO/name)==h,f'Pre-existing file changed: {name}'
    p01prefix='09 Experiments/identity_benchmark_v1/P01_M30_Corporate/'
    expected={k:v for k,v in old.items() if k.startswith(p01prefix)}
    actual={p.relative_to(REPO).as_posix():sha(p) for p in (PERSONA.parent/'P01_M30_Corporate').rglob('*') if p.is_file()}
    assert expected==actual
    exclusion=':(exclude)09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/'
    assert subprocess.check_output(['git','diff','--binary','--','.',exclusion],cwd=REPO)==tracked_before.read_bytes()
    assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=REPO)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO).decode().strip()=='b3b761f6c899919c4f08d2981a750a914cb5182d'
    assert not list(ROOT.rglob('__pycache__'))
    result={
        'lifestyle_sources':'10/10','unique_sha256':'10/10','prompts':'10/10 verbatim',
        'manifest_entries':'10/10','review_rows':'10/10 PENDING; all scores blank',
        'technical_qa':'10/10 valid PNG, full decode OK, 3:4; EXIF recorded',
        'staging_copies':'10/10 byte-identical','web_derivatives':'20/20 verified',
        'lifestyle_marketing':'18 images + 4 copy files verified',
        'replacement_LIFE_10':'10.png visually confirmed as outdoor evening city; source/staging hashes verified',
        'old_office_LIFE_10':'Excluded; superseded history recorded; separate local file not identified',
        'business_public_exports':'18 images + 4 copy files verified; _publish preferred',
        'business_historical_files':'All pre-existing business files byte-identical, including reports/review/QA/manifests',
        'public_labels':'PASS: rendered text and copy denylist + visual layout inspection; no OCR claim',
        'P02_identity':'MASTER, REF01–05 and Collage.jpg unchanged; identity metadata unchanged',
        'P01':f'{len(expected)} files unchanged; same inventory',
        'unrelated_tracked_changes':'Byte-identical to before phase',
        'source_PNG_overwritten':False,'human_review_status':'PENDING',
        'near_duplicate_detection':'SKIPPED: existing detector requires unavailable cv2',
        'commit_created':False,'push_performed':False,
    }
    (ROOT/'02_review/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report='# P02 Lifestyle V1 + business public exports — final report\n\n'
    report+='Package prepared without commit or push. Public presentation is clean; internal review remains PENDING.\n\n## Validation\n\n| Check | Result |\n|---|---|\n'
    for k,v in result.items():report+=f'| {k} | {v} |\n'
    report+='\n## Source mapping / SHA256\n\nRoot originals → 00_source canonical copies; all originals preserved.\n\n| ID | Original | Canonical | Dimensions | Bytes | SHA256 |\n|---|---|---|---|---:|---|\n'
    for a in images:report+=f"| {a['id']} | {a['source_filename']} | {a['canonical_filename']} | {a['width']} × {a['height']} | {a['file_size_bytes']} | `{a['sha256']}` |\n"
    report+='\n## LIFE_10 replacement\n\n10.png is the true evening-city image, selected by visual scene inspection and copied without edits. The earlier office-like attempt is superseded according to user history; no local path was identified. It is not in the canonical ten.\n\n'
    report+='## Prompts and technical QA\n\nTen verbatim supplied prompts plus session identity rule, saved in Markdown/YAML and individual text files. Exact replacement execution prompt, generation model/seed remain unknown. PNG CRC and full decoding pass; exact hashes are unique, dimensions/EXIF recorded in technical_qa.csv. No human scores assigned.\n'
    for name,pack in public.items():
        report+='\n## '+name+' public assets\n\n| File | Dimensions | Source IDs |\n|---|---|---|\n'
        for a in pack['assets']:report+=f"| {a['file']} | {a['width']} × {a['height']} | {', '.join(s['id'] for s in a['source_inputs']) or 'Text only'} |\n"
        report+='\nCopy files:\n\n'+''.join('- '+a['file']+'\n' for a in pack['copy'])
    report+='\n## lifestyle_v1 tree\n\n```text\nlifestyle_v1/\n'
    def tree(folder,depth=1):
        lines=[]
        for p in sorted(folder.iterdir(),key=lambda p:(not p.is_dir(),p.name)):
            lines.append('  '*depth+p.name+('/' if p.is_dir() else ''))
            if p.is_dir():lines.extend(tree(p,depth+1))
        return lines
    lines=tree(ROOT)
    if not (ROOT/'FINAL_REPORT.md').exists():lines.append('  FINAL_REPORT.md')
    report+='\n'.join(lines)+'\n```\n'
    for title,args in [('git status --short',['status','--short']),('git diff --stat',['diff','--stat'])]:
        report+='\n## '+title+'\n\n```text\n'+subprocess.check_output(['git',*args],cwd=REPO,encoding='utf-8')+'```\n'
    report+='\nNew lifestyle/public exports are untracked, so ordinary git diff --stat does not include them. The only changed existing P02 file is its README, updated to link the new packages. Existing business records remain byte-identical.\n\n## Suggested commit message — not executed\n\n`feat(onyx): add P02 lifestyle portfolio session v1 and publish-ready business materials`\n'
    (ROOT/'FINAL_REPORT.md').write_text(report,encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,required=True);p.add_argument('--tracked-before',type=Path,required=True)
    p.add_argument('--request',type=Path,required=True);a=p.parse_args()
    validate(a.baseline,a.tracked_before,a.request)
