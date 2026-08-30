#!/usr/bin/env python3
"""End-to-end test suite. Run: python3 tests.py  — exits nonzero on any failure."""
import csv, os, re, subprocess, sys, time, urllib.request
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__)); DIST = os.path.join(ROOT, "dist")
FAIL = []
def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond: FAIL.append(name)

# ---------- 1. Data integrity ----------
states = {r["state_code"]: r for r in csv.DictReader(open("data/states.csv"))}
cities = list(csv.DictReader(open("data/cities.csv")))
check("data: 23 cities", len(cities) == 23)
check("data: unique slugs", len({c["slug"] for c in cities}) == len(cities))
check("data: every city state_code resolves", all(c["state_code"] in states for c in cities))
check("data: tiers valid", all(c["tier"] in {"1","2","3"} for c in cities))
check("data: local_ndo enum valid", all(c["local_ndo"] in {"yes","partial","no"} for c in cities))
check("data: housing_law enum valid", all(s["housing_law"] in {"explicit","interpreted","none","VERIFY"} for s in states.values()))
req = ["slug","city_label","one_liner","median_price_usd","price_asof","airport","last_reviewed","status"]
check("data: no empty required city fields", all(c[k].strip() for c in cities for k in req))
check("data: every legal row has src+asof", all(s["law_src"].startswith("http") and s["law_asof"] for s in states.values()))
check("data: every published city has sourced price", all(c["price_src"].startswith("http") and "VERIFY" not in c["price_asof"] for c in cities if c["status"]=="published"))
check("data: prices are integers", all(c["median_price_usd"].isdigit() for c in cities))

# ---------- 2. Build outputs ----------
agents = list(csv.DictReader(open("data/agents.csv")))
routes = list(csv.DictReader(open("data/routes.csv")))
cols = list(csv.DictReader(open("data/collections.csv")))
expected = ["index.html","states.html","methodology.html","connect.html","thanks.html","404.html","style.css","analytics.js","sitemap.xml","robots.txt"] + [f"city/{c['slug']}.html" for c in cities] + [f"agents/{a['slug']}.html" for a in agents] + [f"moving/{r['route_slug']}.html" for r in routes] + [f"best/{c['slug']}.html" for c in cols]
missing = [p for p in expected if not os.path.exists(os.path.join(DIST,p))]
check(f"build: all {len(expected)} expected files exist", not missing, str(missing))

# ---------- 3. HTML validity + link graph ----------
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.title=False; s.forms=[]; s.inputs=[]; s.labels=[]; s.ids=[]
    def handle_starttag(s, tag, attrs):
        a=dict(attrs)
        if tag=="a" and a.get("href"): s.links.append(a["href"])
        if tag=="link" and a.get("href"): s.links.append(a["href"])
        if tag=="title": s.title=True
        if tag=="form": s.forms.append(a)
        if tag in ("input","select","textarea"): s.inputs.append(a)
        if tag=="label" and a.get("for"): s.labels.append(a["for"])
        if a.get("id"): s.ids.append(a["id"])

bad_links, no_title = [], []
for pth in expected:
    if not pth.endswith(".html"): continue
    p = P(); p.feed(open(os.path.join(DIST, pth)).read())
    if not p.title: no_title.append(pth)
    base = os.path.dirname(os.path.join(DIST, pth))
    for href in p.links:
        if href.startswith(("http","mailto","tel:","#")): continue
        href = href.split("?")[0]
        if not href: continue
        target = os.path.normpath(os.path.join(base, href))
        if not os.path.exists(target): bad_links.append(f"{pth} → {href}")
check("html: every page has <title>", not no_title, str(no_title))
check("html: zero broken internal links", not bad_links, str(bad_links[:6]))

