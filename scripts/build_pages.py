#!/usr/bin/env python3
"""
يولّد صفحات الخدمات والجنسيات وصفحة الخصوصية وملف sitemap.xml.
التشغيل (اختياري، الصفحات الناتجة موجودة بالفعل في المستودع):  python scripts/build_pages.py
لتغيير نص صفحة: عدّل القوائم SERVICES / NATIONALITIES / PRIVACY_AR / PRIVACY_EN ثم أعد التشغيل.
لتغيير عنوان الموقع (مثلًا بعد شراء دومين): غيّر BASE ثم أعد التشغيل.
"""
import html, json, os

BASE = "https://aflak-coding.github.io/Aflak_Website/"
WA = "966554084322"
LICENSE = "3801238"
CR = "7004359431"
EMAIL = "aflak8785@gmail.com"
UPDATED = "2026-10-17"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = "13"

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16.003 3C8.83 3 3 8.83 3 16c0 2.29.6 4.52 1.74 6.49L3 29l6.7-1.7A12.95 12.95 0 0 0 16 29c7.17 0 13-5.83 13-13S23.17 3 16.003 3zm0 23.7c-1.95 0-3.86-.53-5.53-1.52l-.4-.24-3.98 1.01 1.06-3.88-.26-.4A10.67 10.67 0 0 1 5.3 16c0-5.88 4.82-10.7 10.7-10.7S26.7 10.12 26.7 16s-4.82 10.7-10.7 10.7zm5.87-8c-.32-.16-1.9-.94-2.2-1.04-.3-.1-.5-.16-.72.16-.22.32-.83 1.04-1.02 1.26-.19.22-.38.24-.7.08-.32-.16-1.36-.5-2.59-1.6-.96-.85-1.6-1.9-1.79-2.22-.19-.32-.02-.5.14-.66.15-.14.32-.38.48-.57.16-.19.22-.32.32-.54.1-.22.05-.4-.03-.57-.08-.16-.72-1.74-.99-2.38-.26-.62-.52-.54-.72-.55h-.62c-.22 0-.57.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.12 1.32 3.34c.16.22 2.28 3.48 5.52 4.88.77.33 1.37.53 1.84.68.77.25 1.48.21 2.04.13.62-.09 1.9-.78 2.17-1.53.27-.75.27-1.4.19-1.53-.08-.14-.3-.22-.62-.38z"/></svg>'

