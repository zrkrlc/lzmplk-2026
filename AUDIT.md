# Game Audit Report — puzzle2.html (AFTER CLASS)

Audited: 2026-03-28
Auditor: claude-opus-4-6

---

## Summary

| Metric                  | Count |
|-------------------------|-------|
| Total entities          | 38    |
| Reachable (LOOK + interact) | 33 |
| Partially reachable     | 3     |
| Unreachable             | 2     |
| Contradictions found    | 3     |
| Disclosure violations   | 2     |
| Hint gaps               | 1     |

---

## A) Entity Reachability

### Rooms

| Entity | Mentioned In | LOOK? | Interact? | Notes |
|--------|-------------|-------|-----------|-------|
| DINING | Room desc, movement | Yes (room) | GO DINING | OK |
| COUNTER | Room desc, movement | Yes (room) | GO COUNTER | OK |
| KITCHEN | Room desc, movement | Yes (room) | GO KITCHEN | OK |
| ALLEY | Kitchen room desc ("Back door: ALLEY") | No | GO ALLEY (refused) | OK - intentional fake exit |

### NPCs

| Entity | Mentioned In | LOOK? | TALK? | Notes |
|--------|-------------|-------|-------|-------|
| Usui | Counter desc, dialogue | Yes (LOOK USUI) | Yes (TALK USUI, COUNTER only) | OK - rich interaction |
| Satsuki | Kitchen desc, dialogue | Yes (LOOK SATSUKI) | Yes (TALK SATSUKI, KITCHEN only) | OK - rich interaction |
| Customers (generic) | Dining LOOK AROUND | Yes (LOOK CUSTOMER) | Yes (TALK CUSTOMER) | OK |
| Customer at Table 3 (Aoi) | Dining LOOK AROUND, Satsuki dialogue | Yes (LOOK CUSTOMER 3) | Yes (TALK CUSTOMER 3) | OK - mysterious persona |
| Uchujin-kun (mascot) | All rooms (when present) | Yes (LOOK MASCOT) | Yes (TALK MASCOT) | OK |

### Items (Takeable)

| Entity | Mentioned In | LOOK? | TAKE? | USE? | Notes |
|--------|-------------|-------|-------|------|-------|
| Apron | Counter LOOK AROUND, room desc when revealed | Yes (LOOK APRON) | Yes (TAKE APRON) | Yes (USE APRON) | OK - key puzzle item |
| Bowl | Cabinet (after OPEN) | Yes (LOOK BOWL) | Yes (TAKE BOWL) | Yes (USE BOWL) | OK - key puzzle item |
| Knife | Kitchen room desc (always visible) | No dedicated handler | Yes (TAKE KNIFE) | Yes (USE KNIFE) | OK - red herring |
| Garbage bag | Drawer (after OPEN) | Yes (LOOK DRAWER shows it) | Yes (TAKE BAG) | Yes (USE BAG) | OK - red herring |
| Treats/snacks | Cabinet (after OPEN) | Yes (LOOK TREAT) | Yes (TAKE TREAT) | Yes (USE TREAT) | OK - red herring |

### Scenery (Non-takeable)

