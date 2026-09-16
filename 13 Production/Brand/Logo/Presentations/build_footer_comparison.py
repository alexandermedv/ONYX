from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
R=Path(r'D:\AI\ONYX'); B=R/'13 Production/Brand'
S=3
def glyph(text,font,size,color):
    f=ImageFont.truetype(str(font),size*S)
    box=f.getbbox(text)
    im=Image.new('RGBA',(box[2]-box[0],box[3]-box[1]))
    ImageDraw.Draw(im).text((-box[0],-box[1]),text,font=f,fill=color)
    return im
ser=B/'Typography/CormorantGaramond-Variable.ttf'
sans=Path(r'C:\Windows\Fonts\segoeui.ttf')
gold=(218,177,68,255)
layer=Image.new('RGBA',(1080*S,230*S))
ring=glyph('O',ser,86,gold)
ring.thumbnail((58*S,58*S),Image.Resampling.LANCZOS)
cx=170*S; top=70*S; bottom=160*S
layer.alpha_composite(ring,(cx-ring.width//2,top))
d=ImageDraw.Draw(layer); cy=top+ring.height//2
d.polygon([(cx,cy-18*S),(cx+2*S,cy),(cx,cy+18*S),(cx-2*S,cy)],fill=gold)
word=glyph('O N Y X',ser,20,gold)
layer.alpha_composite(word,(cx-word.width//2,bottom-word.height))
d.line((330*S,top,1010*S,top),fill=gold,width=2*S)
title=glyph('BUSINESS COLLECTION',sans,25,(246,244,239,255))
sub=glyph('PORTFOLIO PREVIEW',sans,19,gold)
layer.alpha_composite(title,(330*S,105*S))
layer.alpha_composite(sub,(330*S,bottom-sub.height))
raw=Image.open(B/'Logo/Presentations/ONYX_MONOGRAM_ONYX_SILK_PRESENTATION_V1.png').convert('RGB')
tex=ImageOps.fit(raw.crop((0,0,int(raw.width*.30),raw.height)),(1080*S,230*S),method=Image.Resampling.LANCZOS)
tex=Image.blend(tex,Image.new('RGB',tex.size,(17,17,17)),.34)
reference=Image.open(R/'13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_01_HERO.jpg').convert('RGB')
canvas=Image.new('RGB',(2190,1420),(25,25,25)); draw=ImageDraw.Draw(canvas)
for i,label in enumerate(['A / PURE BLACK','B / ONYX STONE']):
    foot=(Image.new('RGB',tex.size,(8,8,8)) if i==0 else tex.copy()).convert('RGBA')
    foot.alpha_composite(layer)
    panel=reference.copy(); panel.paste(foot.convert('RGB').resize((1080,230),Image.Resampling.LANCZOS),(0,1120))
    x=i*1110; canvas.paste(panel,(x,70))
    draw.text((x+24,23),label,font=ImageFont.truetype(str(sans),24),fill='white')
canvas.save('footer_checked.png')
canvas.save('footer_checked.jpg',quality=97,subsampling=0)
print('Common foreground layer: ring top = rule top = 70; wordmark bottom = subtitle bottom = 160. Both panels use identical layer.')
