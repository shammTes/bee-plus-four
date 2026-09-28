#!/usr/bin/env python3
import os
import subprocess
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pillow"])
    from PIL import Image, ImageDraw, ImageFont


def make_icon(path, label, bg=(13, 148, 136), size=192):
    img = Image.new("RGB", (size, size), bg)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size // 3
        )
    except Exception:
        font = ImageFont.load_default()
    bbox = d.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((size - tw) / 2, (size - th) / 2 - 4), label, fill=(255, 255, 255), font=font)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "PNG")


def write_set(base, label, bg):
    for dens, s in [
        ("mipmap-mdpi", 48),
        ("mipmap-hdpi", 72),
        ("mipmap-xhdpi", 96),
        ("mipmap-xxhdpi", 144),
        ("mipmap-xxxhdpi", 192),
    ]:
        make_icon(f"{base}/{dens}/ic_launcher.png", label, bg=bg, size=s)


def main():
    write_set("android/app/src/main/res", "4", (13, 148, 136))
    write_set("android/app/src/student/res", "4", (13, 148, 136))
    write_set("android/app/src/seller/res", "S", (13, 148, 136))
    write_set("android/app/src/master/res", "M", (15, 23, 42))
    print("icons ok")


if __name__ == "__main__":
    main()
