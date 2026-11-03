#!/usr/bin/env python3
"""
يضيف السير الذاتية الجديدة تلقائيًا إلى data/cvs-<الدولة>.json (ملف لكل جنسية)

يمر على كل ملف PDF داخل cvs/<الدولة>/ لا يوجد له إدخال في data/cvs.json، ثم:
1) لو الـ PDF فيه نص (مثل نموذج الفلبين وبنغلاديش): يقرأ الاسم والجنسية والعمر والديانة والحالة
   الاجتماعية والمهنة والخبرة والرقم المرجعي مباشرة من النص (دقيق).
2) لو الـ PDF صورة مصوّرة (Scan): يقرأ بـ OCR الكلمات الواضحة فقط (المهنة/الديانة/الحالة).
وبيكمل أي بيانات ناقصة للسير الموجودة (بدون ما يغيّر الموجود).
تُستخرج صورة العاملة (وجه فقط) لتظهر خلف الكرت، ولا يُقرأ رقم الجواز أو الجوال: لا يُحفظ أي منها.
"""
import datetime, hashlib, json, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import cvphoto  # استخراج صورة العاملة من الـ PDF (يحتاج pillow و numpy)
except Exception:
    cvphoto = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "cvs.json")  # الملف القديم الموحّد (يتم نقله تلقائيًا للملفات الجديدة)
DATA_DIR = os.path.join(ROOT, "data")

FOLDERS = {"kenya": ("n1", "K"), "bangladesh": ("n2", "B"), "philippines": ("n3", "P"),
           "ethiopia": ("n4", "E"), "srilanka": ("n5", "S"), "uganda": ("n6", "U")}
NAT_LETTER = {v[0]: v[1] for v in FOLDERS.values()}
NAT_FILE = {v[0]: os.path.join(DATA_DIR, "cvs-%s.json" % k) for k, v in FOLDERS.items()}  # ملف لكل جنسية


