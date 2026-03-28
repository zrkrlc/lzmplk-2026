# lzmplk-2026 — State

[CHECKPOINT] 2026-03-28 13:20

## Intention
> Birthday gift for girlfriend (2026-03-28). Single polished text adventure (Maid Latte / Maid-Sama! theme) with Tiny Glade Steam key as prize. Text adventure IS the primary vehicle of the surprise.

## Position
> **READY TO DEPLOY.** Game renamed to cafe.html, all mechanics complete, exhaustive diagrams generated. Escape mechanic added (CATCH trapped mascot without apron = escapes). Progressive disclosure gates all work. Links updated.

| Component | Status | Notes |
|-----------|--------|-------|
| Game engine | **Done** | Renamed puzzle2→cafe.html |
| Visual style | **Done** | Early 2000s Manila blog aesthetic |
| Progressive disclosure | **Done** | LOOK AROUND → hints unlock |
| NPC dialogue tiering | **Done** | Satsuki/Usui: no hints at tier 1 |
| Interactable styling | **Done** | Cutive Mono, uppercase, gold |
| Win state | **Done** | BOWL trap → APRON catch → prize.html |
| Escape mechanic | **Done** | CATCH trapped w/o apron = escapes + hint |
| Main page | **Done** | index.html → cafe.html |
| Prize page | **Needs content** | Placeholders for Steam key + message |
| Game diagrams | **Done** | 3 area diagrams + combined game-map.html |
| TRY hints | Needs refactor | Too cluttered (defer post-deploy) |

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
- **Flow: index → cafe → prize** →✓ renamed from puzzle2
- **Escape mechanic** →✓ CATCH trapped mascot w/o apron = squirts out + thick fabric hint
- **Gate knife/cabinet/drawer** →✓ all require kitchenLooked first
- **Trapped mascot text** →✓ room desc + LOOK MASCOT show betrayed eyes

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
- All paths relative (deploy to perseidpixels.co/lzmplk/) ✓

## Files Modified
- `src/cafe.html` — renamed from puzzle2.html, escape mechanic, gates, trapped text
- `src/index.html` — links to cafe.html
- `src/prize.html` — fixed play again link
- `src/game-tree.html` — fixed back link
- `src/command-map.html` — fixed back link
- `src/game-map.html` — NEW: combined interaction diagrams
- `src/diagrams/` — NEW: dining/counter/kitchen exhaustive diagrams
- `STATE.md` — this file

## Next
- [ ] **Fill in prize.html** — Steam key, personal message
- [ ] **Deploy** — git push to perseidpixels.co/lzmplk/
- [ ] (post-deploy) Refactor TRY hints — too cluttered
- [ ] (post-deploy) Easter egg discoverability — subtle NPC hints or post-win reveal

## Pickup
**Ready to deploy.** Game at cafe.html (renamed from puzzle2). All mechanics work: progressive disclosure, escape mechanic (CATCH trapped w/o apron = escapes), gates (knife/cabinet/drawer behind kitchenLooked). Exhaustive diagrams at src/diagrams/ and combined game-map.html. **Remaining:** fill prize.html placeholders (Steam key + message), then git push.

---
