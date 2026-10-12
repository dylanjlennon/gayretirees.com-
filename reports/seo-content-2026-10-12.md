# SEO / Content Research — 2026-10-12

Scheduled, read-only research pass. No CSVs, `build.py`, `dist/`, or `tests.py` were touched;
this report file is the only change in this commit.

## Site coverage snapshot (`data/cities.csv`, `data/collections.csv`, `build.py`)

26 city rows, 23 `published`, 3 `draft` (Orlando FL, Portland ME, Charleston SC). State codes
present in `data/cities.csv`: AZ, AR, CA, CO, DE, FL(×5), GA, MA, ME(×2), MI, NC(×2), NM(×2),
NV, OR, PA, SC, TX. `LIFESTYLE_LANES` in `build.py` has six lanes (walkable-towns,
beach-coastal, mountains-seasons, desert-sunbelt, small-town, big-city) — all six already have
published cities. `data/states.csv` carries 18 states; six of them still have **zero** rows in
`data/cities.csv`: **NY, NJ, IL, OH, DC, TN**. This is the sixth consecutive weekly report to
find this unchanged for NY, and the third for TN and IL.

## Since last time (2026-10-05 report)

Checked directly against current repo state and against fresh search results this session:

- No new city rows were added since 10-05 — Orlando, Portland ME, and Charleston SC are still
  `draft`; no NY/NJ/IL/OH/DC/TN rows were added.
- **Correction to last week's Illinois item:** the 10-05 report flagged Illinois's LGBTQ+ and
  HIV Long-Term Care Bill of Rights (HB4359/SB2805) as a "newly signed" legal hook. That was
  wrong — re-checking this week, the bill did **not** pass. Equality Illinois's own 2026
  legislative recap says it did not reach final passage before the spring session adjourned,
  and the Illinois General Assembly's own bill-status page shows it stalled at 2nd reading in
  March 2026, with no signature on record. Pritzker did sign three *other* LGBTQ bills in June
  2026 (medical privacy, hormone-therapy coverage, ID gender markers) — real, but not the LTC
  bill of rights. If a future report or any CSV edit cites this bill, it should be corrected:
  Illinois's `ltc_protections` field correctly remains `no` in `data/states.csv`, and the
  Chicago/Illinois city-row suggestion from 10-05 should rely on general `housing_law=explicit`
  only, not an LTC-specific hook.
  Sources: https://www.equalityillinois.us/2026-legislative-recap/ ,
  https://www.ilga.gov/ftp/legislation/104/BillStatus/HTML/10400HB4359.html

## What's working

No GA4/Search Console access is available to this run (`GA_ID` is still a placeholder per
`TODO.md`, as flagged in every prior report in this series) — this section stays evidence-based
on data alignment, not traffic.

- **Myrtle Beach, SC's retiree-migration signal is now corroborated by a second,
  independent, government source.** Beyond moveBuddha's search-ratio ranking (flagged every
  week since 09-21), the Census Bureau's own March 2026 county-migration story names Horry
  County, SC (where Myrtle Beach sits) as one of the top South Atlantic destinations for
  domestic migration, specifically citing adults 55+ as the group driving most of that
  inflow. Two different methodologies (search intent vs. actual Census residency data) now
  point at the same place. Source:
  https://www.census.gov/library/stories/2026/03/county-domestic-migration-trends.html
- **moveBuddha's two separate 2026 products both still point at the same underlying gaps.**
  Its migration report ranks Myrtle Beach #1 for retirement-destination search interest
  (328-in-to-100-out); its separate 2026 Moving Forecast (built from Moving Cost Calculator
  data) ranks Knoxville, TN #1 for projected in-migration overall. Both cities remain
  unaddressed gaps (see below), and both signals have now recurred across multiple distinct
  moveBuddha products, not just one list.
  Sources: https://www.movebuddha.com/?p=1052440 , https://www.movebuddha.com/?p=1051564
- **Myrtle Beach's HRC Municipal Equality Index score (100/100, 2024 cycle) is a genuinely
  usable fact if that city row is ever built.** Per CLAUDE.md, a third-party rating like HRC
  MEI can be shown as a number only on the rated city's own page, attributed to HRC, with
  publisher/URL/year/as-of date recorded — this score would clear that bar if sourced
  properly at implementation time. Flagging it now so it isn't re-discovered from scratch
  later. Source: WBTW/Grand Strand Pride 2026 coverage citing the HRC 2024 Municipality
  Equality Index, https://www.wbtw.com/news/grand-strand/myrtle-beach/myrtle-beach-hosts-grand-strand-pride-2026/

