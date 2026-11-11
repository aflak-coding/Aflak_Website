# موقع شركة أفلاك للاستقدام

موقع ثابت (HTML / CSS / JS) على GitHub Pages، الدومين: https://aflakrecruitment.com

## خريطة المجلدات

```
/
├── index.html                الصفحة الرئيسية
├── privacy.html              سياسة الخصوصية
├── services/                 صفحات الخدمات (تتولد من scripts/build_pages.py)
├── nationalities/            صفحات الجنسيات (تتولد من scripts/build_pages.py)
├── assets/                   style.css و app.js وبيانات الطاقم/التقييمات والصور
├── data/                     cvs-<الدولة>.json: بيانات السير (تتحدث تلقائيًا + من Pages CMS)
├── cvs/<الدولة>/             ملفات PDF للسير (ارفعها هنا فقط)
├── cvs/photos/               صور العاملات (تُستخرج تلقائيًا)
├── scripts/                  process_cvs.py (قراءة السير) و build_pages.py (توليد الصفحات)
├── .github/workflows/        الأتمتة: process-cvs.yml (معالجة السير) و jekyll-gh-pages.yml (النشر)
├── .pages.yml                إعدادات لوحة Pages CMS
└── docs/                     أدلة داخلية (دليل الزملاء، إعدادات إضافية)
```

## ملفات لازم تفضل في الجذر (لا تنقلها ولا تحذفها)
`index.html` · `CNAME` (الدومين) · `robots.txt` · `sitemap.xml` · `favicon.ico` · `manifest.webmanifest` ·
`BingSiteAuth.xml` و `google….html` (توثيق ملكية الموقع لبينج وجوجل) · `.nojekyll` · `.pages.yml` · `404.html`

## إضافة السير الذاتية
ارفع ملفات PDF داخل `cvs/<الدولة>/`، والـ GitHub Action تقرأ البيانات وتضيفها وتنشر الموقع (راجع `docs/guide-for-colleagues-ar.md`).

## تعديل صفحات الخدمات والجنسيات
عدّل `scripts/build_pages.py` ثم شغّله (`python scripts/build_pages.py`) وارفع المجلدات `services/` و`nationalities/` و`sitemap.xml`. لا تعدّل ملفات HTML المتولدة يدويًا.

## ملاحظة أمان
المستودع والملفات عامة، فأي PDF يُرفع يظهر لأي شخص. لا ترفع إلا السير الذاتية فقط.