# ---------- 4. Forms (Netlify contract) ----------
cp = P(); cp.feed(open(os.path.join(DIST,"connect.html")).read())
intake = [f for f in cp.forms if any(i.get("name")=="form-name" and i.get("value")=="relocation-intake" for i in cp.inputs)]
check("form: intake form present with data-netlify", any("data-netlify" in f for f in cp.forms))
check("form: hidden form-name field (required by Netlify)", any(i.get("name")=="form-name" and i.get("value")=="relocation-intake" for i in cp.inputs))
check("form: honeypot configured", any(f.get("netlify-honeypot")=="bot-field" for f in cp.forms) and any(i.get("name")=="bot-field" for i in cp.inputs))
check("form: posts to existing thanks page", any(f.get("action")=="thanks.html" for f in cp.forms) and os.path.exists(os.path.join(DIST,"thanks.html")))
check("form: markets are client-selected checkboxes (steering guardrail)", sum(1 for i in cp.inputs if i.get("name")=="markets")==24)
check("form: required fields marked", any(i.get("name")=="name" and "required" in i for i in cp.inputs) and any(i.get("name")=="email" and "required" in i for i in cp.inputs))
labeled = all(i.get("id") in cp.labels for i in cp.inputs if i.get("id") and i.get("type")!="hidden")
check("form: a11y — every visible field has a label", labeled)
ip = P(); ip.feed(open(os.path.join(DIST,"index.html")).read())
check("form: newsletter capture on homepage", any(f.get("name")=="newsletter" for f in ip.forms))
city0 = P(); city0.feed(open(os.path.join(DIST,"city",cities[0]["slug"]+".html")).read())
check("form: newsletter capture on city pages", any(f.get("name")=="newsletter" for f in city0.forms))

# ---------- 4b. Analytics: page-level (GA4) + form-level tracking coverage ----------
html_pages = [p for p in expected if p.endswith(".html")]
page_src = {p: open(os.path.join(DIST, p)).read() for p in html_pages}
m = re.search(r'gtag\("config","(G-[A-Za-z0-9-]+)"\)', page_src[html_pages[0]])
check("ga: measurement id present in gtag config", bool(m))
ga_id = m.group(1) if m else None
ga_page_missing = [p for p in html_pages if not ga_id
    or f'googletagmanager.com/gtag/js?id={ga_id}' not in page_src[p]
    or f'gtag("config","{ga_id}")' not in page_src[p]]
check(f"ga: page-level GA4 snippet on all {len(html_pages)} pages (100% coverage)", not ga_page_missing, str(ga_page_missing[:6]))
script_missing = [p for p in html_pages if 'analytics.js" defer' not in page_src[p]]
check(f"ga: analytics.js loaded on all {len(html_pages)} pages", not script_missing, str(script_missing[:6]))

analytics_js = open(os.path.join(DIST, "analytics.js")).read()
check("ga: analytics.js shipped non-empty", len(analytics_js) > 100)
check("ga: click delegation wired for data-ga elements", "data-ga" in analytics_js and "addEventListener('click'" in analytics_js)
check("ga: form_submit tracked via beacon on unload-safe submit", "form_submit" in analytics_js and "transport_type" in analytics_js and "addEventListener('submit'" in analytics_js)

forms_missing_ga = []
for p in html_pages:
    pp = P(); pp.feed(page_src[p])
    for f in pp.forms:
        if "data-ga-form" not in f: forms_missing_ga.append(f"{p}:{f.get('name')}")
check("ga: 100% of forms carry data-ga-form (form-level tracking coverage)", not forms_missing_ga, str(forms_missing_ga[:6]))

phone_click_missing = [p for p in html_pages if 'data-ga="phone_click" data-ga-label="header"' not in page_src[p]]
check(f"ga: header phone CTA tracked (phone_click) on all {len(html_pages)} pages", not phone_click_missing, str(phone_click_missing[:6]))

agent_link_missing = [a["slug"] for a in agents if not (
    'data-ga="phone_click"' in page_src.get(f"agents/{a['slug']}.html", "") and
    'data-ga="email_click"' in page_src.get(f"agents/{a['slug']}.html", ""))]
