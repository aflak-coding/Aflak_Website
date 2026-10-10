#!/usr/bin/env python3
"""
يضيف السير الذاتية الجديدة تلقائيًا إلى data/cvs.json

يمر على كل ملف PDF داخل cvs/<الدولة>/ لا يوجد له إدخال في data/cvs.json، ثم:
- الجنسية: من اسم المجلد (kenya, bangladesh, philippines, ethiopia, srilanka, uganda)
- الاسم: من اسم الملف (Amina-Wanjiku.pdf  ->  Amina Wanjiku)
- الرقم المرجعي: يُولَّد تلقائيًا (E-103 مثلًا)
- الصورة: تُقص تلقائيًا من نموذج "Application for Employment" المعروف
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


def title_name(stem):
    s = re.sub(r"[-_]+", " ", stem).strip()
    return " ".join(w.capitalize() for w in s.split())


def slug(stem):
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "cv"


def run_ocr(pdf, tmp):
    """يرجع (نص, صورة الصفحة) أو (None, None) لو فشلت القراءة."""
    try:
        base = os.path.join(tmp, "page")
        subprocess.run(["pdftoppm", "-r", "200", "-f", "1", "-l", "1", "-png", pdf, base],
                       check=True, capture_output=True, timeout=120)
        img = next(os.path.join(tmp, f) for f in sorted(os.listdir(tmp)) if f.startswith("page") and f.endswith(".png"))
        txt = subprocess.run(["tesseract", img, "-", "--psm", "11", "-l", "eng"],
                             capture_output=True, text=True, timeout=180).stdout
        return txt.upper(), img
    except Exception as e:
        print("   تعذّرت قراءة الملف:", e)
        return None, None


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
                text, img = run_ocr(os.path.join(d, fn), tmp)
                if text:
                    entry.update(detect(text))
                    if "APPLICATION" in text and "EMPLOYMENT" in text:
                        os.makedirs(PHOTOS, exist_ok=True)
                        dest = os.path.join(PHOTOS, slug(stem) + ".jpg")
                        try:
                            crop_photo(img, dest)
                            entry["photo"] = "cvs/photos/" + os.path.basename(dest)
                        except Exception as e:
                            print("   تعذّر قص الصورة:", e)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            entry["file"] = rel
            data.append(entry)
            added += 1
            print("   ->", {k: v for k, v in entry.items() if k != "file"})

    if added:
        os.makedirs(os.path.dirname(DATA), exist_ok=True)
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    print("تمت إضافة %d سيرة" % added)


if __name__ == "__main__":
    main()
