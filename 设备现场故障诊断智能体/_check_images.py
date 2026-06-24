from PIL import Image
import os
from datetime import datetime

base = r'C:\Users\keming\Downloads'
prefix = 'ChatGPT Image Jun 16, 2026'
times = ['11_08_13 AM', '11_08_08 AM', '11_08_04 AM', '11_07_56 AM',
         '11_07_52 AM', '11_07_49 AM', '11_07_45 AM', '11_07_42 AM',
         '11_07_38 AM', '11_07_34 AM', '11_07_30 AM', '11_07_26 AM', '11_07_20 AM']

for t in times:
    fname = f'{prefix}, {t}.png'
    fpath = os.path.join(base, fname)
    if os.path.exists(fpath):
        stat = os.stat(fpath)
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%H:%M:%S')
        size = stat.st_size
        try:
            img = Image.open(fpath)
            dims = f'{img.size[0]}x{img.size[1]}'
        except:
            dims = '?'
        print(f'{mtime} | {size//1024:>4}KB | {dims:>10} | {fname}')
    else:
        print(f'NOT FOUND: {fname}')
