# SEO / Content Research — 2026-10-26

Scheduled, read-only research pass. No CSVs, `build.py`, `dist/`, or `tests.py` were touched;
this report file is the only change in this commit.

## Site coverage snapshot (`data/cities.csv`, `data/collections.csv`, `build.py`)

26 city rows, unchanged from 10-19: 23 `published`, 3 `draft` (Orlando FL, Portland ME,
Charleston SC). `LIFESTYLE_LANES` in `build.py` still has six lanes (walkable-towns,
beach-coastal, mountains-seasons, desert-sunbelt, small-town, big-city), `QUICK_FILTERS` still
covers three collections (no-state-income-tax, explicit-protections, under-400k), and
`data/states.csv` still carries 23 states. Six sourced states still have **zero** rows in
`data/cities.csv`: **NY, NJ, IL, OH, DC, TN**. No new collections exist beyond the nine in
`data/collections.csv`.

## Since last time (2026-10-19 report)

- No repo changes since 10-19 — `git log` / `git status` confirm the three draft rows are
  still draft, no new city or collection rows exist, and the city/state counts above match
  10-19 exactly.
- The long-repeated Myrtle Beach, SC and Knoxville, TN items (now in their 8th and 5th
  consecutive weeks respectively) both got fresh corroborating data this session — see below —
  rather than being repeated on the strength of prior-week sourcing alone.
- Checked whether Illinois' pending LGBTQ+ long-term-care bill (HB4359/SB2805, flagged as
  pending in earlier research) advanced. It did not: Equality Illinois' own 2026 legislative
  recap states neither bill reached final passage this session. This matters for the
  standing `ltc-protections` collection suggestion (item 5 below) — it removes IL as a
  near-term candidate, leaving NY/NJ/DC as the uncovered `ltc_protections=yes` states.
- Did not re-check Jasper County, SC or Las Cruces, NM in depth this week (both logged as
  "watchlist, no LGBTQ-retiree anchor found" as of 10-19); no new search budget was spent on
  them so they're omitted rather than repeated with stale sourcing.

## What's working

No GA4/Search Console access is available to this run (`GA_ID` is still a placeholder per
`TODO.md`, as flagged in every prior report in this series) — this section stays evidence-based
on data alignment, not traffic.

- **South Carolina's position as the site's single most-corroborated unfilled gap got
  materially stronger evidence this week.** HireAHelper's February 2026 retirement-migration
  study (using PGM Solutions data on ~15 million 2025 domestic moves) found South Carolina was
  the single largest *net* gainer of retirement-age (65+) movers of any US state in 2025 — a
  net gain of 5,427 — ahead of Texas and North Carolina, while Florida's inbound and outbound
  retiree flows nearly canceled out (net +815, not even top-10). This is a stronger, more
  current data point than anything cited in the prior 7 weeks of Myrtle Beach suggestions, and
  it validates the site's existing "beach-coastal" SC coverage gap at the state level, not just
  the single-city level.
  Source: https://www.hireahelper.com/moving-statistics/retirement-study-2026/ (via secondary
  coverage at https://www.beckershospitalreview.com/rankings-and-ratings/the-states-cities-seeing-an-influx-of-older-adults/)
- **The existing published Palm Springs and Santa Fe rows' core premise — a dedicated
  LGBTQ+-specific retirement development as a page's anchor fact — is the same pattern this
  week's research found reproduced in California outside the site's current two CA cities**
  (see gap #1 below). That the site already treats "named senior-specific LGBTQ+ housing" as a
  first-class, citable fact (Living Out in Palm Springs, Rainbow Vision in Santa Fe) means the
  new California finding slots into an existing, proven content pattern rather than requiring a
  new one.

## Content gap suggestions

### 1. Walnut Creek, CA (Rossmoor) — new city row (new this week, concrete anchor)
Rossmoor, a ~9,800-resident 55+ gated community in Walnut Creek, CA (East Bay, ~30 min from San
Francisco/BART-connected), has a genuinely citable LGBTQ-retiree anchor comparable to the
site's existing Palm Springs/Santa Fe pattern: an active Rossmoor LGBTQ+ Alliance, a
long-running Rossmoor Lesbian Social Club (founded 2009, oral-history-documented by the GLBT
Historical Society), and recent mainstream coverage describing it as a long-standing draw for
LGBTQ+ retirees. California is already a sourced state (`explicit` housing/PA law, in
`data/states.csv`) with two published cities (Palm Springs, Guerneville), so this is a
same-state addition, not a new-state lift.
One factual nuance a verified-data pass would need to weigh carefully: a September 2026 SFist
piece (citing the San Francisco Chronicle) reports a real, dated incident — a lesbian resident's
tires were slashed during Pride Month — followed by an 18-group "unity day" organized in
response, scheduled for October 2, 2026. This cuts against any "safe haven" framing and should
be handled as a sourced, dated fact if included at all, consistent with CLAUDE.md's ban on our
own superlatives.
- Site mechanism: new row in `data/cities.csv` (CA, West region; likely `desert-sunbelt` does
  not fit — more likely `big-city` given the SF Bay Area proximity, or a new lane if the
  pattern repeats — a human call, not inferred here).
- Sources: https://www.islands.com/2006174/hottest-lgbtq-rossmoor-retirement-village-florida-palm-springs-sleepy-norcal-city-walnut-creek ,
  https://en.wikipedia.org/wiki/Rossmoor,_Walnut_Creek,_California ,
  https://sfist.com/2026/09/28/once-again-the-rossmoor-retirement-community-is-having-some-culture-wars/ ,
  https://oac.cdlib.org/findaid/ark:/13030/c8rr25vz/entire_text/

### 2. Watchlist — Santa Rosa, CA (Fountaingrove Lodge) — new this week, currency unconfirmed
Fountaingrove Lodge in Santa Rosa (Sonoma County), CA is described by multiple sources,
including a PBS documentary (*The Lodge*), as the nation's first state-licensed continuing-care
retirement community built specifically for LGBTQ+ seniors and allies, opened 2013. This would
be an even more direct parallel to Palm Springs' Living Out than Walnut Creek. However, every
source found this session describing it is from its opening period (2013-era); a Caring.com
directory listing is the only evidence it's still operating, and no 2026-dated source
confirms current ownership, occupancy, or status. Flagging as a watchlist item needing a
currency check before it becomes an actionable suggestion — same caveat pattern as prior
reports' Las Cruces/Jasper County items.
- Sources: https://www.builderonline.com/design/projects/california-project-offers-a-place-for-lgbt-seniors-to-call-home_o ,
  https://www.caring.com/articles/lgbt-seniors-worry-about-discrimination ,
  https://weta.org/watch/shows/lodge-1

### 3. Myrtle Beach, SC — new city row (8th consecutive week; now backed by new state-level migration data)
Unchanged recommendation, now with stronger corroboration than any prior week — see "What's
working" above for the HireAHelper 2026 state-level finding (SC = #1 net retiree-migration
gainer nationally). Prior sourcing (moveBuddha inbound ratio, Census Horry County 55+ migration
finding, HRC MEI 100 score, Pride Myrtle Beach nonprofit) still stands unchanged.
- Site mechanism: new row in `data/cities.csv` (SC, Southeast, beach-coastal lane). Would not
  qualify for `explicit-protections` (SC `housing_law` is `none`), but could carry a properly
  sourced HRC MEI number per CLAUDE.md's rating rules.
