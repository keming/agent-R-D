from PIL import Image
import pytesseract
import os

base = r'C:\Users\keming\Downloads'
prefix = 'ChatGPT Image Jun 16, 2026'
times = ['11_08_13 AM', '11_08_08 AM', '11_08_04 AM', '11_07_56 AM',
         '11_07_52 AM', '11_07_49 AM', '11_07_45 AM', '11_07_42 AM',
         '11_07_38 AM', '11_07_34 AM', '11_07_30 AM', '11_07_26 AM', '11_07_20 AM']

for t in times:
    fname = f'{prefix}, {t}.png'
    fpath = os.path.join(base, fname)
    if os.path.exists(fpath):
        img = Image.open(fpath)
        # OCR with Chinese
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        # Get first 5 meaningful lines
        preview = ' | '.join(lines[:5])
        print(f'[{t[:5]}]: {preview[:200]}')
        print()
