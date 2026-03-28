# Physical & Logical Audit Report

## Summary

- Spatial issues: 3
- Physical inconsistencies: 2
- Logical contradictions: 3
- Easter eggs found: 21
- Canon issues: 1

---

## A) Spatial Map

### Layout (as described in code)

```
                        ALLEY
                          |
                     [back door]
                          |
                    +-----------+
                    |  KITCHEN  |
                    |           |
                    +-----+-----+
                          |
                     N/S (north/south)
                          |
                    +-----+-----+
                    |  COUNTER  |
                    |           |
                    +-----+-----+
                          |
                     E/W (east/west)
                          |
                    +-----+-----+
                    |  DINING   |
                    |           |
                    +-----------+
```

### Directional Analysis

| From | To | Direction in code | Direction in description |
|------|-----|-------------------|------------------------|
| DINING | COUNTER | W / west | Room desc says "To the WEST: COUNTER" |
| COUNTER | DINING | E / east | Room desc says "EAST: DINING" |
| COUNTER | KITCHEN | N / north | Room desc (first look) says "North: KITCHEN" |
| KITCHEN | COUNTER | S / south | Room desc says "South: COUNTER" |
| KITCHEN | ALLEY | via "back door" | Room desc says "Back door: ALLEY" |

The ASCII art (lines 486-487) says `[ COUNTER -> ]` with an arrow suggesting the counter is to the right (east) of dining. But the room description says the counter is to the WEST. There is an inconsistency here.

### Spatial Issue #1: DINING-to-COUNTER direction conflict

**The room description** (line 556) says: `To the WEST: COUNTER`
**The handleMove code** (line 913) maps `east` to DINING and `west` to COUNTER.
**The direction hint** (line 958) says: `DINING (E), COUNTER (W), or KITCHEN (N)`.

So the code is internally consistent: COUNTER is west of DINING. But the **ASCII scene art** (line 486) shows `[ COUNTER -> ]` with a right-pointing arrow, which visually suggests east. The arrow likely means "go this way to reach the counter" but the rightward direction fights the W/west mapping.

**Severity:** Low-medium. Confusing to players who read the ASCII art directionally.

### Spatial Issue #2: COUNTER-to-KITCHEN direction labels inconsistent across views

- The `handleLook` first-look description for COUNTER (line 996) says: `East: DINING | North: KITCHEN`
- The persistent `getRoomDesc()` (line 578) says: `EAST: DINING | Through back: KITCHEN`
- The `handleMove` direction hint (line 958) says `KITCHEN (N)`
- The ASCII scene for COUNTER (line 504) shows `<- DINING` on the left and `KITCHEN ->` on the right, both on the same horizontal line.

The first-look says KITCHEN is north. The persistent description says "through back" (ambiguous, but suggests behind/north). The ASCII art places KITCHEN to the right (which reads as east). These conflict.

**Severity:** Low. "Through back" is vague enough to work narratively, but the ASCII art places KITCHEN on the same horizontal axis as DINING, which doesn't match north.

### Spatial Issue #3: ALLEY is mentioned but unreachable

The KITCHEN description (line 619) lists `Back door: ALLEY` as a navigation option. The hint bar even provides a clickable "go alley" button (line 1712). But `handleMove` (lines 949-956) always refuses entry with rotating excuses. The ALLEY is a fake location by design, but presenting it alongside real navigation options without any visual distinction is spatially misleading. Players will try it, get blocked, and may waste time thinking it is puzzle-relevant.

**Severity:** Low. It is a deliberate design choice (Misaki refuses to leave during her shift), but including it in the hint bar is a slight UX issue -- it looks like a real option.

---

## B) Physical Interactions

### BOWL Mechanics

**Trapping:** USE BOWL when the mascot is in the same room (line 1462-1472).

- The mixing bowl is described as "heavy metal, good weight" (line 1398).
- When used: "You bring the bowl down over Uchujin-kun! CLANG! The mascot is trapped! It scrabbles against the metal, tiny face pressed to the rim." (lines 1465-1467)

**Physical plausibility:** Good. A heavy metal mixing bowl inverted over a palm-sized plushie on a flat surface is a reasonable trap. The weight keeps it in place. The "CLANG" and "scrabbles against the metal" are consistent with metal-on-floor and a small object pushing against the interior.

**Does it stay?** Implicitly yes -- the state flag `mascotTrapped` prevents movement (`moveMascot` returns early at line 692). The plushie is described as "palm-sized" so it plausibly cannot tip a heavy metal bowl from inside.

