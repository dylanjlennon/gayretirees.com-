#!/usr/bin/env python3
"""End-to-end test suite. Run: python3 tests.py  — exits nonzero on any failure."""
import csv, html, os, re, subprocess, sys, time, urllib.request
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
check("data: local_ndo enum valid", all(c["local_ndo"] in {"yes","partial","no","VERIFY"} for c in cities))
check("data: housing_law enum valid", all(s["housing_law"] in {"explicit","interpreted","none","VERIFY"} for s in states.values()))
req = ["slug","city_label","one_liner","median_price_usd","price_asof","airport","last_reviewed","status","lifestyle_tags"]
check("data: no empty required city fields", all(c[k].strip() for c in cities for k in req))
LIFESTYLE_VOCAB = {"beach-coastal","mountains-seasons","desert-sunbelt","small-town","big-city"}
check("data: lifestyle_tags use known vocabulary only", all(
    set(t.strip() for t in c["lifestyle_tags"].split(";") if t.strip()) <= LIFESTYLE_VOCAB for c in cities))
check("data: every legal row has src+asof", all(s["law_src"].startswith("http") and s["law_asof"] for s in states.values()))
check("data: every published city has sourced price", all(c["price_src"].startswith("http") and "VERIFY" not in c["price_asof"] for c in cities if c["status"]=="published"))
check("data: prices are integers", all(c["median_price_usd"].isdigit() for c in cities))
check("data: price_metric valid and matches the cited source (Redfin=median_sale, Zillow=typical_value)", all(
    c["price_metric"] == ("median_sale" if "redfin.com" in c["price_src"] else "typical_value") and
    ("redfin.com" in c["price_src"] or "zillow" in c["price_src"]) for c in cities))
check("data: any city with a hero image has alt text (a11y)", all(
    bool(c.get("hero_image_alt","").strip()) for c in cities if c.get("hero_image_url","").strip()))

# ---------- 2. Build outputs ----------
agents = list(csv.DictReader(open("data/agents.csv")))
routes = list(csv.DictReader(open("data/routes.csv")))
cols = list(csv.DictReader(open("data/collections.csv")))
expected = ["index.html","states.html","methodology.html","connect.html","agent-signup.html","agent-profile.html","thanks.html","404.html","style.css","analytics.js","sitemap.xml","robots.txt"] + [f"city/{c['slug']}.html" for c in cities] + [f"agents/{a['slug']}.html" for a in agents] + [f"moving/{r['route_slug']}.html" for r in routes] + [f"best/{c['slug']}.html" for c in cols] + [f"compare/{r['slug_a']}-vs-{r['slug_b']}.html" for r in list(csv.DictReader(open("data/compare.csv")))]
missing = [p for p in expected if not os.path.exists(os.path.join(DIST,p))]
check(f"build: all {len(expected)} expected files exist", not missing, str(missing))
actual = [os.path.relpath(os.path.join(dp,f),DIST) for dp,_,fs in os.walk(DIST) for f in fs if f != ".DS_Store"]
orphans = sorted(set(actual) - set(expected))
check("build: no stale/orphan files left over in dist (removed CSV rows must vanish on rebuild)", not orphans, str(orphans))

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
        if href.startswith(("http","mailto","tel:","#","data:")): continue
        href = href.split("?")[0].split("#")[0]
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
check("form: posts to existing thanks page", any(f.get("action","").startswith("thanks.html") for f in cp.forms) and os.path.exists(os.path.join(DIST,"thanks.html")))
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

agent_intro_missing = [a["slug"] for a in agents if 'data-ga="agent_intro_click"' not in page_src.get(f"agents/{a['slug']}.html", "")]
check("ga: every agent detail page routes contact through the intake form (agent_intro_click), no direct-contact bypass", not agent_intro_missing, str(agent_intro_missing))
bypass_present = [a["slug"] for a in agents if
    f'href="tel:{a["phone"]}"' in page_src.get(f"agents/{a['slug']}.html", "") or
    (a.get("email") and f'href="mailto:{a["email"]}"' in page_src.get(f"agents/{a['slug']}.html", ""))]
