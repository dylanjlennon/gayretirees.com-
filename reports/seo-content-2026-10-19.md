# SEO / Content Research — 2026-10-19

Scheduled, read-only research pass. No CSVs, `build.py`, `dist/`, or `tests.py` were touched;
this report file is the only change in this commit.

## Site coverage snapshot (`data/cities.csv`, `data/collections.csv`, `build.py`)

26 city rows, unchanged from 10-12: 23 `published`, 3 `draft` (Orlando FL, Portland ME,
Charleston SC). `LIFESTYLE_LANES` in `build.py` still has six lanes (walkable-towns,
beach-coastal, mountains-seasons, desert-sunbelt, small-town, big-city) — all six already have
published cities, and `QUICK_FILTERS` still covers three collections (no-state-income-tax,
explicit-protections, under-400k). `data/states.csv` carries 23 states (confirmed SC is now
present, matching 10-05's note). Six sourced states still have **zero** rows in
`data/cities.csv`: **NY, NJ, IL, OH, DC, TN**. This is the seventh consecutive weekly report to
find NY unchanged, and the fourth for TN.

## Since last time (2026-10-12 report)

Checked directly against current repo state and against fresh search results this session:

- No repo changes since 10-12 — Orlando, Portland ME, and Charleston SC are still `draft`; no
  NY/NJ/IL/OH/DC/TN rows were added; no new collections were added.
- Targeted re-searches for Knoxville, TN and Myrtle Beach, SC specifically for October 2026
  turned up no new dated developments beyond what prior reports already cited — both remain
  open on the strength of the migration/demographic data already logged, not new news this
  week. Noting this explicitly so a future report doesn't re-discover the same base facts as if
  they were new.
- The New Jersey LGBTQI+ Senior Bill of Rights (nursing-home protections, cited in earlier
  reports) continues to check out as a real, standing law — re-confirmed this week via a
  secondary summary (SceneMag) describing it as barring nursing homes from refusing preferred
  pronouns or denying access to single-sex spaces. No NJ city row exists yet to attach it to;
  this remains background support for the NJ gap, not a new standalone item.

## What's working

No GA4/Search Console access is available to this run (`GA_ID` is still a placeholder per
`TODO.md`, as flagged in every prior report in this series) — this section stays evidence-based
on data alignment, not traffic.

- **The site's three `no-state-income-tax` cities for existing search patterns (FL, TX, NV)
  keep showing up as the generic recommendation in this week's "LGBTQ friendly retirement, no
  state income tax" results** (Wilton Manors/Fort Lauderdale FL and Austin TX both named
  directly). This is the fourth or fifth week this pattern has reconfirmed — the lane is
  correctly built and the existing rows are well-aligned with real query results, not just
  internal assumption.
  Source: https://www.lcsnet.com/resources/for-seniors/senior-living-options/the-10-best-cities-for-lgbtq-seniors-to-retire-in
- **Las Cruces, NM's HRC Municipal Equality Index score (89/100, 2023 cycle, "second in the
  state for municipal equality" per the city's own tourism site) is a genuinely usable fact if
  a Las Cruces row is ever built** — New Mexico is already a sourced state via Santa Fe/
  Albuquerque, so a third NM city would be a relatively low lift structurally. Flagging the
  number now so it isn't re-discovered from scratch later; per CLAUDE.md it would need its own
  publisher/URL/year/as-of sourcing pass at implementation time, not reuse of this summary.
  Source: https://www.visitlascruces.com/things-to-do/lgbtqia/

## Content gap suggestions

### 1. Myrtle Beach, SC — new city row (seventh consecutive week this has surfaced)
Unchanged recommendation. No new corroborating data this week (see "since last time" above) —
repeating only to keep this the most-repeated open item in the series visible, not because
new evidence arrived. All sourcing from prior reports still stands (moveBuddha inbound ratio,
Census Horry County 55+ migration finding, HRC MEI 100 score, Pride Myrtle Beach nonprofit).
- Site mechanism: new row in `data/cities.csv` (SC, Southeast, beach-coastal lane). Would not
  qualify for `explicit-protections` (SC `housing_law` is `none`), but could carry a properly
  sourced HRC MEI number per CLAUDE.md's rating rules.
- Sources (prior reports): https://www.movebuddha.com/?p=1052440 ,
  https://www.census.gov/library/stories/2026/03/county-domestic-migration-trends.html ,
  https://pridemyrtlebeach.org/

### 2. Knoxville, TN — new city row (fourth consecutive week; TN remains a sourced, zero-city state)
Unchanged recommendation. No new sourcing this week beyond what's already logged (moveBuddha
#1 move-to search interest and #1 projected 2026 inbound-to-outbound forecast, Mayor's LGBTQ+
Liaison office, multiple local orgs). Repeating to keep visible.
- Site mechanism: new row in `data/cities.csv` (TN, Southeast region); would newly qualify for
  the `no-state-income-tax` collection.
