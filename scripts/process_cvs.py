#!/usr/bin/env python3
"""
يضيف السير الذاتية الجديدة تلقائيًا إلى data/cvs.json

يمر على كل ملف PDF داخل cvs/<الدولة>/ لا يوجد له إدخال في data/cvs.json، ثم:
- الجنسية: من اسم المجلد (kenya, bangladesh, philippines, ethiopia, srilanka, uganda)
- الاسم: من اسم الملف (Amina-Wanjiku.pdf  ->  Amina Wanjiku)
- الرقم المرجعي: يُولَّد تلقائيًا (E-103 مثلًا)
- الصورة: تُقص تلقائيًا (من نموذج "Application for Employment" المعروف، أو بكشف الوجه في أي نموذج آخر)
- المهنة والديانة والحالة الاجتماعية: تُقرأ من الملف إن كانت الكلمة واضحة، وإلا تُترك فارغة
لا يتم تخمين العمر أو الخبرة (القراءة الآلية للأرقام غير مضمونة). يمكن إضافتها يدويًا من لوحة Pages CMS.
"""
import json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "cvs.json")
PHOTOS = os.path.join(ROOT, "cvs", "photos")

FOLDERS = {"kenya": ("n1", "K"), "bangladesh": ("n2", "B"), "philippines": ("n3", "P"),
           "ethiopia": ("n4", "E"), "srilanka": ("n5", "S"), "uganda": ("n6", "U")}

# مكان صورة المتقدم في نموذج الطلب (نسب من حجم الصفحة)
PHOTO_BOX = (680 / 918, 161 / 1300, 860 / 918, 322 / 1300)


def norm(p):
    return str(p or "").lstrip("/").replace("\\", "/")


NOISE = re.compile(r"^(?:housemaid|maid|driver|cook|cv|resume|application|form|copy|final|new|scan|file|img|image|pdf)+$", re.I)


def title_name(stem):
    s = re.sub(r"[-_.()]+", " ", stem).strip()
    words = [w for w in s.split() if not NOISE.match(w) and not re.fullmatch(r"\d+", w)]
    if not words:
        words = s.split() or ["CV"]
    return " ".join(w.capitalize() for w in words)


def slug(stem):
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "cv"


def render_and_ocr(pdf, tmp):
    """يرجع (نص, مسار صورة الصفحة الأولى). النص فارغ لو فشلت القراءة، والصورة None لو فشل التحويل."""
    base = os.path.join(tmp, "page")
    try:
        subprocess.run(["pdftoppm", "-r", "200", "-f", "1", "-l", "1", "-png", pdf, base],
                       check=True, capture_output=True, timeout=120)
        img = next(os.path.join(tmp, f) for f in sorted(os.listdir(tmp)) if f.startswith("page") and f.endswith(".png"))
    except Exception as e:
        print("   تعذّر تحويل الملف إلى صورة:", e)
        return "", None
    try:
        txt = subprocess.run(["tesseract", img, "-", "--psm", "11", "-l", "eng"],
                             capture_output=True, text=True, timeout=180).stdout
        return txt.upper(), img
    except Exception as e:
        print("   تعذّرت قراءة النص:", e)
        return "", img


def detect(text):
    out = {}
    if re.search(r"\bHOUSE\s?MAID\b", text) or re.search(r"\bMAID\b", text):
        out["job"] = "svc1"
    elif re.search(r"\bDRIVER\b", text):
        out["job"] = "svc2"
    elif re.search(r"\bNURSE\b", text):
        out["job"] = "svc4"
    if re.search(r"\bMUSLIM\b", text):
        out["rel"] = "m"
    elif re.search(r"\bCHRISTIAN\b", text):
        out["rel"] = "o"
    if re.search(r"\bSINGLE\b", text) and not re.search(r"\bMARRIED\b", text):
        out["st"] = "s"
    elif re.search(r"\bMARRIED\b", text) and not re.search(r"\bSINGLE\b", text):
        out["st"] = "m"
    return out


