/* إحصائيات الزيارات (Google Analytics 4). لا يعمل إلا لو وضعت الرقم في window.GA_ID داخل index.html */
(function(){
  var id=window.GA_ID;
  if(!id||!/^G-[A-Z0-9]{6,}$/i.test(id)) return;
  window.dataLayer=window.dataLayer||[];
  function gtag(){window.dataLayer.push(arguments);}
  window.gtag=gtag;
  var s=document.createElement("script"); s.async=true;
  s.src="https://www.googletagmanager.com/gtag/js?id="+encodeURIComponent(id);
  document.head.appendChild(s);
  gtag("js",new Date());
  gtag("config",id,{anonymize_ip:true});
  function ev(name,params){try{gtag("event",name,params||{});}catch(e){}}
  document.addEventListener("click",function(e){
    var t=e.target.closest?e.target.closest("a,button,.flag"):null; if(!t) return;
    var href=(t.getAttribute&&t.getAttribute("href"))||"";
    if(t.classList.contains("flag")){ev("nationality_view",{nationality:t.getAttribute("data-nat")});return;}
    if(t.closest(".cv-card")&&t.tagName==="BUTTON"){ev(t.classList.contains("btn-wa")?"cv_select_whatsapp":"cv_view",{});return;}
    if(/wa\.me\//.test(href)){ev("whatsapp_click",{place:t.closest(".org-box")?"team":(t.closest("footer")?"footer":"page")});return;}
    if(/^tel:/.test(href)){ev("call_click",{});return;}
    if(/^mailto:|mail\.google\.com/.test(href)){ev("email_click",{});return;}
    if(/snapchat\.com|instagram\.com/.test(href)){ev("social_click",{});return;}
    if(/maps\.app\.goo\.gl|google\.com\/maps/.test(href)){ev("map_click",{});return;}
  });
  document.addEventListener("submit",function(e){
    if(e.target&&e.target.id==="orderForm"){var s=document.getElementById("fType");ev("order_form_submit",{service:s?s.value:""});}
  });
})();