check("integrity: no raw tel:/mailto: bypass to the agent's own number/email on agent detail pages (every lead must route through Dylan)", not bypass_present, str(bypass_present))

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
    check("e2e: sitemap lists all indexable pages", sm.count("<url>")==28+sum(1 for a in agents if a["status"]=="active")+len(routes)+len(cols)+len(list(csv.DictReader(open("data/compare.csv")))))
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
check("ga: all 6 lifestyle explore cards tracked (lifestyle_click)", home.count('data-ga="lifestyle_click"') == 6)
check("ga: all 3 quick-filter pills tracked (quicklist_click)", home.count('data-ga="quicklist_click"') == 3)
check("ga: homepage CTA banners tracked with distinct labels", all(
    f'data-ga-label="{lbl}"' in home for lbl in ("lifestyle_grid","mid_banner","final_banner")))
# ---------- 6. Honesty guarantees ----------
draft_ok = all(("Status: DRAFT" in open(os.path.join(DIST,"city",c["slug"]+".html")).read()) == (c["status"]=="draft") for c in cities)
check("integrity: draft stamp matches data status on every city page", draft_ok)
check("integrity: no placeholder emails shipped", "example.com?subject" not in open(os.path.join(DIST,"connect.html")).read())

# price measure labeling: never call a Zillow typical value a "median"
_LBL = {"median_sale": "Median sale price (Redfin)", "typical_value": "Typical home value (Zillow)"}
def _city_html(c): return open(os.path.join(DIST,"city",c["slug"]+".html")).read()
check("integrity: each city page labels its price with the correct measure and source",
      all(_LBL[c["price_metric"]] in _city_html(c) for c in cities))
check("integrity: no city page calls a Zillow typical value a 'Median home price'",
      all("Median home price" not in _city_html(c) for c in cities))
check("integrity: index explains the two price measures", "not the same measure" in open(os.path.join(DIST,"index.html")).read())

