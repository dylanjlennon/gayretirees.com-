# PRD 0001: Living City Guide (content freshness engine)

Status: DRAFT for Dylan's review — no implementation until the task list is approved ("Go").
Workflow: ai-dev-tasks (`~/Desktop/apps/ai-dev-tasks`) → PRD → `tasks-0001-…md` → one sub-task at a time.

## Roadmap context (four PRDs)

1. **0001 — Living City Guide** (this doc): richer, sourced, visibly-current content for all 23 cities.
2. 0002 — Local Agent Voices: attributed, human-written local contributions + intro flow + disclosure.
3. 0003 — Agent Recruitment & Onboarding: per-city demand report, signup funnel, pricing/Stripe
   (see `research-gayrealestate-com-2026-09-20.md`; pricing decision required first).
4. 0004 — Measurement: GA4 + Netlify form reporting, so agent pitches use real numbers only.

Order matters: agents only sign up if there is real traffic and real intros to show them, and
that comes from the guide. Today: 23 published cities, 1 agent (Asheville), 1 real lead.

## 1. Introduction / Overview

GayRetirees.com helps LGBTQ+ people 55+ decide where to retire. Today each city page has a
sourced fact table (law, tax, price) plus short un-sourced fields (airport, climate, pride
event, LGBTQ district, community org) and a house-voice `editorial_note`. It reads like a
reference sheet and does not signal "this is current." Competitor GayRealEstate.com's city
pages are undated boilerplate — a gap we can win by being sourced, dated, and alive.

**Goal:** every city page is rich, correctly attributed, and visibly current — without
becoming a boring reference site and without breaking CLAUDE.md's accuracy rules.

## 2. Goals

1. All 23 cities carry every section in §4 with a source URL and as-of date per fact group.
2. Every fact group shows a visible "verified <Month Year>" stamp; stale groups are flagged by tests.
3. Site changes visibly month to month (seasonal Pride module, "what changed" feed) without daily/weekly manual work.
4. Comparison pages exist for a curated set of city pairs.
5. Zero unsourced facts and zero fabricated anecdotes shipped (CLAUDE.md / VOICE.md).

## 3. User stories

- As a reader weighing Palm Springs vs. Tucson, I want a side-by-side of law, tax, climate,
  airport and scene so I can decide without opening ten tabs.
- As a safety-first reader, I want to see what recently changed in my target state's law, with
  a date and source, so I know the page is current.
- As a chasing-the-scene reader, I want named LGBTQ+ bars and places with a link and a
  "last checked" date so I'm not sent to a place that closed.
- As a reader in September, I want to see which Pride events are happening now or soon.
- As Dylan, I want to add or refresh a fact by editing a CSV and rebuilding, and have tests
  tell me what's missing or stale.

## 4. Functional requirements

Each city page gets these sections. Every fact group has `*_src` (URL) and `*_asof` (date)
columns; a blank value is marked `VERIFY` and the section hides that item (never guessed).

**Data model**
1. `cities.csv` gains `_src` / `_asof` columns for: airport, climate, pride_event,
   lgbtq_district, community_org, local_ndo (currently un-sourced). Existing sourced columns unchanged.
2. New `data/places.csv`: `city_slug, name, type (bar|café|bookstore|center|health|other),
   url, source, verified_asof, status (open|closed|VERIFY)`. Only places with an official URL
   or citable listing; `closed` rows are excluded from render.
3. New `data/events.csv`: `city_slug, name, month, typical_weeks, url, source, verified_asof`
   (recurring annual events, e.g. Pride). No exact dates unless the organizer's page states them.
4. New `data/updates.csv`: `date, scope (state|city|site), slug, headline, source_url` — one
   line per real change (law, tax, closure, new city data). Drives the "What changed" feed.
5. New `data/climate.csv` (or columns): sourced normals (NOAA or equivalent), airport with
   nearest-commercial distance/drive time, hazard flags with source.
6. New `data/politics.csv`: `scope (state|city), slug_or_code, item, value, source_url, asof`
   — factual, neutral items only. Required items per city (state level from the state code,
   city level per city): governor + party; state legislature control (which party holds each
   chamber, or "split"); mayor + party **or "nonpartisan" where the office is nonpartisan
   (never inferred)**; municipal nondiscrimination ordinance status; notable enacted/pending
   LGBTQ-related legislation. No adjectives, no "vibe," no "blue/red city" labels — just
   who holds the offices and the party as recorded by a cited source.
6a. Third-party ratings (approved 2026-09-20): numeric ratings may be shown **only** when a
   named third party publishes them (e.g. HRC Municipal Equality Index score), with source
   URL, publication year and as-of date, and only on the page for the rated city/state.
   Cities the third party doesn't rate show nothing. Requires a CLAUDE.md rule update (task 1.0).
