# lzmplk-2026 — State

[CHECKPOINT] 2026-03-28 11:45

## Intention
> Birthday gift for girlfriend (2026-03-28). Single polished text adventure (Maid Latte / Maid-Sama! theme) with Tiny Glade Steam key as prize. Text adventure IS the primary vehicle of the surprise.

## Position
> **PLAYABLE + DISCOVERABLE.** Progressive disclosure system complete. LOOK AROUND reveals room contents, hints appear after exploring. NPC dialogue tiered (no spoilers early). All interactables styled distinctly. 185 states, 0 dead ends.

| Component | Status | Notes |
|-----------|--------|-------|
| Game engine | **Done** | 185 states, 0 dead ends |
| Visual style | **Done** | Early 2000s Manila blog aesthetic |
| Progressive disclosure | **Done** | LOOK AROUND → hints unlock |
| NPC dialogue tiering | **Done** | Satsuki/Usui: no hints at tier 1 |
| Interactable styling | **Done** | Cutive Mono, uppercase, gold |
| Win state | **Done** | Links to prize.html |
| Main page | **Done** | Simple intro → game link |
| Prize page | **Done** | Steam key + message placeholders |
| TRY hints | Needs refactor | Too cluttered after LOOK AROUND |

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
- [x] Progressive disclosure — LOOK AROUND reveals objects, hints unlock after
- [x] NPC dialogue tiering — no spoilers at tier 1, vague at tier 2, explicit at tier 3
- [x] Interactable styling — Cutive Mono, uppercase, gold (#8b6914)
- [ ] **Refactor TRY hints** — too cluttered after LOOK AROUND (7+ hints showing)
- [ ] Fill in prize.html placeholders (Steam key, personal message, photo?)
- [ ] Deploy

## Pickup
**Game is playable + discoverable.** Progressive disclosure: LOOK AROUND reveals room objects (styled in Cutive Mono uppercase gold), then TRY hints unlock. NPC dialogue tiered: Satsuki/Usui give no hints at tier 1, vague at tier 2, explicit at tier 3. Plushie now has blond hair like Usui ("perverted outer-space alien" reference). **Issue:** TRY hints too cluttered after exploring (7+ items). Consider: showing only 3-4 most relevant hints, or collapsible hint categories.

## Art Sources (for post-compaction)
- **Itsu cafe pack** — CC-licensed VN maid cafe backgrounds
- **Spiral Atlas house backgrounds** — CC-licensed VN interiors
- Convert via **asc11** or similar ASCII art tool

---
