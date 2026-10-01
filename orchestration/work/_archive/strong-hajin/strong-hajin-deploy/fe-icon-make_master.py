from PIL import Image, ImageDraw, ImageFilter
S = __import__('sys').argv[1]
src = Image.open(f'{S}/src.iconset/icon_512x512@2x.png').convert('RGBA')  # 원본 icons-prod/icon.icns 의 1024 표현
# M bbox (흰 바탕에서 채도 있는 픽셀)
px = src.load(); xs=[]; ys=[]
for y in range(1024):
    for x in range(1024):
        r,g,b,a = px[x,y]
        if a > 0 and 255 - min(r,g,b) > 8: xs.append(x); ys.append(y)
bx0,bx1,by0,by1 = min(xs),max(xs)+1,min(ys),max(ys)+1
PAD = 12
m = src.crop((bx0-PAD, by0-PAD, bx1+PAD, by1+PAD))
mw, mh = bx1-bx0, by1-by0
CANVAS, BODY, R = 1024, 824, 185
MARGIN = (CANVAS - BODY)//2
TARGET_W = round(BODY * 0.60)
k = TARGET_W / mw
assert k < 1, k
m2 = m.resize((round(m.width*k), round(m.height*k)), Image.LANCZOS)
# 몸통 (4x 슈퍼샘플)
SS = 4
mask = Image.new('L', (CANVAS*SS, CANVAS*SS), 0)
ImageDraw.Draw(mask).rounded_rectangle((MARGIN*SS, MARGIN*SS, (MARGIN+BODY)*SS-1, (MARGIN+BODY)*SS-1), R*SS, fill=255)
mask = mask.resize((CANVAS, CANVAS), Image.LANCZOS)
# 옅은 그림자 (macOS 격자 여백 안)
sh = Image.new('RGBA', (CANVAS, CANVAS), (0,0,0,0))
sh_alpha = mask.point(lambda v: v*0.22).filter(ImageFilter.GaussianBlur(14))
sh_alpha = sh_alpha.transform(sh_alpha.size, Image.AFFINE, (1,0,0,0,1,-8))
sh.putalpha(sh_alpha)
body = Image.new('RGBA', (CANVAS, CANVAS), (255,255,255,0)); body.putalpha(mask)
body = Image.new('RGBA', (CANVAS, CANVAS), (255,255,255,255)).copy(); body.putalpha(mask)
out = Image.alpha_composite(sh, body)
layer = Image.new('RGBA', (CANVAS, CANVAS), (0,0,0,0))
ox = round(CANVAS/2 - (PAD + mw/2)*k); oy = round(CANVAS/2 - (PAD + mh/2)*k)
layer.paste(m2, (ox, oy))
# 흰 바탕 조각이므로 몸통 마스크로 한정해 합성
lm = Image.new('L', (CANVAS,CANVAS), 0); lm.paste(255, (ox, oy, ox+m2.width, oy+m2.height))
from PIL import ImageChops
layer.putalpha(ImageChops.multiply(lm, mask))
out = Image.alpha_composite(out, layer)
out.save(f'{S}/icon-master-1024.png')
print(dict(src_M=(bx0,by0,mw,mh), scale=round(k,4), M=(round(mw*k),round(mh*k)), M_pos=(ox+round(PAD*k), oy+round(PAD*k)), M_ratio_body=round(mw*k/BODY,3), M_ratio_body_h=round(mh*k/BODY,3), src_ratio=round(mw/1024,3)))