## Content gap suggestions

### 1. Myrtle Beach, SC — new city row (sixth consecutive week this has surfaced)
Unchanged recommendation, now with two new supporting data points this week (Census Bureau
Horry County 55+ migration finding, and the HRC MEI 100 score noted above). This remains the
single most-repeated open item in this report series.
- Site mechanism: new row in `data/cities.csv` (SC, Southeast, beach-coastal lane). Would not
  qualify for `explicit-protections` (SC `housing_law` is `none`), but could carry a properly
  sourced HRC MEI number per the rules above.
- Sources: https://www.movebuddha.com/?p=1052440 ,
  https://www.census.gov/library/stories/2026/03/county-domestic-migration-trends.html ,
  https://pridemyrtlebeach.org/

### 2. Knoxville, TN — new city row (third consecutive week; TN remains a sourced, zero-city state)
This week's moveBuddha 2026 Moving Forecast independently ranks Knoxville #1 nationally for
projected in-migration (~1.61 arrivals per departure), on top of the 2025-2026 migration report
ranking it #1 for move-to search interest (both flagged previously). TN is a fully-sourced
no-income-tax state in `data/states.csv` with zero city rows — the same durable pattern as NY.
- Site mechanism: new row in `data/cities.csv` (TN, Southeast region); would newly qualify for
  the `no-state-income-tax` collection.
- Sources: https://www.movebuddha.com/?p=1051564 ,
  https://www.knoxvilletn.gov/government/mayors_office/lgbt_equality_in_knoxville

### 3. Reinforcement: Upstate New York still has zero city coverage (sixth consecutive report, longest-standing open item)
No new sourcing beyond the Kiplinger/LinkedIn citations already logged in 09-21/09-28/10-05.
This week's targeted search for fresh Hudson Valley/Woodstock retirement news came back with
only adjacent context (a 50+ social meetup at the Hudson Valley LGBTQ+ Community Center in
Kingston, and Sage Upstate in Syracuse) — real local infrastructure, but nothing new enough to
cite as a standalone hook beyond what's already in the series. Repeating to keep this visible
as the longest-open item across six weeks.
- Site mechanism: unchanged — new row in `data/cities.csv` (NY, Northeast region).
- Sources: https://www.kiplinger.com/retirement/happy-retirement/the-best-places-for-lgbtq-people-to-retire-in-the-us ,
  https://biggayhudsonvalley.com/

### 4. Watchlist — Washington Blade's 2025 "6 cities" list names candidates not yet checked against site coverage (new this week)
This week's buyer-intent search surfaced the Washington Blade's "6 cities where you can retire
with pride" list (2025), which names Fort Lauderdale (covered via Wilton Manors) alongside
Seattle (already an open WA gap per 09-07/09-28) and also Atlanta and Providence, RI — neither
of which has been checked against site coverage in this series before. Georgia is a sourced
state (via Savannah's row) but Atlanta itself has no row; Rhode Island isn't in `data/states.csv`
at all, so a Providence row would be a bigger lift (new state sourcing first). Flagging both as
awareness-only, not proposing a page — neither has independent migration-data corroboration the
way Myrtle Beach/Knoxville do, just inclusion on one buyer-intent list.
- Sources: https://www.washingtonblade.com/2025/08/03/6-cities-where-you-can-retire-with-pride/

### 5. Structural reminder: `ltc-protections` collection still unbuilt (no new evidence, pattern holds)
No change since 10-05's finding. `ltc_protections` is populated and sourced per-state in
`data/states.csv` (DE, MA, MI, NY, NJ, DC all `yes`) but no corresponding row exists in
`data/collections.csv`, and of the `yes` states only DE and MI currently have a published city.
Repeating only to keep it visible, not proposing new action this week.

## Requires human review

These are suggestions only. Per this project's CLAUDE.md, no factual value (law, tax, price, climate) may be added to the CSVs without a real source URL and as-of date, and no page may be marked published without a human verification pass. Review and source each item before implementing.
