import pytesseract
from PIL import Image
import json
import sys

img = Image.open(r"D:\cursor\agentic AI for enterprise\agent-R-D\方案报价智能体\微信图片_20260611130318_79_920.png")
print(f"Image size: {img.size}")

# 获取详细数据（含位置和置信度）
data = pytesseract.image_to_data(img, lang='chi_sim+eng', output_type=pytesseract.Output.DICT)

# 分析每个文字块的平均颜色
results = []
n = len(data['text'])
i = 0
while i < n:
    text = data['text'][i].strip()
    if text:
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        # 扩大采样区域以获取更好的颜色信息
        pad = 3
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img.width, x + w + pad)
        y2 = min(img.height, y + h + pad)
        
        region = img.crop((x1, y1, x2, y2))
        pixels = list(region.getdata())
        
        if pixels:
            r_avg = sum(p[0] for p in pixels) / len(pixels)
            g_avg = sum(p[1] for p in pixels) / len(pixels)
            b_avg = sum(p[2] for p in pixels) / len(pixels)
            
            # 检测红色：R 高，G 和 B 低
            is_red = (r_avg > 150 and g_avg < 100 and b_avg < 100 and r_avg > g_avg * 1.5)
            
            # 检测深红色
            is_dark_red = (r_avg > 100 and g_avg < 80 and b_avg < 80 and r_avg > g_avg * 1.3)
            
            color_info = {
                'text': text,
                'x': x, 'y': y,
                'r': round(r_avg, 1), 'g': round(g_avg, 1), 'b': round(b_avg, 1),
                'is_red': is_red or is_dark_red
            }
            results.append(color_info)
    i += 1

# 按 y 坐标排序，方便阅读
results.sort(key=lambda r: (r['y'], r['x']))

print(json.dumps(results, ensure_ascii=False, indent=2))