def crop_photo(img_path, dest):
    from PIL import Image
    im = Image.open(img_path).convert("RGB")
    w, h = im.size
    box = (int(PHOTO_BOX[0] * w), int(PHOTO_BOX[1] * h), int(PHOTO_BOX[2] * w), int(PHOTO_BOX[3] * h))
    im.crop(box).save(dest, "JPEG", quality=88)


def crop_by_face(img_path, dest):
    """يكشف أكبر وجه في الصفحة ويقص حوله صورة شخصية. يرجع True لو نجح."""
    try:
        import cv2
    except Exception:
        print("   (OpenCV غير مثبت: تخطي كشف الوجه)")
        return False
    im = cv2.imread(img_path)
    if im is None:
        return False
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(70, 70))
    if len(faces) == 0:
        return False
    x, y, w, h = max(faces, key=lambda f: int(f[2]) * int(f[3]))
    H, W = gray.shape
    cw = int(w * 2.2)
    ch = int(h * 2.7)
    x0 = max(0, int(x + w / 2 - cw / 2))
    x1 = min(W, x0 + cw)
    x0 = max(0, x1 - cw)
    y0 = max(0, int(y - h * 0.55))
    y1 = min(H, y0 + ch)
    y0 = max(0, y1 - ch)
    cv2.imwrite(dest, im[y0:y1, x0:x1], [cv2.IMWRITE_JPEG_QUALITY, 88])
    return True


def make_photo(text, img, stem):
    """يرجع مسار الصورة النسبي أو None."""
    if not img:
        return None
    os.makedirs(PHOTOS, exist_ok=True)
    dest = os.path.join(PHOTOS, slug(stem) + ".jpg")
    rel = "cvs/photos/" + os.path.basename(dest)
    if text and "APPLICATION" in text and "EMPLOYMENT" in text:
        try:
            crop_photo(img, dest)
            return rel
        except Exception as e:
            print("   تعذّر القص الثابت:", e)
    try:
        if crop_by_face(img, dest):
            return rel
    except Exception as e:
        print("   تعذّر كشف الوجه:", e)
    return None


def main():
    data = []
    if os.path.exists(DATA):
        with open(DATA, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            sys.exit("data/cvs.json لازم يكون قائمة")
    known = {norm(w.get("file")) for w in data}
    counters = {}
    for w in data:
        m = re.match(r"^([A-Z])-(\d+)$", str(w.get("ref", "")))
        if m:
            counters[m.group(1)] = max(counters.get(m.group(1), 100), int(m.group(2)))

    # تعبئة الصور الناقصة للسير الموجودة
    filled = 0
    for w in data:
        if w.get("photo") or not w.get("file"):
            continue
        pdf = os.path.join(ROOT, norm(w["file"]))
        if not os.path.isfile(pdf):
            continue
        tmp = tempfile.mkdtemp()
        try:
            text, img = render_and_ocr(pdf, tmp)
            photo = make_photo(text, img, os.path.splitext(os.path.basename(pdf))[0])
            if photo:
                w["photo"] = photo
                filled += 1
                print("صورة جديدة لـ", w.get("name"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    added = 0
    for folder, (nat, letter) in FOLDERS.items():
        d = os.path.join(ROOT, "cvs", folder)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.lower().endswith(".pdf"):
                continue
            rel = "cvs/%s/%s" % (folder, fn)
            if rel in known:
                continue
            stem = os.path.splitext(fn)[0]
            print("جديد:", rel)
            entry = {"nat": nat, "name": title_name(stem)}
            counters[letter] = counters.get(letter, 100) + 1
            entry["ref"] = "%s-%d" % (letter, counters[letter])
            tmp = tempfile.mkdtemp()
            try:
                text, img = render_and_ocr(os.path.join(d, fn), tmp)
                if text:
                    entry.update(detect(text))
                photo = make_photo(text, img, stem)
                if photo:
                    entry["photo"] = photo
                else:
                    print("   لم يتم العثور على صورة للقص")
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            entry["file"] = rel
            data.append(entry)
            added += 1
            print("   ->", {k: v for k, v in entry.items() if k != "file"})

    if added or filled:
        os.makedirs(os.path.dirname(DATA), exist_ok=True)
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    print("تمت إضافة %d سيرة، وتعبئة %d صورة" % (added, filled))


if __name__ == "__main__":
    main()
