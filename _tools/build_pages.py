# يبني صفحات ثابتة لجوجل: الخدمات والمناطق وكل منتج + sitemap.xml
# التشغيل: node _tools/export.js && python3 _tools/build_pages.py
import json, os, html, re, datetime, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "_tools", "products.json"), encoding="utf-8"))
P, CATS, BRANDS, FAQ = D["products"], D["cats"], D["brands"], D["faq"]
SITE = "https://arsmart-eg.com"
WA = "201144772044"
TODAY = datetime.date.today().isoformat()
e = lambda s: html.escape(str(s or ""), quote=True)
wa = lambda m: f"https://wa.me/{WA}?text={urllib.parse.quote(m)}"
fmt = lambda n: f"{int(n):,}"

FAB = open(os.path.join(ROOT, "_tools", "fab.html"), encoding="utf-8").read().strip()

AREAS = [("el-shorouk", "الشروق"), ("new-cairo", "التجمع الخامس"), ("el-obour", "العبور"), ("badr", "بدر"),
         ("madinaty", "مدينتي"), ("al-rehab", "الرحاب"), ("katameya", "القطامية"), ("mokattam", "المقطم"),
         ("nasr-city", "مدينة نصر"), ("sodic-east", "سوديك إيست"), ("sodic-villette", "سوديك فيليت"),
         ("new-capital", "العاصمة الإدارية الجديدة"), ("international-medical-center", "المركز الطبي العالمي"),
         ("sheikh-zayed", "الشيخ زايد")]

