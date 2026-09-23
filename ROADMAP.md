# ROADMAP — GayRetirees.com to first dollar

Owner key: **[CLAUDE]** I execute this directly, no input needed. **[DYLAN]**
requires your credentials, money, or legal identity — I cannot do this even
with permission, because it requires logging into an account only you can
own (Google, Netlify, Stripe, a bank). **[CLAUDE+BROWSER]** I can drive it
in Chrome via browser automation, but only while you're logged in — I'll
ask you to open the tab and authenticate, then I take over the clicking.

Current state as of 2026-09-20: **the site is live at gayretirees.com**,
deploying automatically from `github.com/dylanjlennon/gayretirees.com-`
main branch (Netlify build `python3 build.py` → `dist`, `SITE_URL` env var
set). Homepage rearchitected around lifestyle-first browsing. Both forms
(`relocation-intake`, `newsletter`) are active and notify
dylanjlennon@gmail.com on submission. All 23 cities are `status=published`
(prices re-verified 2026-09-20 against Redfin/Zillow, with each row's
measure recorded in `price_metric`). Real GA4 property is live
(`G-HMVXKSHKN9`). Agent signup + profile forms exist. One real agent (Dylan,
Asheville, Unique: A Real Estate Collective); referral-fee model, no Stripe
needed (see Phase 4). `build.py` runs clean and `tests.py` is green
(114 checks). PRD 0001 (living city guide) is built and committed locally: sourced climate/airports/districts/ordinances, political climate, places/events/news, What-changed feed, 21 comparison pages. Pending: push to production, weekly rebuild hook, GA4 baseline, and a second sourcing pass on remaining VERIFY fields. Next PRDs: 0002 local agent voices, 0003 agent recruitment, 0004 measurement.

---

## Phase 1 — Data integrity (blocks flipping any page to published)

- [x] **[CLAUDE]** Real phone number sitewide (828-412-0678)
- [x] **[CLAUDE]** Delete EXAMPLE agent rows (jane-sample, mark-sample)
- [x] **[CLAUDE]** Asheville one_liner differentiated from GayAsheville.com
- [x] **License number confirmed 2026-09-23:** `NC323192` — live in `agents.csv`.
- [x] **Brokerage corrected 2026-09-23:** Dylan is with Unique: A Real Estate
      Collective, not Revel Real Estate (old placeholder) — live everywhere
      it renders, including the RealEstateAgent JSON-LD on the agent page.
- [~] **Email in progress (2026-09-23):** `dylan@gayretirees.com` was not a
      live mailbox (confirmed via DNS — no MX records existed). Cloudflare
      Email Routing is now set up: MX/TXT records added and locked, one
      routing rule (`dylan@gayretirees.com` → `dylanjlennon@gmail.com`) is
      Active. Waiting on Dylan to send a real test email and confirm it
      lands before flipping the `email` field in `agents.csv` off the
      placeholder.
- [x] Tier-1 verification pass — done 2026-08-30 for all 23 states + 23
      cities. 14 cities published with a real sourced price (`price_src`);
      9 (wilton-manors, st-pete, sarasota, key-west, savannah, rehoboth,
      new-hope, provincetown, ogunquit) were held as `draft` at the time.
      **Resolved:** all 23 were sourced and published 2026-09-04, and every
      price was re-pulled 2026-09-20 (Redfin pages via Chrome; Zillow via its
      public ZHVI research CSV, cross-checked against the Zillow city pages).
      That re-pull corrected wilton-manors (was 492118, Zillow shows 579530)
      and guerneville (was 567660, Zillow shows 518406).

## Phase 2 — Get it live (blocks anyone seeing the site)

- [x] **[DYLAN]** Created GitHub repo `dylanjlennon/gayretirees.com-`
      (2026-08-30); **[CLAUDE]** pushed `main`.
- [x] **[CLAUDE+BROWSER]** Netlify project `gayretirees` linked to the repo,
      build command `python3 build.py`, publish dir `dist`, `SITE_URL` env
      var set. Auto-publish on push to `main` is on.
