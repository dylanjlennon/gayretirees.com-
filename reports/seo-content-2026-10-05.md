# SEO / Content Research — 2026-10-05

Scheduled research pass. Read-only against `data/` and `build.py`; no CSVs, `build.py`,
or `dist/` touched. This file is the only change in this commit.

## Site coverage snapshot (from `data/cities.csv`, `data/collections.csv`, `build.py`)

26 city rows, 23 `published`, 3 `draft` (Orlando FL, Portland ME, Charleston SC).
Regions covered: West (CA ×3, NV), Southwest (AZ ×2, NM ×2), Southeast (FL ×5, NC ×2, GA,
SC), Mid-Atlantic (DE, PA), Mountain West (CO), Pacific NW (OR), Texas, Northeast (MA, ME
×2), Midwest (MI), Ozarks (AR). `LIFESTYLE_LANES` in `build.py` has six lanes: walkable
-towns, beach-coastal, mountains-seasons, desert-sunbelt, small-town, big-city — all six
already have published cities.

`data/states.csv` carries 23 states, but seven of them have **zero** rows in
`data/cities.csv`: **NY, NJ, IL, OH, DC, TN, SC-adjacent-but-SC now has one city
(Charleston, draft)**. NY, TN, NJ, IL, OH, DC remain fully unused despite being sourced.
This "sourced state, no city" pattern has now been flagged in every report in this series
since 09-07 for NY, and since 09-21 for TN — it is the single most durable finding across
four consecutive weeks of research.

## What's working

No analytics/ranking data is available to this run (no GA4 property exists yet per
`TODO.md`'s `GA_ID` placeholder, and no search-console or traffic export was provided) — so
this section is evidence-based on data alignment only, not performance, exactly as flagged
in prior reports.

- **Oregon's inbound numbers jumped hard.** United Van Lines' 49th Annual National Movers
  Study (published 2025-12-29, covering the most recent full year) now ranks **Oregon #1
  nationally for inbound migration at 65%**, up from #8 the prior year. The site already has
  a published Portland, OR page — this is now one of the best-supported rows on the whole
  site from a pure migration-momentum standpoint, not just an LGBTQ-culture one.
  Source: https://www.yahoo.com/news/articles/where-americans-moving-2026-4-120906469.html
- **South Carolina's inbound strength keeps compounding**, now from two independent
  sources: United Van Lines has SC at #2 nationally (60.8%), and moveBuddha's 2026 city-
  level data gives **Myrtle Beach, SC** a 7.60 inbound-to-outbound ratio — the single
  strongest of any city in its dataset. The site's one SC row (Charleston, draft) does not
  cover Myrtle Beach; see gap #1 below, which is now a fourth-consecutive-week finding.
  Sources: https://www.yahoo.com/news/articles/where-americans-moving-2026-4-120906469.html ,
  https://www.movebuddha.com/blog/moving-trends/
- **New Jersey's role as a pure "outbound" state is now extremely well evidenced** (8th
  straight year topping outbound migration per United Van Lines) — this is actually a
  reasonable argument for *not* prioritizing an NJ city row even though NJ is a sourced
  state, since the demand signal runs the other direction. Worth noting so this doesn't
  get flagged as an open gap in a future report without this context.
  Source: https://www.roi-nj.com/2025/12/29/lifestyle/n-j-tops-united-van-lines-study-in-outbound-migration-for-eighth-straight-year/

## Content gap suggestions

### 1. Myrtle Beach, SC — new city row (fourth consecutive week this has surfaced)
This is the most-repeated unresolved finding in the report series. 09-21 flagged it from
moveBuddha's then-current inbound ratio; 09-28 added the 65+ population growth stat (+6.3%
YoY, +22% this decade, fastest of any US metro); this week's moveBuddha 2026 data gives it
the single highest inbound ratio (7.60) of any city in their tracked set, and a local
LGBTQ+ nonprofit (Pride Myrtle Beach, est. 2020) already exists to cite as the community
anchor. The site's SC row (Charleston, draft) is a different city with a different
profile (historic port city vs. beach-retiree boomtown) — this would be additive, not a
duplicate. Same caveat as prior reports: SC `housing_law` is `none` in `data/states.csv`,
so this would not qualify for the `explicit-protections` collection regardless.
- Site mechanism: new row in `data/cities.csv` (SC, Southeast, beach-coastal lane).
- Sources: https://www.movebuddha.com/blog/moving-trends/ ,
  https://pridemyrtlebeach.org/

