# THE SHIFT — Complete Game Design

> A Maid Latte text adventure for puzzle 2 of the birthday ARG.

## The Problem

How do you design a text adventure that:
1. **Never dead-ends** — every state has a path forward
2. **Progressively discloses** — hints escalate naturally with struggle
3. **Feels like Maid-Sama!** — captures Usui/Misaki dynamic authentically

---

## Core Insight: The Hint Escalation Model

Traditional text adventures punish exploration with death or soft-locks. We invert this: **every "wrong" action teaches something useful.**

```
Player Action
     │
     ▼
┌─────────────────────────────────────────┐
│  Does this advance the puzzle?          │
│                                         │
│  YES ──► Progress + positive feedback   │
│                                         │
│  NO ───► Hint + character moment        │
│          (Usui teases, Satsuki gushes,  │
│           environment reacts)           │
└─────────────────────────────────────────┘
```

The hint system has **three tiers**:
- **Tier 1 (attempts 0-2):** Vague, atmospheric hints
- **Tier 2 (attempts 3-5):** Clearer direction from NPCs
- **Tier 3 (attempts 6+):** Explicit instructions

---

## Game State Model

### State Variables

```python
@dataclass
class GameState:
    location: Literal["DINING", "COUNTER", "KITCHEN"]
    mascot_location: Literal["TABLE1", "TABLE2", "TABLE3", "COUNTER", "KITCHEN"]
    inventory: set[str]  # {"APRON", "TRAY"}

    # Progress flags
    found_mascot: bool = False      # Spotted it at least once
    talked_usui: bool = False       # Got hint from Usui
    talked_satsuki: bool = False    # Got hint from Satsuki
    attempted_catch: int = 0        # Failed catch attempts
    mascot_caught: bool = False     # WIN STATE

    # Hint escalation
    hint_tier: int = 1              # 1, 2, or 3
```

### Location Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAID LATTE                              │
│                                                                 │
│  ┌───────────────┐      ┌───────────────┐      ┌─────────────┐ │
│  │    KITCHEN    │◄────►│    COUNTER    │◄────►│   DINING    │ │
│  │               │      │               │      │             │ │
│  │  • Satsuki    │      │  • Usui       │      │  • Table 1  │ │
│  │  • Tray       │      │  • Register   │      │  • Table 2  │ │
│  │  • Apron      │      │               │      │  • Table 3  │ │
│  │  • Treats     │      │               │      │  • Customers│ │
│  └───────────────┘      └───────────────┘      └─────────────┘ │
│                                                                 │
│  Movement: GO KITCHEN, GO COUNTER, GO DINING, GO TABLE [1-3]   │
└─────────────────────────────────────────────────────────────────┘
```

### Mascot Movement Pattern

The mascot moves **every 3 commands** if not caught:

```
TABLE2 → TABLE1 → TABLE3 → COUNTER → KITCHEN → TABLE2 (loop)
```

This creates urgency without punishment — player can always find it again.

---

## Complete Command Set

### Universal Commands (work anywhere)

| Command | Effect |
|---------|--------|
| `LOOK` | Describe current location + visible objects |
| `INVENTORY` / `I` | List held items |
| `HELP` | Show available commands |
| `EXAMINE [thing]` | Detailed description |

### Movement Commands

| Command | Valid From | Effect |
|---------|------------|--------|
| `GO KITCHEN` | COUNTER, DINING | Move to kitchen |
| `GO COUNTER` | KITCHEN, DINING | Move to counter |
| `GO DINING` | COUNTER, KITCHEN | Move to dining area |
| `GO TABLE [1-3]` | DINING | Focus on specific table |

### Interaction Commands

| Command | Target | Precondition | Effect |
|---------|--------|--------------|--------|
| `TALK USUI` | Usui | At COUNTER | Hint (tier-dependent) |
| `TALK SATSUKI` | Satsuki | At KITCHEN | Hint about catching method |
| `TAKE APRON` | Apron | At KITCHEN | Add to inventory |
| `TAKE TRAY` | Tray | At KITCHEN | Add to inventory |
| `CATCH MASCOT` | Mascot | Same location | Attempt catch (fails without apron) |
| `USE APRON` | Mascot | Has apron, same location | WIN |
| `USE TRAY` | — | Has tray | Makes noise, mascot pauses 1 turn |

### Easter Egg Commands

| Command | Response |
|---------|----------|
| `PUNCH USUI` | "He sidesteps gracefully. 'Missed me, Kaichou~'" |
| `KISS USUI` | "W-what?! Your face turns bright red. Usui looks intrigued. 'Interesting strategy, Misa-chan.'" |
| `YELL` | "Several customers look alarmed. Usui looks delighted." |
| `IGNORE USUI` | "You feel his amused gaze on your back." |
| `EXAMINE USUI` | "Tall. Annoyingly handsome. Currently wearing that infuriating smirk." |

---

## Dialogue Trees by Character

### USUI TAKUMI

**Addressing Misaki:** "Ayuzawa" (formal), "Misa-chan" (teasing), "Kaichou" (playful)

#### Tier 1 Hints (vague, teasing)

```
TALK USUI [first time]:
    "Pu."
    He's watching something dart under the tables with mild interest.
    "Lively today, isn't it?"