def _read_list(path):
    """يقرأ ملف سير: إما {"cvs": [...]} (الشكل الجديد) أو [...] (القديم). الفاضي = قائمة فاضية."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        raw = f.read().strip()
    obj = json.loads(raw) if raw else []
    if isinstance(obj, dict):
        obj = obj.get("cvs", [])
    if not isinstance(obj, list):
        sys.exit("%s لازم يحتوي على قائمة سير" % os.path.basename(path))
    return obj


def load_all():
    data = _read_list(DATA)  # القديم أولًا (لو موجود)
    for nat, path in NAT_FILE.items():
        data.extend(_read_list(path))
    return data


def save_all(data):
    """يحفظ كل جنسية في ملفها (data/cvs-<الدولة>.json)، ويحذف الملف القديم الموحّد."""
    groups = {n: [] for n in NAT_FILE}
    for w in data:
        groups.setdefault(w.get("nat"), []).append(w)
    os.makedirs(DATA_DIR, exist_ok=True)
    for nat, path in NAT_FILE.items():
        text = json.dumps({"cvs": groups.get(nat, [])}, ensure_ascii=False, indent=2) + "\n"
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old != text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
    if os.path.exists(DATA):
        os.remove(DATA)
NAT_MAP = {"KENYA": "n1", "KENYAN": "n1", "BANGLADESH": "n2", "BANGLADESHI": "n2",
           "PHILIPPINES": "n3", "PHILIPPINE": "n3", "FILIPINO": "n3", "FILIPINA": "n3",
           "ETHIOPIA": "n4", "ETHIOPIAN": "n4", "SRI LANKA": "n5", "SRILANKA": "n5",
           "SRI LANKAN": "n5", "SRILANKAN": "n5", "UGANDA": "n6", "UGANDAN": "n6"}
COUNTRIES = r"OMAN|UAE|KSA|SAUDI|KUWAIT|QATAR|BAHRAIN|LEBANON|JORDAN|SINGAPORE|MALAYSIA|HONG ?KONG|DUBAI|EMIRATES|TAIWAN|CYPRUS"
FIELDS = ("job", "rel", "st", "age", "exp")
NOISE = re.compile(r"^(?:housemaid|maid|driver|cook|cv|resume|application|form|copy|final|new|scan|file|img|image|pdf|aflaak|aflak)+$", re.I)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(p):
    return str(p or "").lstrip("/").replace("\\", "/")


def title_name(stem):
    s = re.sub(r"[-_.()]+", " ", stem).strip()
    words = [w for w in s.split() if not NOISE.match(w) and not re.fullmatch(r"\d+", w)]
    if not words:
        words = s.split() or ["CV"]
    return " ".join(w.capitalize() for w in words)


def make_photo(pdf, rel_pdf):
    """يستخرج صورة العاملة لـ cvs/photos/<الدولة>-<اسم الملف>.jpg ويرجع مسارها (أو "" لو ما لقى صورة)."""
    if cvphoto is None:
        return None  # المكتبات غير مثبتة: نحاول في تشغيلة لاحقة
    parts = rel_pdf.split("/")
    name = "%s-%s-b.jpg" % (parts[1] if len(parts) > 2 else "cv", slug(os.path.splitext(parts[-1])[0]))
    out = os.path.join(ROOT, "cvs", "photos", name)
    return "cvs/photos/" + name if cvphoto.extract_photo(pdf, out) else ""


def slug(stem):
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "cv"


# ---------------------------------------------------------------- قراءة النص (PDF فيه نص)
def read_text_layer(pdf):
    try:
        out = subprocess.run(["pdftotext", "-layout", "-f", "1", "-l", "2", pdf, "-"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""
    return out if len(re.findall(r"[A-Za-z]{3,}", out)) >= 15 else ""


def _first(pattern, text, flags=re.M):
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else None


MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def _age_from_date(y, m, d):
    try:
        b = datetime.date(int(y), int(m), int(d))
    except Exception:
        return None
    today = datetime.date.today()
    a = today.year - b.year - ((today.month, today.day) < (b.month, b.day))
    return a if 16 <= a <= 70 else None


def age_from_text(t):
    """العمر المكتوب صراحة (AGE 34YEARS / 49 Y/O / 28 YEARS OLD) ثم تاريخ الميلاد بكل صيغه."""
    m = re.search(r"\bAGE\b[\s:\-]*(\d{2})(?!\d)", t)
    if m and 16 <= int(m.group(1)) <= 70:
        return int(m.group(1))
    m = re.search(r"(?<!\d)(\d{2})\s*(?:YEARS?\s*OLD|YRS?\s*OLD|Y/O|YO\b)", t)
    if m and 16 <= int(m.group(1)) <= 70:
        return int(m.group(1))
    lab = r"(?:DATE\s+OF\s+BIRTH|BIRTH\s*DATE|BIRTHDAY|D\.?O\.?B\.?)[\s:\-]*"
    mon = "|".join(MONTHS)
    # 11 MAR 1998 / 19 FEBRUARY 1982
    m = re.search(lab + r"(\d{1,2})[\s\-/.]*(" + mon + r")[A-Z]*[\s\-/.,]*(\d{4})", t)
    if m:
        return _age_from_date(m.group(3), MONTHS.index(m.group(2)) + 1, m.group(1))
    # NOVEMBER 14 1977 / NOV 14, 1977
    m = re.search(lab + r"(" + mon + r")[A-Z]*[\s\-/.]*(\d{1,2})[\s\-/.,]*(\d{4})", t)
    if m:
        return _age_from_date(m.group(3), MONTHS.index(m.group(1)) + 1, m.group(2))
    # 01/07/1992 أو 28.02.1999 (اليوم أولًا)
    m = re.search(lab + r"(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})", t)
    if m:
        d, mo = int(m.group(1)), int(m.group(2))
        if mo > 12 and d <= 12:
            d, mo = mo, d
        return _age_from_date(m.group(3), mo, d)
    return None


def exp_from_text(t):
    """prev = عندها خبرة خارجية، new = أول مرة. يرجع None لو غير واضح."""
    if re.search(r"EX[\s\-]*ABROAD", t):
        return "prev"
    if re.search(r"FIRST[\s\-]?TIMER|FIRSTIMER|FRESH\s+(?:FROM|ARRIVAL|CANDIDATE)|NEW\s+ARRIVAL", t):
        return "new"
    i = t.find("PREVIOUS EMPLOYMENT")
    if i >= 0:
        sec = t[i + 19:i + 360]
        # أولًا: كلمات صريحة بأن لا خبرة (NO / NIL / NONE / N/A / FRESH)
        if re.search(r"(?:COUNTRY|PERIOD)[ \t:\-]*(?:NIL|NONE|NO|N/A|NA|FRESH)(?![A-Z])", sec):
            return "new"
        if re.search(r"\b(19|20)\d{2}\b|\d\s*YEARS?|\d\s*YRS|\d\s*MONTHS?|" + COUNTRIES, sec):
            return "prev"
    # جدول من نوع: COUNTRY  POSITION  YEARS ثم صف فيه سنوات
    m = re.search(r"COUNTRY\s+POSITION\s+YEARS?[^\n]*\n([^\n]*)", t)
    if m:
        row = m.group(1)
        if re.search(r"\d", row) or re.search(COUNTRIES, row):
            return "prev"
        if re.search(r"\b(NIL|NONE|NO|N/A)\b", row):
            return "new"
    return None


def job_from_words(t):
    """يبحث عن كلمة المهنة في أي مكان بالنص (للسير ذات التنسيقات المختلفة)."""
    if re.search(r"HOUSE\s?MAID|HOUSEHOLD|DOMESTIC|\bMAID\b|HOUSE\s?KEEPER|NANNY|BABY\s?SITTER|عاملة", t):
        return "svc1"
    if re.search(r"\bDRIVER\b|سائق", t):
        return "svc2"
    if re.search(r"\bCOOK\b|\bCHEF\b|طباخ", t):
        return "svc3"
    if re.search(r"\bNURSE\b|ممرض", t):
        return "svc4"
    return None


DEFAULT_JOB = "svc1"  # لو ما اتعرفت المهنة نهائيًا: عاملة منزلية (يمكن تعديلها من Pages CMS)


def parse_text(raw):
    """يستخرج البيانات من نص الصفحة الأولى. يرجع dict بالمفاتيح المعروفة فقط."""
    t = raw.upper()
    out = {}
    stop = r"(?=\s{2,}|\s+PHONE|\s*$|\s[^\x00-\x7F])"

    name = _first(r"FULL\s*NAME[\s:\-]*([A-Z][A-Z .'\-]{2,60}?)" + stop, t)
    if not name:
        mm = re.search(r"FIRST\s+NAME\s+MIDDLE\s+NAME\s+LAST\s+NAME[^\n]*\n\s*([A-Z][A-Z .'\-]+)", t)
        if mm:
            name = " ".join(mm.group(1).split())
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

    age = age_from_text(t)
    if age:
        out["age"] = age

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

    if "job" not in out:
        j = job_from_words(t)
        if j:
            out["job"] = j

    ref = _first(r"REF\.?\s*NO\.?[\s:]+([A-Z]{1,3}-?\d{2,6})\b", t)
    if ref:
        out["ref"] = ref

    e = exp_from_text(t)
    if e:
        out["exp"] = e
    return out


# ---------------------------------------------------------------- OCR (PDF صورة مصوّرة)
def render_page(pdf, tmp):
    base = os.path.join(tmp, "page")
    try:
        subprocess.run(["pdftoppm", "-r", "300", "-f", "1", "-l", "1", "-png", pdf, base],
                       check=True, capture_output=True, timeout=120)
        return next(os.path.join(tmp, f) for f in sorted(os.listdir(tmp)) if f.startswith("page") and f.endswith(".png"))
    except Exception as e:
        print("   تعذّر تحويل الملف إلى صورة:", e)
        return None


def ocr_text(img):
    """قراءة الصورة بطريقتين (الأولى تحافظ على ترتيب الصفوف) وندمج النتيجة."""
    parts = []
    for psm in ("6", "11"):
        try:
            parts.append(subprocess.run(["tesseract", img, "-", "--psm", psm, "-l", "eng"],
                                        capture_output=True, text=True, timeout=240).stdout.upper())
        except Exception as e:
            print("   تعذّرت قراءة النص (psm %s): %s" % (psm, e))
    return "\n=====\n".join(parts)


def _job_from_position(txt):
    m = re.search(r"POSITION(?:\s+APPLIED)?[\s:]+([A-Z][A-Z ]{2,30})", txt)
    if not m:
        return None
    pos = m.group(1)
    if "DRIVER" in pos:
        return "svc2"
    if re.search(r"MAID|HOUSEHOLD|DOMESTIC|HOUSE\s?KEEPER|NANNY", pos):
        return "svc1"
    if re.search(r"COOK|CHEF", pos):
        return "svc3"
    if "NURSE" in pos:
        return "svc4"
    if "ASSISTANT" in pos:
        return "svc5"
    return None


def _age_from_ocr_dob(txt):
    """تاريخ الميلاد في نص OCR: التسمية غالبًا مشوّهة، فندوّر على التاريخ نفسه (سنة 1950-2008)."""
    mon = "|".join(MONTHS)
    yr = r"(19[5-9]\d|200[0-8])"
    m = re.search(r"(\d{1,2})\s*(" + mon + r")[A-Z]*[\s,./-]*" + yr, txt)
    if m:
        return _age_from_date(m.group(3), MONTHS.index(m.group(2)) + 1, m.group(1))
    m = re.search(r"(" + mon + r")[A-Z]*\s*(\d{1,2})[\s,./-]*" + yr, txt)
    if m:
        return _age_from_date(m.group(3), MONTHS.index(m.group(1)) + 1, m.group(2))
    m = re.search(r"(?<!\d)(" + mon + r")[A-Z]*[\s,./-]*" + yr, txt)  # شهر وسنة فقط
    if m:
        return _age_from_date(m.group(2), MONTHS.index(m.group(1)) + 1, 15)
    return None


def detect(text):
    """يستخرج البيانات من نص OCR (فيه ضجيج): نطبّع الرموز ثم نبحث بتساهل."""
    out = {}
    mn = re.search(r"FULL\s*NAME[\s:|_\-]*([A-Z][A-Z .'\-]{2,40}?)(?=\s[^A-Z\s]|\s{2,}|\s*$)", text, re.M)
    if mn:
        words = [w for w in mn.group(1).split() if len(w) >= 2]
        if 2 <= len(words) <= 5:
            out["name"] = " ".join(w.capitalize() for w in words)
    t = re.sub(r"[|_\u2014\u2013~\[\]{}()]", " ", text)
    t = re.sub(r"[ \t]+", " ", t)
    j = _job_from_position(t) or job_from_words(t)
    if j:
        out["job"] = j
    a = age_from_text(t) or _age_from_ocr_dob(t)
    if a:
        out["age"] = a
    e = exp_from_text(t)
    if e:
        out["exp"] = e
    if re.search(r"\b(?:MUSLIM|ISLAM|ISLAMIC)\b", t):
        out["rel"] = "m"
    elif re.search(r"\b(?:CHRISTIAN|CRISTIAN|CATHOLIC|CATOLIC|PROTESTANT|BORN\s+AGAIN)\b", t):
        out["rel"] = "o"
    mar = re.search(r"MARITAL\s*STATUS[^A-Z]{0,12}(SINGLE|UNMARRIED|MARRIED|WIDOW\w*|DIVORCED|SEPARATED)", t)
    word = mar.group(1) if mar else None
    if not word:
        has_s = re.search(r"\b(?:SINGLE|UNMARRIED)\b", t)
        has_m = re.search(r"\bMARRIED\b", t)
        word = "SINGLE" if has_s and not has_m else ("MARRIED" if has_m and not has_s else None)
    if word in ("SINGLE", "UNMARRIED"):
        out["st"] = "s"
    elif word == "MARRIED":
        out["st"] = "m"
    return out


# ---------------------------------------------------------------- التشغيل
def main():
    data = load_all()
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
        pdf = os.path.join(ROOT, norm(w.get("file"))) if w.get("file") else None
        if pdf and os.path.isfile(pdf) and any(k not in w for k in FIELDS):
            layer = read_text_layer(pdf)
            if layer:
                for k, v in parse_text(layer).items():
                    if k in FIELDS and k not in w:
                        w[k] = v
                        changed = True
        # اسم مأخوذ من اسم الملف (رقم أو "CV ..") → نحاول قراءته من نص الـ PDF
        stem = os.path.splitext(os.path.basename(str(w.get("file") or "")))[0]
        nm = str(w.get("name") or "")
        if pdf and os.path.isfile(pdf) and (nm == title_name(stem) or re.match(r"^(CV\b|\d+$)", nm)):
            lay = read_text_layer(pdf)
            real = parse_text(lay).get("name") if lay else None
            if real and real != nm:
                w["name"] = real
                changed = True
        cur = str(w.get("photo") or "")
        # صور الإصدار القديم (وجه فقط) تُستبدل بصورة الجسم كاملة؛ الصور المرفوعة يدويًا (أسماء مختلفة) لا تُمس
        old_auto = bool(re.match(r"^cvs/photos/[a-z]+-.+\.jpg$", cur)) and not cur.endswith("-b.jpg")
        if ("photo" not in w or old_auto or cur == "") and pdf and os.path.isfile(pdf):
            ph = make_photo(pdf, norm(w.get("file")))
            if ph:
                if old_auto and cur != ph:
                    try:
                        os.remove(os.path.join(ROOT, cur))
                    except OSError:
                        pass
                w["photo"] = ph
                changed = True
            elif ph is not None and "photo" not in w:
                w["photo"] = ""
                changed = True
            elif ph == "" and old_auto:
                pass  # ما لقينا صورة أفضل: نحتفظ بالقديمة
        if "job" not in w and pdf and os.path.isfile(pdf):
            tmp2 = tempfile.mkdtemp()
            try:
                img2 = render_page(pdf, tmp2)
                j = detect(ocr_text(img2)).get("job") if img2 else None
            finally:
                shutil.rmtree(tmp2, ignore_errors=True)
            w["job"] = j or DEFAULT_JOB
            changed = True
        if changed:
            filled += 1
            print("تم تحديث:", w.get("name"))
    # ---- السير الجديدة
    # بصمة محتوى كل ملف موجود، لمنع إضافة نفس الملف مرة ثانية حتى لو اتغير اسمه
    seen = {}
    for w in data:
        f = os.path.join(ROOT, norm(w.get("file"))) if w.get("file") else None
        if f and os.path.isfile(f):
            seen.setdefault(sha(f), w)
    added = 0
    removed = 0
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
            pdf = os.path.join(d, fn)
            digest = sha(pdf)
            if digest in seen:
                print("مكرر (نفس الملف موجود سابقًا باسم %s): تم حذف النسخة الزائدة %s" % (seen[digest].get("file"), rel))
                os.remove(pdf)
                removed += 1
                continue
            print("جديد:", rel)
            tmp = tempfile.mkdtemp()
            try:
                layer = read_text_layer(pdf)
                info = parse_text(layer) if layer else {}
                img = render_page(pdf, tmp)
                if img and (not layer or "job" not in info):
                    for k, v in detect(ocr_text(img)).items():
                        info.setdefault(k, v)
                info.setdefault("job", DEFAULT_JOB)
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
                if re.search(r"whatsapp|^img|^image|^photo|^[0-9a-f]{6,}\b", entry["name"], re.I):
                    entry["name"] = "CV " + ref  # اسم الملف ما فيهوش اسم العاملة؛ عدّله من Pages CMS
                for k in FIELDS:
                    if k in info:
                        entry[k] = info[k]
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            entry["status"] = "available"
            entry["file"] = rel
            ph = make_photo(pdf, rel)
            if ph is not None:
                entry["photo"] = ph
            data.append(entry)
            known.add(rel)
            seen[digest] = entry
            added += 1
            print("   ->", {k: v for k, v in entry.items() if k != "file"})

    save_all(data)
    print("تمت إضافة %d سيرة، واستكمال %d سيرة، وحذف %d ملف مكرر" % (added, filled, removed))


if __name__ == "__main__":
    main()
