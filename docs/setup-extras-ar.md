# إعدادات إضافية (مجانية)

## 1) تسجيل طلبات الفورم في Google Sheets (اختياري)
كل طلب يُرسل من النموذج يُسجَّل كسطر في جدول Google، إضافةً إلى واتساب.

1. افتح https://sheets.google.com وأنشئ جدولًا جديدًا باسم "طلبات أفلاك".
2. في الصف الأول اكتب العناوين: `الوقت | الخدمة | الجنسية | الاسم | الجوال | ملاحظات | اللغة | الصفحة`
3. من القائمة: **Extensions ← Apps Script**. امسح الكود وألصق:

```javascript
function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    if (d.website) return ContentService.createTextOutput("ok");          // فخّ للروبوتات
    var clean = function (v, n) { return String(v || "").slice(0, n); };
    var sh = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    sh.appendRow([new Date(), clean(d.service, 40), clean(d.nationality, 40), clean(d.name, 120),
                  clean(d.phone, 40), clean(d.note, 500), clean(d.lang, 5), clean(d.page, 300)]);
  } catch (err) {}
  return ContentService.createTextOutput("ok");
}
```
4. اضغط **Deploy ← New deployment ← Select type: Web app**. اختر: Execute as **Me**، وWho has access **Anyone**. ثم **Deploy** ووافق على الصلاحيات.
5. انسخ **Web app URL** (يبدأ بـ https://script.google.com/macros/s/...).
6. في `index.html` ابحث عن `window.SHEET_URL=""` وضع الرابط بين علامتي التنصيص. ثم ارفع الملف.
> بيانات العملاء ستُحفظ في حسابك: لا تشارك الجدول إلا مع من يلزم. وهي مذكورة في صفحة الخصوصية.

## 2) Google Analytics 4
راجع قسم الإحصائيات في `README.md` (ضع `G-XXXXXXXXXX` في `window.GA_ID`).

## 3) Bing Webmaster Tools (يظهر موقعك في بحث Bing)
1. ادخل https://www.bing.com/webmasters وسجّل بحساب Microsoft أو Google.
2. اختر **Import your sites from Google Search Console** (استيراد بنقرة، بدون كود).
3. بعد الاستيراد أرسل `sitemap.xml` من قسم Sitemaps.

## 4) UptimeRobot (ينبّهك لو وقع الموقع)
1. سجّل مجانًا في https://uptimerobot.com
2. **Add New Monitor**: النوع HTTP(s)، الرابط رابط موقعك، الفاصل 5 دقائق.
3. أضف بريدك في Alert Contacts ليصلك التنبيه.

## 5) رمز QR للموقع
الملف `assets/img/qr-site.png` يحمل رابط الموقع الحالي. اطبعه أو ضعه في الحالة وبطاقات العمل. **بعد شراء دومين جديد يجب تغييره** (أخبرني وأولّده لك).

## 6) حالة العاملة (متاحة / محجوزة / إخفاء مؤقتًا)
- من Pages CMS ← **السير الذاتية (تعديل البيانات)** ← اضغط على العاملة ← حقل **الحالة** ← Save.
- **محجوزة:** تظهر شارة "محجوزة" ويتعطّل زر الاختيار، وتنزل لآخر القائمة.
- **إخفاء مؤقتًا:** تختفي من الموقع بدون حذفها.
- السير الجديدة تُسجَّل تلقائيًا "متاحة".
- لو لم يظهر حقل "الحالة" في Pages CMS: افتح **Configuration** وألصق آخر نسخة من ملف `.pages.yml`.

## 7) صفحات الخدمات والجنسيات وصفحة الخصوصية
- مولّدة بواسطة `scripts/build_pages.py` (تشغيله اختياري). لتعديل نص صفحة: عدّل القوائم داخل الملف وشغّله، أو عدّل ملف الـ HTML مباشرة.
- بعد شراء دومين: غيّر `BASE` داخل الملف وشغّله ليُحدَّث `sitemap.xml` وروابط الصفحات.
- **صفحة الخصوصية:** نموذج عام مبني على متطلبات نظام حماية البيانات الشخصية. يُفضّل أن يراجعها مستشار قانوني، وأن تحدد الإدارة مدة الاحتفاظ بالبيانات، وتتحقق إن كان يلزم تسجيل الشركة كجهة تحكم لدى الهيئة السعودية للبيانات والذكاء الاصطناعي (سدايا).
