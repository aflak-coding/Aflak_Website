#!/usr/bin/env python3
"""
يضيف السير الذاتية الجديدة تلقائيًا إلى data/cvs.json

يمر على كل ملف PDF داخل cvs/<الدولة>/ لا يوجد له إدخال في data/cvs.json، ثم:
1) لو الـ PDF فيه نص (مثل نموذج الفلبين وبنغلاديش): يقرأ الاسم والجنسية والعمر والديانة والحالة
   الاجتماعية والمهنة والخبرة والرقم المرجعي مباشرة من النص (دقيق).
2) لو الـ PDF صورة مصوّرة (Scan): يقرأ بـ OCR الكلمات الواضحة فقط (المهنة/الديانة/الحالة).
وبيكمل أي بيانات ناقصة للسير الموجودة (بدون ما يغيّر الموجود).
لا تُستخرج أي صور للعاملات، ولا يُقرأ رقم الجواز أو الجوال: لا يُحفظ أي منها في data/cvs.json.
"""
import datetime, json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "cvs.json")

FOLDERS = {"kenya": ("n1", "K"), "bangladesh": ("n2", "B"), "philippines": ("n3", "P"),
           "ethiopia": ("n4", "E"), "srilanka": ("n5", "S"), "uganda": ("n6", "U")}
NAT_LETTER = {v[0]: v[1] for v in FOLDERS.values()}
NAT_MAP = {"KENYA": "n1", "KENYAN": "n1", "BANGLADESH": "n2", "BANGLADESHI": "n2",
           "PHILIPPINES": "n3", "PHILIPPINE": "n3", "FILIPINO": "n3", "FILIPINA": "n3",
           "ETHIOPIA": "n4", "ETHIOPIAN": "n4", "SRI LANKA": "n5", "SRILANKA": "n5",
           "SRI LANKAN": "n5", "SRILANKAN": "n5", "UGANDA": "n6", "UGANDAN": "n6"}
COUNTRIES = r"OMAN|UAE|KSA|SAUDI|KUWAIT|QATAR|BAHRAIN|LEBANON|JORDAN|SINGAPORE|MALAYSIA|HONG ?KONG|DUBAI|EMIRATES|TAIWAN|CYPRUS"
FIELDS = ("job", "rel", "st", "age", "exp")
NOISE = re.compile(r"^(?:housemaid|maid|driver|cook|cv|resume|application|form|copy|final|new|scan|file|img|image|pdf|aflaak|aflak)+$", re.I)


def norm(p):
    return str(p or "").lstrip("/").replace("\\", "/")


def title_name(stem):
    s = re.sub(r"[-_.()]+", " ", stem).strip()
    words = [w for w in s.split() if not NOISE.match(w) and not re.fullmatch(r"\d+", w)]
    if not words:
        words = s.split() or ["CV"]
    return " ".join(w.capitalize() for w in words)


def slug(stem):
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "cv"