### 2. Illinois/Chicago — new state-anchor city, now with a fresh legal hook (new this week)
IL is a sourced state in `data/states.csv` with zero cities, same pattern as NY/TN. This
week's research found a concrete, dated legislative development: Governor Pritzker signed
**SB3490** in 2026, amending the Illinois Act on Aging to add specific protections and
services for older LGBTQ adults, alongside separately-proposed HB4359/SB2805 (the
"Illinois LGBTQ+ and HIV Long-Term Care Bill of Rights," mandating cultural-competency
training and banning discriminatory treatment in long-term-care and assisted-living
facilities). That gives a Chicago/Andersonville row a specific, citable legal-protections
story beyond the generic statewide nondiscrimination law already in `data/states.csv`,
the same way New York's LTC bill of rights (flagged in the 09-21 report) would for an NY
row. Independent query-pattern evidence also surfaced Chicago named as a top "safest city
to retire gay couple" result this session, not just a generic "liberal city" mention.
- Site mechanism: new row in `data/cities.csv` (IL, Midwest region, big-city lane likely).
- Sources: https://hoodline.com/2026/06/pritzker-s-pride-power-play-three-new-laws-boost-lgbtq-protections-in-chicago/ ,
  https://gov.illinois.gov/newsroom/press-release.24908.html

### 3. A new collection mechanism: "LGBTQ+/HIV long-term-care bill of rights" states
This is a structural suggestion rather than a single-city one. Two sourced states now have
a specific, named, dated legal instrument that's narrower and more concrete than the
existing `housing_law` field: New York's LTC resident bill of rights for LGBT/HIV-status
residents (flagged 09-21) and Illinois's SB3490 Act-on-Aging amendment plus the pending
LTC Bill of Rights bill (found this week). This is a distinct axis from
`explicit-protections` (which tracks general housing/public-accommodation law) — it's
specifically about nursing-home/assisted-living conduct, which is a sharper buyer-intent
signal for a retirement-specific audience than general nondiscrimination law. If sourced
state-by-state with real bill citations and as-of dates, this could become either a new
field on `data/states.csv` or a new row in `data/collections.csv` once at least 2-3 cities
in qualifying states are published (currently zero, since neither NY nor IL has a city row
yet — this depends on gap #2 and the standing NY gap being resolved first).
- Site mechanism: new `data/states.csv` field + new `data/collections.csv` row, gated on
  having published cities in qualifying states.
- Sources: https://www.governor.ny.gov/news/governor-hochul-signs-legislation-protect-rights-seniors-living-hiv-and-members-lgbtqia ,
  https://gov.illinois.gov/newsroom/press-release.24908.html

### 4. Watchlist — The Villages, FL (new this week, flagging for awareness only)
moveBuddha's 2026 data gives The Villages, FL the strongest retiree-specific inbound
signal found this session (3.58 inbound ratio, explicitly one of the largest age-
restricted communities in the country). It does have an organized LGBTQ+ social group
(Rainbow Family & Friends, officially sanctioned since 2007), but it reads as "a gay
group within a mostly-straight mega-community" rather than an LGBTQ+-anchored place the
way every other row on the site is — a meaningfully different profile from the rest of
`data/cities.csv`. Flagging as a judgment call for a human to make, not proposing a row.
- Sources: https://www.movebuddha.com/blog/moving-trends/ ,
  https://www.facebook.com/rainbowfamilyvillagesfl/

### 5. Reinforcement: Upstate New York and Knoxville, TN both still open (no new evidence, pattern holds)
No new sourcing this week beyond what's already in the 09-21/09-28 reports. Repeating only
to keep the "longest open items" visible: NY has zero cities despite three straight weeks
of citation (Kiplinger, LinkedIn/Castillo), and Knoxville, TN (moveBuddha's #1 move-to city
+ an official Mayor's LGBTQ+ Liaison office) has zero cities despite two straight weeks.

## Requires human review

These are suggestions only. Per this project's CLAUDE.md, no factual value (law, tax, price, climate) may be added to the CSVs without a real source URL and as-of date, and no page may be marked published without a human verification pass. Review and source each item before implementing.
