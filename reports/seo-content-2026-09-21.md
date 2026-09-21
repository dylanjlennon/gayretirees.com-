# SEO / Content Research — 2026-09-21

Scheduled, read-only research pass. No CSVs, `build.py`, `dist/`, or `tests.py` were touched.

## Since last time (2026-09-07 report)

None of the prior report's suggestions have been implemented yet — checked directly against
current repo state this session:
- No `orlando-fl` row in `data/cities.csv`.
- No South Carolina city row (SC is still a fully-sourced, unused state in `data/states.csv`).
- No `ltc-protections` (or similarly named) collection in `data/collections.csv`.
- `data/states.csv` still has no Minnesota or Washington row.

All four items remain open. This week's research reinforces two of them with fresher, more
specific evidence and adds two new candidates below — it doesn't repeat them unchanged.

One infra note: `TODO.md` shows a real GA4 property was created 2026-09-04
(Measurement ID `G-HMVXKSHKN9`, no longer a placeholder). This session still has no GA4/Search
Console API access, so "what's working" below remains qualitative, based on matching site
coverage against real search results retrieved this session — but if GA4/GSC access can be
wired into a future run, that would replace guesswork with actual query and traffic data.

## What's working

No analytics or ranking data was queried this run (see infra note above) — qualitative only:

- The site's existing state-level tax/law data collections keep matching real migration
  drivers: United Van Lines' 49th National Movers Study (2026) puts Delaware, Wyoming,
  Montana, Oklahoma, and Maine as the states with the highest share of older/retiree movers,
  and separately finds retirement-motivated moves have diversified well beyond Florida. The
  site already covers Delaware (Rehoboth), Maine (Ogunquit), and treats "beyond Florida"
  diversification as a given (AZ/NM/NV/CO/OR desert and mountain coverage) — good structural
  alignment, not something to change.
  Source: https://www.unitedvanlines.com/newsroom/2025-national-movers-study
- North Carolina's continued strength as an inbound state (United Van Lines has it in the
  top tier of inbound states; moveBuddha separately flags Raleigh as pulling retirees out of
  Florida for climate/economy reasons) validates the site's existing two NC pages (Asheville,
  Raleigh–Durham) rather than pointing to a gap.
  Sources: https://www.unitedvanlines.com/newsroom/2025-national-movers-study ,
  https://www.movebuddha.com/blog/migration-moving-report/

## Content gap suggestions

### 1. Portland, Maine — new city row (new this week)
Senior Housing News (published 2026-09-17, i.e. this week) and The Maine Wire (2026-08)
report that Maine's *first* LGBTQ+-focused affordable senior housing complex, "Equality
Commons," opened in Portland, ME in August 2026 — with more than four prospective residents
for every available unit already on the waitlist. This is a distinct, dated, concrete signal
of real unmet LGBTQ+ retiree demand in a city the site doesn't cover. Maine is already a
covered, sourced state (Ogunquit page exists, fully protective per the site's own data), so
this is a pure city-row addition, not a new-state lift.
- Site mechanism: new row in `data/cities.csv` (ME, Northeast region), likely paired with
  Ogunquit in copy as "Maine's two LGBTQ+ options: a real city vs. a beach village."
- Sources: https://seniorhousingnews.com/2026/09/17/senior-living-industry-must-not-forget-lgbtq-residents-workers-as-demand-rises/ ,
  https://www.themainewire.com/2026/08/maines-first-lgbtq-focused-affordable-senior-housing-complex-opens-in-portland/

### 2. Upstate New York (Saratoga Springs / New Paltz / Hudson Valley) — new city row (new this week)
Kiplinger's "Best Places for LGBTQ People to Retire in the US" names Upstate New York
specifically — Troy, Woodstock, Saratoga Springs, and New Paltz (which performed gay
marriages in 2004, seven years before NY marriage equality) — as a real, named LGBTQ+
retirement destination distinct from NYC. `data/states.csv` already carries NY as a state
(the earlier report's LTC-protections research separately flagged NY as one of the states
with LTC-specific protections), but **no NY city exists anywhere in `data/cities.csv`** —
this is the same "sourced state, zero cities" pattern the 2026-09-07 report flagged for SC,
just in a different state, and it's a real, named gap in a genre where NY carries real
credibility (marriage equality history, arts-town culture matching the site's existing
mountains-seasons/small-town lanes).
- Site mechanism: new row in `data/cities.csv` (NY, Northeast region), likely
  `lifestyle_tags` = mountains-seasons;small-town, similar shape to the Asheville or
  Saugatuck rows.
- Sources: https://www.kiplinger.com/retirement/happy-retirement/the-best-places-for-lgbtq-people-to-retire-in-the-us ,
  https://biggayhudsonvalley.com/welcome/

### 3. Refine last week's SC suggestion: Myrtle Beach, not just Hilton Head (evidence update)
Last week's report proposed a Hilton Head/Bluffton/Beaufort SC row based on Census county
growth data. This week's moveBuddha migration report (early-2026 data) gives a sharper,
more specific number: Myrtle Beach, SC posted a 2.60 inbound-to-outbound move ratio — the
single strongest of any metro moveBuddha tracked — with more than a third of inbound movers
over age 65. United Van Lines separately puts South Carolina at #2 nationally for inbound
moves (60.8%). This doesn't replace the Hilton Head idea, but it's a second, independently
sourced SC candidate with fresher and more retiree-specific data — worth having whoever
scopes the SC row decide between (or combine) Myrtle Beach and Hilton Head once someone
does the on-the-ground verification pass.
- Site mechanism: same as last week — new row(s) in `data/cities.csv` (SC, Southeast
  region), leveraging the already-sourced SC row in `data/states.csv`. Same caveat applies:
  SC's `housing_law` is `none`, so it won't qualify for `explicit-protections`.
- Sources: https://www.movebuddha.com/blog/migration-moving-report/ ,
  https://www.unitedvanlines.com/newsroom/2025-national-movers-study

### 4. Reinforcement for last week's LTC-protections collection idea (new source)
A 2026 peer-reviewed comparison in the Journal of the American Medical Directors Association
("Protecting LGBTQ+ Long-Term Care Residents in the United States: Comparisons of 9 Laws")
gives the LTC-protections collection idea from the 2026-09-07 report a stronger, citable
backbone: it documents 9 distinct US laws protecting LGBTQ+ people in long-term care, with
real variance in scope/enforcement, and separately notes under 1-in-5 LTC communities with
resident non-discrimination policies actually name LGBTQ+ protections. This is exactly the
kind of third-party-cited, dated source the site's ranking-claims rule requires before any
copy could describe a place as relatively "better" on this axis. No new suggestion here,
just stronger sourcing for the collection already proposed.
- Source: https://www.jamda.com/article/S1525-8610(26)00033-2/fulltext

## Requires human review

These are suggestions only. Per this project's CLAUDE.md, no factual value (law, tax, price, climate) may be added to the CSVs without a real source URL and as-of date, and no page may be marked published without a human verification pass. Review and source each item before implementing.
