#!/usr/bin/env python3
"""
استخراج صورة العاملة من ملف السيرة الذاتية (PDF) بدون أي نماذج ذكاء اصطناعي خارجية.

الطريقة:
1) لو الـ PDF فيه صور مدمجة: نختار صورة الوجه (الأقرب لشكل صورة شخصية، وفيها لون بشرة)،
   وإن لم توجد فصورة الجسم كاملة. نتجاهل الشعارات واللافتات والخلفيات السوداء.
2) لو الـ PDF صفحة مصوّرة (Scan): نحوّل الصفحة لصورة ونبحث عن كتلة صورة (منطقة كثيفة وغير مسطّحة
   بحجم مناسب) ونقتصها.
لو ما لقينا صورة مقنعة نرجّع False وما نكتب أي ملف (الكرت يعرض أيقونة المهنة بدل الصورة).
"""
import os, re, subprocess, tempfile, shutil

try:
    import numpy as np
    from PIL import Image
except Exception:  # لو المكتبات غير مثبّتة: لا صور، والباقي يشتغل عادي
    np = None
    Image = None

MAX_SIDE = 640


def _skin_fraction(arr):
    """نسبة بكسلات لون البشرة (YCbCr) — تقريبية، تكفي للتفضيل بين الصور."""
    r, g, b = arr[..., 0].astype(float), arr[..., 1].astype(float), arr[..., 2].astype(float)
    cb = 128 - 0.168736 * r - 0.331264 * g + 0.5 * b
    cr = 128 + 0.5 * r - 0.418688 * g - 0.081312 * b
    m = (cr > 133) & (cr < 175) & (cb > 75) & (cb < 128) & (r > 40)
    return float(m.mean())


def _is_flat(arr):
    g = arr.mean(axis=2)
    return g.std() < 12 or g.mean() < 22


def _list_images(pdf, page=1):
    try:
        out = subprocess.run(["pdfimages", "-list", "-f", str(page), "-l", str(page), pdf],
                             capture_output=True, text=True, timeout=60).stdout.splitlines()
    except Exception:
        return []
    rows = []
    for line in out[2:]:
        p = line.split()
        if len(p) < 13:
            continue
        try:
            rows.append({"idx": int(p[1]), "type": p[2], "w": int(p[3]), "h": int(p[4]), "xppi": int(p[12])})
        except Exception:
            continue
    return rows


def _page_size(pdf):
    try:
        out = subprocess.run(["pdfinfo", "-f", "1", "-l", "1", pdf], capture_output=True, text=True, timeout=30).stdout
        m = re.search(r"Page\s+1\s+size:\s+([\d.]+)\s+x\s+([\d.]+)", out) or re.search(r"Page size:\s+([\d.]+)\s+x\s+([\d.]+)", out)
        return float(m.group(1)), float(m.group(2))
    except Exception:
        return 595.0, 842.0


