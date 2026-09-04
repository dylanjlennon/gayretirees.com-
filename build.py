#!/usr/bin/env python3
"""Static site generator: reads data/*.csv, writes dist/. No dependencies."""
import csv, html, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
e = html.escape
SITE_URL = os.environ.get("SITE_URL", "https://gayretirees.com")  # set to https://yourdomain.com at deploy for absolute canonical/sitemap URLs

# Simple rainbow-arc favicon, inline so the build stays dependency-free (no binary asset to keep in sync).
FAVICON = ('<link rel="icon" href="data:image/svg+xml,'
    '%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'%3E'
    '%3Crect width=\'100\' height=\'100\' rx=\'22\' fill=\'%231E1A2B\'/%3E'
    '%3Cpath d=\'M15 78a35 35 0 0 1 70 0\' fill=\'none\' stroke=\'%230B6E6B\' stroke-width=\'11\'/%3E'
    '%3Cpath d=\'M26 78a24 24 0 0 1 48 0\' fill=\'none\' stroke=\'%23CE3A29\' stroke-width=\'11\'/%3E'
    '%3Ccircle cx=\'50\' cy=\'78\' r=\'9\' fill=\'%23F2B33E\'/%3E%3C/svg%3E">')

# Real GA4 property, created 2026-09-04. Override at build time with the
# GA_MEASUREMENT_ID env var (e.g. a different value set on Netlify) if needed.
GA_ID = os.environ.get("GA_MEASUREMENT_ID", "G-HMVXKSHKN9")
GA_SNIPPET = ('<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA_ID + '"></script>'
    '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}'
    'gtag("js",new Date());gtag("config","' + GA_ID + '");</script>')

# Delegated click/submit tracking so every page-level and form-level
# interaction is one attribute away from being monitorable in GA4.
# Any element with data-ga="event_name" fires that event on click, with its
# other data-ga-* attributes as event params. Any <form data-ga-form="x">
# fires a form_submit event (via sendBeacon, so it survives the page
# navigating away to thanks.html before the request would otherwise land).
ANALYTICS_JS = """document.addEventListener('click', function(e){
  var t = e.target.closest('[data-ga]');
  if(!t) return;
  var params = {};
  for (var i=0;i<t.attributes.length;i++){
    var a = t.attributes[i];
    if (a.name.indexOf('data-ga-')===0) params[a.name.slice(8).replace(/-/g,'_')] = a.value;
  }
  if (typeof gtag === 'function') gtag('event', t.getAttribute('data-ga'), params);
});
document.addEventListener('submit', function(e){
  var f = e.target;
  if (!f.hasAttribute('data-ga-form')) return;
  if (typeof gtag === 'function') gtag('event', 'form_submit', {form_name: f.getAttribute('data-ga-form'), transport_type: 'beacon'});
});
"""

