# ROADMAP — GayRetirees.com to first dollar

Owner key: **[CLAUDE]** I execute this directly, no input needed. **[DYLAN]**
requires your credentials, money, or legal identity — I cannot do this even
with permission, because it requires logging into an account only you can
own (Google, Netlify, Stripe, a bank). **[CLAUDE+BROWSER]** I can drive it
in Chrome via browser automation, but only while you're logged in — I'll
ask you to open the tab and authenticate, then I take over the clicking.

Current state as of 2026-08-30: **the site is live at gayretirees.com**,
deploying automatically from `github.com/dylanjlennon/gayretirees.com-`
main branch (Netlify build `python3 build.py` → `dist`, `SITE_URL` env var
set). Homepage rearchitected around lifestyle-first browsing. Both forms
(`relocation-intake`, `newsletter`) are active and notify
dylanjlennon@gmail.com on submission. 14 of 23 cities `status=published`,
9 still `draft` pending a manual price pull. One real agent (Dylan,
Asheville). No live GA4 property yet, no Stripe. `build.py` runs clean,
`tests.py` is green (52/52).

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
      cities. 14 cities now `status=published` with a real sourced price
      (`price_src`). 9 cities (wilton-manors, st-pete, sarasota, key-west,
      savannah, rehoboth, new-hope, provincetown, ogunquit) stay `draft` —
      Redfin/Zillow blocked automated fetches and search-snippet prices for
      those specific markets were too inconsistent to trust. **[DYLAN]** or
      **[CLAUDE+BROWSER]**: needs a manual price pull for those 9 (5 min
      each on Redfin/Zillow directly), or I can do it via Chrome automation
      once the extension is connected.

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

- [ ] **[DYLAN]** or **[CLAUDE+BROWSER]** Create the real GA4 property at
      analytics.google.com. I can navigate and click through this in Chrome
      if you're logged into the right Google account — say the word.
- [ ] **[CLAUDE]** Drop the real Measurement ID into `build.py`'s `GA_ID`
      (or wire `GA_MEASUREMENT_ID` as a Netlify env var), rebuild — event
      plumbing (`analytics.js`, all `data-ga`/`data-ga-form` attrs, 12
      dedicated tests) is already built and waiting for a real ID.

## Ongoing / not blocking launch

- [ ] Agent signup flow doesn't exist yet — today, onboarding a new agent
      means manually adding a row to `agents.csv`. Worth a real form once
      there's more than one paying agent.
- [ ] `dylan_note` fields are human-only per CLAUDE.md — I will never draft
      these, that's you whenever you want a page to carry your own voice.

---

**Immediate ask:** two answers to unblock Phase 1 (email status, license
number); a decision on the remaining 9 unpriced cities; and whether to
submit a test lead through the live form to confirm the notification
email actually lands.
