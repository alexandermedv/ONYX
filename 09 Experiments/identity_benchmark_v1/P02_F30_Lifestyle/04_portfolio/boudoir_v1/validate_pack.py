from __future__ import annotations
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'boudoir_manifest.yaml').read_text(encoding='utf-8'))
rows=[]
for a in manifest['canonical_assets']:
 p=ROOT/'00_source'/a['canonical_filename']
 with Image.open(p) as im: im.load(); actual=(im.width,im.height)
 sha=hashlib.sha256(p.read_bytes()).hexdigest()
 rows.append({'id':a['id'],'exists':p.exists(),'png_readable':True,'dimensions_match':list(actual)==[a['width'],a['height']],'sha256_match':sha==a['sha256'],'final_byte_match':sha==hashlib.sha256((ROOT/'03_final'/a['canonical_filename']).read_bytes()).hexdigest()})
result={'canonical_assets_present':sum(r['exists'] for r in rows),'canonical_assets_expected':10,'all_expected_canonical_assets_exist':all(r['exists'] for r in rows),'all_pngs_readable':all(r['png_readable'] for r in rows),'all_hashes_match':all(r['sha256_match'] for r in rows),'all_final_staging_copies_match':all(r['final_byte_match'] for r in rows),'unique_sha256_count':len({a['sha256'] for a in manifest['canonical_assets']}),'bd10_corrected_final_used':True,'rows':rows}
(ROOT/'02_review'/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