SERVICES = [
    dict(slug="maid", svc="svc1", name="استقدام عاملة منزلية", city="استقدام عاملة منزلية في الرياض",
         desc="تبحث عن عاملة منزلية؟ شركة أفلاك للاستقدام المرخّصة في الرياض تساعدك في استقدام عاملة منزلية. اطّلع على السير الذاتية وتواصل معنا عبر واتساب.",
         lead="عاملة تتولى شؤون البيت من تنظيف وترتيب وغسيل، ويمكنها العناية بالأطفال. اطّلع على السير الذاتية المتاحة، واختر ما يناسب أسرتك.",
         sec="ماذا تشمل الخدمة؟", intro="تختلف المهام من أسرة لأخرى، وفيما يلي أبرز ما يُطلب عادة من العاملة المنزلية:",
         items=["تنظيف المنزل وترتيبه", "الغسيل والكي", "العناية بالأطفال عند الحاجة", "المساعدة في إعداد الطعام (بحسب الاتفاق)"],
         note="نوضح لك التفاصيل والمهام المتفق عليها عند التواصل معنا."),
    dict(slug="driver", svc="svc2", name="استقدام سائق خاص", city="استقدام سائق خاص في الرياض",
         desc="تحتاج سائقًا خاصًا لأسرتك؟ شركة أفلاك للاستقدام المرخّصة في الرياض تساعدك في استقدام سائق خاص. تواصل معنا عبر واتساب.",
         lead="سائق لتنقلات الأسرة اليومية. حدّد الجنسية التي تفضلها وتواصل معنا لمتابعة التفاصيل.",
         sec="ماذا تشمل الخدمة؟", intro="تختلف المهام من أسرة لأخرى، وفيما يلي أبرز ما يُطلب عادة من السائق الخاص:",
         items=["توصيل أفراد الأسرة إلى العمل والمدارس والمشاوير اليومية", "الالتزام بمواعيد الأسرة", "العناية الأساسية بالسيارة (بحسب الاتفاق)"],
         note="نوضح لك التفاصيل والمتطلبات عند التواصل معنا."),
    dict(slug="cook", svc="svc3", name="استقدام طباخ / طباخة", city="استقدام طباخ أو طباخة في الرياض",
         desc="تبحث عن طباخ أو طباخة لمنزلك؟ شركة أفلاك للاستقدام المرخّصة في الرياض تساعدك في الاستقدام. تواصل معنا عبر واتساب.",
         lead="طباخ أو طباخة لإعداد وجبات البيت اليومية بما يناسب ذوق أسرتك.",
         sec="ماذا تشمل الخدمة؟", intro="تختلف المهام من أسرة لأخرى، وفيما يلي أبرز ما يُطلب عادة:",
         items=["إعداد الوجبات اليومية للأسرة", "مراعاة تفضيلات الأسرة الغذائية", "ترتيب المطبخ ونظافته (بحسب الاتفاق)"],
         note="أخبرنا بنوع المطبخ والوجبات التي تفضلها لنوضح لك المتاح."),
    dict(slug="nurse", svc="svc4", name="استقدام ممرضة منزلية", city="استقدام ممرضة منزلية في الرياض",
         desc="تحتاج رعاية منزلية لكبار السن أو المرضى؟ شركة أفلاك للاستقدام المرخّصة في الرياض تساعدك. تواصل معنا عبر واتساب لمعرفة المتاح.",
         lead="للأسر التي تحتاج رعاية منزلية. أخبرنا بالحالة والاحتياج لنوضح لك الخيارات المتاحة.",
         sec="ماذا تشمل الخدمة؟", intro="تختلف الاحتياجات من حالة لأخرى، وفيما يلي أمثلة على ما يُطلب عادة:",
         items=["مرافقة ورعاية يومية داخل المنزل", "المتابعة بحسب تعليمات الطبيب أو الأسرة", "مساعدة في الأنشطة اليومية"],
         note="هذه الخدمة لا تغني عن الاستشارة الطبية. تواصل معنا لمعرفة المتاح والتفاصيل."),
    dict(slug="assistant", svc="svc5", name="استقدام مساعدة شخصية", city="استقدام مساعدة شخصية في الرياض",
         desc="تحتاج مساعدة شخصية تسهّل شؤونك اليومية؟ شركة أفلاك للاستقدام المرخّصة في الرياض تساعدك. تواصل معنا عبر واتساب.",
         lead="مساعدة شخصية تسهّل شؤونك اليومية في المنزل. أخبرنا بما تحتاجه ونوضح لك التفاصيل.",
         sec="ماذا تشمل الخدمة؟", intro="تختلف المهام من أسرة لأخرى، وفيما يلي أمثلة على ما يُطلب عادة:",
         items=["مساعدة في المهام اليومية", "تنظيم شؤون المنزل", "مرافقة داخل المنزل (بحسب الاتفاق)"],
         note="نوضح لك التفاصيل والمهام المتفق عليها عند التواصل معنا."),
]
NATIONALITIES = [
    dict(slug="philippines", nat="n3", name="الفلبين"),
    dict(slug="bangladesh", nat="n2", name="بنغلاديش"),
    dict(slug="kenya", nat="n1", name="كينيا"),
    dict(slug="srilanka", nat="n5", name="سريلانكا"),
]
E = html.escape


def wa_link(text):
    from urllib.parse import quote
    return "https://wa.me/%s?text=%s" % (WA, quote(text))