| Entity | Mentioned In | LOOK? | Other Interaction? | Status |
|--------|-------------|-------|--------------------|--------|
| Table 1 | Dining LOOK AROUND | Yes (LOOK TABLE 1) | GO TABLE (blocked) | OK |
| Table 2 | Dining LOOK AROUND | Yes (LOOK TABLE 2) | GO TABLE (blocked) | OK |
| Table 3 | Dining LOOK AROUND | Yes (LOOK TABLE 3) | GO TABLE (blocked) | OK |
| Fern | Dining LOOK AROUND | Yes (LOOK FERN) | No | OK - mascot hiding spot |
| Specials board | Dining LOOK AROUND | Yes (LOOK MENU/SPECIALS/BOARD) | No | OK - mascot hiding spot |
| Espresso machine | Counter LOOK AROUND | Yes (LOOK ESPRESSO) | No | OK - mascot hiding spot |
| Display case | Counter LOOK AROUND | Yes (LOOK DISPLAY) | No | OK - mascot hiding spot |
| Tip jar | Counter LOOK AROUND | Yes (LOOK TIP) | No | OK - mascot hiding spot |
| Register | Counter LOOK AROUND | Yes (LOOK REGISTER) | No | OK |
| Coffee (Usui's) | Counter LOOK AROUND | Yes (LOOK COFFEE) | No | OK |
| Cabinets | Kitchen LOOK AROUND | Yes (LOOK CABINET) | Yes (OPEN CABINET) | OK |
| Drawer | Kitchen LOOK AROUND | Yes (LOOK DRAWER) | Yes (OPEN DRAWER) | OK |
| Mixing bowls (scenery) | Kitchen LOOK AROUND | Yes (LOOK BOWL) | No | OK - mascot hiding spot |
| Sink | Kitchen LOOK AROUND | Yes (LOOK SINK) | No | OK |
| Oven | Kitchen LOOK AROUND | Yes (LOOK OVEN) | No | OK |
| Costumes | Kitchen LOOK AROUND | Yes (LOOK COSTUME) | No | OK - mascot hiding spot (APRON_PILE) |
| Treat cabinet | Kitchen LOOK AROUND | Yes (LOOK TREAT) | No | OK - mascot hiding spot |
| Recipe book | Kitchen LOOK AROUND | Yes (LOOK RECIPE) | No | OK |
| Shrine | Kitchen LOOK AROUND | Yes (LOOK SHRINE) | No | OK |
| Spice rack | Kitchen LOOK AROUND | Yes (LOOK SPICE) | No | OK |
| Window | Not in room descs | Yes (LOOK WINDOW) | No | OK - ambient |
| Pots/pans | Kitchen room desc (base) | No | No | **UNREACHABLE** |
| Bread knife | Kitchen room desc (always shown) | Covered by LOOK KNIFE? No - no handler | TAKE KNIFE works | **PARTIALLY** - see below |

### Unreachable / Partially Reachable Entities

1. **Pots/pans** (UNREACHABLE): Mentioned in base Kitchen room desc ("Pots, pans, cabinets along the wall") but no LOOK handler exists for "pots" or "pans". Player cannot examine them. They also appear in the ASCII art ("~ pots ~") and LISTEN response ("Pots bubbling").

2. **Bread knife** (PARTIALLY REACHABLE): Shown in Kitchen room desc as a `<span class="item">bread knife</span>` with item styling, but LOOK KNIFE has no handler. `handleLook` will return the generic "You don't see anything special about that." The TAKE and USE handlers do work. Missing: a LOOK response for the knife.

3. **Apron (from Kitchen)** (PARTIALLY REACHABLE): `handleLook` for "apron" has a branch for `state.location === 'KITCHEN'` (line 1046-1048) that shows the apron even when the player is in the kitchen. However, the apron is only takeable from the COUNTER. The Kitchen description never mentions an apron (it's on a hook by the kitchen door, which is at the counter). This is a minor spatial ambiguity -- the LOOK response works from the kitchen, but TAKE does not.

4. **Knife on cutting board** (description mismatch): The room desc says "A bread knife sits on the cutting board" but there is no LOOK handler for "cutting board". Minor.

5. **"Something familiar at Table 3"** in room desc vs. Satsuki's mention of "nephew Aoi" -- both reachable through LOOK CUSTOMER 3 and TALK CUSTOMER 3. OK.

---

## B) Description Consistency

### Contradictions Found

1. **Kitchen navigation directions conflict.**
   - Kitchen room desc says: `Back to: COUNTER | Back door: ALLEY` (line 619)
   - Kitchen LOOK AROUND says: `South: COUNTER` (line 1012)
   - Kitchen hints show: `go counter` and `go alley` (line 1711-1712)
   - The ASCII scene says: `<- COUNTER` (line 523)
   - `handleMove` maps SOUTH to COUNTER from KITCHEN (line 939-946), and NORTH to KITCHEN from COUNTER (line 930-936)
   - **Issue:** Room desc says "Back to" implying you came from there, while LOOK says "South" implying a compass direction. These are consistent enough. However, the COUNTER room says "Through back: KITCHEN" and LOOK says "North: KITCHEN" -- mixing informal and compass directions is fine but slightly inconsistent with the ASCII art which uses `<-` (left arrow, implying west/back, not south).
   - **Severity:** Low. A player would not be confused.

2. **Counter directional labels inconsistent.**
   - Counter room desc says: `EAST: DINING | Through back: KITCHEN` (line 578)
   - Counter LOOK AROUND says: `East: DINING | North: KITCHEN` (line 996)
   - Counter ASCII says: `<- DINING ... KITCHEN ->` (line 504), which implies DINING is west and KITCHEN is east
   - `handleMove` maps: EAST to DINING (line 913), WEST to COUNTER (from DINING, line 922), NORTH to KITCHEN (from COUNTER, line 930)
   - **Issue:** The ASCII art places DINING to the LEFT and KITCHEN to the RIGHT, but the code says DINING is EAST and KITCHEN is NORTH. The ASCII layout contradicts the movement directions. A player typing `E` from COUNTER goes to DINING (which is shown LEFT in ASCII), and `N` goes to KITCHEN (shown RIGHT in ASCII).
   - **Severity:** Medium. Could confuse players who rely on the ASCII art for spatial reasoning.

3. **Knife visibility before LOOK AROUND.**
   - The Kitchen `getRoomDesc()` always shows `A <span class="item">bread knife</span> sits on the cutting board.` regardless of whether `kitchenLooked` is true (line 596-598). This is OUTSIDE the `if (state.kitchenLooked)` block.
   - This means the knife is visible in the room description panel even before the player does LOOK AROUND in the kitchen.
   - **Severity:** Medium. This is a progressive disclosure violation (see Section C).

### Minor Inconsistencies (not contradictions)

- The LOOK AROUND response for Counter mentions `Usui` with item styling (`<span class="item">Usui</span>`) as if he's an item, while the room desc mentions him in regular text. This is fine -- it's drawing attention to him as interactable.
- The LOOK AROUND for Kitchen says "A treat cabinet in the corner" but it's not clear from the room desc where it is physically. Not a real issue.

---

## C) Progressive Disclosure

### Gate: `diningLooked`

| Check | Status |
|-------|--------|
| Customers hidden before LOOK AROUND | **PASS** - Room desc only shows them after `diningLooked` is true (line 551-554) |
| Fern hidden before LOOK AROUND | **PASS** - Same gate (line 553) |
| Specials board hidden before LOOK AROUND | **PASS** - Same gate (line 553) |
| LOOK TABLE/CUSTOMER/FERN/MENU work before gate | **PASS** (with caveat) - These LOOK handlers work regardless of `diningLooked`, but the player wouldn't know to look at them without first seeing them in the room desc. The entities ARE in the ASCII art though (MENU, FERN, T1/T2/T3), so a player reading the ASCII art could guess. This is acceptable. |

### Gate: `counterLooked`

| Check | Status |
|-------|--------|
| Espresso machine hidden before LOOK | **PASS** - Only shown after `counterLooked` (line 570-572) |
| Display case hidden before LOOK | **PASS** |
| Tip jar hidden before LOOK | **PASS** |
| Register hidden before LOOK | **PASS** |
| Coffee hidden before LOOK | **PASS** |
| TALK USUI hint hidden before LOOK | **PASS** - Hint only appears after `counterLooked` (line 1691-1692) |
| `apronRevealed` set on first LOOK | **PASS** - Line 987-989 |
| TAKE APRON hint hidden before LOOK | **PASS** - Hint requires `counterLooked` AND `apronRevealed` (line 1693-1694) |

**Note:** Usui is mentioned in the base room desc ("Usui is leaning against the counter") before LOOK AROUND. The player CAN `TALK USUI` before doing LOOK AROUND -- the hint just won't be visible. This is acceptable; Usui is a prominent NPC, not a hidden item.

### Gate: `kitchenLooked`

| Check | Status |
|-------|--------|
| Cabinets hidden before LOOK | **PASS** - Only shown after `kitchenLooked` (line 592-594) |
| Mixing bowls hidden before LOOK | **PASS** |
| Sink hidden before LOOK | **PASS** |
| Oven hidden before LOOK | **PASS** |
| Costumes hidden before LOOK | **PASS** |
| Treat cabinet hidden before LOOK | **PASS** |
| Recipe book hidden before LOOK | **PASS** |
| Shrine hidden before LOOK | **PASS** |
| Spice rack hidden before LOOK | **PASS** |
| TALK SATSUKI hint hidden before LOOK | **PASS** - Line 1714-1715 |
| OPEN CABINET hint hidden before LOOK | **PASS** - Line 1716-1718 |
| OPEN DRAWER hint hidden before LOOK | **PASS** - Line 1719-1721 |

### Gate: `apronRevealed`

| Check | Status |
|-------|--------|
| Apron not shown in room desc before reveal | **PASS** - Conditional on `apronRevealed` (line 574-576) |
| TAKE APRON blocked before reveal | **PASS** - Returns "Maybe look around first?" (line 1375-1377) |

### Gate: `cabinetOpened`

| Check | Status |
|-------|--------|
| Bowl not shown before OPEN CABINET | **PASS** - Conditional on `cabinetOpened` (line 600-609) |
| TAKE BOWL blocked before cabinet opened | **PASS** - Returns "Maybe check the cabinets?" (line 1390-1392) |
| Treats not shown before OPEN CABINET | **PASS** |
| TAKE TREATS blocked before cabinet opened | **PASS** - Line 1432-1434 |

### Disclosure Violations

1. **KNIFE visible before LOOK AROUND (VIOLATION).**
   - In `getRoomDesc()` for KITCHEN, the knife block (lines 596-598) is OUTSIDE the `if (state.kitchenLooked)` guard. The knife appears in the room description panel immediately upon entering the kitchen, before the player does LOOK AROUND.
   - The `kitchenLooked` gate correctly hides cabinets, bowls, sink, oven, costumes, etc. But the knife escapes this gate.
   - **Fix:** Move the knife display inside the `if (state.kitchenLooked)` block, OR accept this as intentional (the knife is on the cutting board, visible immediately).

2. **CABINET and DRAWER in base Kitchen room desc (MINOR VIOLATION).**
   - The base Kitchen room desc (before LOOK AROUND) says: "Pots, pans, cabinets along the wall. A drawer by the counter." (line 589)
   - This means the player knows about cabinets and the drawer before LOOK AROUND. However, they cannot interact with them (OPEN CABINET/DRAWER) because the hint buttons don't appear until after `kitchenLooked`, and the OPEN handler works regardless of the gate.
   - **Technically:** A player who reads the base room desc could type OPEN CABINET before LOOK AROUND and it would work, bypassing the progressive disclosure for the bowl and treats.
   - **Severity:** Low-medium. The `kitchenLooked` gate on hints discourages this but doesn't prevent it. A text-adventure-savvy player would try OPEN CABINET immediately.

---

## D) Hint Quality — Critical Path Analysis

### Step 1: START at DINING

**Available guidance:**
- Welcome message: "Now it's bouncing from room to room - dining area, counter, kitchen" (tells player the map)
- Hint bar shows: `look around`, `go counter`
- If mascot is here (starts at TABLE2 in DINING): gold hint text appears in room desc

**Verdict:** ADEQUATE. Player knows where they are and what to do.

### Step 2: GO COUNTER

**Available guidance:**
- Room desc mentions "To the WEST: COUNTER"
- Hint bar has `go counter`
- Natural exploration

**Verdict:** ADEQUATE.

### Step 3: LOOK AROUND at COUNTER (reveals apron + Usui available)

**Available guidance:**
- Hint bar always shows `look around`
- First visit to a room naturally prompts looking

**Verdict:** ADEQUATE.

### Step 4: TAKE APRON

**Available guidance:**
- After LOOK AROUND: apron appears in room desc with item styling
- Hint bar shows `take apron` after counter is looked at and apron revealed
- Satsuki tier 2 dialogue: "when I catch stray threads, I use something soft"
- Satsuki tier 3 dialogue: "The apron! Use the apron!"

**Verdict:** ADEQUATE. Multiple hints converge.

### Step 5: GO KITCHEN

**Available guidance:**
- Counter room desc: "Through back: KITCHEN"
- Hint bar: `go kitchen`
- CATCH fail messages (tier 2+): "Maybe something in the KITCHEN could help..."

**Verdict:** ADEQUATE.

### Step 6: LOOK AROUND in KITCHEN (reveals cabinet + Satsuki available)

**Available guidance:**
- Hint bar: `look around`
- Pattern established from previous rooms

**Verdict:** ADEQUATE.

### Step 7: OPEN CABINET (reveals bowl)

**Available guidance:**
- After LOOK AROUND: hint bar shows `open cabinet`
- LOOK CABINET: "Kitchen cabinets along the wall. Who knows what's inside?"
- Satsuki's dialogue doesn't mention cabinets specifically

**Verdict:** ADEQUATE. The hint bar and natural curiosity suffice.

### Step 8: TAKE BOWL

**Available guidance:**
- After OPEN CABINET: bowl appears with item styling
- LOOK BOWL: "A big one might trap something small..." (direct hint!)
- No hint bar button for TAKE BOWL specifically, but item styling signals takeability

**Verdict:** ADEQUATE. The LOOK BOWL hint is excellent.

### Step 9: Find mascot (cycles through rooms)

**Available guidance:**
- Gold-colored hint text appears in room desc when mascot is in current room
- ASCII art shows "* something moved!" when mascot is present
- Mascot cycles on a 3-command interval through all rooms
- Tier 2+ hints give clear location descriptions

**Verdict:** ADEQUATE. The visual cues are strong.

### Step 10: USE BOWL (traps mascot)

**Available guidance:**
- LOOK BOWL: "A big one might trap something small..."
- Hint bar (tier 2+): `use bowl` appears when mascot is visible
- Usui tier 2 noApron: "the direct approach doesn't seem to be working"
- Usui tier 3: "corner it first. Then use something soft."
- After trapping: "Now you just need something soft to wrap it up and carry it safely." (gold text)

**Verdict:** ADEQUATE. Strong convergent hints.

### Step 11: USE APRON (catches trapped mascot)

**Available guidance:**
- After bowl traps mascot: gold text says "something soft to wrap it up"
- Hint bar (tier 2+): `use apron` appears when mascot is trapped and apron in inventory
- Usui tier 3: "corner it first. Then use something soft"
- Satsuki tier 3: "The apron! Use the apron!"

**Verdict:** ADEQUATE.

### Step 12: WIN

**Automatic on USE APRON when mascot is trapped.**

### Hint Gap Identified

**GAP: No guidance from STEP 2 (arrive at COUNTER) to STEP 3 (LOOK AROUND).**

While the hint bar always shows `look around`, a new player might not understand that LOOK AROUND is the primary discovery mechanic. The welcome message says "Type HELP for commands" but HELP doesn't emphasize that LOOK AROUND is mandatory for progression. HELP says: "LOOK [thing] - examine something (or just LOOK for the room)".

A player who goes to COUNTER and immediately tries to TALK USUI (which works, since the handler doesn't require `counterLooked`) would get dialogue but might not realize they need to LOOK AROUND to unlock new items and hints. They could loop between rooms and NPCs indefinitely without discovering the apron.

**Severity:** Low. The hint bar's persistent `look around` button mitigates this. But worth noting that no NPC or text explicitly says "you should look around each room carefully."

---

## E) Additional Findings

### Edge Cases in handleCatch

The `handleCatch` function (line 1565-1610) has a dead code path:

```javascript
if (!canCatchMascot()) {
    if (isMascotInDining() && state.location === 'DINING') {
        // Can see but not at right table
    } else {
        return `The plushie isn't here!...`;
    }
}
```

When `canCatchMascot()` is false but `isMascotInDining()` is true and player is in DINING, the code falls through to the bare-hands catch attempt below. This means `canCatchMascot()` returns false (mascot is in DINING but at a different hiding spot than the player's generic "DINING" location -- wait, actually `canCatchMascot()` just checks if the hiding spot's room matches the player's room). Let me re-examine:

`canCatchMascot()` checks `spot[0] === state.location`. If mascot is at TABLE1 and player is at DINING, `spot[0]` is 'DINING' and `state.location` is 'DINING', so `canCatchMascot()` returns TRUE. The `isMascotInDining()` branch would never be reached in that case. This is dead code -- the condition `!canCatchMascot() && isMascotInDining() && state.location === 'DINING'` can never be true, because `canCatchMascot()` already checks the same room match.

**Severity:** No gameplay impact, but dead code that could confuse future maintainers.

### GRAB verb ambiguity

`GRAB` is mapped to both TAKE (line 762) and CATCH (line 777). Since TAKE is checked first in `processCommand`, `GRAB MASCOT` goes through `handleTake`, which then delegates to `handleCatch` (line 1443-1444). This works correctly but is worth noting -- `GRAB APRON` goes to TAKE, `GRAB MASCOT` goes to CATCH via TAKE.

### Missing OPEN handlers

- `OPEN REGISTER` -- no handler (returns "Open what?")
- `OPEN DISPLAY` / `OPEN CASE` -- no handler
- `OPEN OVEN` -- no handler
- `OPEN TREAT CABINET` -- the `handleOpen` handler checks for "cabinet" which would match "treat cabinet", so this actually opens the main cabinet, not the treat cabinet specifically. A player typing "OPEN TREAT CABINET" would open the cabinets and find the bowl/snacks, which is correct behavior but doesn't match the separate "treat cabinet" entity shown in LOOK AROUND.

### Save/Load robustness

The save system stores `state` and `output.innerHTML`. On load, it uses `Object.assign(state, data.state)`. If the game code adds new state fields in a future version, old saves won't have them and they won't be initialized. Currently mitigated by `const state = { ...defaultState }` being set before `loadGame()`, so old saves will have the new defaults. This is fine.

---

## Recommendations

### Priority 1 (Should fix)

1. **Move knife display inside `kitchenLooked` gate.** The knife appearing before LOOK AROUND breaks progressive disclosure. Either gate it or make it intentional by leaving it outside ALL gates (as a "visible on the counter" item like Usui).

2. **Gate OPEN CABINET/DRAWER behind `kitchenLooked`.** Currently a player can type OPEN CABINET before LOOK AROUND and bypass the progressive disclosure entirely. Add a check: if `!state.kitchenLooked`, return "You should look around first."

3. **Add LOOK KNIFE handler.** The knife has item styling in the room desc and is TAKE-able, but has no LOOK response. A player who types LOOK KNIFE gets the generic "You don't see anything special about that." Add a response like: "A bread knife on the cutting board. Sharp but... no. You're not THAT desperate."

### Priority 2 (Should consider)

4. **Add LOOK POTS handler.** Pots are mentioned in the base Kitchen description and ASCII art. Even a one-liner would help: "Pots on the stove. Satsuki's domain."

5. **Clarify ASCII art directions vs. movement directions.** The Counter ASCII art shows DINING on the left (`<- DINING`) and KITCHEN on the right (`KITCHEN ->`), but movement uses EAST for DINING and NORTH for KITCHEN. Consider either: (a) updating ASCII to use compass-like layout matching the movement model, or (b) dropping compass directions from LOOK AROUND text and using only informal directions ("back to DINING", "through to KITCHEN").

6. **Remove dead code in `handleCatch`.** The `isMascotInDining()` branch inside the `!canCatchMascot()` block is unreachable. Clean it up.

### Priority 3 (Nice to have)

7. **Add a gentle nudge about LOOK AROUND in early game.** If the player's first 3-4 commands don't include LOOK AROUND, consider having Usui or Satsuki say something like "You might want to look around..." This would close the one identified hint gap.

8. **Differentiate OPEN TREAT CABINET from OPEN CABINET.** Currently "open treat cabinet" opens the main cabinet. Either: (a) make the treat cabinet openable separately with its own contents, or (b) rename it in descriptions to avoid confusion (e.g., "snack shelf" instead of "treat cabinet").

9. **Add LOOK CUTTING BOARD handler.** The room desc mentions "cutting board" but it has no LOOK response.

10. **Consider showing inventory in the hint bar or room desc panel** so players don't forget what they're carrying. Currently requires typing INVENTORY.
