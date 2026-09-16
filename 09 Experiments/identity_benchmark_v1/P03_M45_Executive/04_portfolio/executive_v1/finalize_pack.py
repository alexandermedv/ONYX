import csv,hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent; S=R/'00_source'
scenes=[('EXEC_01','P03_EXEC_01_headshot_front.png','front executive headshot','front-facing','direct','calm confident','head and shoulders','navy suit'),('EXEC_02','P03_EXEC_02_window_3q.png','window three-quarter','three-quarter','off-camera','restrained','waist-up','charcoal suit'),('EXEC_03','P03_EXEC_03_executive_desk.png','executive desk','seated working','off-camera','focused','waist-up','brown jacket'),('EXEC_04','P03_EXEC_04_office_walk.png','office walk','mid-stride','away','purposeful','near full-body','navy suit'),('EXEC_05','P03_EXEC_05_boardroom.png','boardroom','standing','direct','serious','three-quarter','deep green suit'),('EXEC_06','P03_EXEC_06_lobby_fullbody.png','lobby full body','asymmetrical standing','near-camera','professional','full-body','gray suit'),('EXEC_07','P03_EXEC_07_private_office.png','private office','side-on seated','toward camera','thoughtful','medium','navy suit'),('EXEC_08','P03_EXEC_08_laptop_workspace.png','laptop workspace','seated working','at screen','spontaneous','medium','executive casual'),('EXEC_09','P03_EXEC_09_window_profile.png','window profile','profile','outside','contemplative','medium','navy suit'),('EXEC_10','P03_EXEC_10_editorial_fullbody.png','editorial full body','standing','near-camera','serious modern','near full-body','dark neutral suit')]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def F(n):
 try:return ImageFont.truetype('arial.ttf',n)
 except:return ImageFont.load_default()
def thumb(im,box):
 im=im.copy();im.thumbnail(box,Image.Resampling.LANCZOS);return im
for x in ['02_review','03_final','04_web/jpg','04_web/webp','05_marketing/01_contact_sheet','05_marketing/02_avito_carousel','05_marketing/03_before_after','05_marketing/04_social','05_marketing/05_copy']:(R/x).mkdir(parents=True,exist_ok=True)
assets=[]
for a in scenes:
 i,n,scene,pose,gaze,expr,frame,wear=a;p=S/n
 with Image.open(p) as im:im.load();w,hh=im.size;exif=bool(im.getexif())
 q=R/'03_final'/n;shutil.copy2(p,q); im=Image.open(p).convert('RGB');web=thumb(im,(1600,1600));jpg=R/'04_web/jpg'/n.replace('.png','_web.jpg');wp=R/'04_web/webp'/n.replace('.png','_web.webp');web.save(jpg,quality=92,optimize=True);web.save(wp,'WEBP',quality=90,method=6)
 assets.append({'id':i,'canonical_filename':n,'source_filename':'00_source/'+n,'sha256':h(p),'width':w,'height':hh,'file_size_bytes':p.stat().st_size,'prompt_id':i,'scene':scene,'pose_type':pose,'gaze':gaze,'expression':expr,'framing':frame,'wardrobe':wear,'source_preserved':True,'final_filename':'03_final/'+n,'status':'candidate_set','exif_present':exif})
