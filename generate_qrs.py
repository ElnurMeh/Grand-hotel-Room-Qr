#!/usr/bin/env python3
"""Generate QR codes for all hotel rooms with room number in center."""
import urllib.request
from PIL import Image, ImageDraw, ImageFont
import os

# All 42 rooms
ROOMS = list(range(205, 218)) + list(range(301, 315)) + list(range(403, 418))

OUTPUT_DIR = '/Users/elnurmehtiyev/otel-demo/qr-rooms'
BASE_URL = 'https://elnurmeh.github.io/Grand-hotel-Room-Qr/demo.html'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Find a system font
FONT_CANDIDATES = [
    '/System/Library/Fonts/Helvetica.ttc',
    '/System/Library/Fonts/Avenir.ttc',
    '/System/Library/Fonts/Supplemental/Arial.ttf',
    '/Library/Fonts/Arial.ttf',
]
font_path = None
for fp in FONT_CANDIDATES:
    if os.path.exists(fp):
        font_path = fp
        break

print(f'Font: {font_path or "default"}')

BRAND_COLOR = '#243d2b'

for room in ROOMS:
    # Download QR
    encoded_url = urllib.parse.quote(f'{BASE_URL}?room={room}&reset=1', safe='')
    qr_url = f'https://api.qrserver.com/v1/create-qr-code/?data={encoded_url}&size=700x700&margin=30&ecc=H'
    out_path = f'{OUTPUT_DIR}/room-{room}.png'

    try:
        urllib.request.urlretrieve(qr_url, out_path)
    except Exception as e:
        print(f'ERR downloading {room}: {e}')
        continue

    # Open and overlay room number in center
    img = Image.open(out_path).convert('RGBA')
    w, h = img.size
    cx, cy = w // 2, h // 2

    draw = ImageDraw.Draw(img)

    # White rounded rectangle in center with brand border
    rect_w = 160
    rect_h = 90
    box = [cx - rect_w // 2, cy - rect_h // 2, cx + rect_w // 2, cy + rect_h // 2]
    draw.rounded_rectangle(box, radius=14, fill='white', outline=BRAND_COLOR, width=5)

    # Room number text in center
    text = str(room)
    if font_path:
        font = ImageFont.truetype(font_path, 56)
    else:
        font = ImageFont.load_default()

    draw.text((cx, cy), text, fill=BRAND_COLOR, font=font, anchor='mm')

    img.save(out_path)
    print(f'OK: room-{room}.png')

print(f'\nDone! {len(ROOMS)} QR codes in {OUTPUT_DIR}')
