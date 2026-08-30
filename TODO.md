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
- [ ] Tier 1 verification pass: states.csv legal fields vs lgbtmap.org,
      cities.csv prices vs Redfin/Zillow; bump as-of dates; flip verified
      flagship cities to status=published
- [ ] Netlify: connect repo, build command `python3 build.py`, publish `dist/`,
      set `SITE_URL=https://gayretirees.com` env var, point domain
- [ ] Netlify Forms → Notifications → route relocation-intake + newsletter
      to Dylan's email
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
