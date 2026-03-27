# SPEC.md — Birthday ARG (lzmplk-2026)

> Three-puzzle ARG for girlfriend's birthday. Early 2000s Manila blog aesthetic meets retro gaming.

## Overview

A password-protected puzzle chain deployed to `perseidpixels.co/lzmplk/`. Each puzzle's answer unlocks the next page. Final reveal: birthday message + Tiny Glade Steam key.

**Target date:** 2026-03-28 (birthday)

---

## Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Page 0        │     │   Puzzle 1      │     │   Puzzle 2      │     │   Puzzle 3      │     │   Prize         │
│   Tutorial      │────▶│   Rebus/Trivia  │────▶│   H2G2 Text     │────▶│   Pokemon on    │────▶│   Birthday      │
│                 │     │                 │     │   Adventure     │     │   3D GBA        │     │   Reveal        │
│   pw: birthday  │     │   pw: puzzle1   │     │   pw: puzzle2   │     │   pw: puzzle3   │     │   pw: prize     │
│                 │     │                 │     │                 │     │                 │     │                 │
│   explains how  │     │   reveals:      │     │   reveals:      │     │   reveals:      │     │   message +     │
│   ARG works     │     │   "puzzle2"     │     │   "puzzle3"     │     │   "prize"       │     │   Steam key     │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
     index.html             puzzle1.html            puzzle2.html            puzzle3.html            prize.html
```

### Password Chain

| Page | File | Encrypted With | Purpose | Reveals |
|------|------|---------------|---------|---------|
| Page 0 | index.html | `birthday` | Tutorial — explains how ARG works | `puzzle1` |
| Puzzle 1 | puzzle1.html | `puzzle1` | Rebus/Trivia game | `puzzle2` |
| Puzzle 2 | puzzle2.html | `puzzle2` | H2G2 Text Adventure | `puzzle3` |
| Puzzle 3 | puzzle3.html | `puzzle3` | Pokemon on 3D GBA | `prize` |
| Prize | prize.html | `prize` | Birthday message + Steam key | — |

---

## Visual Themes

### Page 0 & Puzzle 1: Early 2000s Manila Blog

**Aesthetic:** #fvckinerd energy. Blogger/Blogspot circa 2003-2006. Preteen Manila girl blog (not glittery).

**Elements:**
- Heart cursor (custom SVG)
- Marquee welcome text
- Comic Neue + Georgia fonts
- Dashed borders, cream/dusty pink palette (#faf8f5, #d4a5a5, #6b5b6b)
- Fake visitor counter (000001)
- Blogroll links (about | links | restart?)
- #fvckinerd footer
- Decorative dividers (─ ･ ｡ﾟ☆: *.☽ .* :☆ﾟ. ─)
- ASCII bunny art
- Custom scrollbar (pink on cream)

**Page 0 (Tutorial):**
- Welcome message
- Explains the ARG concept (solve puzzles → unlock next page)
- Gives first password hint or freebie

**Puzzle 1 (Rebus/Trivia):**
- Rebus puzzles (she loves these!)
- Possibly mixed with relationship trivia
- Answer reveals "puzzle2"

**References:**
- [thehtml.review](https://thehtml.review) — minimalist, text-forward, web-native
- [chia.design](https://chia.design) — handmade web, ASCII touches, intentional minimalism
- Cameron's World — Geocities archive energy

### Puzzle 2: H2G2 Text Adventure (Terminal)

**Aesthetic:** Hitchhiker's Guide to the Galaxy / Infocom interactive fiction. Green phosphor terminal.

**Elements:**
- VT323 monospace font
- Green on black (#00ff00 on #0a0a0a)
- CRT scanline effect (CSS)
- ASCII scene window (room visualization)
- Room description panel
- Scrolling command history
- Command input with `> ` prompt
- Clickable hint commands
- Text shadow glow effect

**Gameplay:**
- Mini escape room puzzle
- Commands: look, take, read, examine, use X on Y, inventory, help
- Solve puzzle → reveals password "puzzle3"
- Objects: NOTE (cipher/riddle), KEY, PUZZLE BOX, DOOR

**Mockup:** `mockup-p2.html`

### Page 3: 3D GBA + Pokemon Game

**Aesthetic:** Geocities maximalism + Vaporwave/Y2K mashup

**Elements:**
- Three.js 3D scene
- Game Boy Advance SP model (Sketchfab, CC Attribution)
  - Source: https://sketchfab.com/3d-models/gameboy-advance-sp-b79bb731b6b844fd8c61bee31e26a323
  - Credit: Smoggybeard
- Pokemon game renders on GBA screen
- Starfield/grid background
- Chrome gradients, lens flares, glow effects
- Subtle rotation on hover/drag

**Pokemon Game (on GBA screen):**
- "Wild [Pokemon] appeared!" encounter
- Simple battle or catch mechanic
- Sprites from [Spriters Resource](https://www.spriters-resource.com/)
- Solving/catching reveals "prize" password
- Prize unlocks birthday message + Tiny Glade Steam key

---

## Technical Stack

### Encryption
- **staticrypt** (v3.5.4) — AES-256 client-side encryption
- Custom template (`template.html`) with themed password prompt
- `--remember 1` — password cached for 1 day (survives refresh)

### Deployment
- **Host:** perseidpixels.co/lzmplk/
- **Server:** DigitalOcean droplet (ubuntu-s-1vcpu-1gb-sgp1-01)
- **Web server:** nginx
- **SSL:** Let's Encrypt (certbot)

### Build Commands

```bash
# Encrypt all pages
cd ~/projects/perseidpixels-co/lzmplk

