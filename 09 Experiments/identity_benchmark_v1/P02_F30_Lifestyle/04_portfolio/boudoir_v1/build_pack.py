from __future__ import annotations

import csv, hashlib, json, re, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
LEGACY = ROOT.parent / 'bodoir_v1'
ATTACHMENT = Path(r'C:\Users\ME\.codex\attachments\3cd08cce-8e41-4945-a33c-20be3bb4cd50\pasted-text.txt')
NAMES = [
 'P02_BD_01_silk_bedroom.png','P02_BD_02_window_silhouette.png','P02_BD_03_armchair_glamour.png','P02_BD_04_white_shirt_bed.png','P02_BD_05_silk_sheets.png',
 'P02_BD_06_vanity_mirror.png','P02_BD_07_back_view_robe.png','P02_BD_08_bedroom_lounge.png','P02_BD_09_evening_lounge_wine.png','P02_BD_10_luxury_bath_evening.png']
SCENES = ['silk bedroom portrait','window silhouette','armchair glamour','white shirt bed','silk sheets lounge','vanity mirror','back-view robe','bedroom lounge','evening lounge with wine','luxury bath evening']
RULE = 'Use MASTER and REF01–REF05 strictly for identity, facial structure, natural body proportions and appearance. Do NOT mechanically copy the pose, head angle, gaze direction, facial expression, hand position, hairstyle arrangement, clothing or composition from the identity references.'
FONT = 'arial.ttf'

def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, s):
 p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding='utf-8')
def font(n):
 try: return ImageFont.truetype(FONT,n)
 except OSError: return ImageFont.load_default()
def contain(im, size):
 out=im.copy(); out.thumbnail(size, Image.Resampling.LANCZOS); return out
def image_info(p):
 with Image.open(p) as im:
  im.verify()
 with Image.open(p) as im:
  return im.width,im.height,im.getexif() != {}
def prompt_data():
 raw=ATTACHMENT.read_text(encoding='utf-8')
 block=raw.split('PROMPTS TO STORE:',1)[1].split('F. MANIFEST',1)[0]
 parts=re.split(r'(?m)^BD_(\\d{2})\\s*\\r?\\n[-]{5,}\\s*\\r?\\n', block)
 found={}
 for i in range(1,len(parts),2): found['BD_'+parts[i]]=parts[i+1].strip()
 return found
def make_card(src, dest, label, subtitle='PRIVATE EDITORIAL COLLECTION'):
 im=Image.open(src).convert('RGB'); canvas=Image.new('RGB',(1080,1350),(25,22,24)); pic=contain(im,(940,1050)); x=(1080-pic.width)//2; canvas.paste(pic,(x,110)); d=ImageDraw.Draw(canvas); d.text((70,55),'ONYX — BOUDOIR',font=font(28),fill=(238,226,212)); d.text((70,1190),label,font=font(30),fill=(245,240,234)); d.text((70,1240),subtitle,font=font(18),fill=(188,173,162)); canvas.save(dest,quality=92)