**Can the mascot escape?** No. Once trapped, `mascotTrapped = true` is permanent until the win condition. Physically reasonable for a small plushie under a heavy bowl.

### APRON Mechanics

**Catching a free mascot (fail):** "You throw the apron! It flutters down... and the mascot darts away before it lands." (line 1491)

**Physical plausibility:** Good. A fabric apron thrown through the air would flutter and descend slowly -- a fast-moving target could dodge.

**Catching a trapped mascot (win):** "You sweep the apron over the mascot." (line 1620), then "Uchujin-kun squirms under the fabric, then settles into your arms." (line 1622)

**Physical plausibility:** Good. The sequence is: lift bowl, quickly sweep apron over the exposed plushie, bundle it. "Sweep" implies a quick covering motion. The fabric wraps around the plushie and you scoop it up. This is essentially how you'd catch a small animal (cover with towel/blanket).

**Physical Inconsistency #1:** The code does not model the bowl being removed. When you USE APRON on a trapped mascot, the bowl is still in inventory and the description says "sweep the apron over the mascot" -- but the bowl is presumably still on top. The implied physical sequence is: lift bowl with one hand, sweep apron with other hand. But this is never described. Minor gap in narration rather than a logic error.

### MASCOT Behavior

**Movement:** The mascot cycles through a fixed list of hiding spots every `MOVE_INTERVAL` (3) commands (line 469, 722). When "spooked," it moves twice per cycle.

