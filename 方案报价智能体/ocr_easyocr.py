import easyocr
from PIL import Image
import json

reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
img_path = r"D:\cursor\agentic AI for enterprise\agent-R-D\方案报价智能体\微信图片_20260611130318_79_920.png"
results = reader.readtext(img_path, detail=1)

print(f"Image size: {Image.open(img_path).size}")
print(f"Total text regions found: {len(results)}")
print()

img = Image.open(img_path)
output = []
for (bbox, text, conf) in results:
    xs = [p[0] for p in bbox]
    ys = [p[1] for p in bbox]
    x1, y1 = int(min(xs)), int(min(ys))
    x2, y2 = int(max(xs)), int(max(ys))
    pad = 5
    rx1 = max(0, x1 - pad)
    ry1 = max(0, y1 - pad)
    rx2 = min(img.width, x2 + pad)
    ry2 = min(img.height, y2 + pad)
    region = img.crop((rx1, ry1, rx2, ry2))
    pixels = list(region.getdata())
    if pixels:
        r_avg = sum(p[0] for p in pixels) / len(pixels)
        g_avg = sum(p[1] for p in pixels) / len(pixels)
        b_avg = sum(p[2] for p in pixels) / len(pixels)
        is_red = (r_avg > 150 and g_avg < 120 and b_avg < 120 and r_avg > g_avg * 1.3)
        output.append({
            'text': text, 'y': y1, 'x': x1,
            'conf': round(conf, 3),
            'r': round(r_avg, 1), 'g': round(g_avg, 1), 'b': round(b_avg, 1),
            'is_red': is_red
        })

output.sort(key=lambda o: (o['y'], o['x']))
print(json.dumps(output, ensure_ascii=False, indent=2))