check("ga: agent phone + email links tracked on every agent detail page", not agent_link_missing, str(agent_link_missing))

# ---------- 5. End-to-end over HTTP ----------
srv = subprocess.Popen([sys.executable,"-m","http.server","8901","--directory",DIST], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    codes = {}
    for pth in expected:
        with urllib.request.urlopen(f"http://127.0.0.1:8901/{pth}") as r: codes[pth]=r.status
    check(f"e2e: all {len(expected)} pages serve HTTP 200", all(v==200 for v in codes.values()))
    home = urllib.request.urlopen("http://127.0.0.1:8901/index.html").read().decode()
    check("e2e: matrix renders all 23 rows", home.count('data-region=')==23)
    check("e2e: sort/filter script shipped", "localeCompare" in home and "dataset.r" in home)
    css = urllib.request.urlopen("http://127.0.0.1:8901/style.css").read().decode()
    check("e2e: stylesheet non-empty and served", len(css) > 2000)
    sm = urllib.request.urlopen("http://127.0.0.1:8901/sitemap.xml").read().decode()
    check("e2e: sitemap lists all indexable pages", sm.count("<url>")==27+sum(1 for a in agents if a["status"]=="active")+len(routes)+len(cols))
finally:
    srv.terminate()

# ---------- 5b. Architecture: partner layer, routes, collections ----------
ash = open(os.path.join(DIST,"city","asheville.html")).read()
check("arch: agent card renders on covered city page", "Your person in Asheville" in ash and "Dylan Lennon" in ash)
check("arch: sponsored rel on all paid agent links", 'rel="sponsored"' in ash and 'rel="sponsored"' in open(os.path.join(DIST,"agents","dylan-lennon.html")).read())
check("arch: paid placement disclosed on card", "Sponsored placement" in ash)
check("arch: open markets show recruit block", "Raise your hand" in open(os.path.join(DIST,"city","tucson.html")).read())
rt = open(os.path.join(DIST,"moving","dallas-to-palm-springs.html")).read()
check("arch: route page compares from/to law + tax", "Moving from Dallas" in rt and "State housing law" in rt and "State income tax" in rt)
ntx = open(os.path.join(DIST,"best","no-state-income-tax.html")).read()
import re as _re
n_claim = int(_re.search(r"<strong>(\d+) places qualify", ntx).group(1))
n_true = sum(1 for c in cities if states[c["state_code"]]["income_tax"]=="none")
check("arch: collection counts computed truthfully from data", n_claim == n_true and ntx.count('class="card"') == n_true)
check("arch: phone CTA in header sitewide", 'href="tel:+18284120678"' in ash and 'href="tel:+18284120678"' in open(os.path.join(DIST,"index.html")).read())
cn = open(os.path.join(DIST,"connect.html")).read()
check("arch: agent preselect wired into intake", 'name="preferred_agent"' in cn and 'URLSearchParams' in cn)
# ---------- 5c. Analytics: interaction events (filter/sort/agent-link click) ----------
check("ga: region filter tracked as filter_region event", "gtag('event', 'filter_region'" in home)
check("ga: table sort tracked as sort_table event", "gtag('event', 'sort_table'" in home)
check("ga: agent card CTA tracked with agent_link_click", 'data-ga="agent_link_click"' in ash)
# ---------- 6. Honesty guarantees ----------
draft_ok = all(("Status: DRAFT" in open(os.path.join(DIST,"city",c["slug"]+".html")).read()) == (c["status"]=="draft") for c in cities)
check("integrity: draft stamp matches data status on every city page", draft_ok)
check("integrity: no placeholder emails shipped", "example.com?subject" not in open(os.path.join(DIST,"connect.html")).read())

print()
print(f"{'ALL TESTS PASSED' if not FAIL else str(len(FAIL))+' FAILURES: '+', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
