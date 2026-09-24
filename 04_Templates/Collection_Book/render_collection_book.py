"""Local, data-driven Collection Book renderer. No network or source writes."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from PIL import Image, ImageOps
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FORBIDDEN = re.compile(r'P0\d|BUS_\d|FLUX|LoRA|PuLID|ComfyUI|checkpoint|prompt|generation|AI pipeline|[A-Z]:[\\/]|\.png|\.jpg', re.I)

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def plan(n):
    if n not in (1, 10, 20):
        raise ValueError('Supported photo counts: 1, 10, 20')
    if n == 1:
        return [('hero', [0])]
    # Nine story pages for Signature; paired story for Premium keeps 16 pages.
    if n == 20:
        return [('pair', [i, i+1]) for i in range(0, n, 2)]
    return [('hero',[0]), ('inset',[1]), ('caption',[2]), ('pair',[3,4]),
            ('hero',[5]), ('space',[6]), ('inset',[7]), ('caption',[8]), ('hero',[9])]

def render(data_path, output, root=ROOT, poppler='pdftoppm'):
    data = json.loads(Path(data_path).read_text(encoding='utf-8-sig'))
    if not 1 <= len(data['next_collections']) <= 2:
        raise ValueError('Provide one or two next collections')
    for item in data['next_collections']:
        if item['status'] not in ('coming_soon', 'available'):
            raise ValueError('Unknown collection availability')
        if item.get('qr_url'):
            raise ValueError('QR field reserved; QR rendering is not implemented in v1')
    style = json.loads((HERE/'template/style.json').read_text())
    photos = data['photos']
    story = plan(len(photos))
    expected = {'Preview':1, 'Signature':10, 'Premium':20}
    if expected.get(data['product_tier']) != len(photos):
        raise ValueError('Tier/photo count mismatch')
    paths = [(root/p['path']).resolve() for p in photos]
    if len(set(paths)) != len(paths):
        raise ValueError('Duplicate source paths')
    hashes = [digest(p) for p in paths]
    if len(set(hashes)) != len(hashes):
        raise ValueError('Duplicate source bytes')
    for p, h in zip(photos, hashes):
        if p.get('sha256') and p['sha256'] != h:
            raise ValueError('Source hash mismatch: '+p['path'])
    for key in ('cover_image','hero_image','onyx_selection_image'):
        if data[key] not in [p['path'] for p in photos]:
            raise ValueError(key+' must reference a collection photo')
    if data['hero_image'] != photos[0]['path']:
        raise ValueError('Place hero_image first in photos')
    if data['language'] != 'ru' or data['brand_variant'] != 'editorial_v1':
        raise ValueError('v1 supports ru / editorial_v1 only')
    if not data.get('onyx_mission_heading') or not data.get('onyx_mission_text'):
        raise ValueError('ONYX mission heading and text are required')
    if not data.get('client_display_name') or not data.get('personal_closing_note'):
        raise ValueError('client name and personal closing note are required')
    if not (root/data['cover_brand_art']).is_file():
        raise ValueError('cover_brand_art must be an existing approved asset')
    output = Path(output).resolve()
    if output.exists() and any((output/name).exists() for name in ('preview', 'source_data.json', data['output_stem']+'.pdf')):
        raise ValueError('Output must be a new or empty directory; use a new version')
    if any(output == p or output in p.parents for p in paths):
        raise ValueError('Output overlaps source assets')
    output.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont('Body', str(root/style['body_font'])))
    pdfmetrics.registerFont(TTFont('Display', str(root/style['display_font'])))
    pdf = output/(data['output_stem']+'.pdf')
    if Path(data['output_stem']).name != data['output_stem']:
        raise ValueError('output_stem must be a filename stem')
    c = Canvas(str(pdf), pagesize=tuple(style['canvas']), pageCompression=1, invariant=1)
    c.setTitle(data['collection_name']); c.setAuthor('ONYX'); c.setCreator('ONYX')
    placements, texts = [], []
    page_no = 0
    dark = False
    cache = {}
    stone_cache = {}
    def text(value, x, top, width, size=32, font='Body', color=None, max_height=300):
        if not value:
            return
        if FORBIDDEN.search(value):
            raise ValueError('Internal content in client copy')
        cmap = pdfmetrics.getFont(font).face.charToGlyph
        if any(ord(ch) not in cmap for ch in value if not ch.isspace()):
            raise ValueError('Unsupported font glyph')
        lines = []
        for paragraph in value.split('\n'):
            line = ''
            for word in paragraph.split():
                if pdfmetrics.stringWidth(word,font,size)>width:
                    raise ValueError('Unbreakable text overflow')
                candidate = (line+' '+word).strip()
                if pdfmetrics.stringWidth(candidate,font,size)>width:
                    lines.append(line); line=word
                else:
                    line=candidate
            lines.append(line)
        leading=size*1.4
        if len(lines)*leading>max_height or top+len(lines)*leading>1330:
            raise ValueError('Text overflow')
        c.setFont(font,size); c.setFillColor(HexColor(color or style['warm' if dark else 'dark']))
        for i,line in enumerate(lines):
            c.drawString(x,1350-top-size-i*leading,line)
        texts.append({'page':page_no,'text':value})
    def stone_field(x, top, width, height, mirror=False, light=False):
        key = (int(width), int(height), mirror, light)
        if key not in stone_cache:
            with Image.open(root/data['cover_brand_art']) as source:
                source = source.convert('RGB')
                texture = source.crop((0, 0, int(source.width * .30), source.height))
                texture = ImageOps.fit(texture, (max(1, int(width * 2)), max(1, int(height * 2))), method=Image.Resampling.LANCZOS)
                if mirror:
                    texture = ImageOps.mirror(texture)
                base = (242, 239, 232) if light else (17, 17, 17)
                amount = .88 if light else .34
                texture = Image.blend(texture, Image.new('RGB', texture.size, base), amount)
                buffer = io.BytesIO(); texture.save(buffer, format='JPEG', quality=92, subsampling=0)
                stone_cache[key] = ImageReader(buffer)
        c.drawImage(stone_cache[key], x, 1350-top-height, width, height)
    def monogram(cx, cy, size):
        accent = HexColor(style['accent'])
        c.setFillColor(accent); c.setFont('Display', size)
        c.drawCentredString(cx, cy - size * .29, 'O')
        half_h, half_w = size * .105, max(1.4, size * .010)
        diamond = c.beginPath(); diamond.moveTo(cx, cy + half_h); diamond.lineTo(cx + half_w, cy)
        diamond.lineTo(cx, cy - half_h); diamond.lineTo(cx - half_w, cy); diamond.close()
        c.drawPath(diamond, fill=1, stroke=0)
    def footer(is_dark):
        # Geometry mirrors the approved 1080x230 portfolio footer in the Brandbook.
        stone_field(0, 1120, 1080, 230, light=not is_dark)
        accent = HexColor(style['accent'])
        main = HexColor(style['warm'] if is_dark else style['dark'])
        secondary = accent
        monogram(170, 130, 86)
        c.setFillColor(accent); c.setFont('Display', 20); c.drawCentredString(170, 60, 'O N Y X')
        c.setStrokeColor(accent); c.setLineWidth(1); c.line(330, 160, 1010, 160)
        c.setFillColor(main); c.setFont('Body', 24); c.drawString(330, 106, data.get('footer_title', data['collection_name'].upper()+' COLLECTION'))
        c.setFillColor(secondary); c.setFont('Body', 18); c.drawString(330, 58, 'ONYX COLLECTION BOOK')
        c.setFont('Body', 16); c.drawRightString(1010, 58, f'{page_no:02}')
    def section_label(value, top=96):
        accent = HexColor(style['accent'])
        text(value.upper(), 72, top, 700, 28, 'Body', color=style['accent'], max_height=45)
        c.setStrokeColor(accent); c.setLineWidth(2); c.line(72, 1350-top-47, 232, 1350-top-47)
    def page(is_dark=False, footer_enabled=True):
        nonlocal page_no,dark
        if page_no:
            c.showPage()
        page_no+=1; dark=is_dark
        c.setFillColor(HexColor(style['dark' if dark else 'warm']))
        c.rect(0,0,1080,1350,fill=1,stroke=0)
        if footer_enabled:
            footer(is_dark)
    def photo(path,x,top,w,h,reason='story'):
        absolute=(root/path).resolve()
        if path not in cache:
            with Image.open(absolute) as source:
                im=ImageOps.exif_transpose(source).convert('RGB')
                im.thumbnail((style['image_max_edge'],)*2,Image.Resampling.LANCZOS)
                buf=io.BytesIO(); im.save(buf,format='JPEG',quality=style['jpeg_quality'],subsampling=0)
                cache[path]=(ImageReader(buf),im.size)
        reader,(iw,ih)=cache[path]
        scale=min(w/iw,h/ih); dw,dh=iw*scale,ih*scale
        px,py=x+(w-dw)/2,1350-top-h+(h-dh)/2
        c.drawImage(reader,px,py,dw,dh)
        placements.append({'page':page_no,'path':path,'reason':reason,'rect':[px,py,dw,dh], 'embedded_pixels':[iw,ih], 'crop':False})
    def logo():
        p=root/data['brand_logo']
        with Image.open(p) as im:
            w,h=im.size
        c.drawImage(str(p),72,1198,240,240*h/w,mask='auto')
    page(True)
    stone_field(0, 0, 250, 1120); stone_field(830, 0, 250, 1120, mirror=True)
    monogram(540, 1280, 55)
    c.setFillColor(HexColor(style['accent'])); c.setFont('Display', 20); c.drawCentredString(540, 1230, 'O N Y X')
    c.setStrokeColor(HexColor(style['accent'])); c.setLineWidth(1); c.line(365, 1190, 715, 1190)
    c.setFillColor(HexColor(style['warm'])); c.setFont('Display', 52); c.drawCentredString(540, 1130, data['collection_name'])
    text(data['collection_subtitle'], 300, 250, 480, 24, color=style['accent'], max_height=70)
    photo(data['cover_image'], 262, 360, 556, 740, 'intentional cover reuse')
    page(); section_label('Обращение от ONYX')
    text(data.get('onyx_mission_heading','Ваша коллекция'),72,210,940,83,'Display',max_height=270)
    text(data['onyx_mission_text'],76,590,870,35,max_height=420)
    page(True); section_label('О коллекции')
    text(data['collection_name'],72,210,940,76,'Display',max_height=120)
    text(data['collection_description'],76,380,890,30,max_height=305)
    text('ГДЕ ЭТО РАБОТАЕТ',76,710,850,18,color=style['accent'],max_height=45)
    for i,item in enumerate(data['collection_use_cases']):
        column, row = i % 2, i // 2
        bullet_x, item_x = 76+column*470, 108+column*470
        c.setFillColor(HexColor(style['accent'])); c.circle(bullet_x+8, 1350-(800+row*90), 7, fill=1, stroke=0)
        text(item, item_x, 785+row*90, 390, 27, color=style['warm'], max_height=80)
    page(); section_label('Личная нота')
    text(data.get('closing_heading','Ваша история'),72,230,940,82,'Display',max_height=250)
    text(data['personal_closing_note'],76,580,865,36,max_height=500)
    for layout,indices in story:
        page(layout=='hero', footer_enabled=True)
        if layout=='hero':
            c.setFillColor(HexColor(style['dark'])); c.rect(0, 230, 1080, 1120, fill=1, stroke=0)
            photo(photos[indices[0]]['path'], 0, 0, 1080, 1120)
        elif layout=='pair':
            text('В рабочем ритме',72,160,920,43,'Display',color=style['accent'],max_height=80)
            for i,idx in enumerate(indices):
                photo(photos[idx]['path'],72+i*480,300,456,720)
        elif layout=='space':
            photo(photos[indices[0]]['path'],355,135,653,850)
            text(photos[indices[0]]['caption'],76,480,270,43,'Display',color=style['accent'],max_height=150)
        elif layout=='caption':
            photo(photos[indices[0]]['path'],355,135,653,850)
            text(photos[indices[0]]['caption'],76,480,270,43,'Display',color=style['accent'],max_height=150)
        else:
            photo(photos[indices[0]]['path'],150,90,780,930)
    page(True); section_label('ONYX Selection', 70)
    photo(data['onyx_selection_image'],230,145,780,760,'intentional selection reuse')
    text(data['onyx_selection_note'],76,945,925,28,max_height=135)
    if data.get('motion_asset'):
        motion=data['motion_asset']
        if data['product_tier']!='Premium' or not motion['url'].startswith('https://'):
            raise ValueError('Motion requires Premium and an explicit HTTPS URL')
        text(motion['cta_label'],76,1160,850,29,max_height=70)
        c.linkURL(motion['url'],(76,110,950,190),relative=0)
    page(True); section_label('Следующие коллекции', 70)
    text('Продолжение вашей истории',72,185,940,56,'Display',max_height=100)
    for i,item in enumerate(data['next_collections']):
        top=420+i*280
        text(item['name'],76,top,900,54,'Display',max_height=90)
        text(item['description'],76,top+88,850,29,max_height=100)
        text('Скоро' if item['status']=='coming_soon' else item['cta_label'],76,top+205,850,22,color=style['accent'],max_height=40)
        if item.get('collection_url') and item['status']=='available':
            url=item['collection_url']
            if not url.startswith('https://'):
                raise ValueError('Only explicit HTTPS collection URLs supported')
            c.linkURL(url,(76,1350-top-250,950,1350-top-200),relative=0)
    c.save()
    reader=PdfReader(pdf)
    extracted='\n'.join(p.extract_text() for p in reader.pages)
    if FORBIDDEN.search(extracted):
        raise ValueError('PDF privacy check failed')
    if len(reader.pages)!=6+len(story):
        raise ValueError('Unexpected page count')
    counts=Counter(p['path'] for p in placements if p['reason']=='story')
    if counts!=Counter(p['path'] for p in photos):
        raise ValueError('Story coverage failed')
    if hashes != [digest(p) for p in paths]:
        raise ValueError('Source changed during build')
    if pdf.stat().st_size>15*1024*1024:
        raise ValueError('Mobile PDF exceeds 15 MiB budget')
    preview=output/'preview'; preview.mkdir()
    subprocess.run([poppler,'-scale-to','1350','-jpeg','-jpegopt','quality=92',str(pdf),str(preview/'page')],check=True,capture_output=True)
    previews=sorted(preview.glob('page-*.jpg'))
    if len(previews)!=len(reader.pages):
        raise ValueError('Preview count mismatch')
    for p in previews:
        with Image.open(p) as im:
            im.verify()
    manifest={'schema':'onyx.collection_book.v1','status':'AWAITING_DESIGN_APPROVAL',
        'order_id':data['order_id'],'book_version':data['book_version'],'created_at':data['created_at'],
        'source_data_sha256':digest(data_path),'renderer_sha256':digest(__file__),
        'style_sha256':digest(HERE/'template/style.json'),
        'brand_assets':[{ 'path':data['brand_logo'],'sha256':digest(root/data['brand_logo'])},
            {'path':data['cover_brand_art'],'sha256':digest(root/data['cover_brand_art'])}]+
            [{'path':style[k],'sha256':digest(root/style[k])} for k in ('body_font','display_font')],
        'pdf':{'file':pdf.name,'sha256':digest(pdf),'bytes':pdf.stat().st_size,'pages':len(reader.pages)},
        'sources':[{'path':p['path'],'absolute_path':str(path),'sha256':h} for p,path,h in zip(photos,paths,hashes)],
        'placements':placements,'previews':[{'file':str(p.relative_to(output)),'sha256':digest(p)} for p in previews],
        'qa':{'source_hashes_unchanged':True,'unique_story_coverage':True,'privacy_text_check':True,
              'text_overflow_guard':True,'all_previews_decoded':True,'visual_review':'PENDING',
              'source_approval':'See sample README; historical approval metadata conflicts.'}}
    # JSON is a YAML 1.2 subset; avoids an additional YAML dependency.
    (output/(data['output_stem']+'_manifest.yaml')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (output/'source_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(manifest['pdf']))
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--poppler',default='pdftoppm')
    args=parser.parse_args()
    render(args.data,args.output,args.root,args.poppler)
