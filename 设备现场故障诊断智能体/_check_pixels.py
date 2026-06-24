from PIL import Image
import os

base = r'C:\Users\keming\Downloads'
prefix = 'ChatGPT Image Jun 16, 2026'
times = [
    ('11_08_13 AM', '13'),
    ('11_08_08 AM', '12'),
    ('11_08_04 AM', '11'),
    ('11_07_56 AM', '10'),
    ('11_07_52 AM', '09'),
    ('11_07_49 AM', '08'),
    ('11_07_45 AM', '07'),
    ('11_07_42 AM', '06'),
    ('11_07_38 AM', '05'),
    ('11_07_34 AM', '04'),
    ('11_07_30 AM', '03'),
    ('11_07_26 AM', '02'),
    ('11_07_20 AM', '01'),
]

for t, label in times:
    fname = f'{prefix}, {t}.png'
    fpath = os.path.join(base, fname)
    if os.path.exists(fpath):
        img = Image.open(fpath)
        # Get dominant colors from different regions (top, middle, bottom)
        w, h = img.size
        # Sample 5 horizontal strips
        regions = {
            'top': img.crop((0, 0, w, h//5)).resize((1,1)).getpixel((0,0)),
            'mid_top': img.crop((0, h//5, w, 2*h//5)).resize((1,1)).getpixel((0,0)),
            'mid': img.crop((0, 2*h//5, w, 3*h//5)).resize((1,1)).getpixel((0,0)),
            'mid_bot': img.crop((0, 3*h//5, w, 4*h//5)).resize((1,1)).getpixel((0,0)),
            'bottom': img.crop((0, 4*h//5, w, h)).resize((1,1)).getpixel((0,0)),
        }
        colors = {k: f'RGB({v[0]},{v[1]},{v[2]})' for k,v in regions.items()}
        size_kb = os.path.getsize(fpath) // 1024
        print(f'#{label}: {size_kb}KB | {colors}')