# ---------- 7. Living-guide data (PRD 0001) ----------
import datetime
WARNINGS = []
def warn(name, cond, detail=""):
    """Non-fatal check: prints WARN, never fails the suite (freshness is advisory)."""
    print(("PASS " if cond else "WARN ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond: WARNINGS.append(name)

def load_csv(name): return list(csv.DictReader(open(os.path.join("data", name), newline="", encoding="utf-8")))
def header(name): return next(csv.reader(open(os.path.join("data", name), newline="", encoding="utf-8")))
def parse_asof(v):
    """Accepts YYYY-MM or YYYY-MM-DD; returns a date or None."""
    m = re.fullmatch(r"(\d{4})-(\d{2})(?:-(\d{2}))?", (v or "").strip())
    if not m: return None
    try: return datetime.date(int(m[1]), int(m[2]), int(m[3] or 1))
    except ValueError: return None
def is_url(v): return (v or "").strip().startswith("http")

politics = load_csv("politics.csv"); places = load_csv("places.csv"); events = load_csv("events.csv")
news = load_csv("news.csv"); updates = load_csv("updates.csv"); compare = load_csv("compare.csv")

SCHEMAS = {
    "politics.csv": ["scope","slug_or_code","item","value","party","notes","source_url","asof"],
    "places.csv": ["city_slug","name","type","url","source","verified_asof","status"],
    "events.csv": ["city_slug","name","month","typical_weeks","url","source","verified_asof"],
    "news.csv": ["city_slug","date","outlet","headline","url","kind"],
    "updates.csv": ["date","scope","slug","headline","source_url"],
    "compare.csv": ["slug_a","slug_b","reason"],
}
check("living: new CSV headers match the PRD schema", all(header(n) == h for n, h in SCHEMAS.items()))

slugs = {c["slug"] for c in cities}
MONTHS = {"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"}
check("living: politics enums valid", all(r["scope"] in {"state","city"} and
      r["item"] in {"governor","legislature_upper","legislature_lower","mayor","ordinance","legislation","rating"} for r in politics))
check("living: politics rows reference real states/cities", all(
      (r["slug_or_code"] in states) if r["scope"] == "state" else (r["slug_or_code"] in slugs) for r in politics))
check("living: places enums valid and reference real cities", all(
      r["city_slug"] in slugs and r["type"] in {"bar","cafe","bookstore","center","health","other"} and
      r["status"] in {"open","closed","VERIFY"} for r in places))
check("living: events months valid and reference real cities", all(
      r["city_slug"] in slugs and r["month"] in MONTHS for r in events))
check("living: news kinds valid and reference real cities", all(
      r["city_slug"] in slugs and r["kind"] in {"pride","legal","community","other"} for r in news))
check("living: updates scope valid", all(r["scope"] in {"state","city","site"} for r in updates))
check("living: compare pairs reference distinct real cities", all(
      r["slug_a"] in slugs and r["slug_b"] in slugs and r["slug_a"] != r["slug_b"] for r in compare))
check("living: every populated row has an http source/link and a named source where required", all(
      is_url(r["source_url"]) for r in politics + updates) and all(
      is_url(r["url"]) and r["source"].strip() for r in places + events) and all(
      is_url(r["url"]) and r["outlet"].strip() and r["headline"].strip() for r in news))
check("living: every populated date is ISO (YYYY-MM or YYYY-MM-DD)", all(
      parse_asof(r["asof"]) for r in politics) and all(parse_asof(r["verified_asof"]) for r in places + events) and all(
      parse_asof(r["date"]) for r in news + updates))

# Source + as-of enforcement per fact group. Flip a group to True once its research pass is complete.
ENFORCED = {"airport": True, "climate": True, "pride_event": True,
            "lgbtq_district": True, "community_org": True, "local_ndo": True}
GROUP_COLS = {"climate": ["summer_high_f", "winter_low_f", "hazard_flags"]}
def real(v): return bool(v.strip()) and "VERIFY" not in v
for g, on in ENFORCED.items():
    cols = GROUP_COLS.get(g, [g])
    ok = all(is_url(c[g+"_src"]) and parse_asof(c[g+"_asof"]) for c in cities
             if c["status"] == "published" and any(real(c[k]) for k in cols))
    if on: check(f"living: every published city has {g} source + as-of", ok)
    else: print(f"SKIP living: {g} source/as-of not enforced yet")
check("living: unverified fields never carry a source (no orphan src on VERIFY values)", all(
      not (c[g+"_src"].strip()) for c in cities for g in ENFORCED
      if not any(real(c[k]) for k in GROUP_COLS.get(g, [g]))))
def _html(c): return open(os.path.join(DIST, "city", c["slug"]+".html")).read()
check("living: no VERIFY placeholder text renders on any city page", all("VERIFY" not in _html(c) for c in cities))
check("living: verified climate/airport show an As-of stamp with the source link", all(
      ("As of" in _html(c)) and
      all(html.escape(c[g+"_src"].split(";")[0].strip()) in _html(c) for g in ("airport", "climate") if is_url(c[g+"_src"]))
      for c in cities))

# political climate section: facts only, third-party ratings attributed
def _pol(c):
    h = _html(c); i = h.find('id="politics"')
    return h[i:h.find("</section>", i)] if i >= 0 else ""
check("living: every published city page has a political climate section with a governor/office table",
      all("Local political climate" in _pol(c) and "<th>Office</th>" in _pol(c) for c in cities))
_LABELS = re.compile(r"\b(liberal|conservative|progressive|hostile|friendly|welcoming|purple|red (state|city)|blue (state|city))\b", re.I)
check("living: political section carries no partisan/character labels", all(not _LABELS.search(re.sub(r"<[^>]+>", " ", _pol(c))) for c in cities))
check("living: every third-party rating names its publisher and year", all(
      ("Human Rights Campaign" in r["notes"] and re.search(r"\b20\d\d\b", r["value"])) for r in politics if r["item"] == "rating"))
check("living: rating rows carry a source and as-of", all(is_url(r["source_url"]) and parse_asof(r["asof"]) for r in politics if r["item"] == "rating"))
check("living: every mayor/governor row lists a party value (party or Nonpartisan or VERIFY)", all(r["party"].strip() for r in politics if r["item"] in ("mayor", "governor")))

# places / events / news rendering
import tempfile
TODAY = datetime.date.today()
def _hrefs(h): return re.findall(r'<a\s[^>]*href="(https?://[^"]+)"[^>]*>', h)
_closed = [p for p in places if p["status"] != "open"]
check("living: closed places never render on their city page", all(p["url"] not in _html(next(c for c in cities if c["slug"] == p["city_slug"])) for p in _closed))
_old = [n for n in news if (TODAY - parse_asof(n["date"])).days > 365]
check("living: news older than 12 months is not shown", all(n["url"] not in _html(next(c for c in cities if c["slug"] == n["city_slug"])) for n in _old))
class _A(HTMLParser):
    def __init__(self): super().__init__(); self.bad = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and (a.get("href") or "").startswith("http") and "data-ga" not in a: self.bad.append(a["href"])
def _untracked(c):
    p = _A(); p.feed(_html(c)); return p.bad
check("ga: every outbound link on city pages (places, events, news, sources) carries data-ga", all(not _untracked(c) for c in cities),
      "; ".join(f"{c['slug']}:{_untracked(c)[:1]}" for c in cities if _untracked(c)))
def _build_month(m):
    d = tempfile.mkdtemp()
    subprocess.run([sys.executable, "build.py"], env={**os.environ, "BUILD_MONTH": str(m), "BUILD_DIST": d}, check=True, capture_output=True)
    return open(os.path.join(d, "index.html")).read()
_jun = _build_month(6); _sep = _build_month(9); _dec = _build_month(12)
check("living: Pride module shows June events in June", "Pride events in June" in _jun and "Denver" in _jun)
check("living: Pride module shows September events in September", "Pride events in September" in _sep and "Blue Ridge Pride" in _sep)
check("living: Pride module falls forward to the next month that has events", "Coming up: Pride events in" in _dec)
check("living: Pride module event links carry data-ga", 'data-ga="event_click"' in _jun)

# comparison pages + feed
_cmp_ok = True; _cmp_ga = []; _cmp_ban = []
_BANW = re.compile(r"\b(best|largest|safest|top|leading|greatest|friendliest|#1)\b", re.I)
cities_by_slug = {c["slug"]: c for c in cities}
for r in compare:
    f = os.path.join(DIST, "compare", f"{r['slug_a']}-vs-{r['slug_b']}.html")
    if not os.path.exists(f): _cmp_ok = False; continue
    h = open(f).read(); a, b = cities_by_slug[r["slug_a"]], cities_by_slug[r["slug_b"]]
    _cmp_ok = _cmp_ok and a["status"] == "published" and b["status"] == "published" and a["city_label"].split(",")[0].split(" &")[0] in h
    pa = _A(); pa.feed(h); _cmp_ga += pa.bad
    if _BANW.search(re.sub(r"<[^>]+>", " ", h.split("</header>")[1])): _cmp_ban.append(f)
check("compare: every curated pair renders with both cities published", _cmp_ok and len(compare) >= 20)
check("compare: every pair shares a lifestyle tag", all(
      {t.strip() for t in cities_by_slug[r["slug_a"]]["lifestyle_tags"].split(";")} & {t.strip() for t in cities_by_slug[r["slug_b"]]["lifestyle_tags"].split(";")} for r in compare))
check("compare: no superlative wording on comparison pages", not _cmp_ban, ", ".join(_cmp_ban))
check("ga: every outbound link on comparison pages carries data-ga", not _cmp_ga, ", ".join(_cmp_ga[:2]))
_sm = open(os.path.join(DIST, "sitemap.xml")).read()
check("compare: all comparison pages are in the sitemap", all(f"compare/{r['slug_a']}-vs-{r['slug_b']}.html" in _sm for r in compare))
check("compare: every city in a pair links to its comparison page", all(
      f"compare/{r['slug_a']}-vs-{r['slug_b']}.html" in _html(cities_by_slug[r["slug_a"]]) and f"compare/{r['slug_a']}-vs-{r['slug_b']}.html" in _html(cities_by_slug[r["slug_b"]]) for r in compare))
check("feed: every update has a date, headline and http source", all(parse_asof(u["date"]) and u["headline"].strip() and is_url(u["source_url"]) for u in updates))
_newest = max(updates, key=lambda u: u["date"]) if updates else None
_idx = open(os.path.join(DIST, "index.html")).read()
check("feed: homepage shows the newest update with its source link", bool(_newest) and html.escape(_newest["headline"]) in _idx and html.escape(_newest["source_url"].split(";")[0].strip()) in _idx)
check("feed: city updates appear on that city's page", all(
      html.escape(u["headline"]) in _html(c) for u in updates if u["scope"] == "city" for c in cities if c["slug"] == u["slug"]))
check("feed: state updates appear on that state's city pages", all(
      html.escape(u["headline"]) in _html(c) for u in updates if u["scope"] == "state" for c in cities if c["state_code"] == u["slug"]
      if sum(1 for x in updates if x["scope"] == "state" and x["slug"] == u["slug"]) <= 5))

# sitemap lastmod reflects data dates, not the build date
_lm = dict(re.findall(r"<loc>https?://[^/]+/([^<]+)</loc>(?:<lastmod>([^<]*)</lastmod>)?", _sm))
check("sitemap: every lastmod is an ISO date and never in the future", all((not v) or (parse_asof(v) and parse_asof(v) <= TODAY) for v in _lm.values()))
check("sitemap: city lastmod is at least the city's last_reviewed date", all(_lm.get(f"city/{c['slug']}.html", "") >= c["last_reviewed"] for c in cities))
check("sitemap: pages with no dated data omit lastmod instead of using the build date", all(_lm.get(p, "x") == "" for p in ("methodology.html", "connect.html", "agent-signup.html")))

# copy hygiene (CLAUDE.md: no unsourced rankings/superlatives; keep agent-side jargon off public pages)
_CLAIMS = re.compile(r"second-gayest|america's first|country's first|first [a-z\- ]+ in (arkansas|the )|lowest price|the most (expensive|affordable) (place|option)\b|total acceptance|referral|workhorse|transaction volume", re.I)
check("copy: no unsourced 'first'/ranking claims or agent-side jargon in one-liners and editorial notes",
      not [c["slug"] for c in cities if _CLAIMS.search(c["one_liner"] + " " + c["editorial_note"])],
      ", ".join(c["slug"] for c in cities if _CLAIMS.search(c["one_liner"] + " " + c["editorial_note"])))

# Freshness (advisory only): laws/politics 180d, news 90d, everything else 365d.
TODAY = datetime.date.today()
def stale(v, days):
    d = parse_asof(v); return bool(d) and (TODAY - d).days > days
for g in ENFORCED:
    warn(f"fresh: {g} as-of within 365 days", not any(stale(c[g+"_asof"], 365) for c in cities))
warn("fresh: political rows within 180 days (annual third-party ratings: 400 days)", not any(stale(r["asof"], 400 if r["item"] == "rating" else 180) for r in politics),
     ", ".join(sorted({f"{r['slug_or_code']}/{r['item']}" for r in politics if stale(r["asof"], 400 if r["item"] == "rating" else 180)})))
_newest_news = {}
for r in news:
    d = parse_asof(r["date"])
    if d and (r["city_slug"] not in _newest_news or d > _newest_news[r["city_slug"]]): _newest_news[r["city_slug"]] = d
warn("fresh: each city's newest news item is within 90 days",
     all((TODAY - d).days <= 90 for d in _newest_news.values()),
     ", ".join(sorted(k for k, d in _newest_news.items() if (TODAY - d).days > 90)))
warn("fresh: places/events verified within 365 days", not any(stale(r["verified_asof"], 365) for r in places + events))
warn("fresh: state law rows within 180 days", not any(stale(s["law_asof"], 180) for s in states.values()))
warn("fresh: city prices within 180 days", not any(stale(c["price_asof"], 180) for c in cities))

print()
print(f"{'ALL TESTS PASSED' if not FAIL else str(len(FAIL))+' FAILURES: '+', '.join(FAIL)}" + (f" ({len(WARNINGS)} freshness warning(s))" if WARNINGS else ""))
sys.exit(1 if FAIL else 0)