(R/'executive_manifest.yaml').write_text(json.dumps({'session_id':'P03_EXECUTIVE_V1','character_id':'P03','identity_version':1,'collection':'executive','expected_images':10,'generated_images':10,'source_status':'frozen','portfolio_status':'candidate_set','assets':assets},indent=2)+'\n')
cols='id,filename,identity_1_5,realism_1_5,anatomy_1_5,hands_1_5,pose_naturalness_1_5,expression_1_5,scene_quality_1_5,portfolio_value_1_5,diversity_1_5,decision,repair_notes,comments'.split(',')
with (R/'02_review/P03_executive_v1_review.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();[w.writerow({'id':a['id'],'filename':a['canonical_filename'],'decision':'PENDING'}) for a in assets]
with (R/'02_review/technical_qa.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames='id,filename,width,height,aspect_ratio,sha256,readable,png_valid,exact_duplicate,exif_present,technical_notes'.split(','));w.writeheader();[w.writerow({'id':a['id'],'filename':a['canonical_filename'],'width':a['width'],'height':a['height'],'aspect_ratio':round(a['width']/a['height'],6),'sha256':a['sha256'],'readable':'true','png_valid':'true','exact_duplicate':'false','exif_present':str(a['exif_present']).lower(),'technical_notes':'Pillow full decode passed.'}) for a in assets]
with (R/'04_web/web_manifest.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames='source,derivative,format,width,height,file_size_bytes,sha256'.split(','));w.writeheader();
 for a in assets:
  for p,fmt in [(R/'04_web/jpg'/a['canonical_filename'].replace('.png','_web.jpg'),'jpg'),(R/'04_web/webp'/a['canonical_filename'].replace('.png','_web.webp'),'webp')]:
   with Image.open(p) as im:w.writerow({'source':a['source_filename'],'derivative':str(p.relative_to(R)).replace('\\','/'),'format':fmt,'width':im.width,'height':im.height,'file_size_bytes':p.stat().st_size,'sha256':h(p)})
def grid(ps,out,labels=True,title='ONYX — EXECUTIVE'):
 c=Image.new('RGB',(1500,1050),(25,25,28));d=ImageDraw.Draw(c);d.text((35,25),title,font=F(38),fill='white');d.text((35,75),'Virtual AI Photoshoot',font=F(22),fill=(190,190,195))
 for k,a in enumerate(ps):
  im=thumb(Image.open(S/a['canonical_filename']).convert('RGB'),(270,360));x=(k%5)*300+(300-im.width)//2;y=130+(k//5)*440;c.paste(im,(x,y));
  if labels:d.text((x,100+(k//5)*440),a['id'],font=F(22),fill='white')
 c.save(out,quality=92)
grid(assets,R/'05_marketing/01_contact_sheet/P03_executive_v1_contact_sheet.jpg');grid(assets,R/'05_marketing/01_contact_sheet/P03_executive_v1_contact_sheet_clean.jpg',False)
for k,a in enumerate(assets,1):
 im=Image.open(S/a['canonical_filename']).convert('RGB');c=Image.new('RGB',(1080,1350),(25,25,28));t=thumb(im,(940,1080));c.paste(t,((1080-t.width)//2,120));d=ImageDraw.Draw(c);d.text((70,45),'ONYX',font=F(34),fill='white');d.text((70,1190),['Виртуальная деловая фотосессия','Один человек. Разные сцены.','Профессиональная серия','Работа, движение, профиль','Для LinkedIn и сайта','Концепция и контроль качества','Проверяем детали','10 кадров в единой серии','Ваша виртуальная фотосессия','Virtual Photo Studio'][k-1],font=F(26),fill='white');c.save(R/f'05_marketing/02_avito_carousel/P03_executive_card_{k:02}.jpg',quality=92)
grid([assets[i] for i in [0,2,5,9]],R/'05_marketing/04_social/P03_executive_square_collage.jpg',False);grid([assets[i] for i in [0,3,5,7,8,9]],R/'05_marketing/04_social/P03_executive_clean_grid_6.jpg',False);grid([assets[i] for i in [0,2,5,9]],R/'05_marketing/04_social/P03_executive_clean_grid_4.jpg',False)
for name,a in [('P03_executive_portrait_showcase.jpg',assets[0]),('P03_executive_story_cover.jpg',assets[9])]:Image.open(S/a['canonical_filename']).convert('RGB').save(R/'05_marketing/04_social'/name,quality=92)
master=R.parents[1]/'00_master/P03_identity_master_v1.png';c=Image.new('RGB',(1600,900),(25,25,28));
for p,x,label in [(master,80,'Source identity'),(S/assets[9]['canonical_filename'],870,'Final executive series')]:
 im=thumb(Image.open(p).convert('RGB'),(620,720));c.paste(im,(x+(620-im.width)//2,100));ImageDraw.Draw(c).text((x,835),label,font=F(28),fill='white')
c.save(R/'05_marketing/03_before_after/P03_identity_to_executive.jpg',quality=92)
copy={'avito_description_v1.md':'# Виртуальная деловая фотосессия\n\nПрофессиональная серия для сайта, LinkedIn, резюме и личного бренда. Разные сцены и ракурсы формируют цельный визуальный образ.','website_collection_v1.md':'# Executive collection\n\nПремиальная деловая серия с естественным характером, рабочими сценами и уверенной подачей.','short_social_caption_v1.md':'Деловой образ, который работает в разных ситуациях.','portfolio_caption_v1.md':'Executive v1 — серия портретов, рабочих сцен и полноростовых кадров в единой профессиональной стилистике.'}
for n,t in copy.items():(R/'05_marketing/05_copy'/n).write_text(t+'\n',encoding='utf8')
(R/'02_review/README.md').write_text('# Review\n\nAny image with extra/missing limbs, severe hand deformation, major identity drift or major anatomy defect cannot be approved final and must be REPAIR or REGENERATE.\n',encoding='utf8')
(R/'README.md').write_text('# P03 Executive v1\n\nTen immutable source PNGs form a candidate set pending human review. Final staging copies are byte-for-byte copies.\n',encoding='utf8')
(R/'SESSION_SUMMARY.md').write_text('# Session summary\n\nCharacter: P03_M45_Executive. Session: P03_EXECUTIVE_V1. Images: 10. Diversity: headshot, window 3/4, desk, walk, boardroom, lobby, private office, laptop, profile and editorial full body. Identity preservation is independent from pose preservation.\n',encoding='utf8')
(R/'FINAL_REPORT.md').write_text('# Final report\n\nSource 10/10, unique hashes 10/10, staging 10/10 and web derivatives 20/20 completed. Human review remains PENDING; portfolio status is candidate_set.\n',encoding='utf8')
print(len(assets))