npx staticrypt src/index.html -p "birthday" -d . -t template.html \
  --template-title "welcome" --template-button "enter →" \
  --template-placeholder "the password?" --template-error "nope!" \
  --template-instructions "hint: what day is it?" --short --remember 1

npx staticrypt src/puzzle1.html -p "puzzle1" -d . -t template.html \
  --template-title "puzzle 1" --template-button "enter →" \
  --template-placeholder "the password?" --template-error "nope!" \
  --short --remember 1

npx staticrypt src/puzzle2.html -p "puzzle2" -d . -t template.html \
  --template-title "puzzle 2" --template-button "enter →" \
  --template-placeholder "the password?" --template-error "nope!" \
  --short --remember 1

npx staticrypt src/puzzle3.html -p "puzzle3" -d . -t template.html \
  --template-title "puzzle 3" --template-button "enter →" \
  --template-placeholder "the password?" --template-error "nope!" \
  --short --remember 1

npx staticrypt src/prize.html -p "prize" -d . -t template.html \
  --template-title "🎂" --template-button "enter →" \
  --template-placeholder "the password?" --template-error "nope!" \
  --short --remember 1
```

### Directory Structure

```
lzmplk-2026/
├── SPEC.md              # This file
├── template.html        # Staticrypt password prompt template
├── reset.html           # Clears localStorage, redirects to start
├── 404.html             # Themed 404 page
├── index.html           # Encrypted Page 0 (tutorial)
├── puzzle1.html         # Encrypted Puzzle 1 (rebus/trivia)
├── puzzle2.html         # Encrypted Puzzle 2 (H2G2 adventure)
├── puzzle3.html         # Encrypted Puzzle 3 (Pokemon on GBA)
├── prize.html           # Encrypted Prize (birthday reveal)
├── mockup-p2.html       # H2G2 text adventure mockup (working prototype)
├── src/                 # Unencrypted source files
│   ├── index.html       # Page 0 content (tutorial)
│   ├── puzzle1.html     # Puzzle 1 content (rebus/trivia)
│   ├── puzzle2.html     # Puzzle 2 content (H2G2 adventure)
│   ├── puzzle3.html     # Puzzle 3 content (Pokemon game)
│   └── prize.html       # Prize content (birthday reveal)
└── assets/              # (to be created)
    ├── gba-sp.glb       # 3D GBA model (download from Sketchfab)
    ├── pokemon/         # Pokemon sprites
    ├── photo.jpg        # Birthday photo
    └── u2.mp3           # "With or Without You"
```

---

## Puzzle Content (TBD)

### Page 0: Tutorial
- Type: Welcome/intro page
- Purpose: Explains the ARG, sets the mood
- Gives: Password "puzzle1" (freebie or very easy hint)

### Puzzle 1: Rebus/Trivia
- Type: Visual rebus puzzles + relationship trivia
- Answer: "puzzle2"
- She loves rebus puzzles
- Could mix in inside jokes / shared memories

### Puzzle 2: H2G2 Text Adventure
- Type: Interactive fiction escape room
- Answer: "puzzle3"
- Working mockup at `mockup-p2.html`

### Puzzle 3: Pokemon Game
- Type: Mini Pokemon encounter on 3D GBA
- Answer: "prize"
- Catch/battle mechanic reveals the password

### Prize: Birthday Reveal
- Type: Final celebration page
- Content: Birthday message, photo, audio ("With or Without You")
- Gift: Tiny Glade Steam key

---

## Assets Needed

- [ ] Photo(s) for final reveal
- [ ] Audio: "With or Without You" - U2 (for final page or throughout)
- [ ] GBA SP 3D model (Sketchfab download)
- [ ] Pokemon sprites (Spriters Resource)
- [ ] Tiny Glade Steam key (for gift box)
- [ ] Rebus puzzle images/content

---

## Features

### Implemented
- [x] Staticrypt encryption with custom template
- [x] Early 2000s Manila blog aesthetic (template)
- [x] Heart cursor
- [x] Marquee text, blinking elements
- [x] Fake visitor counter, #fvckinerd, blogroll
- [x] Reset functionality (clears localStorage)
- [x] Remember password for 1 day
- [x] H2G2 text adventure mockup (mockup-p2.html)
- [x] Custom 404 page

### To Build
- [ ] Page 0 content (tutorial)
- [ ] Puzzle 1 content (rebus/trivia)
- [ ] Integrate H2G2 adventure into puzzle2
- [ ] 3D GBA with Three.js for puzzle3
- [ ] Pokemon game on GBA screen
- [ ] Prize page with birthday reveal (photo/audio/Steam key)
- [ ] Rename files to new structure (puzzle1.html, puzzle2.html, etc.)
- [ ] Re-encrypt with new password chain
- [ ] nginx 404 config for /lzmplk/

---

## nginx Config

Add to `/etc/nginx/sites-available/perseidpixels.co`:

```nginx
location /lzmplk/ {
    try_files $uri $uri/ $uri.html /lzmplk/404.html;
}
```

Script at `/tmp/update-nginx-404.sh` (run with sudo).

---

## Personal Details

- Pet name: (TBD)
- Inside jokes to weave in: (TBD)
- U2 song: "With or Without You"
- Gift: Tiny Glade Steam key

---

## References

- [staticrypt](https://github.com/robinmoisson/staticrypt) — client-side encryption
- [thehtml.review](https://thehtml.review) — design inspiration
- [chia.design](https://chia.design) — design inspiration
- [Cameron's World](https://www.cameronsworld.net/) — Geocities archive
- [Sketchfab GBA SP](https://sketchfab.com/3d-models/gameboy-advance-sp-b79bb731b6b844fd8c61bee31e26a323) — 3D model (CC Attribution, credit: Smoggybeard)
- [Spriters Resource](https://www.spriters-resource.com/) — Pokemon sprites
