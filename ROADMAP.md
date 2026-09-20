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
Asheville); no Stripe yet. `build.py` runs clean and `tests.py` is green
(81 checks). Next: `tasks/0001-prd-living-city-guide.md` (living city guide).

---

## Phase 1 — Data integrity (blocks flipping any page to published)

- [x] **[CLAUDE]** Real phone number sitewide (828-412-0678)
- [x] **[CLAUDE]** Delete EXAMPLE agent rows (jane-sample, mark-sample)
- [x] **[CLAUDE]** Asheville one_liner differentiated from GayAsheville.com
- [ ] **[DYLAN]** Confirm: is `dylan@gayretirees.com` a live mailbox yet, or
      should the site show a different working email for now?
- [ ] **[DYLAN]** Dylan's NC real estate license number (`agents.csv`,
      currently `NC-REPLACE`) — this is a legal identifier, I won't guess it.
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
- [ ] **[DYLAN]** Once `dylan@gayretirees.com` is a live mailbox (see Phase 1),
      switch the notification email from the Gmail fallback to that address.

## Phase 4 — Get paid (blocks agent tiers being real products)

- [ ] **[DYLAN]** Stripe account + bank details (identity/banking — has to
      be you).
- [ ] **[DYLAN]** or **[CLAUDE+BROWSER]** Stripe Payment Links for the
      $29/$79/$149/$249 tiers + $19 founding rate, once the account exists.
- [ ] **[CLAUDE]** Wire the payment links into the agent-tier pages once
      they exist.

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
- [ ] Agent pricing is inconsistent between `AGENT-OUTREACH.md` and this file —
      resolve in PRD 0003 (see `tasks/research-gayrealestate-com-2026-09-20.md`).
- [x] City `editorial_note` (renamed from `dylan_note`) may be drafted by Claude
      per `VOICE.md`; agent `blurb`/`testimonial` stay human-only.

---

**Immediate ask:** two answers to unblock Phase 1 (email status, license
number); a decision on the remaining 9 unpriced cities; and whether to
submit a test lead through the live form to confirm the notification
email actually lands.