SERVICES = [
 dict(slug="cctv", name="كاميرات المراقبة", h1="توريد وتركيب كاميرات مراقبة", cats=["cams", "rec"], ic="cam",
      brands="Hikvision · Dahua · Uniview · Tiandy · Imou · EZVIZ",
      intro="بنصمم ونركّب أنظمة كاميرات مراقبة IP و PoE للفيلات والشقق والشركات والمحلات: كاميرات داخلي وخارجي، رؤية ليلية ملونة، أجهزة تسجيل NVR وهاردات مراقبة، ومشاهدة لايف وتسجيل من الموبايل من أي مكان.",
      pts=["معاينة مجانية وتحديد أماكن الكاميرات من غير نقط عمياء", "كاميرات بدقة 2 و4 و8 ميجا (4K) ورؤية ليلية ملونة ColorVu", "تمديدات مرتبة في مواسير وبوكسات، وتنظيم راك الشبكة", "برمجة التطبيق على موبايلك وتعليمك تستخدمه", "إصلاح وإعادة برمجة الأنظمة القديمة واسترجاع الباسوردات", "ضمان 24 شهر وعقود صيانة دورية"]),
 dict(slug="smart-locks", name="الكوالين الذكية", h1="كوالين ذكية Smart Lock بالبصمة والوجه", cats=["locks"], ic="lock",
      brands="Tuya · Smart Life · Lezn · Levana",
      intro="كوالين ذكية للأبواب الخشب والحديد والألوميتال: فتح بالبصمة أو بصمة الوجه أو الكارت أو الباسورد أو من الموبايل، وموديلات بكاميرا عين سحرية تشوف وتكلم اللي على الباب.",
      pts=["كوالين بصمة ووجه وكارت وباسورد ومفتاح طوارئ", "موديلات بكاميرا عين سحرية وجرس على الموبايل", "تركيب على الباب من غير ما يتأثر شكله", "صلاحيات لكل فرد في البيت وسجل دخول وخروج", "سمارت لوك سيكوريت لأبواب الزجاج بالبصمة أو الوجه (Face ID)", "كوالين فنادق وشقق إيجار", "ضمان 24 شهر"]),
 dict(slug="smart-home", name="السمارت هوم و KNX", h1="سمارت هوم و KNX للفيلات والشقق", cats=["smarthome"], ic="home",
      brands="Tuya / Smart Life · SONOFF · KNX · Surpass",
      intro="حوّل بيتك لبيت ذكي: تحكم في الإضاءة والستائر والتكييف والأجهزة من الموبايل أو بالصوت، مع سيناريوهات تشتغل لوحدها. بنركّب أنظمة واي فاي و Zigbee من غير تكسير، وأنظمة KNX للفيلات أثناء التشطيب.",
      pts=["مفاتيح ذكية تاتش وزراير مكان المفاتيح العادية", "موتورات ستائر وريموت IR للتكييف والتلفزيون", "حساسات حركة وأبواب وتسريب مياه ودخان", "شاشات تحكم وسيناريوهات (خروج، نوم، سينما)", "تشغيل مع Alexa و Google Home", "KNX للفيلات والمشروعات الكبيرة"]),
 dict(slug="intercom", name="الإنتركم الصوتي والمرئي", h1="إنتركم صوتي ومرئي للفيلات والعمارات", cats=["intercom"], ic="int",
      brands="Hikvision · Dahua · Bosch",
      intro="إنتركم صوتي ومرئي IP للفيلات والعمارات والكمبوندات: تشوف وتكلم اللي على الباب وتفتحله من الشاشة أو من الموبايل وانت برا البيت.",
      pts=["كيتات فيلا وشاشات داخلية ووحدات خارجية", "إنتركم عمارات بعدد شقق كبير", "فتح الباب من الموبايل", "ربط مع الكاميرات والأكسيس كنترول", "تركيب وبرمجة وتسليم", "ضمان 24 شهر"]),
 dict(slug="access-control", name="الأكسيس كنترول والحضور والانصراف", h1="أكسيس كنترول وأجهزة حضور وانصراف", cats=["access"], ic="acc",
      brands="ZKTeco · Hikvision · SIB",
      intro="أنظمة أكسيس كنترول للشركات والعمارات والبوابات: أجهزة بصمة وجه وكارت وباسورد، أقفال مغناطيسية وكهربائية، وأجهزة حضور وانصراف بتقارير للموظفين.",
      pts=["أجهزة بصمة وجه وكارت 125KHz و 13.56MHz", "أقفال مغناطيسية وكهربائية وأزرار خروج", "باور سبلاي بمخرج بطارية", "تقارير حضور وانصراف وربط بالسوفتوير", "كروت وتاجات وريموتات", "ضمان 24 شهر"]),
 dict(slug="networking", name="الشبكات والواي فاي", h1="شبكات وواي فاي Ruijie Reyee", cats=["network"], ic="net",
      brands="Ruijie / Reyee · TP-Link · Tenda · Mercusys · UniFi",
      intro="تغطية واي فاي كاملة للفيلات والشركات من غير انقطاع، وسويتشات PoE للكاميرات، وتنظيم راكات. إحنا شريك Ruijie / Reyee معتمد.",
      pts=["تصميم تغطية واي فاي لكل الأدوار والجنينة", "أكسس بوينت سقف وحائط وخارجي", "سويتشات PoE للكاميرات", "تنظيم راك وكابلات مترقمة", "إدارة الشبكة من الكلاود", "ضمان 24 شهر"]),
 dict(slug="sound-system", name="الساوند سيستم والسنترالات", h1="ساوند سيستم وسنترالات", cats=["pbx","sound"], ic="sound",
      brands="Master Team · Surpass · Excelltel · Peaktel",
      intro="ساوند سيستم للبيوت والمحلات والمساجد والقاعات: سماعات سقف وحائط وحدائق، أمبليفاير ومايكات ووحدات مؤتمرات، وسنترالات وتليفونات داخلية للفيلات والشركات والفنادق.",
      pts=["سماعات سقف وحائط وخارجية", "أمبليفاير حائط بشاشة وتحكم من الموبايل", "مايكات لاسلكية ووحدات مؤتمرات", "أنظمة 100 فولت للمساحات الكبيرة", "سنترالات وتليفونات داخلية", "ضمان 24 شهر"]),
 dict(slug="electronic-gates", name="البوابات الإلكترونية", h1="بوابات إلكترونية وموتورات بوابات", cats=["access"], ic="acc", types=["remote", "closer", "power"],
      brands="SIB · ZKTeco",
      intro="أتمتة البوابات والجراجات: موتورات وريموتات وريلايات وأكسيس كنترول للبوابات، عشان تفتح البوابة من الريموت أو الموبايل أو بالكارت.",
      pts=["ريموتات وريلايات 433MHz", "فتح البوابة من الموبايل", "ربط مع الإنتركم والأكسيس كنترول", "ردادات وفتاحات أبواب", "صيانة وبرمجة الريموتات", "ضمان 24 شهر"]),
]
WORKS = ["pole-ptz-site", "hik-domes-batch", "villa-corner-bullets", "ruijie-poe-box", "dome-villa-ceiling", "rack-nvr"]

