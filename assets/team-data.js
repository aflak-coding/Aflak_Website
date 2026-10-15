  // ===== جهات التواصل (الهيكل التنظيمي) =====
  // row: ترتيب الصف (1 = الأعلى ، 2 = الذي تحته). الصف الذي فيه خانة واحدة يظهر في المنتصف.
  // icon: chair (تاج) | vice (درع) | calc (محاسب) | group (مجموعة) | person (شخص)
  // color: c1 كحلي غامق | c2 أزرق | c3 أخضر | c4 بنفسجي
  // phone: الرقم بالصيغة الدولية بدون + وبدون أصفار (السعودية 9665xxxxxxxx)
  // msg_ar / msg_en: نص الرسالة الجاهزة في واتساب (اختياري)
  window.TEAM_DATA = [
    {row:1, icon:"chair", color:"c1", ar:"للشكاوى / الإدارة", en:"Complaints / Management", phone:"966554084322",
     msg_ar:"السلام عليكم، أرغب في تقديم شكوى أو ملاحظة بخصوص خدمات الشركة.", msg_en:"Hello, I would like to submit a complaint or feedback about the company's services."},
    {row:1, icon:"vice",  color:"c2", ar:"للاستعلام",          en:"Inquiries",              phone:"966559091933",
     msg_ar:"السلام عليكم، أرغب في الاستعلام عن خدمات الاستقدام.", msg_en:"Hello, I would like to ask about your recruitment services."},
    {row:2, icon:"group", color:"c4", ar:"للتوظيف",            en:"Recruitment",            phone:"966502255955",
     msg_ar:"السلام عليكم، أرغب في التقديم للعمل لدى الشركة.", msg_en:"Hello, I would like to apply for a job at the company."}
  ];
