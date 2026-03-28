# lzmplk-2026 — State

[CHECKPOINT] 2026-03-28 01:30

## Intention
> Birthday gift for girlfriend (2026-03-28). Single polished text adventure (Maid Latte / Maid-Sama! theme) with Tiny Glade Steam key as prize. Text adventure IS the primary vehicle of the surprise.

## Position
> **PLAYABLE.** Main flow complete: index → game → win → prize. Staticrypt removed (URL is the secret). Prose deslopified (34 fixes). Canon fixed (Usui = customer). Next: ASCII art for room backgrounds.

| Component | Status | Notes |
|-----------|--------|-------|
| Game engine | **Done** | 70 states, 0 dead ends |
| Visual style | **Done** | Early 2000s Manila blog aesthetic |
| ASCII maps | **Done** | Aligned, emoji-free, box-drawing chars |
| Flavortext | **Done** | Deslopify (34 fixes) + canon (Usui) complete |
| Win state | **Done** | Links to prize.html |
| Main page | **Done** | Simple intro → game link |
| Prize page | **Done** | Steam key + message placeholders |
| ASCII backgrounds | Optional | VN art → ASCII conversion if time |

## Decisions
- Puzzle 2 theme: Maid-Sama! (not H2G2) →✓ she loves the anime
- Password mechanism: item inside mascot (not NPC speech) →✓ clearer, more satisfying
- Password: "misakitchen" →✓ thematic (but no longer shown — win links to prize)
- NPCs with interiority: Usui talks about England, Satsuki about why she opened cafe →✓ world feels alive
- Ambient commands: LISTEN, SMELL, THINK, WAIT →✓ exploration rewarded
- **PIVOT: Single game (not 3-puzzle ARG)** →✓ reduces scope, increases polish
- **Visual style: Early 2000s Manila blog** →✓ light bg, dusty rose (#d4a5a5), dashed borders
- **Fonts: Pacifico + Silkscreen + Comic Neue** →✓ adventurous, era-appropriate
- **Usui is customer, not employee** →✓ canon-conformance agent fixed
- **Staticrypt: REMOVED** →✓ URL is the secret, no password gate
- **Flow: index → puzzle2 → prize** →✓ text adventure is primary vehicle

## Dead Ends
- H2G2 theme: she doesn't know it well, switched to Maid-Sama!
- beautiful-mermaid: not installed, used handcrafted ASCII for game tree
- 3-puzzle ARG: too much scope for deadline, pivoted to single polished game
- Hand-drawn wireframes: too crude
- VN-style ASCII backgrounds: dropped for deadline, ASCII maps work fine
- Dark terminal aesthetic: switched to light early-2000s blog style
- Emoji in ASCII art: breaks alignment, replaced with ASCII chars

## Constraints
- Deadline: 2026-03-28 (TODAY - birthday)
- Canon accuracy for Maid-Sama! (Usui = customer, not employee) ✓

## Files Modified
- `src/index.html` — simplified intro, links to puzzle2
- `src/puzzle2.html` — text adventure (restyled, deslopified, canon-fixed, win→prize)
- `src/prize.html` — Steam key + message placeholders
- `STATE.md` — this file

## Next
- [x] Fix mascot hint system — tier 1 hints now work in all rooms (COUNTER, KITCHEN), not just DINING
- [x] Add variety to hiding spots — 11 spots across 3 rooms (was 5)
- [ ] Optional: ASCII art backgrounds (VN assets → asc11 conversion)
- [ ] Fill in prize.html placeholders (Steam key, personal message, photo?)
- [ ] Deploy

## Pickup
**Game is playable.** Flow: index.html → puzzle2.html → prize.html. Mascot now hides in 11 different spots across all 3 rooms (tables, fern, menu board, espresso machine, display case, tip jar, bowls, apron pile, treat cabinet). Tier 1 hints are now consistently vague ("something rustles...") in all rooms. Fill in prize.html placeholders before gifting.

## Art Sources (for post-compaction)
- **Itsu cafe pack** — CC-licensed VN maid cafe backgrounds
- **Spiral Atlas house backgrounds** — CC-licensed VN interiors
- Convert via **asc11** or similar ASCII art tool

---