CSS = """.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.stats div{background:var(--surface);border:1px solid rgba(212,166,63,.3);border-radius:12px;padding:10px 6px;text-align:center;display:grid;gap:2px}
.stats b{font-family:var(--display);color:var(--gold2);font-size:1.05rem}.stats small{color:var(--muted);font-size:.78rem}
.btn.inst{flex-basis:100%;background:transparent;border:1px solid var(--gold);color:var(--gold2)}
.fxs{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.fx{display:grid;gap:6px;align-content:start;justify-items:center;text-align:center;padding:16px 12px;border-radius:14px;background:var(--surface);border:1px solid rgba(212,166,63,.22)}
.fx .ic svg{width:34px;height:34px;color:var(--gold)}.fx b{font-size:.98rem}.fx small{color:var(--muted);font-size:.82rem;line-height:1.7}
.fx.warr{border-color:var(--gold)}
.why{background:linear-gradient(160deg,#16130b,#0e0e0e);border:1px solid rgba(212,166,63,.3);border-radius:18px;padding:20px 16px}
.why h2{font-family:var(--display);color:var(--gold2);margin:0 0 14px}
.why-in{display:grid;grid-template-columns:1.4fr 1fr;gap:16px;align-items:center}
.why .fxs{grid-template-columns:repeat(2,1fr)}.why .fx{background:rgba(255,255,255,.03)}
.why-img{background:#fff;border-radius:14px;aspect-ratio:1;display:grid;place-items:center;overflow:hidden}.why-img img{width:100%;height:100%;object-fit:contain}
@media (max-width:760px){.why-in{grid-template-columns:1fr}.why-img{max-width:280px;justify-self:center}}
.cta{text-align:center;background:linear-gradient(135deg,rgba(212,166,63,.22),rgba(212,166,63,.05));border:1px solid var(--gold);border-radius:18px;padding:26px 16px}
.cta h2{font-family:var(--display);font-size:clamp(1.3rem,4.5vw,1.8rem);margin:0 0 8px}.cta p{color:var(--muted);margin:0 0 14px;line-height:1.8}.cta .ctas{justify-content:center}
.bnav{display:none}
@media (max-width:760px){
 .bnav{display:grid;grid-template-columns:repeat(4,1fr);position:fixed;left:0;right:0;bottom:0;z-index:20;background:rgba(17,17,17,.97);border-top:1px solid rgba(212,166,63,.35);padding:6px 4px calc(6px + env(safe-area-inset-bottom,0px));backdrop-filter:blur(8px)}
 .bnav a,.bnav button{display:grid;justify-items:center;gap:2px;color:var(--muted);font:inherit;font-size:.7rem;text-decoration:none;background:none;border:0;padding:4px 0;position:relative}
 .bnav svg{width:22px;height:22px}.bnav .wa{color:#25B864}.bnav .on{color:var(--gold2)}
 .bnav .cnt{position:absolute;top:0;right:calc(50% - 20px);background:var(--gold);color:#111;border-radius:999px;font-size:.65rem;min-width:16px;height:16px;line-height:16px;padding:0 4px;font-weight:700}
 .fab{display:none!important}
 body{padding-bottom:80px}
}

:root{--display:"Cairo","Readex Pro",sans-serif;--ink:#F7F7F7}
.sec{margin:26px 0}.sec-h h2{margin:0 0 12px}.ctas{display:flex;gap:10px;flex-wrap:wrap}.ic svg{display:block}.btn svg{width:18px;height:18px}
.bnav a{font-size:.72rem}.bnav a{font-size:1.1rem}.bnav span{font-size:.7rem}
:root{--bg:#111;--surface:#1B1B1B;--ink:#F7F7F7;--muted:#C2C2C2;--line:#2C2C2C;--gold:#D4A63F;--gold2:#F0CF7A;--wa:#25B864;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Readex Pro",system-ui,"Segoe UI",Tahoma,sans-serif;line-height:1.8;padding:0 16px 90px}
a{color:var(--gold2)}img{max-width:100%}.w{max-width:1100px;margin:auto}
header{position:sticky;top:0;z-index:5;background:rgba(17,17,17,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);margin:0 -16px;padding:10px 16px}
header .w{display:flex;align-items:center;gap:14px;justify-content:space-between}
.logo{display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--gold2);font-family:"Reem Kufi",sans-serif;font-weight:700;font-size:1.2rem}.logo img{width:38px;height:38px;border-radius:9px}
nav.top{display:flex;gap:4px;flex-wrap:wrap}nav.top a{color:var(--muted);text-decoration:none;padding:6px 10px;border-radius:9px;font-size:.9rem}nav.top a:hover{color:var(--gold2);background:var(--surface)}
@media (max-width:760px){nav.top a:not(.keep){display:none}}
.crumb{font-size:.85rem;color:var(--muted);margin:16px 0}.crumb a{color:var(--gold2);text-decoration:none}
h1{font-family:"Reem Kufi","Readex Pro",sans-serif;font-size:clamp(1.5rem,4vw,2.2rem);line-height:1.4;margin:.3em 0}
h2{font-family:"Reem Kufi","Readex Pro",sans-serif;font-size:1.3rem;margin:1.6em 0 .6em}
.lead{color:var(--muted);font-size:1.05rem;max-width:760px}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 18px;border-radius:12px;text-decoration:none;font-weight:700;border:1px solid transparent}
.btn.gold{background:linear-gradient(180deg,var(--gold2),var(--gold));color:#1a1405}.btn.wa{background:var(--wa);color:#fff}.btn.ghost{border-color:#3a3a3a;color:var(--ink)}
.panel{background:var(--surface);border:1px solid rgba(212,166,63,.25);border-radius:16px;padding:18px}
.ticks{list-style:none;padding:0;margin:0;display:grid;gap:8px}.ticks li::before{content:"✓ ";color:var(--gold);font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}
.card{display:grid;gap:6px;background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;color:var(--ink)}
.card .im{aspect-ratio:1;background:#fff;display:grid;place-items:center}.card .im img{width:100%;height:100%;object-fit:contain}
.card b{font-size:.88rem;padding:0 10px;line-height:1.5}.card small{padding:0 10px;color:var(--muted);font-family:"IBM Plex Mono",monospace;font-size:.75rem}
.phm{font-family:"IBM Plex Mono",monospace;color:#8a8a8a;font-size:.8rem;padding:8px;text-align:center}.card .pr{padding:0 10px 10px;color:var(--gold2);font-weight:700}.oos{color:#e07a6a!important}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips a{padding:6px 12px;border-radius:999px;border:1px solid rgba(212,166,63,.35);background:rgba(212,166,63,.08);text-decoration:none;color:var(--ink);font-size:.9rem}
.svcs{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}.svcs a{display:grid;gap:4px;padding:16px;border-radius:14px;background:var(--surface);border:1px solid rgba(212,166,63,.3);text-decoration:none;color:var(--ink)}.svcs small{color:var(--muted)}
.works{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}.works img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px;border:1px solid rgba(212,166,63,.3)}
.steps{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;counter-reset:s}
.steps li{counter-increment:s;background:var(--surface);border-radius:12px;padding:12px;border:1px solid var(--line)}.steps li::before{content:counter(s);color:var(--gold);font-weight:700;margin-left:6px}
details{border:1px solid rgba(212,166,63,.25);border-radius:12px;background:var(--surface);padding:0 14px;margin-bottom:8px}summary{cursor:pointer;padding:12px 0;font-weight:700}details p{color:var(--muted);margin:0 0 12px}
.pd{display:grid;grid-template-columns:1fr 1.1fr;gap:22px;align-items:start}@media (max-width:760px){.pd{grid-template-columns:1fr}}
.pd .im{background:#fff;border-radius:16px;aspect-ratio:1;display:grid;place-items:center;overflow:hidden}.pd .im img{width:100%;height:100%;object-fit:contain}
.price{font-family:"Reem Kufi",sans-serif;font-size:1.8rem;color:var(--gold2);font-weight:700}
table{width:100%;border-collapse:collapse;margin-top:10px}th,td{text-align:right;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--muted);font-weight:400;width:38%}
.mono{font-family:"IBM Plex Mono",monospace;direction:ltr;unicode-bidi:isolate}
ul.det{direction:ltr;text-align:left;color:var(--muted);font-size:.9rem;padding-left:18px}
footer{margin:50px -16px 0;padding:24px 16px;border-top:1px solid var(--line);color:var(--muted);font-size:.9rem}footer .cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}footer a{color:var(--muted);text-decoration:none}footer a:hover{color:var(--gold2)}footer b{color:var(--ink);display:block;margin-bottom:6px}
.fab{position:fixed;left:16px;bottom:18px;width:54px;height:54px;border-radius:50%;background:var(--wa);display:grid;place-items:center;z-index:15;box-shadow:0 10px 30px -8px rgba(37,184,100,.7)}.fab svg{width:28px;height:28px}
"""

