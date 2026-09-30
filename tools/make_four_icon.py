#!/usr/bin/env python3
"""3D-embossed numeral 4 with Eritrean flag stripes clipped INSIDE the glyph."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps

GREEN, BLUE, RED = (0, 150, 70), (30, 110, 190), (220, 16, 28)
GOLD, CREAM = (255, 199, 44), (255, 250, 240)
TILE = (255, 244, 228)  # light clay
INK = (36, 24, 16)

def _font(size):
    for p in (
        '/usr/share/fonts/truetype/lato/Lato-Black.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/System/Library/Fonts/Supplemental/Impact.ttf',
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def make_icon(size=1024):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad, r = int(size * 0.03), int(size * 0.22)
    box = [pad, pad, size - pad, size - pad]
    d.rounded_rectangle(box, radius=r, fill=(*TILE, 255))
    inset = int(size * 0.05)
    d.rounded_rectangle([inset, inset, size - inset, size - inset], radius=int(r * 0.88),
                        outline=(*GOLD, 255), width=max(5, size // 70))

    font = _font(int(size * 0.82))
    tmp = ImageDraw.Draw(Image.new('L', (size, size)))
    bbox = tmp.textbbox((0, 0), '4', font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1] - size * 0.02

    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).text((tx, ty), '4', font=font, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))

    # Flag fill: green over blue, red triangle from the left, gold seam
    flag = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    fd = ImageDraw.Draw(flag)
    fd.rectangle([0, 0, size, size // 2], fill=(*GREEN, 255))
    fd.rectangle([0, size // 2, size, size], fill=(*BLUE, 255))
    fd.polygon([(0, 0), (int(size * 0.62), size // 2), (0, size)], fill=(*RED, 255))
    seam = max(3, size // 90)
    fd.line([(0, size // 2), (size, size // 2)], fill=(*GOLD, 220), width=seam)
    kx, ky, rad = int(size * 0.28), int(size * 0.50), int(size * 0.055)
    fd.ellipse([kx - rad, ky - rad, kx + rad, ky + rad], fill=(*GOLD, 255))
    ir = int(rad * 0.42)
    fd.ellipse([kx - ir, ky - ir, kx + ir, ky + ir], fill=(*GREEN, 255))

    clipped = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    clipped.paste(flag, mask=mask)

    shadow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((tx + size * 0.018, ty + size * 0.022), '4', font=font, fill=(40, 22, 10, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(max(2, size // 55)))
    hi = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(hi).text((tx - size * 0.012, ty - size * 0.014), '4', font=font, fill=(255, 255, 255, 70))
    hi = hi.filter(ImageFilter.GaussianBlur(max(1, size // 90)))
    hi.putalpha(ImageChops.multiply(ImageChops.multiply(hi.split()[-1], mask), Image.new('L', (size, size), 90)))

    outline = mask.filter(ImageFilter.MaxFilter(max(3, size // 90 * 2 + 1)))
    ring = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ring.paste((*GOLD, 255), mask=ImageChops.subtract(outline, mask))

    img = Image.alpha_composite(img, shadow)
    img = Image.alpha_composite(img, ring)
    img = Image.alpha_composite(img, clipped)
    img = Image.alpha_composite(img, hi)

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
    preview = Path(root) / 'design' / 'four_icon_1024.png'
    preview.parent.mkdir(parents=True, exist_ok=True)
    icon.save(preview)
    print('wrote launcher icons +', preview)

if __name__ == '__main__':
    write(sys.argv[1] if len(sys.argv) > 1 else '.')
