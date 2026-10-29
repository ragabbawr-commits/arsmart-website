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
# نهاية الصورة: أول مسافة بيضا طولها >= 1.8% من الطول (قبل سطر "المتجر / ...")
gap = int(H * 0.018)
run = 0
while y < H:
    run = run + 1 if not content[y] else 0
    if run >= gap:
        break
    y += 1
end = y - run + 1

# أسهم السلايدر البرتقاني على الجناب: نمسح المربع بتاعها
W = a.shape[1]
a = a.copy()
orange = (a[..., 0] > 200) & (a[..., 1] > 110) & (a[..., 1] < 190) & (a[..., 2] < 80)
for x0, x1 in [(0, int(W * 0.145)), (int(W * 0.865), W)]:
    ys, xs = np.where(orange[start:end, x0:x1])
    if len(ys):
        cy = start + int(ys.mean())
        h2 = int(W * 0.075)
        a[max(start, cy - h2):cy + h2, x0:x1] = 255
        # خط ظل السلايدر حوالين السهم: رمادي فاتح في نفس الشريط يبقى أبيض
        band = a[max(start, cy - 2 * h2):cy + 2 * h2, x0:x1]
        band[band.min(axis=2) > 200] = 255
# الظلال الرمادي الفاتح جداً حوالين الصورة تبقى أبيض
light = (a.min(axis=2) > 243) & ((a.max(axis=2) - a.min(axis=2)) < 10)
a[light] = 255
im = Image.fromarray(a.astype("uint8"))
reg = a[start:end]
cols = np.where((reg < 238).any(axis=2).any(axis=0))[0]
p = im.crop((cols.min(), start, cols.max() + 1, end))
w, h = p.size
s = int(max(w, h) * 1.12)
c = Image.new("RGB", (s, s), "white")
c.paste(p, ((s - w) // 2, (s - h) // 2))
c.resize((800, 800), Image.LANCZOS).save(out, quality=88)
print(out, "crop", (cols.min(), start, cols.max() + 1, end))
