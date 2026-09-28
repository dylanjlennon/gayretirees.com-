# SEO / Content Research — 2026-09-28

Scheduled, read-only research pass. No CSVs, `build.py`, `dist/`, or `tests.py` were touched.

## Since last time (2026-09-21 report)

Checked directly against current repo state this session — real progress on three of the
four items the 2026-09-07/09-21 reports flagged:

- **Orlando, FL** — now exists as a `draft` row in `data/cities.csv` (not yet `published`).
  Addresses the 2026-09-07 suggestion.
- **Charleston, SC** — now exists as a `draft` row (`housing_law` partial per its one-liner).
  Addresses the SC-city gap first flagged 2026-09-07 (that report proposed Hilton Head; this
  implementation chose Charleston instead — see new Myrtle Beach suggestion below, which is a
  *different* SC city than either).
- **Portland, ME** — now exists as a `draft` row. Addresses the 2026-09-21 suggestion.

All three are still `status=draft`, so per CLAUDE.md's publishing rule they correctly aren't
live yet pending a verified-data pass — that's not a gap, just noting where they stand.

Still open, unchanged since 09-07/09-21:
- No NY city row exists in `data/cities.csv`, despite NY being a fully-sourced state in
  `data/states.csv` and Upstate NY (Troy/Woodstock/Saratoga Springs/New Paltz) surfacing
  *again* in this week's independent search results (see below) — third consecutive report
  to find this.
- No `ltc-protections` (or similarly named) collection exists in `data/collections.csv`,
  despite the `ltc_protections` field already being populated and sourced per-state.
- `data/states.csv` still has no Minnesota or Washington row (both recur in this week's
  "no state income tax" / LGBTQ-friendly search results — Seattle again, same as 09-07).

## What's working

No GA4/Search Console access was available to this session (same limitation as prior
reports) — this section is qualitative, based on matching current coverage against real
search results retrieved this session:

- moveBuddha's 2025-2026 migration report independently confirms Myrtle Beach, SC and the
  broader "Southern retirement destination" pattern the site already leans into via its FL,
  AZ, NM, and now-draft SC coverage — momentum is real and ongoing, not a one-off.
  Source: https://www.movebuddha.com/blog/migration-moving-report/
- The site's `no-state-income-tax` collection continues to map onto exactly the states
  general retirement-tax roundups keep naming (FL, TX, NV, TN, WA) — of those, the site
  already covers FL/TX/NV; TN and WA are the two recurring gaps (see below).
  Source: https://www.fedweek.com/retirement-financial-planning/the-most-tax-friendly-states-for-retirement-in-2026/

## Content gap suggestions

### 1. Knoxville, TN — new city row (new this week)
Tennessee is already a fully-sourced state in `data/states.csv` (no income tax, SS exempt)
but has **zero cities** in `data/cities.csv` — the same "sourced state, unused" pattern this
report series has now caught for SC (resolved via Charleston) and previously for NY (still
open). Knoxville is a strong, concrete candidate: moveBuddha's 2025-2026 migration report
names Knoxville its #1 most popular move-to city for 2026, and separately the City of
Knoxville runs an official Mayor's LGBTQ+ Liaison office plus multiple active local
organizations (SoKno Pride, Blount Pride, Knox Pride, Bryant's Bridge) and an annual Knox
Pridefest — real, citable local infrastructure, not just a vibe claim.
- Site mechanism: new row in `data/cities.csv` (TN, Southeast region), would also newly
  qualify for the `no-state-income-tax` collection.
- Sources: https://www.movebuddha.com/blog/migration-moving-report/ ,
  https://www.knoxvilletn.gov/government/mayors_office/lgbt_equality_in_knoxville ,
  https://www.knoxlgbtbusinesses.com/

### 2. Myrtle Beach, SC — new city row, distinct from the now-drafted Charleston row (new this week)
The 09-21 report flagged Myrtle Beach as a moveBuddha-sourced candidate competing with
Hilton Head for the SC slot; since then the SC gap was filled with Charleston instead —
a different city with different demographics (historic port city vs. beach-resort retiree
metro). This week's research adds a sharper, dated stat: Myrtle Beach's 65+ population grew
6.3% last year alone and >22% over the 2020s, the fastest rate of any US metro this decade,
with roughly 16,000 retirees moving to the Myrtle Beach/Conway/North Myrtle Beach area in
2023. Locally, Pride Myrtle Beach (est. 2020) is an active 501(c)(3) serving the area's
LGBTQ+ community. Since Charleston already covers SC's legal/tax data via the shared state
row, this would be a second, additive SC city rather than a first — same caveat as before:
SC `housing_law` is `none`, so neither SC city qualifies for `explicit-protections`.
- Site mechanism: new row in `data/cities.csv` (SC, Southeast region, beach-coastal lane).
- Sources: https://www.marketbeat.com/articles/once-known-as-dirty-myrtle-myrtle-beach-is-now-the-fastest-growing-us-metro-for-seniors-2025-07-01 ,
  https://pridemyrtlebeach.org/ ,
  https://www.aol.com/myrtle-beach-tops-charts-city-110000598.html

### 3. Reinforcement: Upstate New York still has zero city coverage (third consecutive report)
Upstate NY (Troy, Woodstock, Saratoga Springs, New Paltz) surfaced again this week in
independent "safest cities to retire gay couple" results, same as the 09-21 report's
Kiplinger-sourced finding. NY remains a sourced state with no city row. No new evidence
beyond confirming the pattern is durable, not a one-off search artifact — flagging again
since it's now the single longest-standing open item in this report series.
- Site mechanism: unchanged from 09-21 — new row in `data/cities.csv` (NY, Northeast region).
- Sources: https://www.kiplinger.com/retirement/happy-retirement/the-best-places-for-lgbtq-people-to-retire-in-the-us ,
  https://www.linkedin.com/pulse/seven-best-us-cities-lgbtq-seniors-retire-robert-castillo-xtodc

### 4. Watchlist (bigger lift, new-state work needed — not proposing a page yet)
- **Seattle / Washington** — recurred again this week (no state income tax + "openly
  tolerant environment with an active gay social scene" per this session's search results),
  same as the 09-07 report's finding. WA still isn't in `data/states.csv`; a sourced state
  row would need to exist before any city row makes sense.
- **New Orleans, LA** — new this week: search results surfaced Rainbow Vista, a retirement
  community built specifically for LGBTQ+ residents 55+, in New Orleans. Louisiana isn't in
  `data/states.csv` at all — bigger lift, flagging for awareness only, not proposing yet.
  Source: https://www.seniorliving.org/retirement/lgbt/

## Requires human review

These are suggestions only. Per this project's CLAUDE.md, no factual value (law, tax, price, climate) may be added to the CSVs without a real source URL and as-of date, and no page may be marked published without a human verification pass. Review and source each item before implementing.