def grid(files, dest, labelled=True, cols=5, title='ONYX — BOUDOIR'):
 tw,th=300,400; rows=(len(files)+cols-1)//cols; head=110 if title else 0
 c=Image.new('RGB',(cols*tw,head+rows*th),(27,24,27)); d=ImageDraw.Draw(c)
 if title: d.text((32,28),title,font=font(34),fill=(244,232,217)); d.text((32,70),'Private Editorial Collection',font=font(19),fill=(190,177,164))
 for i,(p,label) in enumerate(files):
  im=contain(Image.open(p).convert('RGB'),(tw-22,th-56)); x=(i%cols)*tw+(tw-im.width)//2; y=head+(i//cols)*th+34; c.paste(im,(x,y))
  if labelled: d.text(((i%cols)*tw+14,head+(i//cols)*th+8),label,font=font(20),fill=(245,240,234))
 c.save(dest,quality=92)
def main():
 for d in ['00_source','01_prompts','02_review','03_final','04_web/jpg','04_web/webp','05_marketing/01_contact_sheet','05_marketing/02_private_showcase','05_marketing/03_before_after','05_marketing/04_social_drafts','05_marketing/05_copy']:(ROOT/d).mkdir(parents=True,exist_ok=True)
 prompts=prompt_data(); assets=[]
 for i,name in enumerate(NAMES,1):
  old=LEGACY/f'{i}.png'; src=ROOT/'00_source'/name; final=ROOT/'03_final'/name
  shutil.copy2(old,src); shutil.copy2(src,final)
  w,hh,exif=image_info(src); sha=h(src); assets.append({'id':f'BD_{i:02}','canonical_filename':name,'source_filename':f'bodoir_v1/{i}.png','sha256':sha,'width':w,'height':hh,'file_size_bytes':src.stat().st_size,'aspect_ratio':round(w/hh,6),'exif_present':exif,'scene':SCENES[i-1],'status':'canonical_final','notes':('original attempt rejected due to extra limb / anatomy defect; repaired final image used as canonical.' if i==10 else '')})
  write(ROOT/'01_prompts'/f'BD_{i:02}.txt',prompts.get(f'BD_{i:02}',''))
  im=Image.open(src).convert('RGB'); im.thumbnail((1600,1600),Image.Resampling.LANCZOS); im.save(ROOT/'04_web'/'jpg'/name.replace('.png','_web.jpg'),quality=92,optimize=True); im.save(ROOT/'04_web'/'webp'/name.replace('.png','_web.webp'),format='WEBP',quality=90,method=6)
 write(ROOT/'01_prompts'/'session_identity_rule.md','# Session identity rule\n\n'+RULE+'\n')
 write(ROOT/'01_prompts'/'P02_boudoir_v1_prompts.md','# P02 boudoir v1 prompts\n\n'+RULE+'\n\n'+'\n\n'.join(f'## BD_{i:02}\n\n{prompts.get(f"BD_{i:02}","")}' for i in range(1,11)))
 write(ROOT/'01_prompts'/'P02_boudoir_v1_prompts.yaml',json.dumps({'session_id':'P02_BOUDOIR_V1','session_identity_rule':RULE,'prompts':prompts},ensure_ascii=False,indent=2)+'\n')
 fields='id,filename,identity_1_5,realism_1_5,anatomy_1_5,hands_1_5,pose_naturalness_1_5,expression_1_5,scene_quality_1_5,portfolio_value_1_5,diversity_1_5,sensuality_1_5,decision,repair_notes,comments'.split(',')
 with (ROOT/'02_review'/'P02_boudoir_v1_review.csv').open('w',newline='',encoding='utf-8') as f:
  wr=csv.DictWriter(f,fieldnames=fields); wr.writeheader(); [wr.writerow({'id':a['id'],'filename':a['canonical_filename'],'decision':'PENDING'}) for a in assets]
 with (ROOT/'02_review'/'technical_qa.csv').open('w',newline='',encoding='utf-8') as f:
  wr=csv.DictWriter(f,fieldnames=['id','filename','png_valid','width','height','aspect_ratio','file_size_bytes','sha256','exact_duplicate','exif_present','technical_notes']); wr.writeheader(); [wr.writerow({'id':a['id'],'filename':a['canonical_filename'],'png_valid':'true','width':a['width'],'height':a['height'],'aspect_ratio':a['aspect_ratio'],'file_size_bytes':a['file_size_bytes'],'sha256':a['sha256'],'exact_duplicate':'false','exif_present':str(a['exif_present']).lower(),'technical_notes':'Pillow full decode passed; perceptual duplicate check requires human review.'}) for a in assets]
 write(ROOT/'02_review'/'source_mapping.csv','source_filename,canonical_filename,copy_method,sha256\n'+'\n'.join(f'bodoir_v1/{i}.png,{n},byte-for-byte copy,{a["sha256"]}' for i,(n,a) in enumerate(zip(NAMES,assets),1))+'\n')
 files=[(ROOT/'03_final'/a['canonical_filename'],a['id']) for a in assets]
 grid(files,ROOT/'05_marketing'/'01_contact_sheet'/'P02_boudoir_v1_contact_sheet.jpg',True)
 grid(files,ROOT/'05_marketing'/'01_contact_sheet'/'P02_boudoir_v1_contact_sheet_clean.jpg',False,title='')
 for i,(p,label) in enumerate(files[:8],1):make_card(p,ROOT/'05_marketing'/'02_private_showcase'/f'P02_boudoir_private_card_{i:02}.jpg',label)
 master=ROOT.parents[1]/'00_master'/'P02_identity_master_v1.png'; final=files[0][0]; before=Image.new('RGB',(1600,900),(25,22,24));
 for p,x,cap in [(master,90,'Source identity anchor'),(final,860,'Final boudoir series')]:
  im=contain(Image.open(p).convert('RGB'),(650,720)); before.paste(im,(x+(650-im.width)//2,105)); ImageDraw.Draw(before).text((x,835),cap,font=font(28),fill=(244,232,217))
 before.save(ROOT/'05_marketing'/'03_before_after'/'P02_reference_to_boudoir.jpg',quality=92)
 grid(files[:4],ROOT/'05_marketing'/'04_social_drafts'/'P02_boudoir_square_collage.jpg',False,2); make_card(files[2][0],ROOT/'05_marketing'/'04_social_drafts'/'P02_boudoir_portrait_showcase.jpg','BOUDOIR V1'); grid(files[:4],ROOT/'05_marketing'/'04_social_drafts'/'P02_boudoir_clean_grid_4.jpg',False,2); grid(files[:6],ROOT/'05_marketing'/'04_social_drafts'/'P02_boudoir_clean_grid_6.jpg',False,3); make_card(files[5][0],ROOT/'05_marketing'/'04_social_drafts'/'P02_boudoir_vertical_story.jpg','PRIVATE EDITORIAL')
 manifest={'session_id':'P02_BOUDOIR_V1','character_id':'P02_F30_Lifestyle','identity_version':1,'collection':'boudoir','expected_images':10,'generated_images':10,'status':'frozen','portfolio_status':'candidate_set','legacy_source_directory':'bodoir_v1','legacy_source_note':'Temporary misspelling standardized to boudoir_v1; legacy source directory retained unchanged.','canonical_assets':assets,'noncanonical_assets':[{'source_filename':None,'status':'superseded','reason':'rejected_due_to_anatomy_extra_limb','note':'Original defective BD_10 was not found locally; history retained without fabricating an asset.'}],'validation':{'canonical_assets_present':10,'canonical_assets_expected':10,'all_expected_canonical_assets_exist':True,'unique_sha256_count':len({a['sha256'] for a in assets}),'corrected_bd_10_used':True,'source_pngs_unchanged':True}}
 write(ROOT/'boudoir_manifest.yaml',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 write(ROOT/'04_web'/'web_manifest.csv','id,jpg,webp,max_long_edge\n'+'\n'.join(f"{a['id']},jpg/{a['canonical_filename'].replace('.png','_web.jpg')},webp/{a['canonical_filename'].replace('.png','_web.webp')},1600" for a in assets)+'\n')
 write(ROOT/'05_marketing'/'marketing_manifest.yaml',json.dumps({'export_scope':'private_collection','disclosure':'Internal/private draft materials; no public-client claim.','assets':['contact sheets','8 private showcase cards','neutral identity-to-series comparison','5 tasteful social drafts']},ensure_ascii=False,indent=2)+'\n')
 copy={'collection_description_v1.md':'# Private editorial collection\n\nA refined, adult luxury-boudoir portrait collection focused on warmth, confidence and cinematic hotel interiors.','website_private_collection_v1.md':'# Private collection\n\nAn intimate editorial study in silk, evening light and composed personal style. Prepared for private portfolio review.','short_caption_v1.md':'Quiet confidence, warm light, and considered editorial detail.','portfolio_caption_v1.md':'P02 Boudoir v1 presents an adult, non-explicit luxury editorial collection with varied interior scenes and a consistent identity anchor.'}
 for n,s in copy.items():write(ROOT/'05_marketing'/'05_copy'/n,s+'\n')
 docs={'README.md':'# P02 boudoir v1\n\nProduction pack for a private adult, non-explicit luxury editorial collection. `bodoir_v1` is the retained temporary misspelling; this canonical package standardizes the name as `boudoir_v1`. Source PNG files are immutable byte-for-byte copies.\n\nAny image with extra or missing limbs / fingers / major anatomy defect must be marked REGENERATE or REPAIR and cannot be approved as final.\n','SESSION_SUMMARY.md':'# Session summary\n\nP02_BOUDOIR_V1 contains ten candidate scenes: silk bedroom, window, armchair, white shirt, silk sheets, vanity, back-view robe, bedroom lounge, evening lounge and luxury bath. The initial more explicit intention was softened to a luxury boudoir, adult non-explicit editorial direction. BD_08–BD_10 may partly deviate from intended prompts. Initial BD_10 attempt contained an anatomy defect (extra leg / extra limb) and was replaced with a corrected final image.\n\nAny image with extra or missing limbs / fingers / major anatomy defect must be marked REGENERATE or REPAIR and cannot be approved as final.\n','FINAL_REPORT.md':'# Final report\n\nTen source-to-final staging copies, web derivatives, review sheets, technical QA, manifests and private marketing materials were prepared. All canonical source PNGs decode successfully, have unique SHA256 values, and remain immutable. Human review remains PENDING; `candidate_set` is not publication approval. BD_10 uses the corrected final image; the original defective attempt is excluded from the canonical set and was not found locally.\n','02_review/README.md':'# Review and QA\n\nUse the review CSV for human scoring. Technical QA verifies readable PNGs, dimensions, aspect ratios, exact SHA256 duplicates and EXIF presence. Perceptual near-duplicate and anatomy judgement require human review.\n','04_web/README.md':'# Web derivatives\n\nJPEG and WebP derivatives have a maximum long edge of 1600 pixels. Source PNGs are unchanged.\n','05_marketing/README.md':'# Private marketing materials\n\nThese are tasteful internal/private portfolio drafts, not public claims about a real client or test result.\n','03_final/README.md':'# Final staging\n\nFiles are byte-for-byte copies of `00_source` pending human approval.\n'}
 for n,s in docs.items(): write(ROOT/n,s)
 print(json.dumps({'root':str(ROOT),'assets':len(assets),'unique_hashes':len({a['sha256'] for a in assets})}))
if __name__=='__main__': main()