def head(p, title, desc, url, ld):
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="{p}assets/img/favicon-48.png">
<link rel="icon" type="image/png" sizes="192x192" href="{p}assets/img/favicon-192.png">
<link rel="apple-touch-icon" href="{p}assets/img/apple-touch-icon.png">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="أفلاك للاستقدام">
<meta property="og:locale" content="ar_SA">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E5C63">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Reem+Kufi:wght@500;600;700&display=swap">
<link rel="stylesheet" href="{p}assets/style.css?v={V}">
</head>
<body>
'''


def header(p, wa):
    return f'''<header class="top"><div class="wrap">
  <a class="brand" href="{p}index.html"><span class="chip"><img src="{p}assets/img/logo-1.jpg" alt="" width="114" height="38"></span><b>أفلاك للاستقدام</b></a>
  <nav aria-label="main"><a href="{p}index.html#services">الخدمات</a><a href="{p}index.html#nationalities">الجنسيات</a><a href="{p}index.html#faq">أسئلة شائعة</a><a href="{p}index.html#order">تواصل معنا</a></nav>
  <a class="btn btn-wa hdr-cta" href="{wa}" target="_blank" rel="noopener">اطلب الآن</a>
</div></header>
<main>
'''


def footer(p, wa):
    svc = " ".join(f'<a href="{p}services/{s["slug"]}.html">{E(s["name"].replace("استقدام ", ""))}</a>' for s in SERVICES)
    nat = " ".join(f'<a href="{p}nationalities/{n["slug"]}.html">{E(n["name"])}</a>' for n in NATIONALITIES)
    return f'''</main>
<footer class="ft"><div class="wrap">
  <div class="ft-seo">
    <div><b>خدماتنا:</b> {svc}</div>
    <div><b>الجنسيات:</b> {nat}</div>
  </div>
  <div class="ft-bottom"><span>أفلاك للاستقدام | الرياض، المملكة العربية السعودية</span><span>ترخيص {LICENSE} | سجل تجاري {CR}</span><a href="{p}privacy.html">سياسة الخصوصية</a></div>
</div></footer>
<a class="fab" href="{wa}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a>
</body>
</html>
'''


def faq_items(extra):
    base = [
        ("هل الشركة مرخّصة؟", f"نعم. شركة مرخّصة من وزارة الموارد البشرية والتنمية الاجتماعية برقم {LICENSE}، وسجلنا التجاري رقم {CR}."),
        ("كم تكلفة الخدمة؟", "تختلف التكلفة حسب الخدمة والجنسية. راسلنا على واتساب ونرسل لك التفاصيل."),
    ]
    return base + [extra]


def page(p, slug_path, title, desc, h1, lead, crumbs_name, body_html, cta1_text, cta2_href, cta2_text, wa_text, faqs, ld_name, ld_type):
    url = BASE + slug_path
    wa = wa_link(wa_text)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": ld_name, "serviceType": ld_type, "url": url,
         "provider": {"@type": "EmploymentAgency", "name": "أفلاك للاستقدام", "url": BASE, "telephone": "+" + WA},
         "areaServed": {"@type": "City", "name": "الرياض"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": crumbs_name, "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]}
    out = head(p, title, desc, url, ld) + header(p, wa)
    out += f'''<section class="lp-hero"><div class="wrap">
  <nav class="crumbs" aria-label="breadcrumb"><a href="{p}index.html">الرئيسية</a> › <span>{E(crumbs_name)}</span></nav>
  <h1>{E(h1)}</h1>
  <p class="lead">{E(lead)}</p>
  <div class="cta-row"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{E(cta1_text)}</a><a class="btn btn-ghost" href="{cta2_href}">{E(cta2_text)}</a></div>