def page(path, title, desc, body, ld=None, img="img/og-cover.jpg", crumb=None):
    depth = path.count("/")
    up = "../" * depth
    canon = f"{SITE}/{path}"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    cr = ""
    if crumb:
        cr = '<div class="crumb">' + " / ".join(f'<a href="{up}{u}">{e(t)}</a>' if u is not None else e(t) for t, u in crumb) + "</div>"
        lds += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, **({"item": f"{SITE}/{u}"} if u is not None else {})} for i, (t, u) in enumerate(crumb)]}, ensure_ascii=False) + "</script>"
    svc_links = "".join(f'<a href="{up}services/{s["slug"]}.html">{e(s["name"])}</a><br>' for s in SERVICES)
    area_links = " · ".join(f'<a href="{up}areas/{a}.html">{e(n)}</a>' for a, n in AREAS)
    out = f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="AR&amp;SMART"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/{img}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#111111"><link rel="icon" href="{up}img/logo-192.png"><link rel="apple-touch-icon" href="{up}img/logo-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500;700&family=Readex+Pro:wght@300;400;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="{up}assets/site.css"><script async src="https://www.googletagmanager.com/gtag/js?id=G-KJRENB4RR2"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-KJRENB4RR2');document.addEventListener('click',function(e){{var a=e.target.closest('a[href*="wa.me"]');if(a)gtag('event','whatsapp_click',{{page:location.pathname}});var t=e.target.closest('a[href^="tel:"]');if(t)gtag('event','phone_click',{{}});}},true);</script>{lds}</head><body>
