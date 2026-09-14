"""Non-destructive P02 BUSINESS V1 packaging; Pillow only, no generation or uploads.

Run with --request <original pasted request> on first build. Subsequent builds can
read the saved prompt manifest. Existing different outputs are never overwritten.
YAML files use JSON-compatible YAML 1.2 so Python stdlib can validate them.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps, features

ROOT = Path(__file__).resolve().parent
PERSONA = ROOT.parents[1]
REPO = next(p for p in ROOT.parents if (p / '.git').exists())
DATE = '2026-09-15'
INK, PAPER, GOLD, MUTED = '#18252b', '#f2efe8', '#ae9269', '#657078'
STEMS = ['headshot_front', 'window_3q', 'executive_desk', 'office_walk',
         'boardroom', 'lobby_fullbody', 'private_office', 'laptop_workspace',
         'window_crossed_arms', 'editorial_fullbody']
# Descriptive observations, not human scores or approval decisions.
OBSERVED = [
    ('contemporary office', 'upright near-frontal', 'camera', 'restrained smile', 'head and shoulders', 'dark navy blazer, light blouse'),
    ('office window', 'standing three-quarter; hands at cuff', 'camera', 'composed, relaxed lips', 'waist up', 'charcoal suit, light blouse'),
    ('executive desk', 'seated, pen over notebook', 'off camera', 'attentive', 'seated desk portrait', 'beige blazer, cream blouse'),
    ('glass office corridor', 'walking with folder', 'past camera', 'focused', 'knees up', 'charcoal suit, ivory blouse'),
    ('boardroom', 'standing with hand on chair', 'camera', 'serious', 'knees up', 'forest-green suit, light blouse'),
    ('office lobby', 'standing, weight shifted, holding bag', 'camera', 'modest smile', 'full body', 'light taupe pantsuit, heels'),
    ('private office', 'seated side-on, hand at chin, notebook on lap', 'camera', 'soft smile', 'seated three-quarter body', 'dark navy suit'),
    ('laptop workspace', 'seated, hands at laptop', 'laptop screen', 'small smile', 'desk / waist up', 'white blouse'),
    ('office window', 'standing profile, crossed arms', 'out of window', 'thoughtful, neutral', 'mid-thigh up', 'dark blazer and trousers'),
    ('architectural office', 'standing, one leg forward, hands in pockets', 'camera', 'slight smile', 'full body', 'dark charcoal pantsuit, light blouse'),
]
NOTES = {
    'BUS_01': 'Near-frontal but not perfectly frontal; confirm head angle and hair arrangement against prompt.',
    'BUS_03': 'Prompt relationship is clear; inspect pen grip and notebook lettering at full size.',
    'BUS_04': 'Inspect stride and document-folder hand; background typography is generated.',
    'BUS_05': 'Inspect fingers on chair and any background lettering.',
    'BUS_06': 'Inspect bag handle, fingers and heels before approval.',
    'BUS_07': 'Visible hand at chin and soft smile differ from armrest / serious-no-smile prompt. Do not treat as prompt-perfect.',
    'BUS_08': 'Inspect laptop fingers and background/book lettering. Desk scene differs clearly from BUS_03 in activity and wardrobe.',
    'BUS_10': 'Dark suit, hands in pockets and slight smile differ from ivory/stone suit, leather portfolio and no-smile prompt. Retained under supplied scene ID as candidate.',
}
RULE = '''Use MASTER and REF01–REF05 strictly for identity.
Preserve the exact canonical woman while allowing genuine variation in:
- pose
- head angle
- gaze direction
- facial expression
- hand position
- hairstyle arrangement
- camera distance
- composition

Do not mechanically copy pose/expression from identity references.'''


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def output(path, data):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        data = data.encode('utf-8')
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f'Refusing to overwrite different existing file: {path}')
    else:
        with path.open('xb') as stream:
            stream.write(data)
    return path


def write_yaml(path, data):
    return output(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def write_csv(path, rows, fields=None):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return output(path, stream.getvalue())


def font(size, bold=False, serif=False):
    name = 'georgia.ttf' if serif else ('segoeuib.ttf' if bold else 'segoeui.ttf')
    return ImageFont.truetype(str(Path('C:/Windows/Fonts') / name), size)


def text(canvas, value, box, size=40, fill=INK, bold=False, serif=False):
    """Fit wrapped text in its reserved box, failing rather than clipping."""
    left, top, right, bottom = box
    draw = ImageDraw.Draw(canvas)
    face = font(size, bold, serif)
    lines = []
    for paragraph in value.split('\n'):
        line = ''
        for word in paragraph.split():
            candidate = (line + ' ' + word).strip()
            if draw.textlength(candidate, font=face) > right - left:
                if not line:
                    raise ValueError(f'Word exceeds text box: {word}')
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    rendered = '\n'.join(lines)
    spacing = max(6, size // 4)
    bounds = draw.multiline_textbbox((left, top), rendered, font=face, spacing=spacing)
    if bounds[3] > bottom:
        raise ValueError(f'Text exceeds box: {value}')
    draw.multiline_text((left, top), rendered, font=face, fill=fill, spacing=spacing)


def place(canvas, path, box):
    """Contain complete image; never crop faces, hands or full-length portraits."""
    x, y, w, h = box
    with Image.open(path) as im:
        picture = ImageOps.contain(im.convert('RGB'), (w, h), Image.Resampling.LANCZOS)
    canvas.paste(picture, (x + (w-picture.width)//2, y + (h-picture.height)//2))


def source(i):
    return ROOT / '00_source' / f'P02_BUS_{i:02d}_{STEMS[i-1]}_v2.png'


def grid(canvas, ids, box, columns, labels=False):
    x, y, w, h = box
    rows = (len(ids) + columns - 1) // columns
    gap = 18
    cw = (w - (columns-1)*gap)//columns
    ch = (h - (rows-1)*gap)//rows
    for k, i in enumerate(ids):
        xx, yy = x + (k % columns)*(cw+gap), y + (k//columns)*(ch+gap)
        label_space = 50 if labels else 0
        place(canvas, source(i), (xx, yy, cw, ch-label_space))
        if labels:
            text(canvas, f'BUS_{i:02d}', (xx, yy+ch-43, xx+cw, yy+ch), 27)


MARKETING = []


def save_marketing(canvas, path, ids, layout, extra_inputs=()):
    data = io.BytesIO()
    canvas.save(data, 'JPEG', quality=95, subsampling=0, optimize=True)
    target = output(path, data.getvalue())
    inputs = [{'id': f'BUS_{i:02d}', 'file': source(i).relative_to(ROOT).as_posix(),
               'sha256': sha(source(i))} for i in ids]
    inputs += [{'id': name, 'file': str(p.relative_to(REPO)).replace('\\', '/'),
                'sha256': sha(p), 'path_base': 'repository'} for name, p in extra_inputs]
    MARKETING.append({'file': target.relative_to(ROOT).as_posix(), 'width': canvas.width,
                      'height': canvas.height, 'sha256': sha(target),
                      'file_size_bytes': target.stat().st_size, 'source_inputs': inputs,
                      'layout': layout, 'status': 'internal_review_candidate',
                      'publish_approved': False, 'processing': 'contain resize and layout only; no retouch or generation'})


def card(number, title, subtitle, ids, columns=1):
    canvas = Image.new('RGB', (1600, 2000), PAPER)
    text(canvas, 'ONYX', (80, 50, 700, 135), 65, serif=True)
    text(canvas, f'BUSINESS / {number:02d}', (1150, 77, 1520, 130), 27, fill=MUTED)
    ImageDraw.Draw(canvas).line((80, 155, 1520, 155), fill=GOLD, width=2)
    text(canvas, title, (80, 195, 1520, 425), 78, bold=True)
    text(canvas, subtitle, (80, 430, 1520, 580), 36, fill=MUTED)
    if ids:
        grid(canvas, ids, (80, 610, 1440, 1190), columns)
    text(canvas, 'Демонстрационный персонаж ONYX', (80, 1840, 1520, 1890), 29)
    text(canvas, 'Внутренний макет • серия ожидает review', (80, 1903, 1520, 1950), 25, fill=MUTED)
    return canvas


def marketing():
    for clean in (False, True):
        c = Image.new('RGB', (2400, 1590), PAPER)
        if clean:
            text(c, 'ONYX', (60, 30, 2000, 145), 76, serif=True)
        else:
            text(c, 'ONYX — BUSINESS', (60, 30, 2200, 140), 76, serif=True)
            text(c, 'Virtual AI Photoshoot', (60, 135, 2200, 210), 40, fill=MUTED)
        grid(c, list(range(1, 11)), (50, 230 if not clean else 160, 2300, 1290 if not clean else 1380), 5, not clean)
        suffix = '_clean' if clean else ''
        save_marketing(c, f'05_marketing/01_contact_sheet/P02_business_v1_contact_sheet{suffix}.jpg', list(range(1, 11)), '5 columns x 2 rows; full image containment')

    specs = [
        ('Виртуальная деловая\nфотосессия', '10 кадров без студийной съёмки', [1, 6], 2),
        ('Один персонаж.\nРазные сцены.', 'Одна внешность — основа всей серии', [1, 3, 9], 3),
        ('От портрета\nдо полного роста', 'Офис • переговорная • движение • полный рост', [1, 4, 5, 6], 2),
        ('Рабочие моменты', 'За ноутбуком, в движении, в профиль', [8, 4, 9], 3),
        ('Ваш деловой образ', 'Резюме • LinkedIn • сайт • личный бренд', [2, 7], 2),
        ('Как устроена серия', 'От концепции к набору кадров', [], 1),
        ('Внимание к деталям', 'Что проверяем перед финальным отбором', [], 1),
        ('Десять кадров.\nОдна коллекция.', 'Разные планы, ракурсы и рабочие ситуации', [1, 3, 4, 6, 8, 9], 3),
        ('Ваш образ.\nНовая обстановка.', 'Виртуальная фотосессия без поездки в студию', [1, 9], 2),
        ('Virtual Photo Studio', 'Деловой образ, который подходит вам', [6, 8], 2),
    ]
    for n, (title, subtitle, ids, cols) in enumerate(specs, 1):
        c = card(n, title, subtitle, ids, cols)
        if n == 6:
            blocks = [('01', 'Концепция и сцены'), ('02', 'Серия с опорой на внешность'),
                      ('03', 'Техническая проверка файлов'), ('04', 'Проверка и отбор человеком'),
                      ('05', 'Подготовка набора для публикации')]
            for k, (num, line) in enumerate(blocks):
                yy = 655 + k*185
                text(c, num, (90, yy, 250, yy+100), 62, fill=GOLD, serif=True)
                text(c, line, (270, yy+8, 1500, yy+130), 46)
            text(c, 'Для этой серии финальный отбор ещё предстоит.', (90, 1660, 1500, 1780), 36, fill=MUTED)
        if n == 7:
            for k, line in enumerate(['Лицо и сходство', 'Руки и пропорции', 'Одежда и мелкие детали', 'Артефакты и надписи', 'Разнообразие серии']):
                yy = 670 + k*180
                ImageDraw.Draw(c).line((90, yy+36, 170, yy+36), fill=GOLD, width=3)
                text(c, line, (220, yy, 1500, yy+110), 52)
            text(c, 'Техническая проверка не заменяет визуальную оценку.', (90, 1670, 1500, 1790), 36, fill=MUTED)
        save_marketing(c, f'05_marketing/02_avito_carousel/P02_business_card_{n:02d}.jpg', ids, f'Avito internal draft card {n}; full image containment')

    # The supplied JPEG collage contains misleading baked-in REAL PHOTOS wording.
    # Use canonical images for an explicitly synthetic reference-to-result layout.
    c = Image.new('RGB', (2100, 1400), PAPER)
    text(c, 'ONYX / ОТ ОБРАЗА К СЕРИИ', (60, 35, 2040, 140), 62, serif=True)
    text(c, 'Демонстрационный персонаж ONYX', (60, 150, 2040, 235), 48, bold=True)
    text(c, 'Синтетические исходные образы', (60, 285, 1010, 345), 34)
    text(c, 'Кандидаты деловой фотосессии', (1090, 285, 2040, 345), 34)
    master = PERSONA/'00_master/P02_identity_master_v1.png'
    ref = PERSONA/'01_references/P02_REF03.png'
    place(c, master, (60, 370, 465, 790)); place(c, ref, (545, 370, 465, 790))
    grid(c, [1, 6], (1090, 370, 950, 790), 2)
    text(c, 'MASTER + REF03', (60, 1190, 1010, 1250), 31, fill=MUTED)
    text(c, 'BUS_01 + BUS_06 • review pending', (1090, 1190, 2040, 1250), 31, fill=MUTED)
    text(c, 'Все показанные изображения созданы с ИИ. Внутренний демонстрационный макет.', (60, 1300, 2040, 1370), 30, fill=MUTED)
    save_marketing(c, '05_marketing/03_before_after/P02_reference_to_business_demo.jpg', [1, 6], 'synthetic reference-to-result, not a real-client before/after', [('MASTER',master),('REF03',ref)])

    # Provisional visual edit: distinct activity, scale and head angle, no human scores.
    for name, size, ids, cols, clean in [
        ('square_selection', (1600,1600), [1,3,6,9], 2, False),
        ('story_cover', (1080,1920), [6], 1, False),
        ('portrait_showcase', (1600,2000), [1,8,9], 3, False),
        ('clean_grid_4', (1800,2440), [1,4,6,9], 2, True),
        ('clean_grid_6', (2100,2020), [1,3,4,6,8,9], 3, True),
    ]:
        w,h=size; c=Image.new('RGB',size,PAPER)
        text(c, 'ONYX', (50,30,w-50,140), 70, serif=True)
        if clean:
            grid(c,ids,(40,155,w-80,h-195),cols)
        else:
            text(c, 'BUSINESS', (50,145,w-50,250), 64,bold=True)
            text(c, 'Виртуальная фотосессия', (50,260,w-50,335), 38,fill=MUTED)
            grid(c,ids,(40,365,w-80,h-550),cols)
            text(c,'Демонстрационный персонаж ONYX',(50,h-150,w-50,h-50),28,fill=MUTED)
        save_marketing(c, f'05_marketing/04_social/P02_business_{name}.jpg', ids, 'provisional diverse selection; full image containment')
    write_yaml('05_marketing/marketing_manifest.yaml', {'session_id':'P02_BUSINESS_V1','status':'internal_review_candidate', 'publish_approved':False, 'assets':MARKETING})


def build(request=None):
    if not features.check('webp'):
        raise RuntimeError('Installed Pillow lacks WebP support; no automatic install.')
    expected = [ROOT/f'P02_BUS_{i:02d}_{stem}.png' for i,stem in enumerate(STEMS,1)]
    if any(not p.is_file() for p in expected):
        raise RuntimeError('Missing original mapping input; do not guess.')
    originals = {str(p):sha(p) for p in expected}
    if request:
        raw = Path(request).read_text(encoding='utf-8-sig')
        section=raw.split('PROMPTS:',1)[1].split('4. IMAGE MANIFEST',1)[0]
        matches=list(re.finditer(r'-{5,}\s*\n(BUS_\d{2})\s*\n-{5,}\s*\n',section))
        prompts={}
        for i,m in enumerate(matches):
            value=section[m.end():matches[i+1].start() if i+1<len(matches) else len(section)]
            prompts[m[1]]=re.split(r'\n={5,}',value)[0].strip()
        assert list(prompts)==[f'BUS_{i:02d}' for i in range(1,11)]
    else:
        saved=json.loads((ROOT/'01_prompts/P02_business_v1_prompts.yaml').read_text(encoding='utf-8'))
        prompts={p['id']:p['prompt'] for p in saved['prompts']}
    prompt_data={'session_id':'P02_BUSINESS_V1','identity_version':1,'session_identity_rule':RULE,
                 'provenance':'Verbatim prompt text supplied by user; actual model, seed and execution settings were not supplied.',
                 'model':None,'seed':None,'generation_settings':None,
                 'prompts':[{'id':key,'prompt':value,'text_sha256':hashlib.sha256(value.encode()).hexdigest()} for key,value in prompts.items()]}
    write_yaml('01_prompts/P02_business_v1_prompts.yaml',prompt_data)
    output('01_prompts/P02_business_v1_prompts.md','# P02 BUSINESS V1 — prompts\n\n## Session identity rule\n\n'+RULE+'\n\n'+'\n\n'.join('## '+key+'\n\n'+value for key,value in prompts.items())+'\n')
    output('01_prompts/session_identity_block.md',RULE+'\n')
    for key,value in prompts.items(): output(f'01_prompts/{key}.txt',value+'\n')
    assets=[]; qa=[]; mappings=[]; web=[]
    for i,original in enumerate(expected,1):
        key=f'BUS_{i:02d}'; name=f'P02_BUS_{i:02d}_{STEMS[i-1]}_v2.png'
        target=output('00_source/'+name,original.read_bytes())
        assert sha(target)==originals[str(original)]
        with Image.open(target) as im:
            assert im.format=='PNG'; im.verify()
        with Image.open(target) as im:
            im.load(); w,h=im.size; exif=bool(im.getexif()); mode=im.mode; rgb=im.convert('RGB')
        scene,pose,gaze,expression,framing,wardrobe=OBSERVED[i-1]
        output('03_final/'+name,target.read_bytes())
        mappings.append({'id':key,'source_filename':original.name,'source_path':original.relative_to(ROOT).as_posix(),
                         'canonical_path':'00_source/'+name,'method':'byte-for-byte copy','sha256':sha(target),'mapping_basis':'matching original scene ID and visual inspection; reserve excluded'})
        assets.append({'id':key,'canonical_filename':name,'source_filename':original.name,
                       'source_path':original.relative_to(ROOT).as_posix(),'canonical_source_path':'00_source/'+name,
                       'sha256':sha(target),'width':w,'height':h,'file_size_bytes':target.stat().st_size,
                       'prompt_id':key,'scene':scene,'pose_type':pose,'gaze':gaze,'expression':expression,
                       'framing':framing,'wardrobe':wardrobe,'description_basis':'observed image; qualitative description only',
                       'status':'candidate','human_decision':'PENDING','source_preserved':True,
                       'final_filename':'03_final/'+name,'final_status':'candidate_staging','publish_approved':False})
        qa.append({'id':key,'filename':name,'width':w,'height':h,'aspect_ratio':round(w/h,8),
                   'sha256':sha(target),'readable':True,'exact_duplicate':False,
                   'technical_notes':f'PNG signature/CRC verified; full decode OK; mode={mode}; EXIF present={exif}; 3:4={w*4==h*3}; near-duplicate skipped: repository dHash requires unavailable cv2; no dependency installed.'})
        # Never upscale a smaller source just to hit a nominal long-edge target.
        rgb.thumbnail((1600,1600),Image.Resampling.LANCZOS)
        for fmt,ext,options in [('JPEG','jpg',{'quality':95,'subsampling':0,'optimize':True}),('WEBP','webp',{'quality':95,'method':6})]:
            buf=io.BytesIO();rgb.save(buf,fmt,**options)
            derivative=output(f'04_web/{ext}/{Path(name).stem}_web.{ext}',buf.getvalue())
            with Image.open(derivative) as check: check.load(); assert check.size==rgb.size
            web.append({'source':'03_final/'+name,'derivative':derivative.relative_to(ROOT).as_posix(),
                        'width':rgb.width,'height':rgb.height,'format':fmt,'file_size':derivative.stat().st_size,'sha256':sha(derivative)})
    hashes=[a['sha256'] for a in assets]
    for row in qa: row['exact_duplicate']=hashes.count(row['sha256'])>1
    assert len(set(hashes))==10
    write_csv('02_review/source_mapping.csv',mappings)
    write_csv('02_review/technical_qa.csv',qa)
    review_fields=['id','filename','identity_1_5','realism_1_5','anatomy_1_5','hands_1_5','pose_naturalness_1_5','expression_1_5','scene_quality_1_5','portfolio_value_1_5','diversity_1_5','decision','repair_notes','comments']
    review=[{**dict.fromkeys(review_fields,''),'id':a['id'],'filename':a['canonical_filename'],'decision':'PENDING'} for a in assets]
    write_csv('02_review/P02_business_v1_review.csv',review,review_fields)
    write_csv('04_web/web_manifest.csv',web)
    identities=[PERSONA/'00_master/P02_identity_master_v1.png']+sorted((PERSONA/'01_references').glob('P02_REF*.png'))
    collage=PERSONA/'02_source_generations/Collage.jpg'
    manifest={'session_id':'P02_BUSINESS_V1','character_id':'P02','character_name':'P02_F30_Lifestyle',
              'identity_version':1,'collection':'business','expected_images':10,'generated_images':10,
              'generated_images_basis':'User reported generation; ten saved images verified locally.',
              'source_status':'frozen','portfolio_status':'review','staging_status':'candidate','publish_approved':False,
              'path_base':'business_v1 unless explicitly stated','prepared_on':DATE,'model':None,'seed':None,
              'canonical_filename_note':'_v2 is the user-requested packaging name; generation version is not independently established.',
              'identity_inputs':[{'file':p.relative_to(PERSONA).as_posix(),'sha256':sha(p),'path_base':'character_directory'} for p in identities],
              'collage_context':{'file':'02_source_generations/Collage.jpg','path_base':'character_directory','sha256':sha(collage),'status':'existing visual source context; not substituted for missing canonical PNG','note':'Embedded REAL PHOTOS text conflicts with synthetic character status; excluded from demo layout.'},
              'images':assets}
    write_yaml('business_manifest.yaml',manifest)
    marketing()
    for p,digest in originals.items(): assert sha(p)==digest
    print(json.dumps({'source_images':len(assets),'prompts':len(prompts),'web_derivatives':len(web),'marketing_assets':len(MARKETING),'unique_hashes':len(set(hashes))}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request',type=Path)
    args=parser.parse_args()
    build(args.request)