</div></section>
'''
    out += body_html
    out += '<section class="s alt"><div class="wrap"><h2 class="title">كيف تبدأ؟</h2><ol class="lp-steps"><li>تواصل معنا عبر واتساب أو نموذج الطلب في الموقع.</li><li>أخبرنا بالخدمة والجنسية التي تفضلها.</li><li>نرد عليك بالتفاصيل والخيارات المتاحة.</li></ol></div></section>\n'
    out += '<section class="s"><div class="wrap"><h2 class="title">أسئلة شائعة</h2>\n' + "\n".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs) + '\n</div></section>\n'
    links = " ".join(f'<a class="lp-chip" href="{p}services/{s["slug"]}.html">{E(s["name"])}</a>' for s in SERVICES)
    links += " " + " ".join(f'<a class="lp-chip" href="{p}nationalities/{n["slug"]}.html">عمالة منزلية من {E(n["name"])}</a>' for n in NATIONALITIES)
    out += f'<section class="s alt"><div class="wrap"><h2 class="title">اكتشف المزيد</h2><div class="lp-chips">{links}</div></div></section>\n'
    out += footer(p, wa)
    return out


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


urls = [BASE]
for s in SERVICES:
    p = "../"
    body = f'<section class="s"><div class="wrap prose"><h2 class="title">{E(s["sec"])}</h2><p>{E(s["intro"])}</p><ul class="lp-list">' + "".join(f"<li>{E(i)}</li>" for i in s["items"]) + f'</ul><p class="lp-note">{E(s["note"])}</p></div></section>\n'
    faqs = faq_items(("ما الجنسيات المتاحة؟", "كينيا، بنغلاديش، الفلبين، وسريلانكا."))
    write(f"services/{s['slug']}.html", page(
        p, f"services/{s['slug']}.html", f"{s['city']} | أفلاك للاستقدام", s["desc"], s["city"], s["lead"], s["name"], body,
        "اطلب عبر واتساب", f"{p}index.html?svc={s['svc']}#order", "اطلب من النموذج",
        f"السلام عليكم، أرغب في طلب: {s['name'].replace('استقدام ', '')}", faqs, s["name"], s["name"]))
    urls.append(BASE + f"services/{s['slug']}.html")

for n in NATIONALITIES:
    p = "../"
    title = f"استقدام عمالة منزلية من {n['name']} في الرياض | أفلاك للاستقدام"
    desc = f"شركة أفلاك للاستقدام المرخّصة في الرياض: تصفّح السير الذاتية المتاحة للعمالة المنزلية من {n['name']} وتواصل معنا عبر واتساب."
    body = f'''<section class="s"><div class="wrap prose"><h2 class="title">تصفّح السير الذاتية من {E(n["name"])}</h2>