<header><div class="w"><a class="logo" href="{up}"><img src="{up}img/logo-192.png" alt="AR&amp;SMART">AR&amp;SMART</a>
<nav class="top"><a href="{up}#home">الرئيسية</a><a href="{up}#services">الخدمات</a><a href="{up}#works">أعمالنا</a><a class="keep" href="{up}#categories">المتجر</a><a href="{up}#calc">حاسبة الهارد</a><a class="keep" href="{up}#contact">اتصل بنا</a></nav></div></header>
<main class="w">{cr}{body}</main>
<footer><div class="w cols"><div><b>AR&amp;SMART · م. رجب مفتاح</b>Eng. Ragab Moftah<br>توريد وتركيب وبرمجة أنظمة الأمان والتحكم الذكي<br>واتساب واتصال: <span class="mono">01144772044</span> · <span class="mono">01061503410</span><br>ضمان 24 شهر · معاينة مجانية</div>
<div><b>خدماتنا</b>{svc_links}</div><div><b>المناطق اللي بنخدمها</b>{area_links}</div></div></footer>
{FAB}<nav class="bnav"><a href="{up}#home">🏠<span>الرئيسية</span></a><a href="{up}#categories">🛒<span>المتجر</span></a><a href="tel:+201144772044">📞<span>اتصل</span></a><a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">💬<span>واتساب</span></a></nav></body></html>"""
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(out)
    return canon

def card(p, up):
    im = f'<img src="{up}{e(p["img"].split("?")[0])}" alt="{e(p["n"])}" loading="lazy">' if p.get("img") else f'<span class="phm">{e(p["m"])}</span>'
    pr = '<span style="color:#7fd1ff">قريباً</span>' if p.get("soon") else f'{fmt(p["p"])} ج.م' if p.get("p") else '<span class="oos">نفذ المخزون</span>'
    return f'<a class="card" href="{up}p/{p["id"]}.html"><span class="im">{im}</span><b>{e(p["n"])}</b><small>{e(p["b"])} {e(p["m"])}</small><span class="pr">{pr}</span></a>'

