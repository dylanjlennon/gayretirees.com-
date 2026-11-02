# SEO / Content Research — 2026-11-02

Scheduled, read-only research pass. No CSVs, `build.py`, `dist/`, or `tests.py` were touched;
this report file is the only change in this commit.

## Site coverage snapshot (`data/cities.csv`, `data/collections.csv`, `build.py`)

26 city rows, unchanged from 10-26: 23 `published`, 3 `draft` (Orlando FL, Portland ME,
Charleston SC). `LIFESTYLE_LANES` in `build.py` still has six lanes (walkable-towns,
beach-coastal, mountains-seasons, desert-sunbelt, small-town, big-city), `QUICK_FILTERS` still
covers three collections (no-state-income-tax, explicit-protections, under-400k), and
`data/states.csv` still carries 23 states. Six sourced states still have **zero** rows in
`data/cities.csv`: **NY, NJ, IL, OH, DC, TN**. No new collections exist beyond the nine in
`data/collections.csv`.

## Since last time (2026-10-26 report)

- `git log`/`git diff` confirm zero changes to `data/cities.csv`, `data/collections.csv`, or
  `build.py` since 10-26 — the three draft rows are still draft, city/state counts match exactly.
- **Fountaingrove Lodge (Santa Rosa, CA) watchlist item is resolved this week.** 10-26 flagged
  it as "currency unconfirmed" because every source found then was from its 2013 opening era.
  This week's search surfaced an October 2026 senior-living guide that lists it among current
  market-rate LGBTQ+ 55+ communities, describing it as checked against its own website that
  month. That's thin but dated evidence of current operation — upgraded from watchlist to an
  actionable suggestion below (item 1), though a verified-data pass should still call the
  community directly before anything goes in a CSV, per the guide's own inconsistency on
  waitlist details.
- Did not re-search Walnut Creek/Rossmoor, Las Cruces NM, or Jasper County SC in depth this
  week (search budget went to Fountaingrove's currency check and a new North Carolina
  migration thread instead) — Rossmoor is repeated below on last week's sourcing only; Las
  Cruces/Jasper County are omitted rather than repeated stale, consistent with how 10-19's
  watchlist items were handled.
- Targeted re-check on Myrtle Beach, SC turned up a dated safety fact not in any prior report
  in this series: in April 2026, a man was charged under Myrtle Beach's local hate-crime
  ordinance after firing gunshots into a well-known LGBTQ+ nightclub there — the first time the
  city has brought charges under that ordinance, per The Sun News via WBTW. No injuries were
  reported. This doesn't change the underlying migration case for a Myrtle Beach row, but it's
  a real, dated fact a future editorial pass should weigh alongside the Pride Myrtle Beach
  nonprofit and the SC net-migration data already logged — consistent with CLAUDE.md's "never
  guess, never omit a sourced complicating fact" posture.

## What's working

No GA4/Search Console access is available to this run (`GA_ID` is still a placeholder per
`TODO.md`, as flagged in every prior report in this series) — this section stays evidence-based
on data alignment, not traffic.

