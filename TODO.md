# Launch Checklist

In order:

- [x] Replace placeholder phone `tel:+18285550100` sitewide (build.py header CTA
      + agents.csv) with real number 828-412-0678. tests.py's hardcoded phone
      literal and agent-card fixture (which pointed at the now-deleted
      jane-sample row) were repointed at asheville/dylan-lennon, the only
      real covered market. All tests green.
- [ ] Replace REPLACE-tagged email and license in agents.csv (Dylan's row) —
      blocked on: is dylan@gayretirees.com a live mailbox, and Dylan's NC
      real estate license number.
- [x] Delete the two EXAMPLE agent rows (jane-sample, mark-sample)
- [x] DECISION (confirmed): removed the 20 `*-to-asheville` route rows from
      routes.csv — consolidated to the single existing Asheville city page
      instead, to avoid duplicating GayAsheville.com content across sites.
      Kept the 3 original routes. The Redfin #1/#2/#3-origin ranking claim
      that lived on the Atlanta/Miami/DC routes was dropped (no source page
      left to carry it); CLAUDE.md's ranking-claims rule updated accordingly.
- [x] Give the Asheville city page (data/cities.csv) a copy pass so its
      one_liner reads as genuinely novel vs. GayAsheville.com — repositioned
      around the retirement angle (retiree-paced WNC life) rather than the
      general relocation pitch GayAsheville.com already owns.
- [x] Tier 1 verification pass (2026-08-30): all 23 states' legal/tax fields
      checked against mapresearch.org (lgbtmap.org rebranded), Tax Foundation,
      state DOR/OTR pages, and AARP/SSA guidance — 6 parallel research passes,
      sources + as-of dates recorded in states.csv. Found and corrected 4
      stale fields: NC income tax 4.5%→3.99%, CO flat-low→flat-mid (4.40%),
      GA flat-low→flat-mid (4.99%), MI flat-low→flat-mid (4.25%). Resolved
      6 of 9 previously-VERIFY ltc_protections fields (NV/CO/IL/PA → no,
      OR/MA/NY/NJ/DC → yes); DE/ME/MI/NM genuinely have no citable source,
      correctly left VERIFY rather than guessed.
      Cities: 14 of 23 got a real sourced median price (Redfin/Zillow) and
      flipped to status=published — asheville, raleigh-durham,
      eureka-springs, phoenix, tucson, santa-fe, albuquerque, austin,
      palm-springs, guerneville, las-vegas, portland, denver, saugatuck.
      9 came back UNVERIFIABLE — Redfin/Zillow blocked automated fetches
      (403) and search-snippet figures for these specific small/volatile
      markets varied too widely to trust (e.g. Key West ranged
      $792K–$1.34M across snapshots): wilton-manors, st-pete, sarasota,
      key-west, savannah, rehoboth, new-hope, provincetown, ogunquit.
      These stay status=draft with the price still flagged VERIFY — no
      guessed numbers shipped. Needs a manual Redfin/Zillow pull per city
      (or a Chrome-automation pass once the browser extension is connected)
      to finish these 9.
      Added price_src column to cities.csv + a test enforcing every
      published city carries a real price source. Also found and fixed a
      real bug while doing this: city pages had a hardcoded "Honest
      downsides section — written by a human, per city, before publish"
      placeholder that would have shipped to real visitors on every
      published page. Added a dylan_note column (blank, human-only per
      CLAUDE.md) — the "Straight talk" section only renders once Dylan
      actually writes one; the "Full write-up coming" note now only shows
      on draft pages, not published ones.
- [x] Netlify: connect repo, build command `python3 build.py`, publish `dist/`,
      set `SITE_URL=https://gayretirees.com` env var — done 2026-08-30.
      Domain was already pointed at Netlify from a prior manual deploy.
- [x] Netlify Forms → Notifications → route relocation-intake + newsletter
      to dylanjlennon@gmail.com — done 2026-08-30. Switch to
      dylan@gayretirees.com once that mailbox is live.
- [ ] Stripe Payment Links for $29/$79/$149/$249 tiers + $19 founding rate
- [x] Analytics plumbing done: GA4 snippet on every page (build.py `GA_SNIPPET`),
      plus a shared `analytics.js` that fires GA4 events for every form
      submission (`data-ga-form`, sent via beacon so it survives the redirect
      to thanks.html) and every tracked click (`data-ga`/`data-ga-*` attrs) —
      phone CTA, agent email/phone links, agent card clicks, region filter,
      table sort. 12 dedicated tests in tests.py assert 100% page/form
      coverage. Still using placeholder ID `G-XXXXXXXXXX` (build.py `GA_ID`).
- [ ] Create the real GA4 property at analytics.google.com, then either
      hardcode the Measurement ID in build.py's `GA_ID` or set it as a
      `GA_MEASUREMENT_ID` Netlify env var (overrides the placeholder at
      build time) — until then no traffic is actually being recorded
