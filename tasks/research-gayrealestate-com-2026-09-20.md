# Research note — GayRealEstate.com (competitor / model reference)

As of 2026-09-20. Sources fetched via WebFetch (page text summarized by a small model) and
WebSearch snippets — **eyeball the primary pages before quoting any figure externally.** No
business plan document was found; this note reconstructs their public model only.

## What they do

- Consumer side: connects LGBTQ+ buyers/sellers with agents; city guides, relocation guides
  (US + Canada), downloadable ebook, lender resources, "100% confidential" contact flow.
  Source: https://www.gayrealestate.com/
- Claims (self-reported, unverified): "30+ years", "$2b+ in sales supported",
  "55,000+ transactions"; lists big-brokerage partnerships. Agent count / city count not stated.
- State page sample (California, 9 agents): plain agent cards, alphabetical order, "Contact"
  button, no dates, no local laws/events/bars on the page, boilerplate bios, footer "© 2026".
  Source: https://www.gayrealestate.com/usa/california/gay-realtors.html

## Agent terms

Source: https://www.gayrealestate.com/gay-realtors-join.html (+ search snippet)

| Option | Cost to agent | Referral fee |
|---|---|---|
| Free profile | $0 upfront, pay only on closed deals | **35%** |
| Subscription | monthly fee (snippet: "based on your city's population") | **25%** |

- Fee is calculated on the HUD-1/CD commission total paid to the agent's brokerage, before
  splits/fees; the 25% rate also applies to bonuses.
- Subscriptions auto-renew every **6 months** on a card; cancel by email 30 days before
  renewal; **no refunds**, full or partial.
- Dollar amounts were NOT on the join page. A search snippet said ~$249/yr adds up to 6
  extra cities + a mini banner — **unverified**.
- Separate domain https://www.gayrealestateagents.com/agent-join shows flat annual profiles:
  $99/yr (primary city) and $129/yr (multi-city, rotates in top results), no referral fee
  mentioned. Affiliation with GayRealEstate.com unconfirmed.

## Gaps we can win on (from their public pages)

1. Undated, boilerplate city content → our sourced + dated + "what changed" pages.
2. Alphabetical agent order, no local voice → attributed local agent voices, city-specific.
3. Punitive terms (6-month auto-renew, no refunds) → month-to-month, cancel anytime.
4. Free tier at 35% is steep → a lower referral fee for founding partners.

## Pricing options for our agent side (decision needed before PRD 0003)

- **A. Free listing, referral-only (recommended start).** Zero risk for the agent; fits where
  we are (1 real lead to date, so nothing to sell yet). Suggest 25% for founding partners —
  it is the number the outreach template already uses and undercuts their 35% free tier.
- **B. Subscription + reduced referral (add later, as the upgrade).** Once we can show
  real per-city lead counts. Mirrors their 35→25 structure.
- **C. Subscription, no referral.** Simple, and a flat advertising fee is the cleanest fit
  for the "placement is sold" boundary in CLAUDE.md — but it forfeits all upside on closings
  (illustration: 3% commission on a $400K sale = $12,000; a 25% referral = $3,000 vs. a
  $100–$300 subscription) and gives us no reason to track outcomes.
- **D. High-ticket exclusive city seat** ("top agent for [CITY]"). Only credible after
  demand is proven in that city; selling exclusivity on an unproven page overreaches.

Existing docs conflict and must be reconciled: AGENT-OUTREACH.md (free 25% / exclusive $29/mo +
15%) vs ROADMAP.md ($29/$79/$149/$249 + $19 founding).

**Legal check needed (not legal advice):** referral fees paid to a non-agent site operator,
and across state lines, can be restricted (RESPA / state license law). Confirm with your
brokerage/broker-in-charge before any agent is charged a per-closing fee.