- Sources (prior reports): https://www.movebuddha.com/?p=1051564 ,
  https://www.knoxvilletn.gov/government/mayors_office/lgbt_equality_in_knoxville

### 3. Reinforcement: Upstate New York still has zero city coverage (seventh consecutive report, longest-standing open item)
No new sourcing beyond the Kiplinger/LinkedIn citations already logged across the series.
Repeating to keep this visible as the longest-open item.
- Site mechanism: unchanged — new row in `data/cities.csv` (NY, Northeast region).
- Sources (prior reports): https://www.kiplinger.com/retirement/happy-retirement/the-best-places-for-lgbtq-people-to-retire-in-the-us ,
  https://biggayhudsonvalley.com/

### 4. Watchlist — Las Cruces, NM (new this week; lower-lift structurally, but LGBTQ-retiree anchor is thin)
This week's search surfaced Las Cruces as a #2-nationally-ranked "move-to" city in one
moveBuddha-sourced ranking (3.44 inbound-search ratio), and it has a real HRC MEI score (89,
2023) and a long-running local LGBTQ nonprofit (New Mexico GLBTQ Centers, though its most
recent confirmable coverage dates to 2010 — would need a currency check before citing). New
Mexico is already a sourced state with two published cities (Santa Fe, Albuquerque), so adding
Las Cruces is a smaller structural lift than opening a new state. However, unlike Santa Fe
(home to the dedicated Rainbow Vision LGBTQ retirement community) Las Cruces' retiree-specific
LGBTQ infrastructure reads thinner in this session's search — general gay-friendly-city
signals, but no retirement-specific anchor comparable to the site's other rows. Flagging as a
judgment call, not proposing a row outright, the same way The Villages, FL was flagged
09-28 and Jasper County, SC is flagged below.
- Site mechanism (if pursued): new row in `data/cities.csv` (NM, Southwest region,
  desert-sunbelt lane likely).
- Sources: https://www.visitlascruces.com/things-to-do/lgbtqia/ ,
  https://coastalmovingservices.com/moving-tips/top-cities-people-are-moving-to/ ,
  https://www.groundworksnm.org/news/las-cruces-opens-glbtq-community-center/2010/6

### 5. Watchlist — Jasper County, SC / Bluffton-Hilton Head area (new this week; strong migration signal, no LGBTQ anchor found)
Multiple independent, government-sourced reports this week (South Carolina Daily Gazette,
Stateline, Post and Courier, all citing the Census Bureau's March 2026 Vintage 2025 county
estimates) name Jasper County, SC as the single fastest-growing county in the nation by
percentage (6% growth), driven substantially by retirees moving into age-55+ communities like
Latitude Margaritaville Hilton Head and Sun City Hilton Head. This is a strong, well-sourced
retiree-migration signal in a state the site already covers (SC, via the draft Charleston row
and the already-flagged Myrtle Beach gap). However, this session's search found no
LGBTQ-specific community anchor for Jasper County/Bluffton/Hilton Head comparable to Myrtle
Beach's Pride Myrtle Beach nonprofit or any other city on the site — flagging for awareness
only, same caveat as The Villages, FL (09-28): real retiree-migration data, but not yet an
LGBTQ-anchored place the way the site's existing rows are. Would need a dedicated search for
local LGBTQ+ social/support infrastructure in the Lowcountry/Beaufort County area before this
becomes an actionable suggestion.
- Sources: https://scdailygazette.com/2026/03/27/jasper-county-leads-nation-in-growth-as-newcomers-move-to-coastal-regions/ ,
  https://stateline.org/2026/03/26/new-census-estimates-show-movers-swelling-population-in-small-southeast-counties/

### 6. Structural reminder: `ltc-protections` collection still unbuilt (no new evidence, pattern holds)
No change since 10-05/10-12's finding. `ltc_protections` is populated and sourced per-state in
`data/states.csv` (DE, MA, MI, NY, NJ, DC all `yes`) but no corresponding row exists in
`data/collections.csv`, and of the `yes` states only DE and MI currently have a published
city. This week's NJ Senior Bill of Rights re-confirmation (see "since last time") strengthens
the underlying case but doesn't change the actionability — still gated on NY/NJ/IL/OH/DC city
rows, none of which exist yet. Repeating only to keep visible.

## Requires human review

These are suggestions only. Per this project's CLAUDE.md, no factual value (law, tax, price, climate) may be added to the CSVs without a real source URL and as-of date, and no page may be marked published without a human verification pass. Review and source each item before implementing.
