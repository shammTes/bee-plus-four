#!/usr/bin/env python3
"""Draw the 4 + Eritrean-flag ribbon launcher icon."""
from pathlib import Path
import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GREEN, BLUE, RED = (0, 165, 80), (58, 137, 201), (234, 28, 36)
GOLD, CREAM, BG = (255, 199, 44), (255, 250, 240), (12, 48, 42)

def make_icon(size=1024):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad, r = int(size * 0.02), int(size * 0.22)
    box = [pad, pad, size - pad, size - pad]
    d.rounded_rectangle(box, radius=r, fill=(*BG, 255))
    inset = int(size * 0.045)
    d.rounded_rectangle([inset, inset, size - inset, size - inset], radius=int(r * 0.92),
                        outline=(*GOLD, 235), width=max(4, size // 80))
    font_path = next((p for p in (
        '/usr/share/fonts/truetype/lato/Lato-Black.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    ) if Path(p).exists()), None)
    font = ImageFont.truetype(font_path, int(size * 0.74)) if font_path else ImageFont.load_default()
    bbox = d.textbbox((0, 0), '4', font=font)
    tx = (size - (bbox[2] - bbox[0])) / 2 - bbox[0] - size * 0.02
    ty = (size - (bbox[3] - bbox[1])) / 2 - bbox[1] - size * 0.03
    sh = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((tx + size * 0.012, ty + size * 0.018), '4', font=font, fill=(0, 0, 0, 150))
    img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(max(2, size // 42))))
    num = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(num).text((tx, ty), '4', font=font, fill=(*CREAM, 255))
    img = Image.alpha_composite(img, num)
    ribbon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ribbon)
    ang = math.atan(-0.50)
    nx, ny = -math.sin(ang), math.cos(ang)
    cx, cy, sw = size * 0.55, size * 0.58, size * 0.072
    def band(offset, color, width):
        def pt(t, off):
            return (cx + t * math.cos(ang) + nx * off, cy + t * math.sin(ang) + ny * off)
        t0, t1 = -size * 1.6, size * 1.6
        rd.polygon([pt(t0, offset - width / 2), pt(t1, offset - width / 2),
                    pt(t1, offset + width / 2), pt(t0, offset + width / 2)], fill=color)
    band(0, (*GOLD, 255), sw * 3 + size * 0.024)
    band(-sw, (*GREEN, 255), sw)
    band(0, (*RED, 255), sw)
    band(sw, (*BLUE, 255), sw)
    img = Image.alpha_composite(img, ribbon)
    top = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(top).text((tx, ty), '4', font=font, fill=(*CREAM, 255))
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rectangle([0, 0, size, int(size * 0.465)], fill=255)
    top.putalpha(Image.composite(top.split()[-1], Image.new('L', (size, size), 0), mask))
    img = Image.alpha_composite(img, top)
    kd = ImageDraw.Draw(img)
    kx, ky, rad = int(size * 0.64), int(size * 0.515), int(size * 0.048)
    kd.ellipse([kx - rad, ky - rad, kx + rad, ky + rad], fill=(*GOLD, 255),
               outline=(160, 110, 12, 255), width=max(2, size // 170))
    ir = int(rad * 0.40)
    kd.ellipse([kx - ir, ky - ir, kx + ir, ky + ir], fill=(*GREEN, 255))
    clip = Image.new('L', (size, size), 0)
    ImageDraw.Draw(clip).rounded_rectangle(box, radius=r, fill=255)
    img.putalpha(Image.composite(img.split()[-1], Image.new('L', (size, size), 0), clip))
    return img

def write(root='.'):
    icon = make_icon(1024)
    sizes = {'mipmap-mdpi': 48, 'mipmap-hdpi': 72, 'mipmap-xhdpi': 96,
             'mipmap-xxhdpi': 144, 'mipmap-xxxhdpi': 192}
    res = Path(root) / 'android/app/src/main/res'
    for name, s in sizes.items():
        d = res / name
        d.mkdir(parents=True, exist_ok=True)
        icon.resize((s, s), Image.Resampling.LANCZOS).save(d / 'ic_launcher.png')
    print('wrote launcher icons')

if __name__ == '__main__':
    write(sys.argv[1] if len(sys.argv) > 1 else '.')