def cta(msg, up):
    return f'<div class="btns"><a class="btn wa" href="{e(wa(msg))}" target="_blank" rel="noopener">كلّمنا على الواتساب</a><a class="btn gold" href="{up}#contact">اطلب معاينة مجانية</a><a class="btn ghost" href="tel:+201144772044">اتصل 01144772044</a></div>'

STEPS = ["تواصل معانا واتساب أو من الموقع", "معاينة مجانية في المكان", "عرض سعر مكتوب بالموديلات والضمان", "توريد وتركيب وبرمجة", "تسليم وتدريب على الموبايل", "ضمان 24 شهر وصيانة"]
steps_html = '<ol class="steps">' + "".join(f"<li>{s}</li>" for s in STEPS) + "</ol>"
faq_html = lambda qs: "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qs)
faq_ld = lambda qs: {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}
BIZ = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "/#business", "name": "AR&SMART - Eng. Ragab Moftah", "url": SITE + "/", "telephone": ["+201144772044", "+201061503410"], "image": SITE + "/img/og-cover.jpg", "address": {"@type": "PostalAddress", "addressLocality": "El Shorouk City", "addressRegion": "Cairo", "addressCountry": "EG"}}

urls = []
by_cat = {}
for p in P:
    by_cat.setdefault(p.get("catId"), []).append(p)
def featured(s):
    l = [p for c in s["cats"] for p in by_cat.get(c, []) if p.get("p") and p.get("img")]
    if s.get("types"): l = [p for p in l if p.get("t") in s["types"]] or l
    l.sort(key=lambda p: -p["p"])
    out, seen = [], set()
    for p in l:
        if p["b"] not in seen: out.append(p); seen.add(p["b"])
    out += [p for p in l if p not in out]
    out = out[:8]
    return out

# ---- صفحات الخدمات
for s in SERVICES:
    up = "../"
    areas = "".join(f'<a href="{up}areas/{a}.html">{e(s["name"])} في {e(n)}</a>' for a, n in AREAS)
    prods = featured(s)
    qs = [FAQ[0], FAQ[1]] + ([FAQ[2], FAQ[3]] if s["slug"] == "cctv" else [FAQ[6]] if s["slug"] == "smart-home" else []) + [FAQ[7]]
    body = f"""<h1>{e(s["h1"])} في القاهرة الجديدة والشروق</h1><p class="lead">{e(s["intro"])}</p>
{cta(f"السلام عليكم، عايز أسأل عن {s['name']}", up)}
<div class="panel"><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in s["pts"])}</ul><p style="margin:12px 0 0;color:var(--muted)">الماركات: <span class="mono">{e(s["brands"])}</span></p></div>
{"<h2>منتجات من المتجر</h2><div class='grid'>" + "".join(card(p, up) for p in prods) + f"</div><p><a href='{up}#c-{s['cats'][0]}'>شوف كل المنتجات بالأسعار ←</a></p>" if prods else ""}
<h2>صور من شغلنا</h2><div class="works">{"".join(f'<img src="{up}img/w/t/{w}.jpg" alt="أعمال AR&amp;SMART" loading="lazy">' for w in WORKS[:4])}</div><p><a href="{up}#works">كل الأعمال ←</a></p>
<h2>إزاي بنشتغل</h2>{steps_html}
<h2>بنركّب {e(s["name"])} في</h2><div class="chips">{areas}</div>
<h2>أسئلة شائعة</h2>{faq_html(qs)}
{cta(f"السلام عليكم، عايز معاينة {s['name']}", up)}"""
    title = f"{s['h1']} | التجمع الخامس والشروق | AR&SMART"
    desc = f"{s['intro'][:120]}… معاينة مجانية وضمان 24 شهر. واتساب 01144772044"
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["h1"], "serviceType": s["name"], "provider": BIZ, "areaServed": [n for _, n in AREAS], "description": s["intro"]}
    urls.append(page(f"services/{s['slug']}.html", title, desc, body, [svc_ld, faq_ld(qs)], crumb=[("الرئيسية", ""), ("الخدمات", "#services"), (s["name"], None)]))

