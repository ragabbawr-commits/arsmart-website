# يقص صورة المنتج من سكرين شوت صفحة منتج (زي fastegy) ويحطها على خلفية بيضا مربعة
# الاستخدام: python3 _tools/crop_shot.py <screenshot> <out.jpg>
import sys
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
a = np.asarray(im).astype(int)
H = a.shape[0]
row_mean = a.mean(axis=(1, 2))

# 1) نهاية الهيدر الغامق: آخر صف غامق في أول 30% من الصورة
dark = np.where(row_mean[: int(H * 0.3)] < 120)[0]
y = (dark.max() + 4) if len(dark) else 0  # +4 يتخطى حافة الهيدر المتدرجة
# 2) نتخطى ظل الهيدر (صفوف رمادي متساوي) لحد أول صف فيه تفاصيل
row_std = a.std(axis=(1, 2))
while y < H and row_std[y] < 6:
    y += 1
top = y

# 3) صفوف فيها محتوى (مش أبيض)
content = ((a < 238).any(axis=2).sum(axis=1) > 3) & (row_std > 6)
# أول صف فيه محتوى بعد top = بداية صورة المنتج
y = top
while y < H and not content[y]:
    y += 1
start = y
# نهاية الصورة: أول مسافة بيضا طولها >= 4% من الطول
gap = int(H * 0.04)
run = 0
while y < H:
    run = run + 1 if not content[y] else 0
    if run >= gap:
        break
    y += 1
end = y - run + 1

reg = a[start:end]
cols = np.where((reg < 238).any(axis=2).any(axis=0))[0]
p = im.crop((cols.min(), start, cols.max() + 1, end))
w, h = p.size
s = int(max(w, h) * 1.12)
c = Image.new("RGB", (s, s), "white")
c.paste(p, ((s - w) // 2, (s - h) // 2))
c.resize((800, 800), Image.LANCZOS).save(out, quality=88)
print(out, "crop", (cols.min(), start, cols.max() + 1, end))