# ---------------------------------------------------------------- قراءة النص (PDF فيه نص)
def read_text_layer(pdf):
    try:
        out = subprocess.run(["pdftotext", "-layout", "-f", "1", "-l", "1", pdf, "-"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""
    return out if len(re.findall(r"[A-Za-z]{3,}", out)) >= 15 else ""


def _first(pattern, text, flags=re.M):
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else None


def parse_text(raw):
    """يستخرج البيانات من نص الصفحة الأولى. يرجع dict بالمفاتيح المعروفة فقط."""
    t = raw.upper()
    out = {}
    stop = r"(?=\s{2,}|\s+PHONE|\s*$|\s[^\x00-\x7F])"

    name = _first(r"FULL\s+NAME[\s:\-]*([A-Z][A-Z .'\-]{2,60}?)" + stop, t)
    if name:
        name = re.sub(r"[\s\-.:]+$", "", name)
        if 1 <= len(name.split()) <= 6:
            out["name"] = " ".join(w.capitalize() for w in name.split())

    nat = _first(r"NATIONALITY[\s:]+([A-Z][A-Z ]{2,20}?)" + stop, t)
    if nat and nat.strip() in NAT_MAP:
        out["nat"] = NAT_MAP[nat.strip()]

    rel = _first(r"RELIGION[\s:]+([A-Z]+)", t)
    if rel:
        out["rel"] = "m" if rel in ("ISLAM", "MUSLIM", "ISLAMIC") else "o"

    st = _first(r"MARITAL\s+STATUS[\s:]+([A-Z]+)", t)
    if st in ("SINGLE", "UNMARRIED"):
        out["st"] = "s"
    elif st == "MARRIED":
        out["st"] = "m"

    age = _first(r"\bAGE\b[\s:]+(\d{2})\b", t)
    if age and 16 <= int(age) <= 70:
        out["age"] = int(age)
    else:
        m = re.search(r"DATE\s+OF\s+BIRTH[\s:]+(\d{1,2})\s+([A-Z]{3})[A-Z]*\s+(\d{4})", t)
        if m:
            try:
                mon = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"].index(m.group(2)) + 1
                b = datetime.date(int(m.group(3)), mon, int(m.group(1)))
                today = datetime.date.today()
                a = today.year - b.year - ((today.month, today.day) < (b.month, b.day))
                if 16 <= a <= 70:
                    out["age"] = a
            except Exception:
                pass

    pos = _first(r"(?:POST\s+APPLIED\s+FOR|POSITION)[\s:]+([A-Z][A-Z ]{2,30}?)" + stop, t)
    if pos:
        if re.search(r"MAID|HOUSEHOLD|DOMESTIC", pos):
            out["job"] = "svc1"
        elif "DRIVER" in pos:
            out["job"] = "svc2"
        elif re.search(r"COOK|CHEF", pos):
            out["job"] = "svc3"
        elif "NURSE" in pos:
            out["job"] = "svc4"
        elif "ASSISTANT" in pos:
            out["job"] = "svc5"

    ref = _first(r"REF\.?\s*NO\.?[\s:]+([A-Z]{1,3}-?\d{2,6})\b", t)
    if ref:
        out["ref"] = ref

    if "EX-ABROAD" in t or "EX ABROAD" in t:
        out["exp"] = "prev"
    else:
        i = t.find("PREVIOUS EMPLOYMENT")
        if i >= 0:
            sec = t[i + 19:i + 320]
            if re.search(r"\b(19|20)\d{2}\b|YEARS?|YRS|MONTHS?|" + COUNTRIES, sec):
                out["exp"] = "prev"
            elif re.search(r"\b(NIL|NONE|N/A|FRESH|FIRST\s+TIME)\b", sec):
                out["exp"] = "new"
    return out


# ---------------------------------------------------------------- OCR (PDF صورة مصوّرة)
def render_page(pdf, tmp):
    base = os.path.join(tmp, "page")
    try:
        subprocess.run(["pdftoppm", "-r", "200", "-f", "1", "-l", "1", "-png", pdf, base],
                       check=True, capture_output=True, timeout=120)
        return next(os.path.join(tmp, f) for f in sorted(os.listdir(tmp)) if f.startswith("page") and f.endswith(".png"))
    except Exception as e:
        print("   تعذّر تحويل الملف إلى صورة:", e)
        return None


def ocr_text(img):
    try:
        return subprocess.run(["tesseract", img, "-", "--psm", "11", "-l", "eng"],
                              capture_output=True, text=True, timeout=180).stdout.upper()
    except Exception as e:
        print("   تعذّرت قراءة النص:", e)
        return ""


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


# ---------------------------------------------------------------- التشغيل
def main():
    data = []
    if os.path.exists(DATA):
        with open(DATA, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            sys.exit("data/cvs.json لازم يكون قائمة")
    known = {norm(w.get("file")) for w in data}
    used_refs = {str(w.get("ref", "")) for w in data}
    counters = {}
    for w in data:
        m = re.match(r"^([A-Z])-(\d+)$", str(w.get("ref", "")))
        if m:
            counters[m.group(1)] = max(counters.get(m.group(1), 100), int(m.group(2)))

    # ---- استكمال السير الموجودة (بيانات ناقصة من النص) + تنظيف الصور القديمة
    filled = 0
    for w in data:
        changed = False
        if "photo" in w:
            w.pop("photo")
            changed = True
        pdf = os.path.join(ROOT, norm(w.get("file"))) if w.get("file") else None
        if pdf and os.path.isfile(pdf) and any(k not in w for k in FIELDS):
            layer = read_text_layer(pdf)
            if layer:
                for k, v in parse_text(layer).items():
                    if k in FIELDS and k not in w:
                        w[k] = v
                        changed = True
        if changed:
            filled += 1
            print("تم تحديث:", w.get("name"))
    old_photos = os.path.join(ROOT, "cvs", "photos")
    if os.path.isdir(old_photos):
        for f in os.listdir(old_photos):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                os.remove(os.path.join(old_photos, f))
                filled += 1

    # ---- السير الجديدة
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
            pdf = os.path.join(d, fn)
            tmp = tempfile.mkdtemp()
            try:
                layer = read_text_layer(pdf)
                info = parse_text(layer) if layer else {}
                img = render_page(pdf, tmp)
                if not layer and img:
                    info.update(detect(ocr_text(img)))
                final_nat = info.get("nat") or nat
                if final_nat != nat:
                    print("   تنبيه: الجنسية في الملف تختلف عن المجلد، تم اعتماد جنسية الملف")
                entry = {"nat": final_nat, "name": info.get("name") or title_name(stem)}
                letter2 = NAT_LETTER.get(final_nat, letter)
                ref = info.get("ref")
                if not ref or ref in used_refs:
                    counters[letter2] = counters.get(letter2, 100) + 1
                    ref = "%s-%d" % (letter2, counters[letter2])
                used_refs.add(ref)
                entry["ref"] = ref
                for k in FIELDS:
                    if k in info:
                        entry[k] = info[k]
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            entry["status"] = "available"
            entry["file"] = rel
            data.append(entry)
            known.add(rel)
            added += 1
            print("   ->", {k: v for k, v in entry.items() if k != "file"})

    if added or filled:
        os.makedirs(os.path.dirname(DATA), exist_ok=True)
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    print("تمت إضافة %d سيرة، واستكمال %d سيرة" % (added, filled))


if __name__ == "__main__":
    main()