# ---- صفحات المناطق
for a, n in AREAS:
    up = "../"
    svcs = "".join(f'<a href="{up}services/{s["slug"]}.html"><b>{e(s["name"])} في {e(n)}</b><small>{e(s["intro"][:95])}…</small></a>' for s in SERVICES)
    qs = [(f"هل المعاينة في {n} مجانية؟", f"أيوه، المعاينة مجانية في {n}. بنيجي نشوف المكان ونقترح الحل المناسب لميزانيتك من غير أي التزام."), FAQ[1], FAQ[2], FAQ[7]]
    others = " · ".join(f'<a href="{x}.html">{e(m)}</a>' for x, m in AREAS if x != a)
    body = f"""<h1>كاميرات مراقبة وسمارت هوم وكوالين ذكية في {e(n)}</h1>
<p class="lead">AR&amp;SMART بتوصلك في {e(n)}: توريد وتركيب وبرمجة كاميرات المراقبة، الكوالين الذكية، السمارت هوم و KNX، الإنتركم الصوتي والمرئي، الأكسيس كنترول والحضور والانصراف، الشبكات والواي فاي، الساوند سيستم والسنترالات، والبوابات الإلكترونية — للفيلات والشقق والشركات والمحلات. معاينة مجانية وضمان 24 شهر.</p>
{cta(f"السلام عليكم، عايز معاينة في {n}", up)}
<h2>خدماتنا في {e(n)}</h2><div class="svcs">{svcs}</div>
<h2>صور من شغلنا</h2><div class="works">{"".join(f'<img src="{up}img/w/t/{w}.jpg" alt="تركيب كاميرات وأنظمة أمان" loading="lazy">' for w in WORKS)}</div>
<h2>إزاي بنشتغل</h2>{steps_html}
<h2>أسئلة شائعة</h2>{faq_html(qs)}
<h2>مناطق تانية بنخدمها</h2><p>{others}</p>
{cta(f"السلام عليكم، عايز أسأل عن خدماتكم في {n}", up)}"""
    title = f"كاميرات مراقبة وسمارت هوم في {n} | AR&SMART"
    desc = f"تركيب كاميرات مراقبة وكوالين ذكية وسمارت هوم وإنتركم وأكسيس كنترول وشبكات في {n}. معاينة مجانية وضمان 24 شهر. واتساب 01144772044"
    ld = dict(BIZ, areaServed=n)
    urls.append(page(f"areas/{a}.html", title, desc, body, [ld, faq_ld(qs)], crumb=[("الرئيسية", ""), ("المناطق", None), (n, None)]))

