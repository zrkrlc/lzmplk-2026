# AFTER CLASS — Consolidated Audit Findings

**Date:** 2026-03-28
**Auditors:** claude-opus-4-6 (computational + physical)

---

## Executive Summary

| Category | Issues |
|----------|--------|
| Unreachable entities | 2 (pots/pans, cutting board) |
| Partially reachable | 3 (knife, apron from kitchen, treat cabinet) |
| Disclosure violations | 2 (knife visible before LOOK, OPEN CABINET works before LOOK) |
| Spatial inconsistencies | 3 (ASCII arrows vs compass, ALLEY in hints) |
| Physical issues | 2 (apron take asymmetry, bowl removal implicit) |
| Logical contradictions | 3 (trapped mascot desc, GRAB verb, dead code) |
| Canon issues | 0 (Uchujin-kun is original but fits) |
| Easter eggs | 21 (all well-crafted) |

---

## Priority 1: Must Fix Before Gift

### 1. Knife escapes progressive disclosure
- **Location:** `getRoomDesc()` for KITCHEN
- **Issue:** Knife block is OUTSIDE `if (state.kitchenLooked)` — appears before LOOK AROUND
- **Fix:** Move knife display inside the kitchenLooked gate

### 2. OPEN CABINET/DRAWER works before LOOK AROUND
- **Location:** `handleOpen()`
- **Issue:** Player can bypass disclosure by typing OPEN CABINET before LOOK AROUND
- **Fix:** Add guard: if `!state.kitchenLooked`, return "You should look around first."

### 3. Missing LOOK KNIFE handler
- **Location:** `handleLook()`
- **Issue:** LOOK KNIFE returns generic fallback despite knife having item styling
- **Fix:** Add handler: "A bread knife on the cutting board. Sharp but... no. You're not THAT desperate."

### 4. Trapped mascot still shows old hiding-spot text
- **Location:** `getRoomDesc()` and mascot hint functions
- **Issue:** After USE BOWL, descriptions still say "wedged behind espresso machine" etc.
- **Fix:** Add check: if `state.mascotTrapped && isMascotVisible()`, show "trapped under the bowl"

---

## Priority 2: Should Fix

### 5. ASCII art directions conflict with compass
- **Issue:** COUNTER ASCII shows `KITCHEN ->` (right), but compass says NORTH
- **Suggestion:** Use informal directions everywhere ("through back", "towards dining") OR fix ASCII layout

### 6. ALLEY appears in hint bar despite being unreachable
- **Location:** `updateHints()` KITCHEN section
- **Fix:** Remove `go alley` from hints, or gray it out

### 7. Apron visible from KITCHEN but only takeable from COUNTER
- **Issue:** LOOK APRON works from kitchen side, but TAKE fails
- **Suggestion:** Either allow TAKE from kitchen, or remove LOOK APRON kitchen response

### 8. Add LOOK handlers for pots/pans and cutting board
- **Issue:** Mentioned in descriptions but not lookable
- **Fix:** Add simple one-liner responses

---

## Priority 3: Nice to Have

### 9. Bowl removal implicit in win sequence
- **Issue:** Goes from "trapped under bowl" to "sweep apron" without lifting bowl
- **Suggestion:** Add line: "You carefully lift the bowl—"

### 10. GRAB verb routing ambiguity
- **Issue:** `grab` alone returns "Take what?" instead of catch behavior
- **Minor:** Works for `grab mascot` via redirect

### 11. Dead code in handleCatch
- **Issue:** `isMascotInDining()` branch has empty body
- **Fix:** Clean up for maintainability

---

## Easter Eggs (All Working)

### Ambient Commands
- LISTEN (room-specific sounds)
- SMELL (room-specific scents)
- THINK (internal monologue + hints)
- WAIT (existential dread)

### Usui Interactions
- KISS USUI (nuclear blush)
- HUG USUI (survival instincts)
- PUNCH/HIT/SLAP/KICK USUI (catches wrist)
- IGNORE USUI ("I'll wait, Ayuzawa")
- BLUSH (he notices)
- YELL/SCREAM ("PERVERTED OUTER-SPACE ALIEN!")

### Canon References
- MOE (summons Satsuki)
- CHESS (beat a champion)
- ROOFTOP/FALL (survived)
- CALL MOM (she can NEVER know)
- CRY (Idiot Trio reference)
- QUIT (Misaki doesn't quit)
- Table 3 customer (Aoi Hyoudou cameo)
- LOOK SHRINE (Misaki/Usui photo, "SATSUKI.")

### Failure States (Educational)
- USE KNIFE on mascot (horrible feeling)
- USE BAG (tears through)
- USE TREATS (snatches and bolts)
- CATCH bare-handed (progressive hints)

---

## Validation Results

From `validate_game_tree.py`:
- **1,110 reachable states**
- **30 win states**
- **0 dead ends**
- **All progressive disclosure gates verified**
- **Optimal path: 10 steps**

---

## Files Created

- `AUDIT.md` — Computational audit (entity reachability, hints, disclosure)
- `AUDIT-PHYSICAL.md` — Physical/logical audit (spatial, interactions, canon)
- `command-map.html` — Full command reference per room
- `game-tree.html` — Visual state tree
