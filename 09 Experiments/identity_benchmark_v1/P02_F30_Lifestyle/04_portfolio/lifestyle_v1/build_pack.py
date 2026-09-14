"""Package saved lifestyle images and create parallel business _publish exports.

Python + existing Pillow; no image generation, installation, source editing or upload.
Uses the committed business builder's text/font/contain helpers read-only via runpy.
Refuses to replace different existing files. Human review is never auto-approved.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import runpy
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps, features

ROOT = Path(__file__).resolve().parent
BUSINESS = ROOT.parent/'business_v1'
PERSONA = ROOT.parents[1]
REPO = next(p for p in ROOT.parents if (p/'.git').exists())
HELPERS = runpy.run_path(str(BUSINESS/'build_pack.py'))
text, place = HELPERS['text'], HELPERS['place']
PAPER, INK, GOLD, MUTED = '#f2efe8', '#18252b', '#ae9269', '#657078'
STEMS = ['cafe_window','city_walk','home_morning','book_cafe','rooftop_sunset',
         'weekend_street','balcony_profile','cozy_sofa','travel_lobby','evening_city']
OBSERVED = [
    ('cafe window','seated, hand at chin and cup','out of window','thoughtful','seated portrait','white shirt, dark trousers'),
    ('city street','walking, one hand in pocket','off camera','composed','near full length','camel coat, neutral top, jeans, sneakers'),
    ('home kitchen','standing with mug, hair loosely gathered','down at mug','peaceful','three-quarter body','cream knit sweater, neutral trousers'),
    ('reading cafe','seated with open book, crossed legs','down at book','absorbed','seated three-quarter body','ivory turtleneck, beige coat'),
    ('rooftop sunset','rear three-quarter, holding glass','back toward camera','subtle smile','three-quarter portrait','black sleeveless dress'),
    ('pedestrian street','walking, hand at hair, carrying bag','off camera','open smile','knees up','white T-shirt, tan jacket, blue jeans'),
    ('balcony at dusk','side profile, leaning on railing, hand at chin','distance','contemplative','three-quarter body','light blouse, neutral trousers'),
    ('home sofa','seated with folded leg, hand at hair, holding cup','camera','warm slight smile','seated portrait','oversized knit sweater, relaxed trousers'),
    ('hotel lobby','walking with wheeled suitcase','toward lobby','focused','near full length','light long coat, fitted top, wide trousers, sneakers'),
    ('evening city street','rear three-quarter, hand holding coat','back toward camera','slight smile','three-quarter portrait','black dress, dark coat'),
]
REVIEW_FIELDS=['id','filename','identity_1_5','realism_1_5','anatomy_1_5','hands_1_5',
               'pose_naturalness_1_5','expression_1_5','scene_quality_1_5',
               'portfolio_value_1_5','diversity_1_5','decision','repair_notes','comments']


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(data,str): data=data.encode('utf-8')
    if path.exists():
        if path.read_bytes()!=data: raise RuntimeError(f'Refusing to replace {path}')
    else:
        with path.open('xb') as f: f.write(data)
    return path


def yaml(path,data):
    return put(path,json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def csvfile(path,rows,fields=None):
    f=io.StringIO(newline=''); w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),lineterminator='\n')
    w.writeheader(); w.writerows(rows); return put(path,f.getvalue())


def photo(i):return ROOT/'00_source'/f'P02_LIFE_{i:02d}_{STEMS[i-1]}.png'


def grid(canvas, paths, box, columns, labels=None):
    x,y,w,h=box; rows=(len(paths)+columns-1)//columns; gap=18
    cw=(w-(columns-1)*gap)//columns;ch=(h-(rows-1)*gap)//rows
    for k,p in enumerate(paths):
        xx=x+(k%columns)*(cw+gap); yy=y+(k//columns)*(ch+gap)
        place(canvas,p,(xx,yy,cw,ch-(48 if labels else 0)))
        if labels:text(canvas,labels[k],(xx,yy+ch-40,xx+cw,yy+ch),27)


def public_pack(root, collection, images, prefix, publish=False):
    """Create new, separately manifested clean public assets; old records are inputs only."""
    suffix='_publish' if publish else ''
    records=[]; corpus=[]
    def label(c,value,box,size=40,**kw):
        corpus.append(value);text(c,value,box,size,**kw)
    def paths(ids):return [root/images[i-1]['canonical_source_path'] for i in ids]
    def save(c,rel,ids,extra=()):
        buf=io.BytesIO();c.save(buf,'JPEG',quality=95,subsampling=0,optimize=True)
        p=put(root/rel,buf.getvalue())
        inputs=[{'id':images[i-1]['id'],'path':images[i-1]['canonical_source_path'],'sha256':images[i-1]['sha256'],'path_base':'session'} for i in ids]
        inputs += [{'id':name,'path':p.relative_to(REPO).as_posix(),'sha256':sha(p),'path_base':'repository'} for name,p in extra]
        records.append({'file':p.relative_to(root).as_posix(),'width':c.width,'height':c.height,
                        'file_size_bytes':p.stat().st_size,'sha256':sha(p),'source_inputs':inputs,
                        'export_role':'preferred_public_layout','rendered_text':list(corpus),
                        'processing':'contain resize and composition; no source edit, retouch or AI upscale'})
        corpus.clear()
    base='05_marketing'
    for clean in (False,True):
        c=Image.new('RGB',(2400,1590),PAPER)
        label(c,'ONYX' if clean else 'ONYX — '+collection.upper(),(60,30,2300,145),76,serif=True)
        if not clean:label(c,'Virtual AI Photoshoot',(60,135,2300,210),40,fill=MUTED)
        ids=list(range(1,11));grid(c,paths(ids),(50,160 if clean else 230,2300,1380 if clean else 1290),5,None if clean else [a['id'] for a in images])
        save(c,f'{base}/01_contact_sheet/P02_{collection}_v1_contact_sheet'+('_clean' if clean else '')+suffix+'.jpg',ids)
    if collection=='lifestyle':
        specs=[
            ('Виртуальная lifestyle-\nфотосессия','10 стильных кадров без студии',[1,5],2),
            ('Один образ.\nРазные моменты.','Единая внешность — разные сцены и настроения',[3,6,7],3),
            ('В ритме вашей жизни','Кафе • город • дом • путешествия • вечер',[1,2,3,5,9,10],3),
            ('Живые эмоции','Улыбка, задумчивость и спокойствие',[6,4,8],3),
            ('Личная история\nв фотографиях','Lifestyle • личный бренд • путешествия • соцсети',[2,8],2),
            ('От идеи к серии','Концепция, внешность, сцены и внимание к деталям',[],1),
            ('Качество в деталях','Что важно для цельной фотосессии',[],1),
            ('Десять кадров.\nРазные настроения.','От утреннего кафе до вечернего города',[1,3,5,6,9,10],3),
            ('Ваш образ —\nновая история','Виртуальная фотосессия ONYX',[3,10],2),
            ('Virtual Photo Studio','Помогаем людям выглядеть так, как они хотят выглядеть.',[7,9],2),
        ]
        selected=[1,3,5,6,7,9];hero=5; show=[1,6,9];demo_ids=[3,10]
    else:
        specs=[
            ('Виртуальная деловая\nфотосессия','10 профессиональных кадров без студии',[1,6],2),
            ('Один образ.\nРазные сцены.','Единая внешность — основа всей серии',[1,3,9],3),
            ('От портрета\nдо полного роста','Офис • переговорная • движение • полный рост',[1,4,5,6],2),
            ('Рабочие моменты','За ноутбуком, в движении, в профиль',[8,4,9],3),
            ('Ваш деловой образ','Резюме • LinkedIn • сайт • личный бренд',[2,7],2),
            ('Как устроена серия','От концепции к набору кадров',[],1),
            ('Внимание к деталям','Что важно при подготовке делового образа',[],1),
            ('Десять кадров.\nОдна коллекция.','Разные планы, ракурсы и рабочие ситуации',[1,3,4,6,8,9],3),
            ('Ваш образ.\nНовая обстановка.','Виртуальная фотосессия без поездки в студию',[1,9],2),
            ('Virtual Photo Studio','Помогаем людям выглядеть так, как они хотят выглядеть.',[6,8],2),
        ]
        selected=[1,3,4,6,8,9];hero=6;show=[1,8,9];demo_ids=[1,6]
    for n,(title,sub,ids,cols) in enumerate(specs,1):
        c=Image.new('RGB',(1600,2000),PAPER)
        label(c,'ONYX',(80,50,700,135),65,serif=True)
        label(c,f'{collection.upper()} / {n:02d}',(1130,77,1520,130),27,fill=MUTED)
        ImageDraw.Draw(c).line((80,155,1520,155),fill=GOLD,width=2)
        label(c,title,(80,195,1520,425),78,bold=True)
        label(c,sub,(80,430,1520,585),36,fill=MUTED)
        if ids:grid(c,paths(ids),(80,610,1440,1240),cols)
        else:
            lines=(['Концепция фотосессии','Опора на внешность','Разнообразные сцены и ракурсы','Проверка деталей и отбор','Подготовка цельной серии'] if n==6
                   else ['Лицо и сходство','Руки и пропорции','Одежда и мелкие детали','Артефакты и надписи','Разнообразие и целостность серии'])
            for k,line in enumerate(lines):
                yy=680+k*205
                label(c,f'{k+1:02d}',(90,yy,245,yy+100),62,fill=GOLD,serif=True)
                label(c,line,(270,yy+8,1500,yy+155),46)
        label(c,'ONYX / Virtual Photo Studio',(80,1910,1520,1970),29,fill=MUTED)
        save(c,f'{base}/02_avito_carousel/P02_{collection}_card_{n:02d}{suffix}.jpg',ids)
    master=PERSONA/'00_master/P02_identity_master_v1.png';ref=PERSONA/'01_references/P02_REF03.png'
    c=Image.new('RGB',(2100,1400),PAPER)
    label(c,'ONYX / ОТ ОБРАЗА К СЕРИИ',(60,35,2040,140),62,serif=True)
    label(c,'Виртуальная фотосессия',(60,165,2040,245),45)
    label(c,'Исходный образ персонажа',(60,290,1010,350),34)
    label(c,'Lifestyle-серия ONYX' if collection=='lifestyle' else 'Деловая серия ONYX',(1090,290,2040,350),34)
    place(c,master,(60,375,465,850));place(c,ref,(545,375,465,850))
    grid(c,paths(demo_ids),(1090,375,950,850),2)
    label(c,'ONYX / Virtual Photo Studio',(60,1300,2040,1370),30,fill=MUTED)
    save(c,f'{base}/03_before_after/P02_reference_to_{collection}{suffix}.jpg',demo_ids,[('MASTER',master),('REF03',ref)])
    for name,size,ids,cols,clean in [
        ('square_selection',(1600,1600),[selected[i] for i in (0,1,2,3)],2,False),
        ('story_cover',(1080,1920),[hero],1,False),
        ('portrait_showcase',(1600,2000),show,2,False),
        ('clean_grid_4',(1800,2440),[selected[i] for i in (0,2,3,4)],2,True),
        ('clean_grid_6',(2100,2020),selected,3,True),
    ]:
        w,h=size;c=Image.new('RGB',size,PAPER);label(c,'ONYX',(50,30,w-50,140),70,serif=True)
        if clean:grid(c,paths(ids),(40,155,w-80,h-195),cols)
        else:
            label(c,collection.upper(),(50,145,w-50,250),64,bold=True)
            label(c,'Виртуальная фотосессия',(50,260,w-50,335),38,fill=MUTED)
            if name=='portrait_showcase':
                place(c,paths(ids)[0],(50,390,870,1430))
                place(c,paths(ids)[1],(945,390,600,700));place(c,paths(ids)[2],(945,1120,600,700))
            else:grid(c,paths(ids),(40,365,w-80,h-430),cols)
        save(c,f'{base}/04_social/P02_{collection}_{name}{suffix}.jpg',ids)
    collection_ru='lifestyle' if collection=='lifestyle' else 'деловая'
    scenes=('Утреннее кафе, прогулка по городу, уютный дом, закат на крыше и вечерняя улица.' if collection=='lifestyle'
            else 'Крупный портрет, рабочий кабинет, переговорная, движение и полный рост.')
    copy={
        'avito_description_v1':f'# Виртуальная {collection_ru} фотосессия ONYX\n\nДесять кадров, объединённых одним образом. {scenes}\n\nПродуманная серия помогает подобрать фотографию под настроение и задачу. В основе подхода — концепция, внимание к внешности, разнообразие сцен и аккуратный отбор.\n\n'+('Для личного бренда, социальных сетей и истории о себе — без поездки в студию.' if collection=='lifestyle' else 'Для резюме, LinkedIn, сайта и социальных сетей — без поездки в студию.')+'\n\nРасскажите, какой образ вы хотите создать и где планируете использовать фотографии.\n',
        f'website_{collection}_collection_v1':f'# ONYX {collection.title()}\n\nОдин образ — разные моменты. {scenes}\n\nКоллекция объединяет десять фотографий с разными планами, ракурсами и настроением. Виртуальная фотосессия открывает новые возможности для личного визуального образа.\n',
        'short_social_caption_v1':f'ONYX {collection.title()}: десять кадров, один образ, разные истории. {scenes}\n\nВиртуальная фотосессия ONYX.\n',
        'portfolio_caption_v1':f'# ONYX / {collection.upper()}\n\n{scenes}\n\nСерия из десяти кадров: внешность объединяет коллекцию, а свет, движение и обстановка создают разные настроения. Виртуальная фотосессия ONYX.\n',
    }
    copy_records=[]
    for stem,value in copy.items():
        p=put(root/base/'05_copy'/f'{stem}{suffix}.md',value)
        copy_records.append({'file':p.relative_to(root).as_posix(),'sha256':sha(p),'text':value})
    yaml(root/base/('publishing_manifest.yaml' if publish else 'marketing_manifest.yaml'),
         {'session_id':f'P02_{collection.upper()}_V1','export_role':'preferred_public_layout',
          'approval_note':'Clean layout is not human approval; existing session review state remains authoritative.',
          'historical_records_unchanged':True,'rendering':'Pillow JPEG quality 95, subsampling 0; no crop or source edit',
          'assets':records,'copy':copy_records})
    return records


def build(request):
    if not features.check('webp'):raise RuntimeError('WebP unavailable; do not install automatically')
    raw=request.read_text(encoding='utf-8-sig')
    rule=raw.split('Сохранить session-level rule:',1)[1].split('Сохранить все 10 prompts.',1)[0].strip()
    section=raw.split('PROMPTS:',1)[1].split('E. LIFESTYLE MANIFEST',1)[0]
    markers=list(re.finditer(r'-{5,}\s*\n(LIFE_\d{2})\s*\n-{5,}\s*\n',section))
    prompts=[]
    for k,m in enumerate(markers):
        value=section[m.end():markers[k+1].start() if k+1<len(markers) else len(section)]
        value=re.split(r'\n={5,}',value)[0].strip()
        prompts.append({'id':m[1],'prompt':value,'text_sha256':hashlib.sha256(value.encode()).hexdigest()})
    assert [p['id'] for p in prompts]==[f'LIFE_{i:02d}' for i in range(1,11)]
    yaml(ROOT/'01_prompts/P02_lifestyle_v1_prompts.yaml',{'session_id':'P02_LIFESTYLE_V1',
         'session_identity_rule':rule,'prompt_provenance':'Verbatim user-supplied prompts; exact replacement execution prompt not separately supplied.',
         'model':None,'seed':None,'prompts':prompts})
    put(ROOT/'01_prompts/session_identity_block.md',rule+'\n')
    put(ROOT/'01_prompts/P02_lifestyle_v1_prompts.md','# P02 LIFESTYLE V1 — prompts\n\n## Session identity rule\n\n'+rule+'\n\n'+'\n\n'.join('## '+p['id']+'\n\n'+p['prompt'] for p in prompts)+'\n')
    for p in prompts:put(ROOT/'01_prompts'/f"{p['id']}.txt",p['prompt']+'\n')
    assets=[];qa=[];web=[];mapping=[]
    for i,stem in enumerate(STEMS,1):
        key=f'LIFE_{i:02d}';name=f'P02_{key}_{stem}.png';original=ROOT/('P02_LIFE_01_cafe_window.png' if i==1 else f'{i}.png')
        target=put(ROOT/'00_source'/name,original.read_bytes());assert sha(target)==sha(original)
        with Image.open(target) as im:assert im.format=='PNG';im.verify()
        with Image.open(target) as im:im.load();w,h=im.size;exif=bool(im.getexif());rgb=im.convert('RGB')
        put(ROOT/'03_final'/name,target.read_bytes())
        scene,pose,gaze,expression,framing,wardrobe=OBSERVED[i-1]
        note=('Verified visually as true outdoor evening-city replacement; user reports earlier office-like attempt. Earlier file not identified locally.' if i==10 else 'Observed description, not a human score; inspect prompt adherence separately.')
        assets.append({'id':key,'canonical_filename':name,'source_filename':original.name,'source_path':original.name,
                       'canonical_source_path':'00_source/'+name,'sha256':sha(target),'width':w,'height':h,'file_size_bytes':target.stat().st_size,
                       'prompt_id':key,'scene':scene,'pose_type':pose,'gaze':gaze,'expression':expression,'framing':framing,'wardrobe':wardrobe,
                       'status':'finalized_candidate_set','human_decision':'PENDING','source_preserved':True,'final_filename':'03_final/'+name,'notes':note})
        qa.append({'id':key,'filename':name,'width':w,'height':h,'aspect_ratio':w/h,'sha256':sha(target),'readable':True,
                   'png_valid':True,'exact_duplicate':False,'exif_present':exif,
                   'technical_notes':'PNG CRC verified and full decode OK; no pixel edit. Near duplicates skipped: existing repository dHash requires unavailable cv2.'})
        mapping.append({'id':key,'source_filename':original.name,'canonical_path':'00_source/'+name,'sha256':sha(target),
                        'mapping_basis':'scene content visually inspected; evening-city replacement confirmed for LIFE_10','copy_method':'byte-for-byte'})
        rgb.thumbnail((1600,1600),Image.Resampling.LANCZOS)
        for fmt,ext,options in [('JPEG','jpg',{'quality':95,'subsampling':0,'optimize':True}),('WEBP','webp',{'quality':95,'method':6})]:
            buf=io.BytesIO();rgb.save(buf,fmt,**options);p=put(ROOT/'04_web'/ext/f'{Path(name).stem}_web.{ext}',buf.getvalue())
            web.append({'source':'03_final/'+name,'derivative':p.relative_to(ROOT).as_posix(),'width':rgb.width,'height':rgb.height,
                        'format':fmt,'file_size':p.stat().st_size,'sha256':sha(p)})
    assert len({a['sha256'] for a in assets})==10
    csvfile(ROOT/'02_review/technical_qa.csv',qa)
    csvfile(ROOT/'02_review/source_mapping.csv',mapping)
    csvfile(ROOT/'02_review/P02_lifestyle_v1_review.csv',[{**dict.fromkeys(REVIEW_FIELDS,''),'id':a['id'],'filename':a['canonical_filename'],'decision':'PENDING'} for a in assets],REVIEW_FIELDS)
    csvfile(ROOT/'04_web/web_manifest.csv',web)
    identities=[PERSONA/'00_master/P02_identity_master_v1.png']+sorted((PERSONA/'01_references').glob('P02_REF*.png'))+[PERSONA/'02_source_generations/Collage.jpg']
    yaml(ROOT/'lifestyle_manifest.yaml',{'session_id':'P02_LIFESTYLE_V1','character_id':'P02','identity_version':1,'collection':'lifestyle',
         'expected_images':10,'generated_images':10,'generated_images_basis':'Ten supplied selected files; total attempt count unknown.',
         'source_status':'frozen','portfolio_status':'finalized_candidate_set','human_review_status':'PENDING','publish_approved':False,
         'path_base':'lifestyle_v1','model':None,'seed':None,
         'identity_inputs':[{'path':p.relative_to(PERSONA).as_posix(),'path_base':'character_directory','sha256':sha(p)} for p in identities],
         'noncanonical':[{'scene_id':'LIFE_10','file':None,'status':'superseded','reason':'superseded_by_evening_city_replacement',
                          'presence':'not_located','basis':'User-reported earlier office-like attempt; no local filename inferred.','replacement_source':'10.png'}],
         'images':assets})
    life_records=public_pack(ROOT,'lifestyle',assets,'LIFE')
    business=json.loads((BUSINESS/'business_manifest.yaml').read_text(encoding='utf-8'))
    bus_records=public_pack(BUSINESS,'business',business['images'],'BUS',publish=True)
    print(json.dumps({'lifestyle_sources':10,'web':20,'lifestyle_marketing':len(life_records),'business_publish':len(bus_records)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--request',type=Path,required=True)
    build(parser.parse_args().request)