def _from_embedded(pdf, tmp):
    """الصفحة الأولى فقط. ممنوع الصفحة الثانية: في نماذج بنغلاديش هي صورة جواز السفر!"""
    pw, ph = _page_size(pdf)
    heads, bodies = [], []
    for page in (1,):
        rows = _list_images(pdf, page)
        if not rows:
            continue
        prefix = os.path.join(tmp, "e%d" % page)
        try:
            subprocess.run(["pdfimages", "-j", "-f", str(page), "-l", str(page), pdf, prefix], check=True,
                           capture_output=True, timeout=120)
        except Exception:
            continue
        files = {}
        for f in os.listdir(tmp):
            m = re.match(r"e%d-(\d+)\." % page, f)
            if m:
                files[int(m.group(1))] = os.path.join(tmp, f)
        for r in rows:
            if r["type"] != "image" or r["idx"] not in files:
                continue
            w, h = r["w"], r["h"]
            if min(w, h) < 120:
                continue
            ratio = w / float(h)
            if ratio > 1.7 or ratio < 0.45:
                continue  # لافتة/شعار/شريط
            cover = (w / max(r["xppi"], 1) * 72) / pw
            if cover > 0.8:
                continue  # صورة بعرض الصفحة = صفحة مصوّرة أو خلفية، مش صورة شخص
            try:
                im = Image.open(files[r["idx"]]).convert("RGB")
            except Exception:
                continue
            arr = np.asarray(im.resize((max(1, w // 4), max(1, h // 4))))
            if _is_flat(arr):
                continue
            item = (_skin_fraction(arr), w * h, im)
            (bodies if ratio < 0.78 else heads).append(item)
    pool = bodies if bodies else heads  # نفضّل صورة الجسم كاملة، ولو مش موجودة فصورة الوجه
    if not pool:
        return None
    pool.sort(key=lambda t: (-t[1], -t[0]))  # الأكبر حجمًا أولًا
    return pool[0][2]


# ---------------------------------------------------------------- صفحة مصوّرة (Scan)
def _render(pdf, tmp, dpi=110):
    base = os.path.join(tmp, "pg")
    try:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-f", "1", "-l", "1", "-png", pdf, base],
                       check=True, capture_output=True, timeout=120)
        f = next(os.path.join(tmp, x) for x in sorted(os.listdir(tmp)) if x.startswith("pg") and x.endswith(".png"))
        return Image.open(f).convert("RGB")
    except Exception:
        return None


def _components(page, top, nonwhite_min, std_min, close):
    """كتل كثيفة في الصفحة (صور)، ترجع [(x0,y0,x1,y1,cells)] بالبكسل."""
    W, H = page.size
    arr = np.asarray(page).astype(float)
    lum = arr.mean(axis=2)
    cell = 8
    gh, gw = int(H * top) // cell, W // cell
    L = lum[:gh * cell, :gw * cell].reshape(gh, cell, gw, cell)
    nonwhite = (L < 232).mean(axis=(1, 3))
    std = L.std(axis=(1, 3))
    mean = L.mean(axis=(1, 3))
    d = (nonwhite > nonwhite_min) & ((std > std_min) | (mean < 90))
    for _ in range(close):
        e = d.copy()
        e[1:, :] |= d[:-1, :]; e[:-1, :] |= d[1:, :]; e[:, 1:] |= d[:, :-1]; e[:, :-1] |= d[:, 1:]
        d = e
    seen = np.zeros_like(d, dtype=bool)
    out = []
    for y in range(gh):
        for x in range(gw):
            if not d[y, x] or seen[y, x]:
                continue
            stack = [(y, x)]; seen[y, x] = True
            ys, xs = [], []
            while stack:
                cy, cx = stack.pop(); ys.append(cy); xs.append(cx)
                for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                    if 0 <= ny < gh and 0 <= nx < gw and d[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; stack.append((ny, nx))
            n = len(xs)
            x0, y0, x1, y1 = min(xs), min(ys), max(xs) + 1, max(ys) + 1
            out.append((x0 * cell, y0 * cell, x1 * cell, y1 * cell, n / float((x1 - x0) * (y1 - y0))))
    return out


def _photo_like(crop_arr):
    """الصور فيها درجات رمادي متوسطة كثيرة، أما النص والجداول فأبيض/أسود تقريبًا."""
    g = crop_arr.mean(axis=2)
    mid = ((g > 55) & (g < 200)).mean()
    return mid > 0.38


def _pick(page, comps, head_only):
    W, H = page.size
    best = None
    for x0, y0, x1, y1, fill in comps:
        w, h = x1 - x0, y1 - y0
        area = w * h / float(W * H)
        ratio = w / float(h)
        if w > 0.4 * W or fill < 0.5 or not (0.006 <= area <= 0.4):
            continue
        crop_arr = np.asarray(page.crop((x0, y0, x1, y1)))
        if not _photo_like(crop_arr):
            continue
        if head_only == "body":
            if not (0.3 <= ratio <= 0.78) or area < 0.03 or _skin_fraction(crop_arr) < 0.03:
                continue
            score = area
        elif head_only:
            if not (0.6 <= ratio <= 1.5) or area > 0.08 or y0 > H * 0.42:
                continue
            score = area
        else:
            if not (0.6 <= ratio <= 1.5) or y0 > H * 0.45:
                continue
            skin = _skin_fraction(np.asarray(page.crop((x0, y0, x1, y1))))
            if skin < 0.03:
                continue
            score = min(skin, 0.5) * 0.5 + (0.5 if 0.75 <= ratio <= 1.45 else 0) + (0.2 if y0 < H * 0.45 else 0)
        if best is None or score > best[0]:
            best = (score, (x0, y0, x1, y1))
    return best[1] if best else None


def _trim_rows(im):
    """لو فيه فجوة بيضاء داخل الاقتصاص (بعدها شريط عنوان/نص ملتصق بالصورة) نقطع عندها."""
    g = np.asarray(im).mean(axis=2)
    H = g.shape[0]
    mid = ((g > 55) & (g < 200)).mean(axis=1)
    step = 4
    n = H // step
    gap = [mid[i * step:(i + 1) * step].mean() < 0.2 and g[i * step:(i + 1) * step].mean() > 215 for i in range(n)]
    i = int(n * 0.4)
    while i < int(n * 0.92):
        if gap[i] and i + 1 < n and gap[i + 1]:
            return im.crop((0, 0, im.size[0], max(8, i * step - 2)))
        i += 1
    return im


def _from_scan(pdf, tmp):
    page = _render(pdf, tmp)
    if page is None:
        return None
    W, H = page.size
    # 1) صورة الجسم كاملة (طويلة)
    box = _pick(page, _components(page, 1.0, 0.7, 10, 2), "body")
    # 2) وإلا صورة شخصية في أعلى الصفحة
    if box is None:
        box = _pick(page, _components(page, 1.0, 0.6, 8, 2), True)
    # 2) أي كتلة صورة في الصفحة
    if box is None:
        box = _pick(page, _components(page, 1.0, 0.82, 14, 2), False)
    if box is None:
        return None
    hi = _render(pdf, tmp, 220)
    k = hi.size[0] / float(W) if hi is not None else 1.0
    hi = hi or page
    pad = 4  # نقصّ الإطار الرفيع حول الصورة
    crop = hi.crop((int((box[0] + pad) * k), int((box[1] + pad) * k), int((box[2] - pad) * k), int((box[3] - pad) * k)))
    return _trim_rows(crop)


def extract_photo(pdf, out_path):
    """يحفظ صورة العاملة في out_path (jpg). يرجع True لو نجح."""
    if np is None or Image is None:
        return False
    tmp = tempfile.mkdtemp()
    try:
        im = _from_embedded(pdf, tmp)
        if im is None:
            im = _from_scan(pdf, tmp)
        if im is None:
            return False
        im.thumbnail((MAX_SIDE, MAX_SIDE))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        im.save(out_path, "JPEG", quality=82, optimize=True)
        return True
    except Exception as e:
        print("   تعذّر استخراج الصورة:", e)
        return False
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