<p>اطّلع على السير الذاتية المتاحة للعمالة المنزلية من {E(n["name"])}، وقارن بينها حسب العمر والخبرة والحالة الاجتماعية والديانة، ثم اختر ما يناسب أسرتك.</p>
<ul class="lp-list"><li>اضغط «تصفّح السير الذاتية» لعرض القائمة.</li><li>استخدم الفلاتر لتضييق الاختيار.</li><li>اضغط «اختيار وإرسال عبر واتساب» ليصلنا اختيارك.</li></ul>
<p class="lp-note">قد تتغير السير المتاحة وحالة التوفر باستمرار، فتواصل معنا للتأكد قبل اتخاذ القرار.</p></div></section>
'''
    faqs = faq_items(("ما الخدمات التي يمكن طلبها؟", "عاملة منزلية، وسائق خاص، وطباخ أو طباخة، وممرضة منزلية، ومساعدة شخصية (بحسب التوفر)."))
    write(f"nationalities/{n['slug']}.html", page(
        p, f"nationalities/{n['slug']}.html", title, desc, f"استقدام عمالة منزلية من {n['name']}",
        f"تصفّح السير الذاتية المتاحة من {n['name']} واختر ما يناسب أسرتك. نحن في الرياض ونرد عليك عبر واتساب.",
        f"عمالة منزلية من {n['name']}", body, "اطلب عبر واتساب", f"{p}index.html?nat={n['nat']}#cvs", "تصفّح السير الذاتية",
        f"السلام عليكم، أرغب في الاستفسار عن استقدام عمالة منزلية من {n['name']}", faqs, f"استقدام عمالة منزلية من {n['name']}", "استقدام عمالة منزلية"))
    urls.append(BASE + f"nationalities/{n['slug']}.html")

# ---------------- privacy page (Arabic + English) ----------------
PRIVACY_AR = [
    ("من نحن", f"<p>شركة أفلاك للاستقدام، مرخّصة من وزارة الموارد البشرية والتنمية الاجتماعية برقم {LICENSE}، وسجل تجاري رقم {CR}، ومقرها الرياض، حي قرطبة، شارع خالد بن الوليد. هذه السياسة توضح كيف نجمع بياناتك الشخصية ونستخدمها ونحميها عند استخدامك هذا الموقع.</p>"),
    ("البيانات التي نجمعها", "<ul><li><b>عند إرسال نموذج الطلب:</b> الاسم، ورقم الجوال، والخدمة والجنسية المفضلة، والملاحظات (اختيارية).</li><li><b>عند التواصل معنا</b> عبر واتساب أو الهاتف أو البريد الإلكتروني: ما ترسله إلينا من معلومات.</li><li><b>بيانات الاستخدام</b> (عند تفعيل الإحصائيات): الصفحات التي تزورها، ونوع الجهاز والمتصفح، والموقع التقريبي، ومعرّف ملف تعريف الارتباط.</li><li><b>بيانات السير الذاتية المنشورة للعمالة:</b> الاسم، والجنسية، والمهنة، والعمر، والديانة، والحالة الاجتماعية، والخبرة، والرقم المرجعي، وملف السيرة الذاتية. تُنشر بموافقة صاحب السيرة ولغرض الاستقدام فقط.</li></ul>"),
    ("لماذا نستخدم بياناتك", "<ul><li>الرد على استفساراتك وطلباتك ومتابعتها.</li><li>ترشيح الخيارات المناسبة لك.</li><li>تحسين الموقع وفهم كيفية استخدامه.</li><li>الالتزام بالأنظمة المعمول بها.</li></ul>"),
    ("موافقتك", "<p>بإرسالك نموذج الطلب أو تواصلك معنا فإنك توافق على معالجة بياناتك وفق هذه السياسة. يمكنك سحب موافقتك في أي وقت بالتواصل معنا.</p>"),
    ("مشاركة البيانات ومزوّدو الخدمة", "<p>لا نبيع بياناتك. قد تُعالج بياناتك عبر مزوّدي خدمات نستخدمهم لتشغيل الموقع والتواصل معك، ومنهم: واتساب (Meta)، وGoogle (البريد، والجداول، والإحصائيات، والخرائط)، وGitHub (استضافة الموقع). وقد تتم المعالجة على خوادم خارج المملكة. ونتخذ ما يلزم لحماية بياناتك وفق الأنظمة.</p>"),
    ("ملفات تعريف الارتباط (Cookies)", "<p>قد نستخدم Google Analytics لقياس الزيارات وتحسين الموقع، وهو يعتمد على ملفات تعريف الارتباط. يمكنك حظرها أو حذفها من إعدادات المتصفح.</p>"),
    ("مدة الاحتفاظ", "<p>نحتفظ بالبيانات للمدة اللازمة لتحقيق الغرض منها أو للالتزام بالأنظمة، ثم نحذفها أو نُخفي هويتها.</p>"),
    ("حقوقك", f"<p>لك الحق في معرفة بياناتك، والاطلاع عليها، وطلب تصحيحها أو حذفها، وسحب موافقتك. لممارسة حقوقك راسلنا على <a href=\"mailto:{EMAIL}\">{EMAIL}</a> أو عبر واتساب، ونسعى للرد خلال 30 يومًا. ولك تقديم شكوى إلى الجهة المختصة (الهيئة السعودية للبيانات والذكاء الاصطناعي) عند الاقتضاء.</p>"),
    ("حماية البيانات", "<p>نتخذ إجراءات تقنية وتنظيمية معقولة لحماية بياناتك من الوصول أو الإفصاح غير المصرّح به. ولا يوجد نقل أو تخزين إلكتروني آمن بنسبة 100%.</p>"),
    ("بيانات الأطفال", "<p>الموقع غير موجّه لمن هم دون 18 عامًا، ولا نجمع بياناتهم عمدًا.</p>"),
    ("تحديث السياسة", f"<p>قد نحدّث هذه السياسة، وسيظهر تاريخ آخر تحديث أدناه. آخر تحديث: {UPDATED}.</p>"),
]
PRIVACY_EN = [
    ("Who we are", f"<p>Aflaak Recruitment Company is licensed by the Ministry of Human Resources and Social Development (license {LICENSE}, commercial registration {CR}) and is based in Riyadh. This policy explains how we collect, use and protect your personal data when you use this website.</p>"),
    ("Data we collect", "<ul><li><b>Request form:</b> name, mobile number, preferred service and nationality, and optional notes.</li><li><b>Contacting us</b> by WhatsApp, phone or email: the information you send us.</li><li><b>Usage data</b> (when analytics is enabled): pages visited, device and browser type, approximate location, and a cookie identifier.</li><li><b>Published worker CVs:</b> name, nationality, job, age, religion, marital status, experience, reference number and the CV file. Published with the CV owner's consent and for recruitment purposes only.</li></ul>"),
    ("Why we use your data", "<ul><li>To answer and follow up on your inquiries and requests.</li><li>To suggest suitable options.</li><li>To improve the website.</li><li>To comply with applicable regulations.</li></ul>"),
    ("Your consent", "<p>By sending the request form or contacting us you agree to the processing of your data under this policy. You may withdraw your consent at any time by contacting us.</p>"),
    ("Sharing and service providers", "<p>We do not sell your data. Your data may be processed by service providers we use to run the site and communicate with you, including WhatsApp (Meta), Google (email, sheets, analytics, maps) and GitHub (website hosting). Processing may take place on servers outside the Kingdom. We take the steps required by law to protect your data.</p>"),
    ("Cookies", "<p>We may use Google Analytics to measure visits and improve the site; it relies on cookies. You can block or delete cookies in your browser settings.</p>"),
    ("Retention", "<p>We keep data for as long as needed for its purpose or to comply with regulations, then delete it or anonymize it.</p>"),
    ("Your rights", f"<p>You have the right to know about, access, correct or delete your data and to withdraw consent. To exercise your rights, email <a href=\"mailto:{EMAIL}\">{EMAIL}</a> or message us on WhatsApp; we aim to reply within 30 days. You may also complain to the competent authority (the Saudi Data and AI Authority).</p>"),
    ("Data security", "<p>We take reasonable technical and organizational measures to protect your data. No method of electronic transmission or storage is 100% secure.</p>"),
    ("Children", "<p>This website is not directed at people under 18 and we do not knowingly collect their data.</p>"),
    ("Updates", f"<p>We may update this policy; the last-updated date is shown here. Last updated: {UPDATED}.</p>"),
]
wa = wa_link("السلام عليكم، لدي استفسار عن سياسة الخصوصية.")
ld = {"@context": "https://schema.org", "@type": "WebPage", "name": "سياسة الخصوصية", "url": BASE + "privacy.html"}
out = head("", "سياسة الخصوصية | أفلاك للاستقدام", "سياسة الخصوصية لشركة أفلاك للاستقدام: البيانات التي نجمعها وكيف نستخدمها وحقوقك.", BASE + "privacy.html", ld) + header("", wa)
out += '<section class="lp-hero"><div class="wrap"><nav class="crumbs"><a href="index.html">الرئيسية</a> › <span>سياسة الخصوصية</span></nav><h1>سياسة الخصوصية</h1><p class="lead">نحترم خصوصيتك. توضح هذه الصفحة البيانات التي نجمعها وكيف نستخدمها. <a href="#en" style="color:#fff;text-decoration:underline">English version below</a></p></div></section>\n'
out += '<section class="s"><div class="wrap prose privacy">' + "".join(f"<h2>{E(t)}</h2>{b}" for t, b in PRIVACY_AR) + '</div></section>\n'
out += '<section class="s alt" id="en"><div class="wrap prose privacy" dir="ltr" lang="en"><h1 style="font-size:32px;margin-bottom:12px">Privacy Policy</h1>' + "".join(f"<h2>{E(t)}</h2>{b}" for t, b in PRIVACY_EN) + '</div></section>\n'
out += footer("", wa)
write("privacy.html", out)
urls.append(BASE + "privacy.html")

# ---------------- sitemap ----------------
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for i, u in enumerate(urls):
    pr = "1.0" if i == 0 else ("0.4" if u.endswith("privacy.html") else "0.8")
    sm += f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{UPDATED}</lastmod>\n    <changefreq>{'weekly' if i == 0 else 'monthly'}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n"
sm += "</urlset>\n"
write("sitemap.xml", sm)
print("pages written:", len(urls) - 1, "+ sitemap")