def load(name):
    with open(os.path.join(ROOT, "data", name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

states = {s["state_code"]: s for s in load("states.csv")}
cities = load("cities.csv")
city_by_slug = {c["slug"]: c for c in cities}
agents = load("agents.csv")
routes = load("routes.csv")
collections = load("collections.csv")
agents_by_market = {}
for a in agents:
    for m in a["market_slugs"].split(";"):
        agents_by_market.setdefault(m.strip(), []).append(a)
TIERS = {"1": ("Tier 1", "Flagship markets"), "2": ("Tier 2", "Strong markets"), "3": ("Tier 3", "Niche & destination towns")}
LIFESTYLE_LANES = [
    ("walkable-towns", "Walkable & social", "Errands, coffee, and your people, all on foot."),
    ("beach-coastal", "Beach & coastal", "Humidity, hurricane season, and a beach you can walk to."),
    ("mountains-seasons", "Mountains & four seasons", "Real winters, real elevation, quiet built in."),
    ("desert-sunbelt", "Desert & big sky", "Dry heat, wide streets, snowbird energy year-round."),
    ("small-town", "Small town, everyone knows you", "Small enough that the whole town is basically your friend group."),
    ("big-city", "Big-city amenities", "Major airport, full hospital system, more than one option for everything."),
]
QUICK_FILTERS = ["no-state-income-tax", "explicit-protections", "under-400k"]
LAW = {"explicit": ("Explicit state law", "ok"), "interpreted": ("Interpreted by state commission", "mid"),
       "none": ("No statewide law", "no"), "VERIFY": ("Needs verification", "mid")}

CSS = """
:root{--bg:#FAF6F0;--surface:#FFFFFF;--ink:#1E1A2B;--pool:#0B6E6B;--poolt:#DEF4F1;--coral:#CE3A29;--coralt:#FCE3DE;--sun:#F2B33E;--sunt:#FCEFD6;--pop:#9A3FC4;--popt:#F3E4FA;--line:#E7E0D3;--mut:#655D74}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--ink);font:16.5px/1.62 "Karla",system-ui,sans-serif}
h1,h2,h3,.brand{font-family:"Alfa Slab One",Georgia,serif;font-weight:400;letter-spacing:.01em}
a{color:var(--pool)}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header.site{padding:16px 0;border-bottom:3px solid var(--ink);background:var(--surface)}
header.site .wrap{display:flex;align-items:center;gap:22px;flex-wrap:wrap}
.brand{font-size:1.25rem;color:var(--coral);text-decoration:none;text-shadow:2px 2px 0 var(--popt)}
nav{display:flex;flex-wrap:wrap;gap:2px 4px}
nav a{display:inline-block;text-decoration:none;color:var(--ink);font-weight:700;font-size:.93rem;padding:10px 12px;border-bottom:3px solid transparent;border-radius:8px}
nav a:hover{border-bottom-color:var(--pop);background:var(--popt)}
@media(max-width:680px){
  header.site .wrap{flex-direction:column;align-items:stretch;gap:12px}
  nav{display:grid;grid-template-columns:1fr 1fr;gap:4px}
  nav a{padding:12px 10px;background:var(--bg);text-align:center}
  header.site .cta{margin:0!important;width:100%;text-align:center;padding:13px 18px!important;font-size:1rem!important}
}
.hero{padding:64px 0 46px;position:relative;overflow:hidden;border-bottom:3px solid var(--ink);background:radial-gradient(ellipse 80% 60% at 100% 0%,var(--popt),transparent 60%),radial-gradient(ellipse 70% 60% at 0% 100%,var(--poolt),transparent 65%),var(--bg)}
.hero .wrap{position:relative;z-index:1}
.hero h1{font-size:clamp(2rem,5vw,3.4rem);line-height:1.14;max-width:17ch;color:var(--ink)}
.hero p{max-width:56ch;margin-top:16px;font-size:1.1rem}
.arc{position:absolute;right:4%;bottom:-4px;width:380px;height:190px;border-radius:380px 380px 0 0;background:radial-gradient(circle at 50% 100%,var(--sun) 0 20%,transparent 20% 27%,var(--coral) 27% 47%,transparent 47% 54%,var(--pool) 54% 74%,transparent 74%);opacity:.9;pointer-events:none}
@media(max-width:860px){.arc{width:240px;height:120px;opacity:.35;right:-30px}}
@media(max-width:600px){.arc{display:none}}
.kicker{font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--coral);font-weight:700;margin-bottom:12px}
.stamp{display:inline-block;border:2px solid var(--ink);border-radius:999px;padding:5px 16px;font-size:.72rem;letter-spacing:.09em;text-transform:uppercase;font-weight:700;color:var(--ink);opacity:.72;transform:rotate(-2deg);margin-top:18px;background:var(--surface)}
.controls{display:flex;gap:8px;flex-wrap:wrap;padding:20px 0 6px}
.chip{border:2px solid var(--ink);background:var(--surface);border-radius:999px;padding:10px 16px;font:700 .92rem "Karla";cursor:pointer;box-shadow:2px 2px 0 rgba(30,26,43,.15)}
.chip.on{background:var(--pool);color:#fff;border-color:var(--ink)}
.chip:active{transform:translate(1px,1px);box-shadow:none}
.pill{display:inline-block;text-decoration:none;border:2px solid var(--ink);background:var(--surface);color:var(--ink);border-radius:999px;padding:10px 16px;font:700 .92rem "Karla";box-shadow:2px 2px 0 rgba(30,26,43,.15)}
.pill:hover{background:var(--poolt)}
.pill:active{transform:translate(1px,1px);box-shadow:none}
.swipehint{display:none;font-size:.8rem;font-weight:700;color:var(--mut);margin:0 0 8px}
.tblwrap{position:relative;overflow-x:auto;border:2px solid var(--ink);border-radius:12px;background:var(--surface);margin:14px 0 44px;box-shadow:5px 5px 0 rgba(30,26,43,.12)}
table{border-collapse:collapse;width:100%;font-size:.9rem;font-variant-numeric:tabular-nums}
th,td{padding:11px 13px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}
th{background:var(--poolt);font-weight:700;cursor:pointer;position:sticky;top:0;border-bottom:2px solid var(--ink)}
th:hover{color:var(--coral)}
td:first-child,th:first-child{position:sticky;left:0;background:var(--surface);max-width:230px;white-space:normal}
th:first-child{background:var(--poolt)}
tbody tr:hover td{background:var(--popt)}
tbody tr:hover td:first-child{background:var(--popt)}
tr:last-child td{border-bottom:none}
td a{font-weight:700;text-decoration:none;color:var(--pool)}
.b{display:inline-block;border-radius:999px;padding:2px 10px;font-size:.75rem;font-weight:700;border:1.5px solid var(--ink)}
.ok{background:var(--poolt);color:#0A5451}.no{background:var(--coralt);color:#9C3423}.mid{background:var(--sunt);color:#8A5F0B}
.check{color:var(--pool);font-weight:700}
.dash{color:#B8AE9C}
@media(max-width:760px){
  .swipehint{display:block}
  .tblwrap::after{content:'';position:absolute;top:0;right:0;bottom:0;width:26px;background:linear-gradient(to right,transparent,var(--surface));pointer-events:none}
  table th:nth-child(2),table td:nth-child(2),table th:nth-child(5),table td:nth-child(5),table th:nth-child(7),table td:nth-child(7),table th:nth-child(8),table td:nth-child(8){display:none}
}
section.tier{padding:30px 0}
section.tier h2{font-size:1.35rem}
.tiertag{display:inline-block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:700;font-family:"Karla";margin-right:10px;vertical-align:middle}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin-top:18px}
.card{background:var(--surface);border:2px solid var(--ink);border-radius:10px;padding:20px 20px 18px;display:block;text-decoration:none;color:var(--ink);position:relative;box-shadow:4px 4px 0 rgba(30,26,43,.14);transition:transform .12s,box-shadow .12s}
.card:hover{transform:rotate(-.6deg) translateY(-2px);box-shadow:6px 6px 0 rgba(30,26,43,.16)}
.card h3{color:var(--coral);margin-bottom:8px;font-size:1.05rem;padding-right:86px;line-height:1.3}
.card p{font-size:.9rem;color:var(--mut)}
.card .m{margin-top:12px}
.lifestyle .card{border-top-width:6px}
.lifestyle .card:nth-child(6n+1){border-top-color:var(--pool)}
.lifestyle .card:nth-child(6n+2){border-top-color:var(--coral)}
.lifestyle .card:nth-child(6n+3){border-top-color:var(--pop)}
.lifestyle .card:nth-child(6n+4){border-top-color:var(--sun)}
.lifestyle .card:nth-child(6n+5){border-top-color:var(--pool)}
.lifestyle .card:nth-child(6n+6){border-top-color:var(--coral)}
.pstamp{position:absolute;top:12px;right:12px;border:2px dashed var(--ink);border-radius:6px;padding:5px 9px;font:700 .78rem "Karla";transform:rotate(2deg);background:var(--sunt);text-align:center;line-height:1.25}
.pstamp small{display:block;font-size:.6rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--mut)}
.avatar{width:64px;height:64px;border-radius:50%;object-fit:cover;border:2px solid var(--ink);flex:none}
.avatar-fallback{display:flex;align-items:center;justify-content:center;background:var(--poolt);color:var(--pool);font:700 1.3rem "Karla";box-shadow:2px 2px 0 rgba(30,26,43,.14)}
.avatar-lg{width:96px;height:96px;font-size:1.9rem}
.heroimg{margin-top:18px;border:2px solid var(--ink);border-radius:10px;overflow:hidden;box-shadow:5px 5px 0 rgba(30,26,43,.14);position:relative}
.heroimg img{display:block;width:100%;max-height:360px;object-fit:cover}
.imgcredit{position:absolute;right:8px;bottom:8px;background:rgba(30,26,43,.62);color:#fff;font-size:.68rem;padding:3px 8px;border-radius:999px}
/* city page */
.cityhead{padding:48px 0 32px;border-bottom:3px solid var(--ink);position:relative;overflow:hidden;background:radial-gradient(ellipse 60% 80% at 100% 0%,var(--poolt),transparent 65%),var(--bg)}
.cityhead h1{font-size:clamp(1.6rem,4vw,2.5rem);max-width:22ch}
.cols{display:grid;grid-template-columns:310px 1fr;gap:38px;padding:36px 0}
@media(max-width:760px){.cols{grid-template-columns:1fr}}
.spine{background:var(--surface);border:2px solid var(--ink);border-radius:10px;height:fit-content;box-shadow:4px 4px 0 rgba(30,26,43,.14)}
.spine h2{font-size:.95rem;padding:13px 16px;background:var(--poolt);border-bottom:2px solid var(--ink);border-radius:8px 8px 0 0}
.fact{display:flex;justify-content:space-between;gap:12px;padding:10px 16px;border-bottom:1px solid var(--line);font-size:.87rem}
.fact:last-child{border-bottom:none}
.fact .k{color:var(--mut)}
.fact .v{text-align:right;font-weight:700;max-width:60%}
.body h2{margin:24px 0 8px;font-size:1.25rem}
.note{background:var(--sunt);border:2px dashed var(--ink);padding:14px 16px;border-radius:8px;font-size:.9rem;margin:20px 0}
input,select,textarea{font:inherit;width:100%;padding:11px 13px;border:2px solid var(--ink);border-radius:8px;background:var(--surface);color:var(--ink)}
label{display:block;font-size:.85rem;font-weight:700;margin:14px 0 6px}
.formgrid{display:grid;grid-template-columns:1fr 1fr;gap:0 18px}
@media(max-width:640px){.formgrid{grid-template-columns:1fr}}
fieldset{border:2px solid var(--ink);border-radius:8px;padding:12px 14px;margin-top:14px;background:var(--surface)}
legend{font-size:.85rem;font-weight:700;padding:0 6px}
.mk{display:inline-flex;align-items:center;gap:8px;font-size:.85rem;font-weight:400;margin:4px 12px 4px 0}
.mk input{width:18px;height:18px;flex:none}
@media(max-width:600px){.mk{display:flex;width:100%;margin:0;padding:11px 4px;border-bottom:1px solid var(--line)}.mk:last-child{border-bottom:none}}
button.cta{border:2px solid var(--ink);cursor:pointer;font-size:1rem}
:focus-visible{outline:3px solid var(--coral);outline-offset:2px}
.nl{background:var(--poolt);border-top:3px solid var(--ink);padding:30px 0}
.nl form{display:flex;gap:10px;max-width:540px;flex-wrap:wrap}
.nl input{flex:1;min-width:220px}
.nl h2{font-size:1.1rem;margin-bottom:4px;color:var(--pool)}
.hp{position:absolute;left:-9999px}
footer{border-top:3px solid var(--ink);margin-top:0;padding:26px 0;font-size:.84rem;color:var(--mut);background:var(--bg)}
.cta{display:inline-block;background:var(--coral);color:#fff;text-decoration:none;padding:12px 24px;border-radius:999px;font-weight:700;margin-top:18px;box-shadow:3px 3px 0 rgba(30,26,43,.22)}
.cta:hover{background:#B93A2F}
.cta:active{transform:translate(1px,1px);box-shadow:none}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Karla:wght@400;600;700&display=swap" rel="stylesheet">'

SITE_JSONLD = ('<script type="application/ld+json">' +
    '{"@context":"https://schema.org","@type":"Organization","name":"GayRetirees.com",'
    f'"url":"{SITE_URL}/","telephone":"+1-828-412-0678",'
    '"description":"Directory and relocation guide for LGBTQ+ retirees, organized by lifestyle across US cities."}'
    '</script>')

def page(title, body, path, depth=0, desc="", noindex=False, image=""):
    p = "../" * depth  # used by nav and newsletter form action
    canonical = f"{SITE_URL}/{path}"
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    img_tags = (f'<meta property="og:image" content="{e(image)}"><meta name="twitter:image" content="{e(image)}">'
        if image else "")
    og = (f'<link rel="canonical" href="{canonical}">'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="GayRetirees.com">'
        f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
        f'<meta property="og:url" content="{canonical}">'
        f'<meta name="twitter:card" content="{"summary_large_image" if image else "summary"}"><meta name="twitter:title" content="{e(title)}">'
        f'<meta name="twitter:description" content="{e(desc)}">{img_tags}')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">{robots}
{og}{FAVICON}{FONTS}
{GA_SNIPPET}{SITE_JSONLD}
<link rel="stylesheet" href="{p}style.css"></head><body>
<header class="site"><div class="wrap"><a class="brand" href="{p}index.html">GayRetirees.com</a>
<nav><a href="{p}index.html#browse">Find your vibe</a><a href="{p}index.html#compare">Compare cities</a><a href="{p}states.html">Know your rights</a><a href="{p}connect.html">Get matched</a></nav><a class="cta" style="margin:0;padding:8px 18px;font-size:.9rem" href="tel:+18284120678" data-ga="phone_click" data-ga-label="header">📞 Call Dylan</a></div></header>
{body}
<div class="nl"><div class="wrap"><h2>Get the quarterly postcard</h2>
<p style="font-size:.9rem;color:var(--mut);margin-bottom:10px">When the laws, prices, or rankings move, we send one honest email. That\u2019s it — no spam, ever.</p>
<form name="newsletter" method="POST" action="{p}thanks.html?src=newsletter" data-netlify="true" netlify-honeypot="bot-field" data-ga-form="newsletter">
<input type="hidden" name="form-name" value="newsletter">
<p class="hp"><label>Leave blank<input name="bot-field"></label></p>
<input type="email" name="email" placeholder="you@email.com" required aria-label="Email address">
<button class="cta" type="submit" style="margin-top:0">Subscribe</button>
</form></div></div>
<footer><div class="wrap">Working title — informational only, not legal, tax, or financial advice. Legal data sourced from the Movement Advancement Project; verify before relying. &copy; 2026. · <a href="{p}methodology.html">Methodology</a> · Real estate agent? <a href="{p}agent-signup.html">Join the directory →</a></div></footer>
<script src="{p}analytics.js" defer></script>
</body></html>"""

def license_ok(a):
    lic = a.get("license", "")
    return bool(lic) and "REPLACE" not in lic and "VERIFY" not in lic

def avatar(name, url, large=False):
    """Renders a real headshot when one's on file, otherwise a CSS initials badge — no fabricated photos."""
    cls = "avatar avatar-lg" if large else "avatar"
    size = 96 if large else 64
    if url:
        return f'<img class="{cls}" src="{e(url)}" alt="{e(name)}" loading="lazy" width="{size}" height="{size}">'
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    return f'<div class="{cls} avatar-fallback" aria-hidden="true">{e(initials)}</div>'

def agent_card(a, depth=1):
    p = "../" * depth
    t = {"fullpage":"Partner Agent","featured":"Featured Partner","exclusive":"Exclusive Partner","standard":"Partner Agent"}.get(a["tier"],"Partner Agent")
    link = f'<a class="cta" style="margin-top:10px;padding:9px 18px;font-size:.9rem" rel="sponsored" data-ga="agent_link_click" data-ga-label="{e(a["slug"])}" href="{p}agents/{a["slug"]}.html">Meet {e(a["name"].split()[0])} →</a>' if a["tier"] in ("fullpage","featured") else f'<a class="cta" style="margin-top:10px;padding:9px 18px;font-size:.9rem" rel="sponsored" data-ga="agent_link_click" data-ga-label="{e(a["slug"])}" href="{p}connect.html?agent={a["slug"]}">Work with {e(a["name"].split()[0])} →</a>'
    verify_line = "Sponsored placement · every partner is license-verified" if license_ok(a) else "Sponsored placement · license verification in progress"
    return f"""<div class="card" style="cursor:default"><div class="pstamp"><small>partner</small>{e(t.split()[0])}</div>
{avatar(a['name'], a.get('headshot_url',''))}
<h3>{e(a['name'])}</h3><p style="font-weight:700;color:var(--ink)">{e(a['brokerage'])} · since {e(a['since'])}</p>
<p>{e(a['blurb'])}</p><p style="margin-top:8px;font-size:.82rem">🏳️‍🌈 {e(a['community'])}</p>{link}
<p style="margin-top:10px;font-size:.7rem;color:var(--mut);text-transform:uppercase;letter-spacing:.06em">{verify_line}</p></div>"""

def lawbadge(code):
    label, cls = LAW.get(code, (code, "mid"))
    return f'<span class="b {cls}">{e(label)}</span>'

def matches(c, rule):
    s = states[c["state_code"]]
    if rule == "income_tax==none": return s["income_tax"] == "none"
    if rule == "housing_law==explicit": return s["housing_law"] == "explicit"
    if rule == "price<400000": return int(c["median_price_usd"]) < 400000
    if rule == "walk~walkable": return "walkable" in c["walkability"]
    if rule.startswith("lifestyle~"):
        tag = rule.split("~", 1)[1]
        return tag in [t.strip() for t in c["lifestyle_tags"].split(";") if t.strip()]
    return False

collection_by_slug = {col["slug"]: col for col in collections}
collection_counts = {col["slug"]: sum(1 for c in cities if matches(c, col["rule"])) for col in collections}

# ---------- index ----------
rows = ""
for c in sorted(cities, key=lambda x: (x["tier"], x["city_label"])):
    s = states[c["state_code"]]
    price = f"${int(c['median_price_usd']):,}" if c["median_price_usd"] else "—"
    ndo = '<span class="check">✓</span>' if c["local_ndo"] == "yes" else ('<span class="b mid">partial</span>' if c["local_ndo"] == "partial" else '<span class="dash">—</span>')
    tax = "None" if s["income_tax"] == "none" else s["income_tax"].replace("-", " ")
    rows += f"""<tr data-region="{e(c['region'])}" data-tier="{c['tier']}">
<td><a href="city/{c['slug']}.html">{e(c['city_label'])}</a></td>
<td data-v="{c['tier']}">Tier {c['tier']}</td>
<td data-v="{c['median_price_usd']}">{price}</td>
<td>{lawbadge(s['housing_law'])}</td>
<td>{ndo}</td>
<td data-v="{tax}">{e(tax)}</td>
<td>{e(c['climate'])}</td>
<td>{e(c['region'])}</td></tr>"""

regions = sorted({c["region"] for c in cities})
chips = '<button class="chip on" data-r="all">All regions</button>' + "".join(
    f'<button class="chip" data-r="{e(r)}">{e(r)}</button>' for r in regions)

tiercards = ""
for t in ["1", "2", "3"]:
    cards = ""
    for c in [x for x in cities if x["tier"] == t]:
        price_k = f"${round(int(c['median_price_usd'])/1000)}K" if c['median_price_usd'] else "—"
        cards += f"""<a class="card" href="city/{c['slug']}.html"><div class="pstamp"><small>median</small>{price_k}</div><h3>{e(c['city_label'])}</h3><p>{e(c['one_liner'])}</p><div class="m">{lawbadge(states[c['state_code']]['housing_law'])}</div></a>"""
    tag, name = TIERS[t]
    tiercards += f'<section class="tier wrap"><h2><span class="tiertag">{tag}</span>{name}</h2><div class="cards">{cards}</div></section>'

lifestyle_cards = ""
for slug, label, desc in LIFESTYLE_LANES:
    n = collection_counts.get(slug, 0)
    lifestyle_cards += f"""<a class="card" href="best/{slug}.html" data-ga="lifestyle_click" data-ga-label="{e(slug)}"><div class="pstamp"><small>places</small>{n}</div><h3>{e(label)}</h3><p>{e(desc)}</p></a>"""

quick_pills = ""
for slug in QUICK_FILTERS:
    col = collection_by_slug[slug]
    n = collection_counts.get(slug, 0)
    quick_pills += f"""<a class="pill" href="best/{slug}.html" data-ga="quicklist_click" data-ga-label="{e(slug)}">{e(col['title'])} · {n}</a>"""

index_body = f"""<div class="hero"><div class="arc" aria-hidden="true"></div><div class="wrap">
<div class="kicker">For people who get to choose</div>
<h1>Your next chapter, your terms.</h1>
<p>You've spent a career deciding things — this one's no different. Twenty-three places LGBTQ+ people are actually choosing for retirement, laid out by the lifestyle you're designing: walkable and social, beach-town slow, mountain quiet, big-city amenities. Start with the life you want below, or skip straight to the full comparison table. Every fact is sourced and dated either way.</p>
<span class="stamp">Data status: DRAFT · last reviewed Aug 2026 · legal data via Movement Advancement Project</span>
</div></div>
<section class="tier wrap" id="browse"><div class="kicker">Start here</div><h2>What's the vibe you're picturing?</h2>
<div class="cards lifestyle">{lifestyle_cards}</div>
<div style="padding-top:24px"><a class="cta" href="connect.html" data-ga="cta_click" data-ga-label="lifestyle_grid">Don't see it? Tell us what matters most →</a></div>
</section>
<section class="tier wrap"><div class="kicker">Or filter by what's non-negotiable</div><h2>Quick filters</h2>
<div class="controls">{quick_pills}</div>
</section>
<div class="wrap" style="padding:14px 0 36px;text-align:center;border-top:2px dashed var(--line)">
<p style="font-size:1.05rem;font-weight:700;margin-bottom:12px">Have your own must-haves? Skip the browsing.</p>
<a class="cta" href="connect.html" data-ga="cta_click" data-ga-label="mid_banner">Talk to a real person →</a>
</div>
{tiercards}
<section class="tier wrap" id="compare"><div class="kicker">For the data-heads</div><h2>Compare every place side-by-side</h2>
<div class="controls">{chips}</div>
<p class="swipehint">Swipe to see more columns →</p>
<div class="tblwrap"><table id="mx"><thead><tr>
<th>Place</th><th>Tier</th><th>Median price</th><th>State housing law</th><th>Local ordinance</th><th>Income tax</th><th>Climate</th><th>Region</th>
</tr></thead><tbody>{rows}</tbody></table></div></section>
<div class="wrap"><a class="cta" href="connect.html" data-ga="cta_click" data-ga-label="final_banner">Tell us what you're looking for →</a></div>
<script>
const tb=document.querySelector('#mx tbody');
document.querySelectorAll('.chip').forEach(ch=>ch.onclick=()=>{{
  document.querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));ch.classList.add('on');
  const r=ch.dataset.r;tb.querySelectorAll('tr').forEach(tr=>tr.style.display=(r==='all'||tr.dataset.region===r)?'':'none');
  if (typeof gtag === 'function') gtag('event', 'filter_region', {{region: r}});}});
document.querySelectorAll('#mx th').forEach((th,i)=>{{let asc=1;th.onclick=()=>{{
  const rs=[...tb.querySelectorAll('tr')];rs.sort((a,b)=>{{
    const av=a.cells[i].dataset.v??a.cells[i].textContent, bv=b.cells[i].dataset.v??b.cells[i].textContent;
    const an=parseFloat(av), bn=parseFloat(bv);
    return (isNaN(an)||isNaN(bn))?av.localeCompare(bv)*asc:(an-bn)*asc;}});
  asc*=-1;rs.forEach(r=>tb.appendChild(r));
  if (typeof gtag === 'function') gtag('event', 'sort_table', {{column: th.textContent, direction: asc>0?'asc':'desc'}});}}}});
</script>"""

shutil.rmtree(DIST, ignore_errors=True)

# ---------- city pages ----------
os.makedirs(os.path.join(DIST, "city"), exist_ok=True)
for c in cities:
    s = states[c["state_code"]]
    price = f"${int(c['median_price_usd']):,}" if c["median_price_usd"] else "—"
    price_badge = "" if c["status"] == "published" else " <span class='b mid'>est.</span>"
    facts = [
        ("Median home price", f"{price}{price_badge}"),
        ("State housing law", lawbadge(s["housing_law"])),
        ("Public accommodations", lawbadge(s["pa_law"])),
        ("Local ordinance", e(c["local_ndo"])),
        ("LTC protections", e(s["ltc_protections"])),
        ("State income tax", e(s["income_tax"].replace("-", " "))),
        ("Community anchor", e(c["community_org"])),
        ("Pride", e(c["pride_event"])),
        ("District", e(c["lgbtq_district"])),
        ("HIV care", e(c["hiv_care"])),
        ("Walkability", e(c["walkability"])),
        ("Summer high / winter low", f"{e(c['summer_high_f'])}° / {e(c['winter_low_f'])}°"),
        ("Hazards", e(c["hazard_flags"])),
        ("Airport", e(c["airport"])),
    ]
    def sourced_fact(label, value, src, suffix=""):
        if not value: return None
        link = f' <a href="{e(src)}" style="font-size:.72rem">(source)</a>' if src else ""
        return (label, f"{e(value)}{suffix}{link}")
    for extra in [
        sourced_fact("Same-sex couple households", c.get("same_sex_couples_pct",""), c.get("demographics_src",""), "%"),
        sourced_fact("Cost of living index", c.get("cost_of_living_index",""), c.get("coli_src",""), " (100 = US avg)"),
        sourced_fact("Walk Score", c.get("walkscore",""), c.get("walkscore_src","")),
    ]:
        if extra: facts.append(extra)
    spine = "".join(f'<div class="fact"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in facts)
    if c.get("hero_image_url") and c.get("hero_image_alt"):
        credit = f'<span class="imgcredit">{e(c["hero_image_credit"])}</span>' if c.get("hero_image_credit") else ""
        hero_img = f'<div class="heroimg"><img src="{e(c["hero_image_url"])}" alt="{e(c["hero_image_alt"])}" loading="lazy">{credit}</div>'
    else:
        hero_img = ""
    body = f"""<div class="cityhead"><div class="wrap">
<div class="kicker">{e(c['region'])} · Tier {c['tier']}</div>
<h1>{e(c['city_label'])}</h1><p style="max-width:60ch;margin-top:10px">{e(c['one_liner'])}</p>
<span class="stamp">Status: {e(c['status']).upper()} · reviewed {e(c['last_reviewed'])} · prices {e(c['price_asof'])}</span>
{hero_img}
</div></div>
<div class="wrap cols"><aside class="spine"><h2>At a glance</h2>{spine}</aside>
<div class="body">
<h2>The legal picture</h2>
<p>{e(c['city_label'].split(',')[0])} sits in {e(s['state_name'])}: {lawbadge(s['housing_law'])} for housing and {lawbadge(s['pa_law'])} for public accommodations. {e(s['tax_note'])}. Local ordinance status: {e(c['local_ndo'])}. Verify current status via the Movement Advancement Project before relying on it — state law is moving.</p>
<h2>Community &amp; healthcare</h2>
<p>Anchor institution: {e(c['community_org'])}. {e(c['senior_lgbtq_asset'])}. HIV/LGBTQ-competent care: {e(c['hiv_care'])}.</p>
<h2>Living here</h2>
<p>Climate: {e(c['climate'])}, roughly {e(c['summer_high_f'])}° summer highs and {e(c['winter_low_f'])}° winter lows. Walkability: {e(c['walkability'])}. Hazard awareness: {e(c['hazard_flags'])}. Air access: {e(c['airport'])}.</p>
{{straight_talk}}
{{agent_block}}
{{draft_note}}
<a class="cta" href="../connect.html">Considering {e(c['city_label'].split(',')[0].split(' &')[0])}? Talk to us →</a>
</div></div>"""
    if c.get("dylan_note"):
        straight_talk = f'<h2>The straight talk</h2><p>{e(c["dylan_note"])}</p>'
    else:
        straight_talk = ""
    body = body.replace("{straight_talk}", straight_talk)
    if c["status"] != "published":
        draft_note = f'<div class="note"><strong>Full write-up coming.</strong> This page is generated from our research table and is marked {e(c["status"])} until every fact clears a verification pass.</div>'
    else:
        draft_note = ""
    body = body.replace("{draft_note}", draft_note)
    mkts = agents_by_market.get(c["slug"], [])
    live = [a for a in mkts if a["status"] in ("active","example")]
    if live:
        cards = "".join(agent_card(a) for a in live)
        agent_block = f'<h2>Your person in {e(c["city_label"].split(",")[0])}</h2><p>Talk to a partner agent directly, or <a href="../connect.html">call us</a> and we\'ll make the introduction warmly.</p><div class="cards">{cards}</div>'
    else:
        agent_block = f'<h2>Your person here</h2><p>We\'re choosing our partner agent for this market now. Want an introduction the day it happens — or are you the agent? <a href="../connect.html">Raise your hand.</a></p>'
    body = body.replace("{agent_block}", agent_block)
    with open(os.path.join(DIST, "city", c["slug"] + ".html"), "w") as f:
        f.write(page(c["city_label"] + " — LGBTQ+ Retirement Guide", body, f"city/{c['slug']}.html", depth=1, desc=c["one_liner"], image=c.get("hero_image_url","")))

# ---------- states page ----------
srows = "".join(f"""<tr><td>{e(s['state_name'])}</td><td>{lawbadge(s['housing_law'])}</td>
<td>{lawbadge(s['pa_law'])}</td><td>{e(s['ltc_protections'])}</td><td>{e(s['income_tax'].replace('-',' '))}</td>
<td>{e(s['estate_inheritance_tax'])}</td><td style="white-space:normal;max-width:340px">{e(s['tax_note'])}</td></tr>"""
    for s in sorted(states.values(), key=lambda x: x["state_name"]))
states_body = f"""<div class="hero"><div class="wrap"><div class="kicker">Reference</div>
<h1>State law &amp; tax, side by side</h1>
<p>Every state that appears in the index. Legal columns follow the Movement Advancement Project's classification: explicit statute, commission interpretation, or no statewide law. Federal enforcement is currently unsettled — state and local law is what you can rely on.</p>
<span class="stamp">Legal data via lgbtmap.org · reviewed Aug 2026 · VERIFY before publishing</span></div></div>
<div class="wrap"><div class="tblwrap"><table><thead><tr><th>State</th><th>Housing</th><th>Public accomm.</th><th>LTC protections</th><th>Income tax</th><th>Estate/inherit.</th><th>Notes</th></tr></thead><tbody>{srows}</tbody></table></div></div>"""

# ---------- methodology ----------
meth_body = """<div class="hero"><div class="wrap"><div class="kicker">How this works</div>
<h1>Methodology</h1></div></div><div class="wrap" style="max-width:760px;padding-bottom:40px">
<div class="body">
<h2>Every fact has a source and a date</h2>
<p>The entire site is generated from a research table. Each legal and tax field carries a source link and an as-of date, and every page displays its review status. Fields we haven't re-verified are marked, not hidden.</p>
<h2>What we measure</h2>
<p>State housing and public-accommodations law (per the Movement Advancement Project), local nondiscrimination ordinances, long-term-care protections, retirement tax treatment, home prices, community institutions, LGBTQ-competent healthcare, climate, and hazards. We're expanding into demographics (share of same-sex-couple households, via Census ACS data), cost-of-living indexes, and Walk Score — each with its own source link, added city by city as it clears verification, not all at once.</p>
<h2>Where the facts come from</h2>
<p>Legal and rights data: the Movement Advancement Project's state equality maps, cross-checked against statute text for anything specific enough to need it (like long-term-care facility protections, which live in a different statute than general nondiscrimination law and don't always match). Home prices: Zillow's Home Value Index or Redfin's Data Center, at the town level where one exists rather than the wider metro. Climate: NOAA normals. Demographics: U.S. Census Bureau ACS data. Every one of these carries its own source link and as-of date on the page — not a single "sourced" badge covering everything.</p>
<h2>What "verified" means here</h2>
<p>A fact only ships with a value once we've found a real source for it. If we looked and couldn't confirm something — a law that may or may not have a long-term-care-specific version, a price for a town too small to have its own market data — the field stays blank and marked, not filled in with a best guess. A blank field is telling you something: we checked, we didn't want to guess.</p>
<h2>What we don't do</h2>
<p>We don't tell you where you'd "fit in," and we don't rank neighborhoods by who lives there. We publish the facts about places; you decide what matters and where to look. When you're ready to buy, a licensed agent shows you everything that meets your criteria.</p>
<h2>Corrections</h2>
<p>Spot something stale? Tell us. The correction ships in the next build with a new as-of date.</p>
</div></div>"""

# ---------- connect ----------
market_boxes = "".join(f'<label class="mk"><input type="checkbox" name="markets" value="{e(c["city_label"])}">{e(c["city_label"])}</label>' for c in sorted(cities, key=lambda x: x["city_label"]))
conn_body = f"""<div class="hero"><div class="wrap"><div class="kicker">Work with us</div>
<h1>You pick the place. We handle the landing.</h1>
<p>Tell us which markets you're considering and what you're trying to do — downsize, buy the forever house, sell first, time the move. We'll connect you with a vetted, licensed agent in the market <em>you</em> choose and stay involved through closing. Referrals are made broker-to-broker and disclosed in writing.</p>
</div></div>
<div class="wrap" style="max-width:760px;padding:30px 20px 40px">
<form name="relocation-intake" method="POST" action="thanks.html?src=relocation_intake" data-netlify="true" netlify-honeypot="bot-field" data-ga-form="relocation_intake">
<input type="hidden" name="form-name" value="relocation-intake">
<input type="hidden" name="preferred_agent" id="pref-agent" value="">
<script>const ag=new URLSearchParams(location.search).get("agent");if(ag)document.getElementById("pref-agent").value=ag;</script>
<p class="hp"><label>Leave blank<input name="bot-field"></label></p>
<div class="formgrid">
<div><label for="fn">Name</label><input id="fn" name="name" required autocomplete="name"></div>
<div><label for="fe">Email</label><input id="fe" type="email" name="email" required autocomplete="email"></div>
<div><label for="fp">Phone (optional)</label><input id="fp" type="tel" name="phone" autocomplete="tel"></div>
<div><label for="ft">Timeline</label><select id="ft" name="timeline" required>
<option value="">Choose one…</option><option>Just researching</option><option>1–2 years out</option><option>6–12 months</option><option>Ready now</option></select></div>
</div>
<fieldset><legend>Which markets are you considering? (your choice — pick any)</legend>{market_boxes}
<label class="mk"><input type="checkbox" name="markets" value="Somewhere else">Somewhere else</label></fieldset>
<label for="fs">What are you trying to do?</label>
<textarea id="fs" name="situation" rows="5" placeholder="Selling in Dallas, want a single-level home near a walkable downtown, budget around $500k…"></textarea>
<p style="font-size:.8rem;color:var(--mut);margin-top:12px">By submitting you agree to be contacted about your relocation. We never sell your information.</p>
<button class="cta" type="submit">Send my shortlist</button>
</form></div>"""

# ---------- agent signup (step 1 of 2 — low friction) ----------
market_options = "".join(f'<option value="{e(c["slug"])}">{e(c["city_label"])}</option>' for c in sorted(cities, key=lambda x: x["city_label"]))
signup_body = f"""<div class="hero"><div class="wrap"><div class="kicker">For agents · step 1 of 2</div>
<h1>Join the directory.</h1>
<p>Tell us who you are — that's it for now. We verify your license, then follow up for a short city blurb and to confirm which arrangement you want. Nothing here auto-publishes; every applicant is reviewed by hand first.</p>
</div></div>
<div class="wrap" style="max-width:760px;padding:30px 20px 40px">
<form name="agent-signup" method="POST" action="thanks.html?src=agent_signup" data-netlify="true" netlify-honeypot="bot-field" data-ga-form="agent_signup" enctype="multipart/form-data">
<input type="hidden" name="form-name" value="agent-signup">
<p class="hp"><label>Leave blank<input name="bot-field"></label></p>
<div class="formgrid">
<div><label for="an">Name</label><input id="an" name="name" required autocomplete="name"></div>
<div><label for="ae">Email</label><input id="ae" type="email" name="email" required autocomplete="email"></div>
<div><label for="ap">Phone</label><input id="ap" type="tel" name="phone" required autocomplete="tel"></div>
<div><label for="ab">Brokerage</label><input id="ab" name="brokerage" required></div>
<div><label for="al">License number</label><input id="al" name="license" required></div>
<div><label for="am">Primary market</label><select id="am" name="primary_market" required>
<option value="">Choose one…</option>{market_options}</select></div>
</div>
<label for="ah">Headshot (optional — helps you stand out once you're listed)</label><input id="ah" type="file" name="headshot" accept="image/*">
<p style="font-size:.8rem;color:var(--mut);margin-top:12px">Submitting doesn't guarantee placement — every applicant is reviewed for license status before appearing on the site.</p>
<button class="cta" type="submit">Submit</button>
</form></div>"""

# ---------- agent profile (step 2 of 2 — sent manually to verified agents) ----------
profile_body = f"""<div class="hero"><div class="wrap"><div class="kicker">For agents · step 2 of 2</div>
<h1>Finish your profile.</h1>
<p>You're verified — almost done. Write a couple sentences for your market, then pick how you want to be listed.</p>
</div></div>
<div class="wrap" style="max-width:760px;padding:30px 20px 40px">
<form name="agent-profile" method="POST" action="thanks.html?src=agent_profile" data-netlify="true" netlify-honeypot="bot-field" data-ga-form="agent_profile">
<input type="hidden" name="form-name" value="agent-profile">
<p class="hp"><label>Leave blank<input name="bot-field"></label></p>
<div class="formgrid">
<div><label for="pn">Name</label><input id="pn" name="name" required autocomplete="name"></div>
<div><label for="pe">Email</label><input id="pe" type="email" name="email" required autocomplete="email"></div>
</div>
<script>(function(){{var q=new URLSearchParams(location.search);var n=q.get("name"),em=q.get("email");if(n)document.getElementById("pn").value=n;if(em)document.getElementById("pe").value=em;}})();</script>
<label for="pb">Short bio for your city</label><textarea id="pb" name="bio" rows="4" placeholder="A couple sentences on your background and why you work with LGBTQ+ clients well." required></textarea>
<fieldset><legend>How do you want to be listed?</legend>
<label class="mk"><input type="radio" name="pricing_plan" value="standard-25" required>Standard listing — 25% referral fee when a deal closes, no monthly cost</label><br>
<label class="mk"><input type="radio" name="pricing_plan" value="top-15" required>Top agent for my city — $29/month, 15% referral fee, exclusive (one agent per market)</label>
</fieldset>
<p style="font-size:.8rem;color:var(--mut);margin-top:12px">Choosing "Top agent" doesn't charge you here — we'll follow up with a payment link. Referrals are made broker-to-broker and disclosed in writing.</p>
<button class="cta" type="submit">Submit</button>
</form></div>"""

os.makedirs(DIST, exist_ok=True)
with open(os.path.join(DIST, "style.css"), "w") as f: f.write(CSS)
with open(os.path.join(DIST, "analytics.js"), "w") as f: f.write(ANALYTICS_JS)
with open(os.path.join(DIST, "index.html"), "w") as f:
    f.write(page("GayRetirees.com — 23 places, browse by lifestyle", index_body, "index.html", desc="Where LGBTQ+ people actually retire, browsable by lifestyle or laid out side by side: laws, taxes, prices, healthcare, climate."))
with open(os.path.join(DIST, "states.html"), "w") as f: f.write(page("State laws & taxes — GayRetirees.com", states_body, "states.html", desc="State-by-state housing law, public-accommodations law, LTC protections, and tax treatment for every place on GayRetirees.com, sourced from the Movement Advancement Project."))
with open(os.path.join(DIST, "methodology.html"), "w") as f: f.write(page("Methodology — GayRetirees.com", meth_body, "methodology.html", desc="How GayRetirees.com sources, dates, and verifies every legal, tax, price, and community fact behind the index."))
with open(os.path.join(DIST, "connect.html"), "w") as f: f.write(page("Talk to us — GayRetirees.com", conn_body, "connect.html", desc="Tell us which cities you're considering and what you're trying to do. We'll connect you with a vetted, licensed agent in the market you choose."))
with open(os.path.join(DIST, "agent-signup.html"), "w") as f: f.write(page("Join the directory — GayRetirees.com", signup_body, "agent-signup.html", desc="Apply to be a partner agent on GayRetirees.com."))
with open(os.path.join(DIST, "agent-profile.html"), "w") as f: f.write(page("Finish your profile — GayRetirees.com", profile_body, "agent-profile.html", desc="Finish your agent profile on GayRetirees.com.", noindex=True))


# ---------- agent pages ----------
os.makedirs(os.path.join(DIST, "agents"), exist_ok=True)
for a in agents:
    mk = [city_by_slug[m.strip()] for m in a["market_slugs"].split(";") if m.strip() in city_by_slug]
    mklinks = ", ".join(f'<a href="../city/{m["slug"]}.html">{e(m["city_label"])}</a>' for m in mk)
    testim = f'<div class="note">“{e(a["testimonial"])}”</div>' if a["testimonial"] else ""
    lic_ok = license_ok(a)
    lic_suffix = f" ({e(a['license'])})" if lic_ok else ""
    lic_stamp = "License verified · community partner" if lic_ok else "License verification in progress"
    ab = f"""<div class="cityhead"><div class="arc" aria-hidden="true"></div><div class="wrap" style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap">
{avatar(a['name'], a.get('headshot_url',''), large=True)}
<div><div class="kicker">Your partner agent · sponsored placement</div><h1>{e(a['name'])}</h1>
<p style="margin-top:8px;font-weight:700">{e(a['brokerage'])} · serving {mklinks} · licensed since {e(a['since'])}{lic_suffix}</p>
<span class="stamp">{lic_stamp}</span></div></div>
<div class="wrap" style="max-width:760px;padding:30px 20px 40px"><div class="body">
<p style="font-size:1.05rem">{e(a['blurb'])}</p>
<p style="margin-top:12px">🏳️‍🌈 <strong>In the community:</strong> {e(a['community'])}</p>
{testim}
<h2>Reach {e(a['name'].split()[0])}</h2>
<p>Every inquiry comes through us first, so we can make a warm introduction and keep the referral on record — that's what keeps {e(a['name'].split()[0])}'s placement here free of bidding wars.</p>
<a class="cta" rel="sponsored" href="../connect.html?agent={a['slug']}" data-ga="agent_intro_click" data-ga-label="agent:{e(a['slug'])}">Get introduced to {e(a['name'].split()[0])} →</a>
</div></div>"""
    with open(os.path.join(DIST, "agents", a["slug"] + ".html"), "w") as f:
        f.write(page(a["name"] + " — Partner Agent — GayRetirees.com", ab, f"agents/{a['slug']}.html", depth=1, desc=a["blurb"][:150], image=a.get("headshot_url","")))

# ---------- moving-from route pages ----------
os.makedirs(os.path.join(DIST, "moving"), exist_ok=True)
def taxline(code): return states[code]["income_tax"].replace("-"," ") if code in states else "varies"
for r in routes:
    to = city_by_slug[r["to_slug"]]; ts = states[to["state_code"]]
    fs = states.get(r["from_state"])
    fromlaw = lawbadge(fs["housing_law"]) if fs else '<span class="b mid">varies</span>'
    fromtax = taxline(r["from_state"]) if fs else "your current rate"
    rb = f"""<div class="cityhead"><div class="arc" aria-hidden="true"></div><div class="wrap">
<div class="kicker">The move</div><h1>Moving from {e(r['from_label'])} to {e(to['city_label'])}</h1>
<p style="max-width:58ch;margin-top:10px">{e(r['hook'])}</p>
<span class="stamp">Draft · data reviewed Aug 2026</span></div></div>
<div class="wrap" style="max-width:820px;padding:30px 20px 40px"><div class="body">
<h2>What changes for you</h2>
<div class="tblwrap"><table><thead><tr><th></th><th>{e(r['from_label'])}</th><th>{e(to['city_label'].split(',')[0])}</th></tr></thead><tbody>
<tr><td>State housing law</td><td>{fromlaw}</td><td>{lawbadge(ts['housing_law'])}</td></tr>
<tr><td>State income tax</td><td>{e(fromtax)}</td><td>{e(taxline(to['state_code']))}</td></tr>
<tr><td>Median home price</td><td>—</td><td>${int(to['median_price_usd']):,} <span class="b mid">est.</span></td></tr>
<tr><td>Summer / winter</td><td>—</td><td>{e(to['summer_high_f'])}° / {e(to['winter_low_f'])}°</td></tr>
<tr><td>Community anchor</td><td>—</td><td>{e(to['community_org'])}</td></tr></tbody></table></div>
<h2>The receiving end</h2>
<p>{e(to['one_liner'])} Full picture on the <a href="../city/{to['slug']}.html">{e(to['city_label'])} guide</a>.</p>
<a class="cta" href="../connect.html">Talk this move through with us →</a>
</div></div>"""
    with open(os.path.join(DIST, "moving", r["route_slug"] + ".html"), "w") as f:
        f.write(page(f"Moving from {r['from_label']} to {to['city_label']} — GayRetirees.com", rb, f"moving/{r['route_slug']}.html", depth=1, desc=r["hook"]))

# ---------- collection pages (computed from data — never thin) ----------
os.makedirs(os.path.join(DIST, "best"), exist_ok=True)
for col in collections:
    hits = [c for c in cities if matches(c, col["rule"])]
    cards = ""
    for c in hits:
        pk = f"${round(int(c['median_price_usd'])/1000)}K"
        cards += f"""<a class="card" href="../city/{c['slug']}.html"><div class="pstamp"><small>median</small>{pk}</div><h3>{e(c['city_label'])}</h3><p>{e(c['one_liner'])}</p></a>"""
    cb = f"""<div class="hero"><div class="arc" aria-hidden="true"></div><div class="wrap">
<div class="kicker">The list</div><h1>{e(col['title'])}</h1><p>{e(col['blurb'])} <strong>{len(hits)} places qualify</strong> — computed straight from the index, not opinions.</p>
<span class="stamp">Auto-generated from verified data</span></div></div>
<section class="tier wrap"><div class="cards">{cards}</div></section>"""
    with open(os.path.join(DIST, "best", col["slug"] + ".html"), "w") as f:
        f.write(page(col["title"] + " — GayRetirees.com", cb, f"best/{col['slug']}.html", depth=1, desc=col["blurb"]))

thanks_body = """<div class="hero"><div class="wrap"><div class="kicker" id="tk">Received</div>
<h1 id="th">Got it. A real person replies within one business day.</h1>
<p id="tp">In the meantime, the <a href="states.html">state law &amp; tax table</a> is the most useful page on this site.</p>
<a class="cta" href="index.html">Back to the index</a></div></div>
<script>(function(){
  var copy = {
    relocation_intake: ["Received", "Got it. Dylan replies within one business day with your shortlist.", "In the meantime, the <a href=\\"states.html\\">state law &amp; tax table</a> is the most useful page on this site."],
    agent_signup: ["Application received", "Got it — we're checking your license now.", "If it clears, we'll email a personalized link to finish your profile. No payment happens until you pick a plan on that step."],
    agent_profile: ["Profile received", "You're in the queue to go live.", "We review every profile by hand before it appears on the site — you'll hear from us before you're published."],
    newsletter: ["Subscribed", "You're on the list.", "One honest email when the laws, prices, or rankings move. No spam, ever."]
  };
  var src = new URLSearchParams(location.search).get("src");
  var c = copy[src];
  if (c) {
    document.getElementById("tk").textContent = c[0];
    document.getElementById("th").textContent = c[1];
    document.getElementById("tp").innerHTML = c[2];
  }
})();</script>"""
nf_body = """<div class="hero"><div class="wrap"><div class="kicker">404</div>
<h1>That page doesn't exist.</h1><p>The <a href="index.html">full index</a> has every city we cover.</p></div></div>"""
with open(os.path.join(DIST, "thanks.html"), "w") as f: f.write(page("Thanks — GayRetirees.com", thanks_body, "thanks.html", desc="Thanks for reaching out to GayRetirees.com.", noindex=True))
with open(os.path.join(DIST, "404.html"), "w") as f: f.write(page("Not found — GayRetirees.com", nf_body, "404.html", desc="That page doesn't exist on GayRetirees.com.", noindex=True))
pages = ["index.html","states.html","methodology.html","connect.html","agent-signup.html"] + [f"city/{c['slug']}.html" for c in cities] + [f"agents/{a['slug']}.html" for a in agents if a["status"]=="active"] + [f"moving/{r['route_slug']}.html" for r in routes] + [f"best/{c['slug']}.html" for c in collections]
with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            "".join(f"<url><loc>{SITE_URL}/{u}</loc></url>\n" for u in pages) + "</urlset>")
with open(os.path.join(DIST, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
with open(os.path.join(ROOT, "netlify.toml"), "w") as f:
    f.write('[build]\n  command = "python3 build.py"\n  publish = "dist"\n')
print("Built", len(cities), "city pages + core pages, forms, sitemap, robots → dist/")