- **moveBuddha's September 2026 moving-trends update reconfirms South Carolina and North
  Carolina as the two strongest in-migration states in the country** (SC #1 at a 2.02 overall
  in/out ratio per the mid-2026 report, NC holding the #2 destination spot at 1.77 as of
  September). The site already has two published North Carolina cities (Asheville,
  Raleigh–Durham) and a long-standing open suggestion for a South Carolina city (Myrtle Beach,
  this series' most-repeated item) — this week's data is further confirmation the site's
  existing Southeast emphasis lines up with real current migration demand, not stale priors.
  Source: https://movebuddha.com/blog/moving-trends ; https://www.movebuddha.com/?p=1072049
- **The Fountaingrove Lodge resolution (see "Since last time") extends the site's proven
  "named LGBTQ+-specific senior housing" pattern (Living Out/Palm Springs, Rainbow Vision/Santa
  Fe) to a third California anchor**, alongside last week's Rossmoor finding — two independent,
  concrete LGBTQ-retiree housing developments in Sonoma/East Bay CA that the site's existing
  structure (CA already sourced via Palm Springs/Guerneville) could absorb without a new-state
  lift.

## Content gap suggestions

### 1. Santa Rosa, CA (Fountaingrove Lodge) — new city row (upgraded from 10-26 watchlist)
Fountaingrove Lodge, a 10-acre, 55+ continuing-care community in Santa Rosa (Sonoma County) built
specifically for LGBTQ+ seniors and allies, is described by multiple sources as the nation's
first state-licensed CCRC built specifically for LGBTQ+ seniors — the same category of anchor
fact as Palm Springs' Living Out and Santa Fe's Rainbow Vision, both of which the site already
treats as first-class citable facts. Last week's flag was that every source was from its 2013
opening; this week an October 2026 senior-living guide lists it among current market-rate
options, checked against its own site that month. Run by Oakmont Senior Living.
A verified-data pass should call the community directly to confirm current pricing/occupancy
before any CSV entry — the October 2026 guide's own waitlist note appears to conflate it with
a different community, so it's not reliable for that detail.
- Site mechanism: new row in `data/cities.csv` (CA, West region, likely `small-town` or
  `mountains-seasons` lane — Sonoma County wine country, not desert — a human call).
- Sources: https://www.seniorlivingguide.com/communities/fountaingrove-lodge-4210-thomas-lake-harris-dr-santa-rosa-ca-95403/ ,
  https://www.builderonline.com/design/projects/california-project-offers-a-place-for-lgbt-seniors-to-call-home_o ,
  https://seniorly.com/assisted-living/california/santa-rosa/fountaingrove-lodge-l-g-b-t-q

### 2. Walnut Creek, CA (Rossmoor) — new city row (repeated from 10-26, no new sourcing this week)
Unchanged recommendation; not re-searched this week (see "Since last time"). Rossmoor's active
LGBTQ+ Alliance, long-running Lesbian Social Club, and the 2026 "unity day" response to a
documented hate incident still stand as logged 10-26 — see that report for full sourcing and
the editorial caveat about not framing it as a "safe haven."
- Site mechanism: new row in `data/cities.csv` (CA, West region).
- Sources (prior report): https://www.islands.com/2006174/hottest-lgbtq-rossmoor-retirement-village-florida-palm-springs-sleepy-norcal-city-walnut-creek ,
  https://sfist.com/2026/09/28/once-again-the-rossmoor-retirement-community-is-having-some-culture-wars/

### 3. Myrtle Beach, SC — new city row (9th consecutive week; new dated safety fact this week)
Unchanged core recommendation (SC #1 nationally on both HireAHelper's 2025 net-retiree-migration
data and moveBuddha's 2026 in/out ratio), but see "Since last time" above for a new, real fact a
verified-data pass should weigh: an April 2026 hate-crime-ordinance prosecution tied to gunfire
at a Myrtle Beach LGBTQ+ nightclub. This doesn't negate the migration case; it's exactly the
kind of sourced, dated complicating fact CLAUDE.md's accuracy rules call for surfacing rather
than omitting if this row gets built.
- Site mechanism: new row in `data/cities.csv` (SC, Southeast, beach-coastal lane). Would not
  qualify for `explicit-protections` (SC `housing_law` is `none`), but could carry a properly
  sourced HRC MEI number per CLAUDE.md's rating rules.
- Sources: https://www.wbtw.com/news/grand-strand/myrtle-beach/myrtle-beach-hosts-grand-strand-pride-2026/amp/ ,
  https://www.hireahelper.com/moving-statistics/retirement-study-2026/ ,
  https://pridemyrtlebeach.org/

### 4. Knoxville, TN — new city row (6th consecutive week; not re-searched this week)
Unchanged recommendation; no new search budget spent this week (see "Since last time"). All
prior sourcing (moveBuddha inbound ratio, Club XYZ closure, May 2026 Knox Pride center incident,
Mayor's LGBTQ+ Liaison office) stands as logged in the 10-26 report.
- Site mechanism: new row in `data/cities.csv` (TN, Southeast region); would newly qualify for
  the `no-state-income-tax` collection.
- Sources (prior reports): https://www.movebuddha.com/?p=1051564 ,
  https://www.knoxvilletn.gov/government/mayors_office/lgbt_equality_in_knoxville

### 5. Watchlist — Wilmington, NC (new this week; strong migration signal, LGBTQ anchor unverified)
PODS' 2026 moving-trends analysis names the Myrtle Beach–Wilmington market the single most
moved-to area in the country as of its May 2026 report, and a 2026 Islands.com list (via Qnotes
Carolinas) names Wilmington among North Carolina's LGBTQ-friendly cities. However, this is a
weaker gap than it first looks: North Carolina is already a sourced state with two published
cities (Asheville, Raleigh–Durham), and Wilmington's own HRC Municipal Equality Index score is
unclear from this session's search — the most recent figure found (66/100) dates to the 2022
cycle, with no 2026 figure confirmed. No retiree-specific LGBTQ+ social infrastructure
(community center, senior programming) was found for Wilmington specifically, unlike the site's
existing rows. Flagging as a watchlist item needing a dedicated LGBTQ-infrastructure search and
a current MEI check, not proposing a row outright — same treatment as Las Cruces (10-19) and
Jasper County (10-19).
- Sources: https://portcitydaily.com/local-news/2025/01/03/study-wilmington-area-no-1-place-people-are-moving-to/ ,
  https://qnotescarolinas.com/nc-lgbtq-friendly-cities-ranking-2026/ ,
  https://www.islands.com/2087316/most-inclusive-north-carolina-cities-lgbtq-people-welcoming-communities-comfortable-living

### 6. Reinforcement: Upstate New York still has zero city coverage (9th consecutive report, longest-standing open item)
No new sourcing beyond citations already logged across the series.
- Site mechanism: unchanged — new row in `data/cities.csv` (NY, Northeast region).
- Sources (prior reports): https://www.kiplinger.com/retirement/happy-retirement/the-best-places-for-lgbtq-people-to-retire-in-the-us ,
  https://biggayhudsonvalley.com/

### 7. Structural reminder: `ltc-protections` collection still unbuilt
No change since prior reports. `ltc_protections` is populated and sourced per-state in
`data/states.csv` (DE, MA, MI, NY, NJ, DC all `yes`) but no corresponding row exists in
`data/collections.csv`, and of the `yes` states only DE and MI currently have a published city.
This week's search also reconfirmed the broader picture is still patchy nationally — a federal
LGBTQ+ Long-Term Care Bill of Rights has been proposed but multiple sources call its passage
unlikely in the current Congress, and California and New Jersey remain the only states with
statewide (not just municipal) long-term-care-specific LGBTQ+ protections per this week's
search, alongside DC. Still gated on NY/NJ/DC city rows, none of which exist yet.
- Sources: https://www2.law.temple.edu/lppp/enacting-long-term-care-bill-of-rights-for-lgbtq-older-adults/ ,
  https://hotspotsmagazine.com/2026/04/02/aging-while-queer-leaves-many-older-adults-unprotected-in-long-term-care/

## Requires human review

These are suggestions only. Per this project's CLAUDE.md, no factual value (law, tax, price, climate) may be added to the CSVs without a real source URL and as-of date, and no page may be marked published without a human verification pass. Review and source each item before implementing.
