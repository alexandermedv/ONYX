"""Materialize reproducible identity metadata for the P03 canonical asset set."""
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parent
items=[
 ('approved_collage','02_source_generations/P03_approved_character_collage_v1.png','approved visual source for identity'),
 ('MASTER','00_master/P03_identity_master_v1.png','primary canonical identity anchor'),
 ('REF01','01_references/P03_REF01.png','frontal, face-focused clean identity reference'),
 ('REF02','01_references/P03_REF02.png','three-quarter alternate head geometry reference'),
 ('REF03','01_references/P03_REF03.png','distant body-proportions reference'),
 ('REF04','01_references/P03_REF04.png','alternate pose and styling reference'),
 ('REF05','01_references/P03_REF05.png','diversity reference with alternate wardrobe and framing'),
]
assets=[]
for role,rel,semantic in items:
 p=ROOT/rel
 with Image.open(p) as im: im.load(); w,h=im.size
 assets.append({'role':role,'path':rel,'semantic':semantic,'width':w,'height':h,'file_size_bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={'character_id':'P03_M45_Executive','identity_version':1,'status':'frozen','canonical_assets':assets,'noncanonical_attempts':[],'validation':{'canonical_assets_present':len(assets),'canonical_assets_expected':7,'all_expected_canonical_assets_exist':len(assets)==7,'hashes_recorded':True,'dimensions_recorded':True}}
def write(rel,obj): (ROOT/rel).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('identity_manifest.yaml',manifest)
write('00_master/master_metadata.yaml',{'character_id':'P03_M45_Executive','identity_version':1,'status':'frozen','asset':assets[1],'provenance':'Generated from the approved P03 character collage using the built-in ImageGen backend; visually reviewed before identity freeze.'})
write('01_references/references_metadata.yaml',{'character_id':'P03_M45_Executive','identity_version':1,'status':'frozen','references':assets[2:],'provenance':'Each reference was generated from the approved P03 character collage, visually reviewed, and saved under its canonical filename.'})
(ROOT/'README.md').write_text('# P03 M45 Executive\n\nP03 is a synthetic 45–48 year old European executive character for ONYX leadership, business and premium lifestyle portfolios. Identity v1 is frozen: use the approved collage, MASTER and REF01–REF05 only as identity references, never as poses or scene templates. P01 and P02 are independent portfolio characters.\n\nCanonical identity assets are documented in `identity_manifest.yaml`. Earlier failed attempts, if any, are non-canonical.\n',encoding='utf-8')
(ROOT/'02_source_generations/README.md').write_text('# Approved source generation\n\n`P03_approved_character_collage_v1.png` is the approved visual source from which P03 identity v1 was established. It is a synthetic four-panel concept board and is not a canonical reference replacement.\n',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