- [x] `gayretirees.com` DNS already pointed at Netlify with a live Let's
      Encrypt cert (was done before this session — found already configured,
      site had a prior manual CLI deploy under the same Netlify project).

## Phase 3 — Get leads flowing (blocks the intake form doing anything)

- [x] **[CLAUDE+BROWSER]** Netlify Forms → Notifications → both
      `relocation-intake` and `newsletter` route to dylanjlennon@gmail.com
      on any submission. Form detection enabled + redeployed; dashboard
      confirms "2 forms collecting data."
- [ ] **[DYLAN]** or **[CLAUDE+BROWSER]** Sanity-check by actually submitting
      a test lead through the live site and confirming the email lands —
      not done yet, since submitting a form is a discrete action worth your
      go-ahead rather than assuming.
- [ ] **[DYLAN]** Once the test email in Phase 1 confirms delivery, decide
      whether to switch Netlify Forms notifications from the Gmail fallback
      to `dylan@gayretirees.com` — since that address now just forwards to
      the same Gmail inbox, this is optional, not blocking.

## Phase 4 — Get paid (blocks agent tiers being real products)

- [x] **Decision (2026-09-23):** pricing reconciled — the old $29/$79/$149/$249
      + $19-founding tier ladder here conflicted with AGENT-OUTREACH.md's
      actual pitch and was never implemented. Going with the simpler,
      already-tested model from AGENT-OUTREACH.md, informed by
      `tasks/research-gayrealestate-com-2026-09-20.md`'s competitive read:
      **free to list, 25% referral fee paid at closing, no subscription.**
      That undercuts GayRealEstate.com's free-tier rate (35%) and needs no
      payment processor — referral fees are paid broker-to-broker at
      closing, same as any other real estate referral.
- [x] No Stripe needed for this model — removed from the blocking path.
      Revisit only if/when a paid exclusive-city tier gets added later,
      once real per-city lead volume justifies asking agents for money
      up front (see the research note's option D).
- [ ] **[DYLAN]** Legal check (not legal advice, just a flag): confirm with
      your broker-in-charge at Unique: A Real Estate Collective that
      referral fees paid to you as the site operator, including across
      state lines, are fine under RESPA and state license law before any
      agent is actually charged one.

## Phase 5 — Know what's working

- [x] Real GA4 property created 2026-09-04; Measurement ID `G-HMVXKSHKN9` is
      the default `GA_ID` in `build.py` (overridable via `GA_MEASUREMENT_ID`).
      Event plumbing (`analytics.js`, `data-ga`/`data-ga-form` attrs, dedicated
      tests) is live.
- [ ] **[DYLAN]** Read GA4 and share numbers (or grant API access) so agent
      pitches (PRD 0003) use real traffic and lead counts only.

## Ongoing / not blocking launch

- [x] Agent signup flow exists (`agent-signup.html` → `agent-profile.html`).
      Approved agents are still added to `agents.csv` by hand.
- [x] Agent pricing inconsistency resolved 2026-09-23 — see Phase 4.
- [x] City `editorial_note` (renamed from `dylan_note`) may be drafted by Claude
      per `VOICE.md`; agent `blurb`/`testimonial` stay human-only.

## Phase 6 — Finish the data foundation

- [ ] **[CLAUDE, blocked on a working Redfin/Zillow pull]** 3 cities stuck in
      `draft` (`orlando`, `portland-me`, `charleston`) — same automated-fetch
      blocking that held up 9 cities before. Each is dead SEO weight as a
      draft page; needs a manual price pull per city to flip to `published`.
- [ ] **[CLAUDE]** Freshness pass: `tests.py` currently WARNs on 5
      political rows past 180 days (austin, charleston, raleigh-durham,
      rehoboth, savannah) and 10 cities' newest news item past 90 days
      (albuquerque, austin, charleston, eureka-springs, orlando, phoenix,
      portland, sarasota, saugatuck, st-pete). Not broken, but worth a
      recurring re-check so "as of" dates don't quietly go stale.
- [ ] **[CLAUDE, needs source research]** `PERSONA.md` names two real gaps in
      the buyer-archetype data that's otherwise fully sourced-and-dated
      everywhere else on the site: no "family-adjacent" axis (flight access
      to kids/chosen family) and no trans-specific healthcare-access rating
      (only `hiv_care` exists today). Both fit the site's existing
      sourced-CSV-column pattern and would differentiate from every generic
      retirement site — this is exactly the kind of depth GayRealEstate.com
      doesn't have (see the research note's "gaps we can win on").

