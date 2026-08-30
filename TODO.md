# Launch Checklist

In order:

- [ ] Replace placeholder phone `tel:+18285550100` sitewide (build.py header CTA
      + agents.csv) with real OpenPhone/GVoice number
- [ ] Replace REPLACE-tagged emails and license in agents.csv (Dylan's row)
- [ ] Delete the two EXAMPLE agent rows (jane-sample, mark-sample)
- [ ] DECISION (confirm with Dylan first): remove the 20 `*-to-asheville` rows
      from routes.csv — they're slated to live on GayAsheville.com instead;
      keep the 3 original routes
- [ ] Tier 1 verification pass: states.csv legal fields vs lgbtmap.org,
      cities.csv prices vs Redfin/Zillow; bump as-of dates; flip verified
      flagship cities to status=published
- [ ] Netlify: connect repo, build command `python3 build.py`, publish `dist/`,
      set `SITE_URL=https://gayretirees.com` env var, point domain
- [ ] Netlify Forms → Notifications → route relocation-intake + newsletter
      to Dylan's email
- [ ] Stripe Payment Links for $29/$79/$149/$249 tiers + $19 founding rate
- [ ] Analytics (Plausible or GA4) snippet in build.py page template