**How does a plushie move?** The intro says it "fell out of your bag" and is "bouncing from room to room." The LOOK MASCOT description says it has "big eyes and a knowing smirk" and "blinks." The game leaves the mechanism ambiguous -- it is either magic, Misaki's perception, or the plushie is genuinely animated. This is consistent with the anime's tone (Maid-Sama! doesn't have supernatural elements, but the game adds a light fantastical touch via the plushie).

**Physical plausibility of movement pattern:** The mascot moves through DINING spots, COUNTER spots, and KITCHEN spots in a fixed cycle. It does not respect walls -- it can jump from DINING to COUNTER to KITCHEN without passing through intermediate rooms. This is fine for gameplay abstraction but is physically impossible without doors/pathways. Since the cafe's rooms are connected (DINING-COUNTER-KITCHEN in a line), the mascot would need to pass through the COUNTER to go from DINING to KITCHEN. The cycle (TABLE2 -> ESPRESSO -> TABLE1 -> BOWLS -> ...) has it jump rooms frequently. Acceptable for a "bouncing plushie" abstraction.

### Item Locations

| Item | Location | Plausibility |
|------|----------|-------------|
| Apron on hook by kitchen door | COUNTER (visible after LOOK) | Good -- the kitchen door connects counter to kitchen, and an apron hook there makes sense |
| Bowl in cabinet | KITCHEN (after OPEN CABINET) | Good -- mixing bowls in kitchen cabinets is standard |
| Bread knife on cutting board | KITCHEN (always visible) | Good |
| Garbage bags in drawer | KITCHEN (after OPEN DRAWER) | Good |
| Treats/snacks in cabinet | KITCHEN (after OPEN CABINET) | Good -- staff snacks in a kitchen cabinet |

**Physical Inconsistency #2: Apron visibility from KITCHEN**

The apron hangs "by the kitchen door" (line 575, 994). It can only be TAKEN from COUNTER (line 1372-1373). But LOOK APRON from KITCHEN (line 1046-1048) returns: "A white apron hanging on a hook. Satsuki made it herself..." -- it is visible from the kitchen side too.

This is physically consistent (a hook on a door is visible from both sides), but the asymmetry in the TAKE logic (only from COUNTER) is slightly odd. If you can see it from the kitchen, you should be able to take it from the kitchen. This is likely a deliberate design choice (forces the player to go to COUNTER), but it is a minor physical inconsistency.

### NPC Positions

**Usui:** Always at COUNTER. "Leaning against the counter" (line 501-502, 566-567). His position is consistent across all interactions. He never moves to other rooms. If you try to talk to him from another room: "Usui is at the counter" (line 1272). Consistent.

**Satsuki:** Always in KITCHEN. "Barely contained" (line 588), "vibrating excitedly" (line 521). She never moves. Talk from other rooms: "Satsuki is in the kitchen" (line 1315). Consistent.

**Exception in win sequence:** "A familiar presence appears beside you" (line 1623) -- Usui appears wherever you win, even if that is the KITCHEN or DINING. Similarly, "Satsuki appears from the kitchen" (line 1631). This implies Usui walks to your location and Satsuki emerges from the kitchen. Physically plausible as a cutscene moment.

---

## C) Logical Consistency

### State Persistence

| State | Persists? | Evidence |
|-------|-----------|---------|
| Items in inventory | Yes | `state.inventory` array, checked throughout |
| Cabinet opened | Yes | `state.cabinetOpened` flag, checked in descriptions and TAKE |
| Drawer opened | Yes | `state.drawerOpened` flag |
| Apron revealed | Yes | `state.apronRevealed` flag |
| Mascot trapped | Yes | `state.mascotTrapped` flag |
| Room looked flags | Yes | `diningLooked`, `counterLooked`, `kitchenLooked` |
| Won state | Yes | `state.won` flag |

All state persists correctly via `saveGame()` to localStorage after every command (line 1760).

### Item Removal from Descriptions

When you take the APRON, the room description correctly stops showing it:
- Line 574: `if (state.apronRevealed && !state.inventory.includes('APRON'))` -- only shows apron if not taken.
- Line 993: Same check in first-look description.
- ASCII scene line 504: `apronRevealed && !hasApron ? '[APRN]' : '      '` -- removes from ASCII.

When you take the BOWL, the cabinet description updates (lines 601-608).
When you take the BAG, the drawer description updates (lines 612-616).

All correct.

### Failure States

**USE APRON without trapping:** "You throw the apron! It flutters down... and the mascot darts away before it lands." (line 1491). Logical and physical.

**USE APRON when mascot is not present:** "The plushie isn't here. It's bouncing around somewhere else." (line 1481). Correct.

**CATCH bare-handed:** Rotating fail messages (lines 1590-1596). Mascot moves afterward. Correct.

**USE BOWL when mascot not present:** "You're holding a bowl. The plushie isn't here." (line 1457). Correct.

### Logical Contradiction #1: GRAB is ambiguous verb

Line 762: `if (verb === 'take' || verb === 'get' || verb === 'grab' || verb === 'pick')` routes GRAB to `handleTake`.
Line 777: `if (verb === 'catch' || verb === 'grab')` routes GRAB to `handleCatch`.

But because the TAKE check comes first in the if-chain (line 762 before 777), GRAB will always be treated as TAKE, never as CATCH. This means `grab mascot` goes through `handleTake`, which at line 1443 redirects `grab mascot` to `handleCatch`. So it works by accident for the mascot case. But `grab apron` would be TAKE (correct), and `grab` alone would return "Take what?" (line 1447) rather than attempting a catch.

**Severity:** Low. The only common `grab` target players would try is the mascot, which works via the redirect. But `grab` with no arguments returns "Take what?" instead of the catch behavior, which is slightly illogical.

### Logical Contradiction #2: Trapped mascot location is frozen but descriptions don't reflect this

When the mascot is trapped (`mascotTrapped = true`), movement stops (line 692). The mascot stays at whatever hiding spot it was in. But the room descriptions and ASCII scenes still show the generic mascot hints based on `isMascotVisible()`. This means if you trap the mascot at, say, the ESPRESSO spot in COUNTER, you get the hint "Uchujin-kun is wedged behind the espresso machine!" in the room description -- but it is actually under a bowl on the floor.

The game does show a post-trap message ("Now you just need something soft to wrap it up and carry it safely"), but subsequent LOOK commands will still show the old hiding spot description. The trapped state does not update the hiding spot descriptions.

**Severity:** Medium. After trapping, the player should see "The mascot is trapped under the bowl" rather than the old hiding-spot description.

### Logical Contradiction #3: `handleCatch` has dead code path

Lines 1567-1571:
```javascript
if (isMascotInDining() && state.location === 'DINING') {
    // Can see but not at right table
} else {
    return `The plushie isn't here! It must have bounced to another room...`;
}
```

This block is reached when `canCatchMascot()` returns false. The `isMascotInDining()` branch has an empty body -- it falls through to the rest of the function. This means if the mascot is in DINING but `canCatchMascot()` fails (which should not happen since `canCatchMascot` checks the same room condition), the code falls through silently. In practice, `canCatchMascot()` and `isMascotInDining() && state.location === 'DINING'` are equivalent for the DINING case, so this dead code path is never actually reached. But it is confusing code.

**Severity:** Very low. Dead code, no player impact.

---

## D) Easter Eggs

### Ambient Commands

| # | Command | Room | Response Summary | Makes Sense? |
|---|---------|------|-----------------|-------------|
| 1 | LISTEN | DINING | Cups, murmurs, J-pop, "tiny plushie feet" | Yes. Nice environmental detail. "Tiny plushie feet on tile" is a cute touch. |
| 2 | LISTEN | COUNTER | Espresso, Usui humming British pop, Satsuki singing | Yes. Usui is half-British in canon -- nice detail. |
| 3 | LISTEN | KITCHEN | Pots, mixer, Satsuki narrating cooking like a TV show, "secret ingredient is LOVE" | Yes. In character for Satsuki. |
| 4 | SMELL | DINING | Coffee, vanilla, floral perfume | Yes. Standard cafe smells. |
| 5 | SMELL | COUNTER | Coffee, Usui's cologne "something expensive that you definitely haven't memorised" | Yes. Great characterization -- Misaki's denial. |
| 6 | SMELL | KITCHEN | Cookies, caramelizing sugar, lemon cleaner | Yes. Spotless kitchen matches Satsuki's personality. |
| 7 | WAIT | Any | 4 rotating messages about time passing | Yes. Messages are in character. |
| 8 | THINK | Any | 5 rotating internal monologues | Yes. Rich characterization. Excellent Misaki voice. |

### Usui Interaction Easter Eggs

| # | Command | Response Summary | Rewarding? |
|---|---------|-----------------|-----------|
| 9 | PUNCH/HIT/SLAP/KICK USUI | He catches your wrist without looking. "Violent today, Kaichou." | Yes. Classic Usui reflex, in character. |
| 10 | KISS USUI | Brain short-circuit. "Not here, Misa-chan." Nuclear blush. | Yes. Perfect romcom energy. Very in character. |
| 11 | HUG USUI | Consider it for 0.3 seconds, survival instincts kick in | Yes. Misaki's internal conflict, well done. |
| 12 | YELL/SCREAM/SHOUT | "USUI, YOU PERVERTED OUTER-SPACE ALIEN!" said out loud | Yes. Iconic Misaki line. |
| 13 | IGNORE USUI | "I'll wait, Ayuzawa." He always waits. | Yes. Threatening tenderness. Very Usui. |
| 14 | BLUSH | Already blushing, Usui notices | Yes. Cute. |

### Other Easter Eggs

| # | Command | Response Summary | Rewarding? |
|---|---------|-----------------|-----------|
| 15 | ALIEN/ALIENS | "PERVERTED OUTER-SPACE ALIEN!" said out loud | Yes. Duplicate of YELL in shorter form. |
| 16 | CALL MOM | "She can NEVER know about this job" | Yes. In character -- Misaki's secret. |
| 17 | MOE / SAY MOE | Satsuki materializes. "Did someone say MOE?!" | Yes. Perfect Satsuki. |
| 18 | CHESS | No time. Usui "once beat a national champion." | Yes. Canon reference (Usui is absurdly talented). |
| 19 | ROOFTOP/ROOF/FALL | Remembering Usui falling off school building | Yes. Major canon event. |
| 20 | CRY/SOB | Refuse to cry. "Handled delinquents, budget crises, and the Idiot Trio" | Yes. The Idiot Trio is a canon reference. |
| 21 | QUIT/GIVE UP/SURRENDER | "Misaki Ayuzawa does not quit." | Yes. Core character trait. |

### Other Notable Interactions

- **DANCE/SING**: Workplace dignity, Satsuki is singing anyway. In character.
- **LOOK SELF**: "Panicked, determined, flustered by a certain blond idiot." Great voice.
- **LOOK REGISTER**: Photo of staff taped to side. Warm detail.
- **LOOK SHRINE**: Candid photo of Misaki and Usui. "SATSUKI." Perfect reaction.
- **Table 3 customer**: Blonde pigtails, black bow, red dress, blue eyes, judgmental. This is **Aoi Hyoudou** (Satsuki's nephew who crossdresses). Misaki recognizes but refuses to engage. Satsuki later mentions "My nephew Aoi sometimes helps out here" and "he might be here today." Excellent cross-reference.
- **USE KNIFE on mascot**: Misaki feels horrible, puts it away. Good -- prevents dark path, in character.
- **USE BAG on mascot**: Tears through thin plastic. Physical and logical.
- **USE TREATS**: Snatches cookie and bolts. Plausible plushie behavior.

### Contradiction Check on Easter Eggs

No contradictions found. Easter eggs are self-contained and do not conflict with game state or other descriptions.

---

## E) Canon Accuracy (Maid-Sama! / Kaichou wa Maid-sama!)

### Character Roles

| Character | Game Role | Canon Role | Accurate? |
|-----------|-----------|------------|-----------|
| Misaki Ayuzawa | Player character (maid, narrator) | Student council president, secret maid at Maid Latte | Yes |
| Usui Takumi | Customer at counter, not employee | Customer who discovered Misaki's secret, frequent visitor | Yes |
| Satsuki Hyoudou | Kitchen, manager | Manager of Maid Latte, moe-obsessed | Yes |
| Aoi Hyoudou | Table 3 customer (implied, unnamed) | Satsuki's nephew, crossdresses, works at cafe sometimes | Yes |

### Character Voice Check

- **Misaki:** Determined, prideful, flustered by Usui, denies feelings, Student Council President identity. All accurate.
- **Usui:** Smirking, teasing, protective underneath, calls her "Ayuzawa" / "Misa-chan" / "Kaichou." British background hinted ("Reminds me of England"). All accurate.
- **Satsuki:** Moe-obsessed, enthusiastic, ships Misaki/Usui, motherly. All accurate.

### Setting Details

- Maid Latte cafe: correct name, correct atmosphere (maid cafe with food service)
- "Welcome home, Master~" greeting: canon accurate (standard maid cafe greeting used in the series)
- Maid uniforms, themed food items ("Moe Moe Parfait"): consistent with canon's exaggerated maid cafe culture
- Seika High visible through window: canon (Misaki is student council president there)
- Usui's talents (chess champion, martial arts, surviving rooftop fall): canon
- "Perverted outer-space alien": Misaki's canonical insult for Usui
- The Idiot Trio: canon (Shirokawa, Kurosaki, Sarashina -- three male students who frequent Maid Latte)
- Miyabigaoka student council: canon (rival school)

### Canon Issue #1: "Uchujin-kun" plushie

There is no "Uchujin-kun" plushie in the Maid-Sama! canon. This is an original creation for the game -- a green alien plushie with blond hair that resembles Usui. The game establishes it clearly as something Misaki bought from a capsule machine and won't admit looks like Usui. This is a **new addition**, not a contradiction. It is consistent with Misaki's character (buying something that reminds her of Usui while denying it).

**Severity:** Not an issue. Original addition that fits canon characterization.

### Canon Observation: Timeline/Era

The game mentions "J-pop from the speakers" and "phone" (customer laughing at phone). The original manga ran 2006-2013. A modern smartphone suggests a contemporary setting update, which is fine for a fan game.

---

## Issues Found (Prioritized)

### Medium Priority

1. **[Logical] Trapped mascot still shows old hiding-spot descriptions.** After trapping with the bowl, room descriptions and mascot hints still reference the pre-trap hiding spot (e.g., "wedged behind the espresso machine") instead of acknowledging the trapped state. Players may be confused about whether the trap worked.

2. **[Spatial] ASCII art directional arrows conflict with compass directions.** The DINING ASCII scene shows `[ COUNTER -> ]` (suggesting east/right), but the compass direction is WEST. The COUNTER ASCII scene shows `KITCHEN ->` (suggesting east/right), but the compass direction is NORTH. Players who read the ASCII art directionally will be confused.

### Low Priority

3. **[Physical] Apron visible from KITCHEN but only takeable from COUNTER.** The apron hangs "by the kitchen door" and LOOK APRON works from both rooms, but TAKE APRON only works from COUNTER. Since the item is on the boundary between rooms, it should arguably be takeable from either side.

4. **[Logical] GRAB verb routing is ambiguous.** `grab` routes to TAKE (not CATCH) due to if-chain ordering. Works for `grab mascot` via redirect, but `grab` alone returns "Take what?" instead of catch behavior.

5. **[Spatial] ALLEY appears in hint bar despite being unreachable.** The "go alley" hint button in the KITCHEN suggests it is a real destination, but it always refuses. This could waste player time or cause confusion.

6. **[Logical] Dead code in handleCatch.** The `isMascotInDining()` branch (lines 1567-1571) has an empty body and can never be reached in a way that differs from the else branch. No player impact but confusing code.

### Informational

7. **[Physical] Bowl removal during win sequence is implicit.** The transition from "trapped under bowl" to "sweep apron over mascot" skips the step of removing the bowl. Could add a line about lifting the bowl for completeness.

8. **[Canon] Uchujin-kun is not from the source material.** Original game creation, but fits well. Not a problem.
