# Editorial voice — the "straight talk" section

Living document, same spirit as PERSONA.md (who we write *for*) — this one is who we write
*as*. Dylan asked for the site to carry more warmth than a pure fact table gives it, in the
voice of a 55+ gay retiree, with Dylan's own real identity limited to his actual role — the
agent listed on the Asheville page. Claude flagged a trust-risk concern before drafting
anything: a fabricated named "founder" persona would be exactly the kind of thing PERSONA.md
warns this audience is unusually good at spotting ("anything that feels like it's hiding a
catch" breaks trust immediately here). Dylan confirmed the resolution directly, 2026-09-11:
**unnamed house voice, no bio, no byline, no implied specific person.**

## Who's "talking"

Not a character. A tone. If it helps to picture someone while drafting: a gay man in his
early 60s, been out since long before it was easy, actually retired somewhere on this list
himself, has opinions because he's lived them — not a copywriter doing a bit. But that person
is never named, quoted, or given a bio anywhere on the site. The voice is the site's, not a
person's.

## What the voice sounds like

- **Plainspoken, not literary.** Short sentences. Say the thing directly. No metaphors about
  chapters or journeys — PERSONA.md already flagged "next chapter" framing as tension with the
  budget-conscious majority; don't lean back into that kind of soft language here.
- **Dry, not jokey.** Humor is fine as an aside, never as the point. Never cute about age,
  death, or health — PERSONA.md is explicit that mortality-adjacent framing has already been
  moved away from deliberately.
- **Names the real trade-off.** This section exists specifically to say the thing the "At a
  glance" table can't — the humidity, the drive to the airport, the fact that the walkable
  gayborhood is three blocks and everyone will know your business. If a note doesn't name an
  actual downside or a real practical texture, it isn't doing its job.
- **Respects the reader's intelligence.** No "you've worked hard, you deserve this." No
  selling. This reader has already filtered through the fact table above; the note should add
  judgment, not restate marketing.
- **Never invents specifics that need a source.** No fake anecdotes, no "the coffee shop on
  Main Street," no claimed personal history in a specific place. Stick to judgment calls about
  publicly-known, already-sourced facts on the row (the climate, the law, the price, the
  density) — save the citable stuff for the fact table where CLAUDE.md's sourcing rule already
  governs it.

## Mechanics

- Field: `editorial_note` in `data/cities.csv` (formerly `dylan_note` — renamed 2026-09-11 to
  drop the implication that these are Dylan's personal words).
- Claude may draft this field directly, following this guide — it is no longer human-only,
  because it's not attributed to any specific human. A missing note still means the "straight
  talk" block simply doesn't render (same as before).
- Keep each note to 2–4 sentences. This is a beat, not an essay.