- Sources: https://www.movebuddha.com/?p=1052440 ,
  https://www.hireahelper.com/moving-statistics/retirement-study-2026/ ,
  https://pridemyrtlebeach.org/

### 4. Knoxville, TN — new city row (5th consecutive week; mixed signal this week)
The underlying migration case is reconfirmed this week: moveBuddha's 2026 trends report still
projects Knoxville as having the strongest inbound-to-outbound ratio in the nation (~1.61
newcomers per 1 leaving). But this week's search also surfaced two negative, dated local
developments worth weighing in any human review: Club XYZ, one of Knoxville's last two LGBTQ+
bars, is closing after a 22-year run over a rent/landlord dispute (following an earlier
queer-owned coffee shop's closure), and Knox Pride's community center had a "security incident"
with an armed individual in May 2026 (resolved; center reopened next day; police described the
person as unhoused and trespassed, not describing it as a targeted hate incident). These don't
negate the state-tax/migration case for a TN row, but they're relevant, dated facts a city-page
editorial pass should know about rather than present a thinner social-infrastructure picture
than currently exists.
- Site mechanism: new row in `data/cities.csv` (TN, Southeast region); would newly qualify for
  the `no-state-income-tax` collection.
- Sources: https://www.advocate.com/news/club-xyz-one-of-knoxvilles-last-remaining-lgbtq-bars-says-a-rent-increase-and-landlord-dispute-will-force-it-to-close-after-22-years-in-business ,
  https://www.wkyt.com/2026/05/07/knox-pride-center-closed-after-security-incident-with-armed-person/ ,
  https://www.knoxvilletn.gov/government/mayors_office/lgbt_equality_in_knoxville

### 5. Reinforcement: Upstate New York still has zero city coverage (8th consecutive report, longest-standing open item)
No new sourcing beyond citations already logged across the series.
- Site mechanism: unchanged — new row in `data/cities.csv` (NY, Northeast region).
- Sources (prior reports): https://www.kiplinger.com/retirement/happy-retirement/the-best-places-for-lgbtq-people-to-retire-in-the-us ,
  https://biggayhudsonvalley.com/

### 6. Structural reminder: `ltc-protections` collection still unbuilt (narrower now — IL's pending bill failed to pass)
No corresponding row exists yet in `data/collections.csv` for `ltc_protections` even though
`data/states.csv` already has it populated per-state (DE, MA, MI, NY, NJ, DC all `yes`). New
information this week narrows the realistic path: Illinois' pending LGBTQ+ long-term-care
bill of rights (HB4359/SB2805) did not pass this session per Equality Illinois' own 2026
legislative recap, so IL isn't a near-term candidate to add alongside DE/MI's existing
coverage. The collection remains gated on NY/NJ/DC city rows, none of which exist yet (NY is
item 5 above; NJ and DC have no open suggestion in this series yet).
- Sources: https://www.equalityillinois.us/2026-legislative-recap/ ,
  https://www.ilga.gov/ftp/legislation/104/BillStatus/HTML/10400HB4359.html

## Requires human review

These are suggestions only. Per this project's CLAUDE.md, no factual value (law, tax, price, climate) may be added to the CSVs without a real source URL and as-of date, and no page may be marked published without a human verification pass. Review and source each item before implementing.
