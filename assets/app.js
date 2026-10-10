(function(){
  var WA = "966554084322";
  var ORDER_NUMS = ["966559091933","966554566335","966505538004","966502255955","966505538006","966554144889"];
  var D = {
    ar:{
      brand:"أفلاك للاستقدام", nav_services:"الخدمات", nav_faq:"أسئلة شائعة", nav_contact:"تواصل معنا", nav_team:"فريقنا", nav_home:"الرئيسية", nav_nat:"الجنسيات", map_h:"موقعنا", ft_links:"روابط سريعة", ft_about:"أفلاك للاستقدام مكتب مرخّص من وزارة الموارد البشرية والتنمية الاجتماعية، يقدّم خدمات استقدام العمالة المنزلية في الرياض بخدمة احترافية ومتابعة مستمرة.", ft_rights:"جميع الحقوق محفوظة © 2026 أفلاك للاستقدام",
      hero_h:"مع أفلاك الخدمة معاك",
      hero_p:"نسهّل لك رحلة استقدام العمالة المنزلية من خلال خدمة احترافية، خيارات موثوقة، ومتابعة مستمرة.",
      cta_start:"ابدأ طلبك", cta_svc:"تعرّف على خدماتنا",
      svc_h:"خدماتنا", svc_sub:"اضغط على أي خدمة لننتقل مباشرة إلى نموذج الطلب.",
      svc1:"استقدام عاملة منزلية", svc1d:"عاملة تتولى شؤون البيت من تنظيف وترتيب، ويمكنها العناية بالأطفال. أخبرنا بما يناسب أسرتك ونرشّح لك الأنسب.",
      svc2:"استقدام سائق خاص", svc2d:"سائق لتنقلات الأسرة اليومية. حدّد الجنسية التي تفضلها ونتابع معك الإجراءات.",
      ask:"اطلب هذه الخدمة",
      nat_h:"الجنسيات المتاحة", nat_sub:"نستقدم من ست دول. اضغط على علم الدولة لتصفّح السير الذاتية.", n1:"كينيا", n2:"بنغلاديش", n3:"الفلبين", n4:"إثيوبيا", n5:"سريلانكا", n6:"أوغندا",
      c_h:"املأ بياناتك ونتواصل معك", c_sub:"يصل طلبك إلينا على واتساب، ونرد عليك في ساعات العمل.",
      c_wa:"واتساب", c_phone:"اتصال", c_mail:"البريد الإلكتروني", c_addr:"العنوان",
      addr:"شارع خالد بن الوليد، حي قرطبة، الدور الأول فوق صيدلية كنوز، مكتب 34، الرياض",
      c_hours:"ساعات العمل", hours:"يوميًا من 9 صباحًا حتى 11 مساءً", c_social:"حسابات التواصل", c_map:"فتح في خرائط جوجل", ct_h:"بيانات التواصل", ct_pin:"شركة أفلاك للاستقدام", team_h:"فريق العمل", team_sub:"تواصل مع أي فرد من فريقنا مباشرة عبر واتساب.", team_wa:"تواصل عبر واتساب", team_call:"اتصال", ft_support:"لمزيد من الدعم", msg_team:"السلام عليكم، أود التواصل بخصوص خدمات أفلاك للاستقدام.",
      f_h:"طلب خدمة", f_type:"الخدمة المطلوبة", f_nat:"الجنسية المفضلة", f_name:"الاسم", f_phone:"رقم الجوال", f_note:"ملاحظات (اختياري)", f_send:"أرسل الطلب عبر واتساب", any:"أي جنسية",
      cv_newtab:"فتح في تبويب جديد", cv_close:"إغلاق", cv_back:"رجوع للجنسيات", cv_title:"السير الذاتية: ", cv_count:"{n} سيرة ذاتية متاحة", cv_view:"عرض السيرة الذاتية (PDF)", cv_pick:"اختيار وإرسال عبر واتساب",
      cv_empty:"سيتم إضافة السير الذاتية لهذه الجنسية قريبًا. تواصل معنا على واتساب لنرشّح لك الأنسب.",
      f_age:"العمر", f_rel:"الديانة", f_st:"الحالة", f_exp:"الخبرة", age_u:"{n} سنة", rel_m:"مسلم", rel_o:"غير مسلم", st_s:"غير متزوج", st_m:"متزوج", exp_new:"قادم جديد", exp_prev:"خبرة سابقة",
      more_h:"أرسل الطلب لباقي أرقامنا", more_p:"فتحنا لك واتساب على الرقم الأول. اضغط على كل رقم بالترتيب لإرسال نفس الطلب.", more_done:"تم",
      msg_pick:"السلام عليكم، أرغب في اختيار: ", msg_cv:"رابط السيرة الذاتية: ", msg_ref:"الرقم المرجعي: ",
      faq_h:"أسئلة شائعة", faq_sub:"أجوبة سريعة قبل أن تتواصل معنا.",
      q6:"ما الخدمات المتاحة؟", a6:"استقدام عاملة منزلية وسائق شخصي، ويمكنك أيضًا طلب طباخ أو طباخة، أو ممرضة منزلية، أو مساعدة شخصية من نموذج الطلب.",
      q1:"هل المكتب مرخّص؟", a1:"نعم. مكتب مرخّص من وزارة الموارد البشرية والتنمية الاجتماعية برقم 3801238، وسجلنا التجاري رقم 7004359431.",
      q3:"كم السعر؟", a3:"يختلف السعر حسب الخدمة والجنسية. راسلنا على واتساب ونرسل لك التفاصيل.",
      q4:"ما الجنسيات المتاحة؟", a4:"كينيا، بنغلاديش، الفلبين، إثيوبيا، سريلانكا، وأوغندا.",
      q5:"أين المكتب ومتى يفتح؟", a5:"في الرياض، حي قرطبة، شارع خالد بن الوليد، الدور الأول فوق صيدلية كنوز، مكتب 34. نعمل يوميًا من 9 صباحًا حتى 11 مساءً.",
      foot1:"أفلاك للاستقدام | الرياض، المملكة العربية السعودية", foot2:"ترخيص 3801238 | سجل تجاري 7004359431",
      msg_hello:"السلام عليكم، أرغب في طلب: ", msg_nat:"الجنسية المفضلة: ", msg_name:"الاسم: ", msg_phone:"الجوال: ", msg_note:"ملاحظات: ",
      msg_gen:"السلام عليكم، أريد الاستفسار عن خدمات الاستقدام.",
      svcs:{svc1:"عاملة منزلية",svc2:"سائق شخصي",svc3:"طباخ / طباخة",svc4:"ممرضة منزلية",svc5:"مساعدة شخصية"}, title:"أفلاك للاستقدام | مكتب استقدام مرخّص في الرياض", alt:"أفلاك للاستقدام"
    },
    en:{
      brand:"Aflaak Recruitment", nav_services:"Services", nav_faq:"FAQ", nav_contact:"Contact", nav_team:"Our team", nav_home:"Home", nav_nat:"Nationalities", map_h:"Our location", ft_links:"Quick links", ft_about:"Aflaak Recruitment is an office licensed by the Ministry of Human Resources and Social Development, providing household worker recruitment services in Riyadh with professional service and ongoing follow-up.", ft_rights:"\u00a9 2026 Aflaak Recruitment. All rights reserved.",
      hero_h:"With Aflaak, service is with you",
      hero_p:"We make your household recruitment journey easier with a professional service, trusted options, and ongoing follow-up.",
      cta_start:"Start your request", cta_svc:"See our services",
      svc_h:"Our services", svc_sub:"Tap any service to jump straight to the request form.",
      svc1:"Recruit a housemaid", svc1d:"A housemaid who takes care of the home, from cleaning to tidying, and can also look after children. Tell us what suits your family and we'll suggest the best match.",
      svc2:"Recruit a private driver", svc2d:"A driver for your family's daily trips. Choose the nationality you prefer and we'll follow up on the paperwork with you.",
      ask:"Request this service",
      nat_h:"Available nationalities", nat_sub:"We recruit from six countries. Tap a flag to browse CVs.", n1:"Kenya", n2:"Bangladesh", n3:"Philippines", n4:"Ethiopia", n5:"Sri Lanka", n6:"Uganda",
      c_h:"Fill in your details and we'll contact you", c_sub:"Your request reaches us on WhatsApp and we reply during working hours.",
      c_wa:"WhatsApp", c_phone:"Phone", c_mail:"Email", c_addr:"Address",
      addr:"Khalid Bin Al Waleed Street, Qurtubah, first floor above Kunooz Pharmacy, office 34, Riyadh",
      c_hours:"Working hours", hours:"Daily, 9 AM to 11 PM", c_social:"Social accounts", c_map:"Open in Maps", ct_h:"Contact details", ct_pin:"Aflaak Recruitment Office", team_h:"Our team", team_sub:"Message any of our team directly on WhatsApp.", team_wa:"Message on WhatsApp", team_call:"Call", ft_support:"More support", msg_team:"Hello, I would like to ask about Aflaak Recruitment's services.",
      f_h:"Service request", f_type:"Service needed", f_nat:"Preferred nationality", f_name:"Name", f_phone:"Mobile number", f_note:"Notes (optional)", f_send:"Send request on WhatsApp", any:"Any nationality",
      cv_newtab:"Open in new tab", cv_close:"Close", cv_back:"Back to nationalities", cv_title:"CVs: ", cv_count:"{n} CVs available", cv_view:"View CV (PDF)", cv_pick:"Select & send on WhatsApp",
      cv_empty:"CVs for this nationality will be added soon. Message us on WhatsApp and we'll suggest the best match.",
      f_age:"Age", f_rel:"Religion", f_st:"Status", f_exp:"Experience", age_u:"{n} years", rel_m:"Muslim", rel_o:"Non-Muslim", st_s:"Single", st_m:"Married", exp_new:"New arrival", exp_prev:"Previous experience",
      more_h:"Send the request to our other numbers", more_p:"WhatsApp opened for the first number. Tap each number in order to send the same request.", more_done:"Sent",
      msg_pick:"Hello, I would like to select: ", msg_cv:"CV link: ", msg_ref:"Reference no.: ",
      faq_h:"FAQ", faq_sub:"Quick answers before you get in touch.",
      q6:"Which services do you offer?", a6:"Recruiting a housemaid or a personal driver. You can also request a cook, a home nurse or a personal assistant through the request form.",
      q1:"Is the office licensed?", a1:"Yes. We are licensed by the Ministry of Human Resources and Social Development (license 3801238), and our commercial registration is 7004359431.",
      q3:"How much does it cost?", a3:"Prices depend on the service and nationality. Message us on WhatsApp and we'll send the details.",
      q4:"Which nationalities are available?", a4:"Kenya, Bangladesh, the Philippines, Ethiopia, Sri Lanka and Uganda.",
      q5:"Where is the office and when is it open?", a5:"In Riyadh, Qurtubah district, Khalid Bin Al Waleed Street, first floor above Kunooz Pharmacy, office 34. Open daily from 9 AM to 11 PM.",
      foot1:"Aflaak Recruitment | Riyadh, Saudi Arabia", foot2:"License 3801238 | Commercial registration 7004359431",
      msg_hello:"Hello, I would like to request: ", msg_nat:"Preferred nationality: ", msg_name:"Name: ", msg_phone:"Mobile: ", msg_note:"Notes: ",
      msg_gen:"Hello, I would like to ask about your recruitment services.",
      svcs:{svc1:"Housemaid",svc2:"Personal driver",svc3:"Cook",svc4:"Home nurse",svc5:"Personal assistant"}, title:"Aflaak Recruitment | Licensed recruitment office in Riyadh", alt:"Aflaak Recruitment Office"
    }
  };
  var lang="ar";
  try{var s=localStorage.getItem("aflak-lang"); if(s==="en"||s==="ar") lang=s;}catch(e){}
  function $(id){return document.getElementById(id);}
  function wa(t){return "https://wa.me/"+WA+"?text="+encodeURIComponent(t);}

  function apply(){
    var d=D[lang];
    document.documentElement.lang=lang;
    document.documentElement.dir=lang==="ar"?"rtl":"ltr";
    document.title=d.title;
    document.querySelectorAll("[data-i18n]").forEach(function(el){var k=el.getAttribute("data-i18n"); if(d[k]!==undefined) el.textContent=d[k];});
    $("langBtn").textContent = lang==="ar" ? "English" : "العربية";
    $("langBtn").setAttribute("aria-label", lang==="ar" ? "Change language to English" : "تغيير اللغة إلى العربية");
    Array.prototype.forEach.call($("fType").options,function(o){o.textContent=d.svcs[o.value];});
    Array.prototype.forEach.call($("fNat").options,function(o){o.textContent=(o.value==="any")?d.any:d[o.value];});
    document.querySelector(".logo-card img").alt=d.alt;
    var gen=wa(d.msg_gen);
    ["waLink","waIco","fab"].forEach(function(id){var e=$(id); if(e) e.href=gen;});
    document.querySelectorAll(".wa-gen").forEach(function(a){a.href=gen;});
    renderCVs();
    renderTeam();
    renderMore();
  }

  function goOrder(svc){
    if(svc && $("fType").querySelector('option[value="'+svc+'"]')) $("fType").value=svc;
    var f=$("order");
    f.scrollIntoView({behavior:"smooth",block:"start"});
    var form=$("orderForm"); form.classList.add("flash");
    setTimeout(function(){form.classList.remove("flash");},1600);
    setTimeout(function(){try{$("fName").focus({preventScroll:true});}catch(e){$("fName").focus();}},700);
  }

  $("langBtn").addEventListener("click",function(){
    lang = lang==="ar" ? "en" : "ar";
    try{localStorage.setItem("aflak-lang",lang);}catch(e){}
    apply();
  });
  document.querySelectorAll(".row").forEach(function(r){
    r.addEventListener("click",function(){goOrder(r.getAttribute("data-svc"));});
  });
  document.querySelectorAll("[data-goorder]").forEach(function(a){
    a.addEventListener("click",function(e){e.preventDefault();goOrder();});
  });
  $("orderForm").addEventListener("submit",function(e){
    e.preventDefault();
    var d=D[lang], nat=$("fNat").value;
    var msg=d.msg_hello+d.svcs[$("fType").value]+"\n"+d.msg_nat+(nat==="any"?d.any:d[nat])+"\n"+d.msg_name+$("fName").value.trim()+"\n"+d.msg_phone+$("fPhone").value.trim();
    var note=$("fNote").value.trim(); if(note) msg+="\n"+d.msg_note+note;
    pend={msg:msg,done:ORDER_NUMS.map(function(_,i){return i===0;})};
    window.open(waTo(ORDER_NUMS[0],msg),"_blank","noopener");
    renderMore();
    $("more").scrollIntoView({behavior:"smooth",block:"nearest"});
  });

  var pend=null;
  function waTo(n,t){return "https://wa.me/"+n+"?text="+encodeURIComponent(t);}
  function fmtNum(n){return "+"+n.slice(0,3)+" "+n.slice(3,5)+" "+n.slice(5,8)+" "+n.slice(8);}
  function renderMore(){
    var box=$("more");
    if(!pend){box.hidden=true;return;}
    var d=D[lang];
    box.hidden=false; box.textContent="";
    box.appendChild(mk("b","",d.more_h));
    box.appendChild(mk("p","",d.more_p));
    var nextI=pend.done.indexOf(false);
    ORDER_NUMS.forEach(function(n,i){
      var b=mk("button","btn btn-line more-btn"+(pend.done[i]?" done":"")+(i===nextI?" next":""));
      b.type="button";
      b.appendChild(mk("span","mi",String(i+1)));
      b.appendChild(mk("span","ltr",fmtNum(n)));
      if(pend.done[i]) b.appendChild(mk("span","ok","\u2713 "+d.more_done));
      b.addEventListener("click",function(){
        pend.done[i]=true;
        window.open(waTo(n,pend.msg),"_blank","noopener");
        renderMore();
      });
      box.appendChild(b);
    });
  }

  var CVS = window.CVS_DATA || {};
  function relPath(p){return String(p||"").replace(/^\/+/,"");}
  function loadCVJson(){
    return fetch("data/cvs.json?v="+Date.now()).then(function(r){return r.ok?r.json():[];}).then(function(arr){
      if(!Array.isArray(arr)) return;
      var merged={n1:[],n2:[],n3:[],n4:[],n5:[],n6:[]};
      Object.keys(CVS).forEach(function(k){merged[k]=(CVS[k]||[]).slice();});
      arr.forEach(function(w){
        if(!w||!w.nat||!w.file||!w.name) return;
        w.file=relPath(w.file); if(w.photo) w.photo=relPath(w.photo);
        (merged[w.nat]=merged[w.nat]||[]).push(w);
      });
      CVS=merged; renderCVs();
    }).catch(function(){});
  }
  var curNat=null;
  function mk(t,c,x){var e=document.createElement(t); if(c) e.className=c; if(x!==undefined) e.textContent=x; return e;}
  function renderCVs(){
    var sec=$("cvs");
    if(!curNat){sec.hidden=true; return;}
    var d=D[lang], list=CVS[curNat]||[], grid=$("cvGrid");
    sec.hidden=false;
    $("cvTitle").textContent=d.cv_title+d[curNat];
    $("cvCount").textContent=list.length?d.cv_count.replace("{n}",list.length):"";
    $("cvEmpty").hidden=list.length>0;
    grid.textContent="";
    list.forEach(function(w){
      var url=new URL(w.file,location.href).href;
      var card=mk("div","cv-card");
      var top=mk("div","cv-top");
      if(w.photo){
        var im=mk("img","cv-photo"); im.src=w.photo; im.alt=w.name; im.width=72; im.height=88; im.loading="lazy"; top.appendChild(im);
      } else {
        var ic=mk("div","cv-ic"); ic.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/></svg>';
        top.appendChild(ic);
      }
      var tt=mk("div"); tt.appendChild(mk("h3","",w.name));
      var meta=[]; if(w.job&&d.svcs[w.job]) meta.push(d.svcs[w.job]); if(w.ref) meta.push(d.msg_ref+w.ref);
      if(meta.length) tt.appendChild(mk("p","cv-meta",meta.join(" | ")));
      top.appendChild(tt); card.appendChild(top);
      var facts=[];
      if(w.age) facts.push([d.f_age,d.age_u.replace("{n}",w.age)]);
      if(w.rel) facts.push([d.f_rel,d["rel_"+w.rel]]);
      if(w.st) facts.push([d.f_st,d["st_"+w.st]]);
      if(w.exp) facts.push([d.f_exp,d["exp_"+w.exp]]);
      if(facts.length){
        var dl=mk("dl","cv-facts");
        facts.forEach(function(f){var r=mk("div"); r.appendChild(mk("dt","",f[0])); r.appendChild(mk("dd","",f[1])); dl.appendChild(r);});
        card.appendChild(dl);
      }
      var v=mk("button","btn btn-line",d.cv_view); v.type="button"; card.appendChild(v);
      v.addEventListener("click",function(){openViewer(w,url,function(){p.click();});});
      var p=mk("button","btn btn-wa",d.cv_pick); p.type="button";
      p.addEventListener("click",function(){
        var m=d.msg_pick+w.name+(w.ref?" ("+w.ref+")":"")+"\n"+d.msg_nat+d[curNat]+(w.job&&d.svcs[w.job]?"\n"+d.svcs[w.job]:"")+"\n"+d.msg_cv+url;
        window.open(wa(m),"_blank","noopener");
      });
      card.appendChild(p);
      grid.appendChild(card);
    });
  }
  function openViewer(w,url,pick){
    var dlg=$("cvDlg");
    if(!dlg.showModal||window.matchMedia("(pointer:coarse)").matches||window.innerWidth<700){window.open(url,"_blank","noopener");return;}
    $("cvDlgName").textContent=w.name;
    $("cvDlgOpen").href=url;
    $("cvDlgPick").onclick=function(){dlg.close();pick();};
    $("cvFrame").src=url;
    dlg.showModal();
  }
  $("cvDlgClose").addEventListener("click",function(){$("cvDlg").close();});
  $("cvDlg").addEventListener("click",function(e){if(e.target===this) this.close();});
  $("cvDlg").addEventListener("close",function(){$("cvFrame").src="about:blank";});
  function openNat(k){
    curNat=k;
    document.querySelectorAll(".flag[data-nat]").forEach(function(f){f.setAttribute("aria-pressed",f.getAttribute("data-nat")===k?"true":"false");});
    renderCVs();
    $("cvs").scrollIntoView({behavior:"smooth",block:"start"});
  }
  document.querySelectorAll(".flag[data-nat]").forEach(function(f){
    f.addEventListener("click",function(){openNat(f.getAttribute("data-nat"));});
    f.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();openNat(f.getAttribute("data-nat"));}});
  });
  $("cvBack").addEventListener("click",function(){
    curNat=null;
    document.querySelectorAll(".flag[data-nat]").forEach(function(f){f.setAttribute("aria-pressed","false");});
    renderCVs();
    $("nationalities").scrollIntoView({behavior:"smooth",block:"start"});
  });

  var TEAM = window.TEAM_DATA || [];
  var WAI = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16.003 3C8.83 3 3 8.83 3 16c0 2.29.6 4.52 1.74 6.49L3 29l6.7-1.7A12.95 12.95 0 0 0 16 29c7.17 0 13-5.83 13-13S23.17 3 16.003 3zm0 23.7c-1.95 0-3.86-.53-5.53-1.52l-.4-.24-3.98 1.01 1.06-3.88-.26-.4A10.67 10.67 0 0 1 5.3 16c0-5.88 4.82-10.7 10.7-10.7S26.7 10.12 26.7 16s-4.82 10.7-10.7 10.7zm5.87-8c-.32-.16-1.9-.94-2.2-1.04-.3-.1-.5-.16-.72.16-.22.32-.83 1.04-1.02 1.26-.19.22-.38.24-.7.08-.32-.16-1.36-.5-2.59-1.6-.96-.85-1.6-1.9-1.79-2.22-.19-.32-.02-.5.14-.66.15-.14.32-.38.48-.57.16-.19.22-.32.32-.54.1-.22.05-.4-.03-.57-.08-.16-.72-1.74-.99-2.38-.26-.62-.52-.54-.72-.55h-.62c-.22 0-.57.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.12 1.32 3.34c.16.22 2.28 3.48 5.52 4.88.77.33 1.37.53 1.84.68.77.25 1.48.21 2.04.13.62-.09 1.9-.78 2.17-1.53.27-.75.27-1.4.19-1.53-.08-.14-.3-.22-.62-.38z"/></svg>';
  var CALLI = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>';
  function renderTeam(){
    var g=$("teamGrid"); if(!g) return;
    var d=D[lang]; g.textContent="";
    var rows={};
    TEAM.forEach(function(m){var r=m.row||1; (rows[r]=rows[r]||[]).push(m);});
    Object.keys(rows).sort(function(x,y){return x-y;}).forEach(function(r){
      var rowEl=mk("div","team-row"+(Number(r)===1?" apex":""));
      rows[r].forEach(function(m){
        var name=(lang==="en"&&m.en)?m.en:m.ar, role=(lang==="en"&&m.role_en)?m.role_en:m.role_ar;
        var c=mk("div","tm"+(Number(r)===1?" lead":""));
        if(m.photo){var im=mk("img","tm-ph"); im.src=m.photo; im.alt=name; im.width=96; im.height=96; im.loading="lazy"; c.appendChild(im);}
        else c.appendChild(mk("div","tm-ph",name.charAt(0)));
        c.appendChild(mk("h3","",name));
        c.appendChild(mk("p","tm-role",role));
        var b=mk("a","tm-wa"); b.href=waTo(m.phone,d.msg_team); b.target="_blank"; b.rel="noopener";
        b.setAttribute("aria-label",d.team_wa+": "+name); b.title=d.team_wa; b.innerHTML=WAI;
        var cl=mk("a","tm-call"); cl.href="tel:+"+m.phone;
        cl.setAttribute("aria-label",d.team_call+": "+name); cl.title=d.team_call; cl.innerHTML=CALLI;
        var acts=mk("div","tm-acts"); acts.appendChild(b); acts.appendChild(cl);
        c.appendChild(acts); rowEl.appendChild(c);
      });
      g.appendChild(rowEl);
    });
  }

  // scroll reveal
  var rows=document.querySelectorAll(".row");
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(en){ if(en.isIntersecting){en.target.classList.add("in"); io.unobserve(en.target);} });
    },{threshold:0.22});
    rows.forEach(function(r){io.observe(r);});
  } else { rows.forEach(function(r){r.classList.add("in");}); }
  apply();
  loadCVJson();
})();