## Phase 7 — Turn the lookup tool into a matching experience

- [ ] **[CLAUDE, needs Dylan's sign-off on scope]** A short multi-question
      wizard (budget range → non-negotiable protections → climate
      tolerance → walkability) that outputs a ranked 2-3 city shortlist and
      captures an email *in exchange for the shortlist* — this fixes the
      newsletter form's current "asks for an email, gives nothing back"
      problem, which `PERSONA.md` itself flags as a trust-breaker. Feeds the
      connect.html form with pre-filled context, shortening the funnel.
- [ ] **[CLAUDE]** An affordability calculator using data already in the
      CSVs (state income tax, SS exemption, property price): "moving from
      [your state] to Asheville saves ~$X/year in state tax on a $60K
      retirement income." A concrete personal number is stickier than a
      static comparison table.

## Phase 8 — Trust, legal, and roster diversity

- [ ] **[DYLAN]** Confirm with your broker-in-charge (Phase 4) — this is the
      same legal check, listed here too since it blocks recruiting agent #2.
- [ ] **[DYLAN]** `PERSONA.md`'s own open question: current agent roster and
      testimonial copy skews toward gay men. Worth addressing directly as
      you recruit agents 2+, both in who you approach and in a copy review
      so the site reads as welcoming across the LGBTQ+ spectrum, not just
      to the demographic of the one agent listed so far.

## Phase 9 — Analytics-driven growth loop

- [ ] **[DYLAN]** Read GA4 and share numbers, or grant API access (this is
      also Phase 5's blocking ask — repeated here because everything below
      depends on it).
- [ ] **[CLAUDE, once GA4 access exists]** Set up conversion funnels (vibe
      card → city page → connect form) to see actual drop-off points
      instead of guessing.
- [ ] **[CLAUDE, once GA4 access exists]** Use `data-ga` event data (already
      instrumented sitewide) to see which vibe cards/filters get used most —
      that's the signal for which of the 3 draft cities, or which new city
      entirely, to prioritize sourcing next.
- [ ] **[DYLAN+CLAUDE]** Once there's real traffic data, recruit agents 2
      through ~5 using actual per-city numbers as the pitch, per
      `AGENT-OUTREACH.md`.

## Phase 10 — Technical hardening

- [x] **Regression test added 2026-09-23** (`tests.py`): asserts the mobile
      column-hiding CSS rule stays scoped to `#mx` and never regresses to a
      bare `table` selector — this is the exact bug fixed earlier today
      (it had silently hidden the governor/mayor name on every city's
      political-climate table, three columns on states.html, and an entire
      city's data on every compare/*.html page, on any screen under 760px).
- [ ] **[CLAUDE]** A basic Lighthouse/accessibility pass now that the site
      has real traffic potential — check color contrast, ARIA labeling on
      the vibe-card filters, and keyboard navigation, per `PERSONA.md`'s
      "click targets sized generously" and "150-200% zoom" requirements.

## Phase 11 — SEO & content moat

- [ ] **[CLAUDE]** Once Phase 6's 3 draft cities publish, expand comparison
      page coverage (`compare/*.html`) to include them — each comparison
      page is its own indexable long-tail search result.
- [ ] **[DYLAN]** Backlinks from LGBTQ+ aging/retirement orgs (SAGE, HRC,
      local Pride organizations already cited as sources on city pages) —
      worth reaching out once there's a second published agent to point to
      as proof the directory is real, not a one-person side project.

---

**Immediate ask:** send a test email to `dylan@gayretirees.com` to confirm
the new Cloudflare routing works (Phase 1); read/share GA4 numbers (Phases
5 and 9); and a decision on the remaining 3 unpriced draft cities (Phase 6).
