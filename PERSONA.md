# Who we're building for

Living document. This drives UI/copy decisions sitewide — when a design choice is in
question, check it against this first. Refine it as we learn more; don't let it go stale.

## Primary persona

LGBTQ+, 55–75, seriously considering (not just daydreaming about) where to retire.
Financially comfortable enough to relocate — home equity, pension, Social Security — but
budget-conscious, not wealthy. Many lived through real discrimination earlier in life
(employment, housing, healthcare, family rejection); legal protections on this site aren't
abstract policy trivia to them, they're personal history repeating or not repeating.

Some are newly out or newly comfortable being visibly out, and this may be the first major
life decision they're making as an openly LGBTQ+ person. Others have been out for decades
and are specifically screening for LGBTQ+-safe, not just LGBTQ+-tolerant, places to age.

Not assumed to be tech-savvy. Time-rich (retired or near it) but not necessarily comfortable
with modern web patterns — hover states, infinite scroll, multi-step JS flows. Design for
someone using a laptop trackpad or an iPad, at a larger-than-default zoom level, who has not
memorized "the menu is the hamburger icon."

## What breaks trust immediately

- Small text, low contrast, cramped click targets
- Parallax, autoplay video, scroll-triggered animation — reads as gimmicky, not trustworthy,
  and can be genuinely disorienting (vestibular issues are more common in this age range)
- Anything that feels like it's hiding a catch — unclear who they're actually talking to,
  vague "trust us" copy, fees that surface late
- A form that asks a lot before giving anything back

## What builds trust

- Every fact sourced and dated (already a site principle — keep it)
- A real name, a real phone number, a real face (Dylan's presence on the site matters more
  here than on a typical startup)
- One obvious next action per page — never competing CTAs of equal visual weight
- Copy that names the real fear directly ("will I be safe here," "will my spouse be
  recognized at the hospital") instead of gesturing around it

## Design requirements this implies

1. Body text stays large and high-contrast; nothing shrinks below current baseline
2. Every core fact — city snapshot, price, laws, "talk to an agent" — reachable in 1–2 clicks
   from the homepage, no exceptions
3. "Contact an agent" is the single most visually dominant action on any page it appears on
4. No parallax, no scroll-triggered motion, no autoplay
5. Layout has to hold together at 150–200% browser zoom, not just on a designer's laptop
6. Click/tap targets sized generously — err toward "too big" over "too clever"

## Buyer archetypes (how the primary persona splits by priority)

- **Stretch-the-pension** — income tax and price above all else
- **Chasing-the-scene** — will pay a premium for walkable density (Provincetown, Wilton Manors)
- **Safety-first** — explicit legal protections are non-negotiable regardless of price or vibe
- **Family-adjacent** — flight access to kids/chosen family beats any lifestyle lane (currently
  no data supports this axis — flagged in ROADMAP as a gap)
- **Health-first** — named competent care access decides everything (partially covered via
  `hiv_care`, not trans-specific — also a flagged gap)

## Open questions — refine together, don't guess at these alone

- [ ] Single or partnered as the default assumed reader? Changes copy ("you and your spouse"
      vs. "you").
- [ ] Current agent roster and testimonial copy skews toward gay men — is that just where the
      first agents happen to be, or should copy be written more broadly across the LGBTQ+
      spectrum from day one regardless of who's currently listed?
- [ ] How tech-savvy is a fair assumption, really? Affects how much we lean on JS-driven
      filtering vs. plain links people can right-click/bookmark.