TALK USUI [mascot visible, tier 1]:
    "That thing moves fast."
    His eyes follow the mascot.
    "...Almost like it's running from something. Or someone~"

TALK USUI [mascot not visible, tier 1]:
    "Looking for something, Ayuzawa?"
    That infuriating smirk.
    "I might have seen something green go that way."
    [Points toward mascot's current location]
```

#### Tier 2 Hints (clearer direction)

```
TALK USUI [tier 2]:
    "You know..."
    He leans on the counter.
    "Chasing it directly doesn't seem to be working."
    "Maybe try... a different approach?"
    [If not talked to Satsuki: "The manager seems excited about something."]

TALK USUI [has apron, tier 2]:
    "Ah. You found it."
    He nods at the apron.
    "Soft things are good for catching soft things, Misa-chan."
```

#### Tier 3 Hints (explicit)

```
TALK USUI [tier 3]:
    "Ayuzawa."
    He's stopped smirking. Almost looks... helpful?
    "Use the apron. It's in the kitchen. Throw it over the mascot."
    "...You're welcome."
```

#### Win State Dialogue

```
[After catching mascot with apron]:
    Usui appears beside you. How does he move so quietly?

    "Interesting mascot, Misa-chan."
    He examines Uchūjin-kun.
    "Green. Alien. Vaguely familiar somehow..."

    Your face burns.

    "I like it."
    He tucks a small note into your apron pocket.
    "The password to the next room is: [PASSWORD]"

    "Don't lose that one too~"
```

---

### SATSUKI HYŌDŌ (Manager)

**Speech style:** Enthusiastic, moe-obsessed, exclamation marks

#### Standard Interactions

```
TALK SATSUKI [first time]:
    "Misa-chan! Did you see it?!"
    Her eyes are sparkling dangerously.
    "A MASCOT! In MY cafe! It's so MOE!"
    "You have to catch it gently! Use something soft!"

TALK SATSUKI [after first]:
    "The apron! Use the apron!"
    She gestures frantically at the hook.
    "Soft fabric! It won't hurt the little darling!"

EXAMINE SATSUKI:
    The manager of Maid Latte.
    Currently vibrating with excitement over the escaped mascot.
    Her costume-making instincts have been activated.
```

---

### UCHŪJIN-KUN (The Mascot)

**Description:** A small alien plushie. Green. Suspiciously Usui-shaped if you squint.

```
EXAMINE UCHŪJIN-KUN:
    A palm-sized alien plushie with big eyes and a knowing smirk.
    Green body, silver antennae.
    You definitely didn't buy it because it reminded you of anyone.
    ...
    It's looking at you.

TALK UCHŪJIN-KUN:
    It doesn't respond.
    Unlike some perverted outer-space aliens you know.

CATCH UCHŪJIN-KUN [no apron]:
    You lunge for it—
    It bounces away at the last second.
    Was that thing always this fast?!
    [mascot moves to next location]
    [attempted_catch += 1]

CATCH UCHŪJIN-KUN [with apron, USE APRON]:
    You sweep the apron over the mascot in one smooth motion.
    Got it!
    Uchūjin-kun squirms under the fabric, then settles.

    [WIN STATE - trigger Usui's final dialogue]
```

---

## Complete Game Tree

### Win Conditions

There is exactly **ONE win condition:**
- `USE APRON` (or `USE APRON ON MASCOT`) while:
  - Player has APRON in inventory
  - Player is in same location as mascot

### State Transitions

```
┌─────────────────────────────────────────────────────────────────┐
│                      GAME START                                 │
│                                                                 │
│  Location: DINING                                               │
│  Mascot: TABLE2                                                 │
│  Inventory: []                                                  │
│  Hint tier: 1                                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXPLORATION PHASE                            │
│                                                                 │
│  Player can:                                                    │
│  • LOOK — discover mascot location                              │
│  • GO [location] — navigate cafe                                │
│  • TALK USUI — get hints (tier-dependent)                       │
│  • TALK SATSUKI — learn about apron                             │
│  • EXAMINE [anything] — world-building + hints                  │
│                                                                 │
│  Hint tier escalates after 3, 6 failed attempts                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ACQUISITION PHASE                            │
│                                                                 │
│  Player realizes they need APRON:                               │
│  • Direct discovery: EXAMINE KITCHEN, LOOK in KITCHEN           │
│  • Satsuki hint: "Use something soft!"                          │
│  • Usui hint (tier 2+): "The manager seems excited"             │
│  • Usui hint (tier 3): "Use the apron. It's in the kitchen."    │
│                                                                 │
│  TAKE APRON — adds to inventory                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CATCH PHASE                                │
│                                                                 │
│  Player must:                                                   │
│  1. Locate mascot (LOOK, or track movement pattern)             │
│  2. Go to mascot's location                                     │
│  3. USE APRON                                                   │
│                                                                 │
│  Optional: USE TRAY first to freeze mascot for 1 turn           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       WIN STATE                                 │
│                                                                 │
│  • Mascot caught                                                │
│  • Usui delivers password                                       │
│  • Link to puzzle3.html appears                                 │
└─────────────────────────────────────────────────────────────────┘
```

### No Dead-End Proof

Every state has a valid forward path because:

1. **Mascot loops infinitely** — it never escapes or disappears
2. **Apron is always available** — no preconditions to TAKE APRON
3. **Hints escalate** — player will eventually get explicit instructions
4. **No consumables** — apron doesn't break, can retry infinitely
5. **No timing failures** — mascot movement creates urgency but not death

---

## Progressive Disclosure Matrix

| Attempts | Usui Hint | Satsuki Hint | Environment |
|----------|-----------|--------------|-------------|
| 0-2 | "Lively today" | "So moe!" | Mascot visible when in same room |
| 3-5 | "Different approach?" | "Use something soft!" | Failed catches mention mascot's speed |
| 6+ | "Use the apron. Kitchen." | "THE APRON!" | Description explicitly mentions apron when in kitchen |

### Hint Trigger Conditions

```python
def get_hint_tier(state: GameState) -> int:
    total_attempts = state.attempted_catch
    if total_attempts >= 6:
        return 3
    elif total_attempts >= 3:
        return 2
    return 1

def should_escalate_environment_hints(state: GameState) -> bool:
    """Make environmental descriptions more helpful"""
    return state.hint_tier >= 2 or state.attempted_catch >= 2
```

---

## Room Descriptions

### DINING (Start Location)

```
LOOK [tier 1]:
    Maid Latte's dining area.

    Three tables with customers enjoying their parfaits.
    The gentle hum of conversation fills the air.

    To the WEST is the COUNTER. Through the door, the KITCHEN.

    [If mascot here]: Something green darts under TABLE [N].

LOOK [tier 2+]:
    Maid Latte's dining area.

    Three tables. Customers. The usual.

    [If mascot here]: Uchūjin-kun is clearly visible under TABLE [N].
    You could try to CATCH it... if you had something to catch it WITH.
```

### COUNTER

```
LOOK:
    The service counter.

    Usui is leaning against it, watching you with that look.
    The cash register sits unused. No customers waiting.

    DINING is to the EAST. KITCHEN through the back.

    [If mascot here]: The mascot has somehow gotten onto the counter.
    Usui is poking it experimentally. "Pu."
```

### KITCHEN

```
LOOK [tier 1]:
    The kitchen.

    Satsuki is here, practically bouncing with excitement.
    Pots, pans, and maid costumes in various states of completion.
    An APRON hangs on a hook. A metal TRAY sits on the counter.

    [If mascot here]: Uchūjin-kun has found the treat cabinet.

LOOK [tier 2+]:
    The kitchen.

    Satsuki. Cooking stuff. Costumes.
    There's an APRON on the hook. It looks soft. Good for catching things.
    A TRAY might make useful noise.
```

---

## Implementation Notes

### Command Parser

Accept flexible input:
```
Canonical: USE APRON ON MASCOT
Also accept:
  - USE APRON
  - CATCH MASCOT WITH APRON
  - THROW APRON AT MASCOT
  - APRON MASCOT
  - CATCH
```

### Mascot Movement Timer

```javascript
let commandCount = 0;
const MOVE_INTERVAL = 3;

function processCommand(cmd) {
    commandCount++;
    if (commandCount % MOVE_INTERVAL === 0 && !state.mascotCaught) {
        moveMascot();
    }
    // ... handle command
}
```

### Failure Messages (Vary to avoid repetition)

```javascript
const catchFailMessages = [
    "You lunge — it bounces away!",
    "Almost! It slips through your fingers.",
    "The mascot zips past your grabbing hands.",
    "Uchūjin-kun: 1, Misaki: 0",
    "It's faster than it looks...",
];
```

---

## Password Reveal

The password that unlocks puzzle3.html should be:
- **Thematically appropriate** — related to Maid-Sama! or the relationship
- **Not guessable** — unique enough that players must complete the puzzle

Suggestions:
- `misachan` — Usui's nickname for her
- `ayuzawa` — her name, from Usui's perspective
- `outerspace` — callback to "perverted outer-space alien"
- `[user's choice]` — you mentioned changing passwords later

---

## File Structure

```
puzzle2.html          ← Encrypted with staticrypt, password "puzzle2"
├── Embedded CSS      ← Terminal aesthetic (VT323, green on black, CRT effect)
├── Embedded JS       ← Game engine
│   ├── GameState     ← State management
│   ├── CommandParser ← Input handling
│   ├── Renderer      ← Output display
│   └── DialogueTree  ← Character responses
└── Game Data         ← Rooms, objects, dialogue (JSON or inline)
```
