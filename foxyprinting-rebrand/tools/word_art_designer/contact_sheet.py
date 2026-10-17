"""Contact sheet of the generated masks (for checking by eye). Usage: contact_sheet.py masks_dir out.jpg [start] [count]"""
import json, sys
from PIL import Image, ImageDraw
r = json.load(open(sys.argv[1] + '/report.json')); ok = [x for x in r if 'file' in x]
print(len(r), len(ok), [x['handle'] for x in r if 'error' in x])
start = int(sys.argv[3]) if len(sys.argv) > 3 else 0; count = int(sys.argv[4]) if len(sys.argv) > 4 else len(ok)
ok = ok[start:start + count]
T = 130; cols = 10; rows = (len(ok) + cols - 1) // cols
sheet = Image.new('RGB', (cols * T, rows * T), 'white'); d = ImageDraw.Draw(sheet)
for i, x in enumerate(ok):
    m = Image.open(x['file']).convert('RGBA'); bg = Image.new('RGBA', m.size, (225, 225, 225, 255)); bg.alpha_composite(m); bg = bg.convert('RGB'); bg.thumbnail((T - 6, T - 18))
    sheet.paste(bg, ((i % cols) * T + 3, (i // cols) * T + 3)); d.text(((i % cols) * T + 3, (i // cols) * T + T - 14), str(start + i), fill='black')
sheet.save(sys.argv[2], quality=85); print(sheet.size)
