# SEO / Content Research — 2026-09-07

Scheduled, read-only research pass. No CSVs, `build.py`, or `dist/` were touched.
This is the first report in `reports/` — no prior report to compare against, so no
"since last time" section.

## Coverage snapshot (from data/cities.csv, data/collections.csv, LIFESTYLE_LANES in build.py)

- 23 published cities across CA, FL, NC, DE, AZ, NM, NV, CO, OR, TX, GA, MA, ME, PA, MI, AR.
- Florida coverage: Wilton Manors/Ft Lauderdale, St Petersburg/Gulfport, Sarasota/Bradenton, Key West — **no Orlando**.
- `data/states.csv` carries fully-sourced rows for **South Carolina** and **Tennessee** (tax notes, law status, sources) but **zero cities in either state appear in `data/cities.csv`** — the state-level data is already there and unused.
- 6 lifestyle lanes (walkable-towns is a collection only, not a homepage lane): beach-coastal, mountains-seasons, desert-sunbelt, small-town, big-city, walkable-towns.
- 9 collections total, including `no-state-income-tax`, `explicit-protections`, `under-400k`. No collection currently surfaces the `ltc_protections` field that already exists per-state in `data/states.csv`.

## What's working

No analytics, Search Console, or ranking data was available to this session — GA4 is still a placeholder property per `TODO.md`, and this pass had no access to real traffic figures. So this section is qualitative only, based on matching existing coverage against real search results retrieved this session:

- The site's core FL/AZ/NM cluster (Wilton Manors, Palm Springs, Tucson, Santa Fe) matches the cities named most often across the "best LGBTQ retirement" roundups this session pulled up (Kiplinger, 55places, LCS Living, SeniorAdvice) — good alignment between existing coverage and what people are actually searching for and clicking on in these lists.
- The `no-state-income-tax` and `explicit-protections` collections map directly onto the two motivations Census Bureau reporting names as primary drivers of retiree migration this year (cost/tax, then legal protections) — the site's filtering structure already matches the real decision criteria.

## Content gap suggestions

### 1. Orlando, FL — new city row
Orlando comes up repeatedly and specifically in this session's search results as an LGBTQ+ retirement destination distinct from Ft Lauderdale/Wilton Manors: The Center Orlando runs a dedicated senior program (the "OWLs" program) and a local SAGE chapter, and multiple roundups cite Orlando by name alongside Ft Lauderdale as Florida's other major LGBTQ+ retiree hub. Florida is already a covered, no-income-tax state on the site, so this is a pure city-row addition with no new state data needed.
- Site mechanism: new row in `data/cities.csv` (FL, Southeast region).
- Sources: https://thecenterorlando.org/senior/ , https://www.senioradvice.com/articles/americas-best-cities-for-gay-friendly-retirement , https://www.55places.com/blog/lgbtq-friendly-area-to-retire

### 2. Hilton Head / Bluffton / Beaufort, SC — new city row (leverages an already-sourced state row)
Two independent signals converge here. First, Census Bureau Vintage 2025 population estimates name Jasper County, SC (adjacent to Hilton Head) as the fastest-growing county in the country by percentage, driven by the retiree building boom around Hilton Head; Stateline's coverage of the same data flags small Southeast counties, especially in SC, as the frontier of the current retiree migration wave. Second, this session's own search turned up Sun City Hilton Head — a large active-adult community — with documented interest from same-sex married couples, plus an active Beaufort County LGBTQ community group. `data/states.csv` already has a fully-sourced SC row (senior income deductions, SS exempt, no explicit housing-law protection) sitting unused because no SC city exists in `data/cities.csv`.
- Caveat for whoever verifies this: SC's `housing_law` is `none`, so an SC city would not qualify for the `explicit-protections` collection — that should be stated plainly in copy, not glossed over, consistent with the "no superlatives, no unearned claims" rule.
- Site mechanism: new row in `data/cities.csv` (SC, Southeast region).
- Sources: https://stateline.org/2026/03/26/new-census-estimates-show-movers-swelling-population-in-small-southeast-counties/ , https://www.census.gov/library/stories/2026/03/county-domestic-migration-trends.html , https://www.suncityhiltonhead.org/ , https://www.tripadvisor.com/ShowTopic-g54273-i170-k9653309-LGBT_friendly-Hilton_Head_South_Carolina.html

### 3. New collection: LGBTQ-inclusive long-term-care protections
Search results this session repeatedly surfaced long-term-care/nursing-home discrimination as a distinct, real concern in this space — separate from general housing or public-accommodation law — with sources noting LGBTQ+ seniors "rely more on nursing homes... because they are less likely to have adult children," and citing a specific, real wave of state-level LTC protections (CA 2017, DC/Montgomery Co. 2020, NJ/NY 2021, OR 2023, MA 2025). `data/states.csv` already carries a sourced `ltc_protections` field (`yes` for DE, OR, MA, MI, NY; `partial` for NM) that today only appears buried in each state's row on the states table and each city's "at a glance" spine. There is no collection page aggregating it, despite it matching a real query pattern ("gay retirement community legal protections") this session actually retrieved.
- Site mechanism: new row in `data/collections.csv` with a rule against the existing `ltc_protections` field (would need a small, additive rule case in `build.py`'s `matches()` alongside the existing `income_tax`/`housing_law` cases — no new factual data required, purely surfaces what's already sourced).
- Sources: https://ojin.nursingworld.org/MainMenuCategories/ANAMarketplace/ANAPeriodicals/OJIN/TableofContents/Vol-20-2015/No2-May-2015/Articles-Previous-Topics/Changing-the-Culture-of-Long-Term-Care-Combating-Heterosexism.html , https://www.chcs.org/resource/meeting-the-health-and-social-needs-of-lgbtq-older-adults-through-medicaid/ , https://www.care.com/c/finding-lgbtq-friendly-senior-care-facility/

### 4. Watchlist (bigger lift — flagging, not proposing yet)
- **Minneapolis, MN** — an LCS Living roundup names Minneapolis specifically as "the most gay-friendly city in 2024," citing same-sex household density and an absence of anti-LGBTQ+ legislation. The site has no Midwest big-city coverage in this genre (only Saugatuck, a small resort town). Minnesota isn't in `data/states.csv` at all, so this needs a new *state* row (with sourced law/tax data) before a city row makes sense — bigger lift than #1/#2 above. Source: https://www.lcsliving.com/resources/for-seniors/senior-living-options/the-10-best-cities-for-lgbtq-seniors-to-retire-in/
- **Seattle/Washington state** — retirementliving.com names Washington's lack of state income tax as a retiree draw; same "new state row needed first" constraint applies. Source: https://www.retirementliving.com/best-states-for-lgbtq-retirees

## Requires human review

These are suggestions only. Per this project's CLAUDE.md, no factual value (law, tax, price, climate) may be added to the CSVs without a real source URL and as-of date, and no page may be marked published without a human verification pass. Review and source each item before implementing.
