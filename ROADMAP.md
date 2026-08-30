# ROADMAP — GayRetirees.com to first dollar

Owner key: **[CLAUDE]** I execute this directly, no input needed. **[DYLAN]**
requires your credentials, money, or legal identity — I cannot do this even
with permission, because it requires logging into an account only you can
own (Google, Netlify, Stripe, a bank). **[CLAUDE+BROWSER]** I can drive it
in Chrome via browser automation, but only while you're logged in — I'll
ask you to open the tab and authenticate, then I take over the clicking.

Current state as of 2026-08-30: 23 city pages + 23 state rows, all
`status=draft` (DRAFT stamp renders sitewide). One real agent (Dylan,
Asheville). No git remote, no Netlify site, no live GA4 property, no
Stripe. `build.py` runs clean, `tests.py` is green (39/39).

---

## Phase 1 — Data integrity (blocks flipping any page to published)

- [x] **[CLAUDE]** Real phone number sitewide (828-412-0678)
- [x] **[CLAUDE]** Delete EXAMPLE agent rows (jane-sample, mark-sample)
- [x] **[CLAUDE]** Asheville one_liner differentiated from GayAsheville.com
- [ ] **[DYLAN]** Confirm: is `dylan@gayretirees.com` a live mailbox yet, or
      should the site show a different working email for now?
- [ ] **[DYLAN]** Dylan's NC real estate license number (`agents.csv`,
      currently `NC-REPLACE`) — this is a legal identifier, I won't guess it.
- [ ] **[CLAUDE]** Tier-1 verification pass: for each of the 23 states, check
      `housing_law` / `pa_law` / `ltc_protections` / `income_tax` /
      `ss_taxed` / `estate_inheritance_tax` against a citable source
      (lgbtmap.org for LGBTQ+ legal fields, state DOR pages for tax), record
      `law_src` + `law_asof`. For each of the 23 cities, check
      `median_price_usd` against Redfin/Zillow, record `price_asof`. Flip
      `status: draft → published` only for rows that come out fully sourced.
      This is the single biggest blocker to the site saying anything with
      confidence — starting once you confirm scope below.

## Phase 2 — Get it live (blocks anyone seeing the site)

- [ ] **[DYLAN]** Create a GitHub repo, give me the remote URL (or push
      access) — right now this repo has no remote at all, it's local-only.
- [ ] **[DYLAN]** or **[CLAUDE+BROWSER]** Netlify: connect the repo, build
      command `python3 build.py`, publish dir `dist`, set env var
      `SITE_URL=https://gayretirees.com`. I can drive this in Chrome if
      you'd rather watch than click.
- [ ] **[DYLAN]** Point the `gayretirees.com` domain's DNS at Netlify
      (registrar login required — that's you).

## Phase 3 — Get leads flowing (blocks the intake form doing anything)

- [ ] **[DYLAN]** Netlify Forms → Notifications → route `relocation-intake`
      and `newsletter` submissions to a real inbox.
- [ ] **[CLAUDE]** Sanity-check the notification routing once it's live
      (submit a test lead, confirm it lands).

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
number), and a scope decision on the verification pass (all 23
states/cities, or a smaller flagship set first — I'd suggest flagship
first so we can publish something real sooner rather than boiling the
ocean).