6b. New `data/news.csv`: `city_slug, date, outlet, headline, url, kind (pride|legal|community|other)`
   — manually curated, verbatim headline, link out only (no article text copied), from named
   outlets. Only items of clear LGBTQ+ relevance to that city. Old items age out of the page
   but stay in the CSV.

**Page content**
7. City page renders, in order: snapshot table (exists) → climate/weather + airport →
   law & tax (exists) → local political climate (factual items) → LGBTQ+ places (linked) →
   Pride & events → straight-talk note (exists) → agent/advocate block (exists; voices are PRD 0002).
8. Every section shows "Verified <Month Year> · Source" with the link (`rel="noopener"`).
9. A section with no verified data shows nothing — not a placeholder claim.
10. "What changed" feed on the homepage and per state/city, from `updates.csv`, newest first.
11. Homepage "Pride this month" module from `events.csv`, computed at build time from the
    current month; falls back to the next upcoming month.
12. Comparison pages `/compare/<a>-vs-<b>.html` for a curated list in `data/compare.csv`
    (not all 253 pairs), built purely from existing city/state fields + a linked cross-reference.
13. Site rebuilds on a schedule (weekly) so month-based modules stay correct; sitemap
    `lastmod` reflects real data dates, not build time.

**Quality gates (tests.py)**
14. Published city missing any required `_src`/`_asof` → test fails.
15. Fact group older than its freshness limit (laws/politics 180 days, news 90 days,
    places/events/others 365 days) → test **warns** (prints WARN, does not fail the suite).
    Missing source/as-of (req. 14) still fails.
16. No comparative/superlative wording in new copy (CLAUDE.md "Claims and rankings").
17. New links carry `data-ga` attributes and are covered by the `ga:` tests.

**Research method**
18. Research produces CSV rows with source + as-of, done per region in parallel passes.
    Anything unverifiable stays `VERIFY`.
19. Reddit and similar forums may be read to discover **what retirees actually ask/worry
    about**, then answered from primary/official sources. They are never quoted, never cited as
    fact, and never scraped in bulk (check each site's terms first).

## 5. Non-goals

- No agent-voice submission flow, intro flow, or pricing (PRDs 0002–0003).
- No daily/weekly manual content, no automated news scraping (curated links only, req. 6b),
  no user accounts or comments.
- No rankings or "best/#1" claims (unless a third-party-cited page is deliberately approved —
  see Open Questions).
- No named/bylined editorial persona (VOICE.md, 2026-09-11 decision).
- No hero images beyond what is sourced/credited (currently 0/23 have one).

## 6. Design considerations

- PERSONA.md rules stand: large high-contrast text, no parallax/animation, one dominant CTA,
  holds at 150–200% zoom. New sections use plain headings and lists, not tabs or carousels.
- "Alive" comes from dated stamps, the feed, and the seasonal module — not motion.

## 7. Technical considerations

- Stay static: CSV → `build.py` → `dist/`. Never hand-edit `dist/`.
- Weekly rebuild via a Netlify build hook triggered by a scheduled GitHub Action
  (creating the hook needs Dylan's go-ahead in Netlify).
- Reuse existing patterns in `build.py` (`load`, `page`, `clean`) and `tests.py` style.
- Data quirk: TODO.md/ROADMAP.md say 14 cities published and GA4 not live; the data shows
  23 published and GA4 live. Refresh those docs as part of this work.

## 8. Success metrics

- 23/23 cities pass the new source/as-of tests; 0 `VERIFY` values rendered.
- Baseline GA4 engagement per city page captured before launch (no target set until we have
  a baseline — will not invent one).
- Count of `updates.csv` entries per month (target set with Dylan; suggest ≥ 4/month).
- Intro-form submissions per city page (feeds PRD 0003's demand report).

## 9. Open questions

Resolved 2026-09-20 (Dylan):
- Comparison pairs: go ahead — ~20 pairs chosen by lifestyle tag, listed in `data/compare.csv`.
- Third-party ratings (HRC MEI "and others like it"): **approved**, with req. 6a guardrails.
- Political climate: include who currently holds state and local office and their party (req. 6).
- Staleness: **warn**, not fail (req. 15).
- Events: local Prides and similar events, plus newsworthy Pride/LGBTQ+ items per city (req. 6b).

- Prices: Dylan approved (2026-09-20) looking up city median prices on Redfin/Zillow and citing
  the page + date. Task 1.0 audits every city's `price_src`/`price_asof`; any that are weak or
  stale are re-pulled (browser, one city at a time, read-only) and re-sourced.
- Officeholders: official government site is authoritative for "current"; Ballotpedia is the
  cross-check. If they disagree, use the official site and note it; if unresolved, `VERIFY`.

Still open: none.