# ---- صفحات المنتجات
for p in P:
    up = "../"
    img = p["img"].split("?")[0] if p.get("img") else ""
    rows = [("الماركة", e(p["b"])), ("الموديل", f'<span class="mono">{e(p["m"])}</span>')] + ([("الكود", f'<span class="mono">{e(p["c"])}</span>')] if p.get("c") else []) + ([("النوع", e(p["type"]))] if p.get("type") else []) + ([("التردد", e(p["freq"]))] if p.get("freq") else []) + [(e(k), e(v)) for k, v in (p.get("h") or [])]
    feats = "".join(f"<li>{e(x)}</li>" for x in (p.get("s") or []))
    det = "".join(f"<li>{e(x)}</li>" for x in (p.get("d") or []))
    price = '<div class="price" style="font-size:1.3rem;color:#7fd1ff">قريباً</div>' if p.get("soon") else f'<div class="price">{fmt(p["p"])} <small>ج.م</small></div>' if p.get("p") else '<div class="price oos" style="font-size:1.3rem">نفذ المخزون حالياً</div>'
    msg = f"السلام عليكم، عايز أطلب:\n{p['n']}\n{p['b']} {p['m']}" + (f"\nكود: {p['c']}" if p.get("c") else "") + (f"\nالسعر: {fmt(p['p'])} ج.م" if p.get("p") else "")
    inst = f"السلام عليكم، عايز أطلب توريد وتركيب:\n{p['n']}\n{p['b']} {p['m']}" + (f"\nكود: {p['c']}" if p.get("c") else "")
    ask = f"السلام عليكم، المنتج ده هيتوفر إمتى؟\n{p['n']}\n{p['b']} {p['m']}" + (f"\nكود: {p['c']}" if p.get("c") else "")
    btns = (f'<a class="btn wa" href="{e(wa(msg))}" target="_blank" rel="noopener">اطلب على الواتساب</a><a class="btn gold" href="{up}#p-{p["id"]}">أضف للسلة في المتجر</a><a class="btn inst" href="{e(wa(inst))}" target="_blank" rel="noopener">اطلب توريد وتركيب</a>' if p.get("p")
            else f'<a class="btn wa" href="{e(wa(ask.replace("المنتج ده هيتوفر إمتى؟", "عايز أحجز المنتج ده أول ما ينزل:")))}" target="_blank" rel="noopener">احجز أول ما ينزل على الواتساب</a>' if p.get("soon")
            else f'<a class="btn wa" href="{e(wa(ask))}" target="_blank" rel="noopener">اسأل عن التوفر على الواتساب</a>')
    rel = [x for x in by_cat.get(p.get("catId"), []) if x is not p and (x.get("t") or "") == (p.get("t") or "")][:4]
    gal = "".join(f'<img src="{up}{e(u)}" alt="{e(p["n"])} - صورة {k+2}" loading="lazy" style="width:100%;border-radius:12px;margin-top:10px;background:#fff">' for k, u in enumerate(p.get("imgs") or []))
    body = f"""<div class="pd"><div><div class="im">{f'<img src="{up}{e(img)}" alt="{e(p["n"])} {e(p["m"])}">' if img else ""}</div>{gal}</div><div>
<h1>{e(p["n"])}</h1><p class="mono" style="color:var(--muted);margin:0">{e(p["b"])} · {e(p["m"])}</p>{price}{p.get("stats","")}
{f'<p>{e(p["use"])}</p>' if p.get("use") else ""}{f'<ul class="ticks">{feats}</ul>' if feats else ""}
<table>{"".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)}</table>
<div class="btns">{btns}</div><p style="color:var(--muted);font-size:.9rem">توريد وتركيب وبرمجة · ضمان 24 شهر · توصيل في القاهرة الجديدة والشروق</p></div></div>
{p.get("extra","").replace('src="img/','src="../img/')}
{f'<h2>المواصفات التفصيلية</h2><ul class="det">{det}</ul>' if det else ""}
{f'<h2>منتجات مشابهة</h2><div class="grid">' + "".join(card(x, up) for x in rel) + "</div>" if rel else ""}"""
    title = f"{p['n']} {p['b']} {p['m']}" + (f" | سعر {fmt(p['p'])} ج.م" if p.get("p") else "") + " | AR&SMART"
    desc = f"{p['n']} {p['b']} {p['m']}" + (f" بسعر {fmt(p['p'])} جنيه" if p.get("p") else "") + ". " + (p.get("use") or "") + " توريد وتركيب وضمان 24 شهر. واتساب 01144772044"
    ld = {"@context": "https://schema.org", "@type": "Product", "name": f"{p['n']} {p['m']}", "brand": {"@type": "Brand", "name": p["b"]}, "model": p["m"], **({"sku": str(p["c"])} if p.get("c") else {}), **({"image": f"{SITE}/{img}"} if img else {}), "description": desc,
          **({"offers": {"@type": "Offer", "price": p["p"], "priceCurrency": "EGP", "availability": "https://schema.org/InStock", "url": f"{SITE}/p/{p['id']}.html", "seller": {"@type": "Organization", "name": "AR&SMART"}}} if p.get("p") else {})}
    cat = p.get("catName") or "المتجر"
    urls.append(page(f"p/{p['id']}.html", title, desc[:300], body, [ld], img=img or "img/og-cover.jpg", crumb=[("الرئيسية", ""), (cat, f"#c-{p.get('catId')}"), (p["m"], None)]))

os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "site.css"), "w", encoding="utf-8").write(CSS)
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', f"  <url><loc>{SITE}/</loc><lastmod>{TODAY}</lastmod><priority>1.0</priority></url>"]
for u in urls:
    pr = "0.9" if "/services/" in u or "/areas/" in u else "0.6"
    sm.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
sm.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
print(len(urls), "pages")
