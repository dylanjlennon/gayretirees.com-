# Price source audit — 2026-09-20

Scope: `median_price_usd` / `price_asof` / `price_src` for all 23 cities in `data/cities.csv`.

## Findings

- All 23 rows carry a Redfin or Zillow source URL and a year-month as-of. No blog/aggregator sources.
  (The earlier "9 unverifiable cities" in TODO.md/ROADMAP.md have since been sourced.)
- **Metric mismatch (accuracy issue):** the site labels every value "Median home price", but
  - **7 cities** cite a **Redfin** housing-market page → median *sale price*:
    asheville, phoenix, tucson, santa-fe, albuquerque, austin, raleigh-durham.
  - **16 cities** cite **Zillow** → *typical home value* (ZHVI, a smoothed, seasonally adjusted
    mid-tier value), not a median sale price: 13 via `zillow.com/home-values/...` pages
    (palm-springs, wilton-manors, st-pete, rehoboth, sarasota, las-vegas, denver, portland,
    savannah, key-west, saugatuck, eureka-springs, guerneville) and 3 via Zillow's public ZHVI
    CSV (provincetown, ogunquit, new-hope).
  Mixing the two under one "median" label is not accurate, and sorting/comparing across them
  is apples-to-oranges.
- Oldest as-of: eureka-springs 2026-04 (~5 months). Under the 6-month staleness bar but the
  oldest in the set; re-pull when convenient.
- URL liveness was not machine-verified (Zillow/Redfin return 403 to non-browser clients).

## Decision

Rather than replace every value, record which metric each row uses and label it honestly:
- new column `price_metric` = `median_sale` (Redfin) | `typical_value` (Zillow ZHVI)
- city pages/cards show "Median sale price" or "Typical home value", plus the source name
- comparison and sort UI notes that the two measures differ
- spot-check a sample of sources in the browser (values match the cited page)

## Method note

Counts tallied from the `price_src` host/path in `data/cities.csv` (redfin.com = 7,
zillow.com/home-values = 13, files.zillowstatic.com ZHVI CSV = 3; total 23).
