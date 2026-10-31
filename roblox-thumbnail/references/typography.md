# Typography

**rxz** · the title, measured.

Type is the only part of a thumbnail that is always readable or always broken. It is also the part image models
cannot do. This file is the spec `scripts/thumb.py` implements — read it when you need to argue with the default.

---

## The numbers

| Thing | Value | Why |
|---|---|---|
| Canvas | 1920 × 1080 | 16:9, the only ratio Roblox serves |
| Safe margin | 6% (115 px) | Crops and platform chrome live in the last few percent |
| Reserved corner | bottom-right 18% × 14% | Name, player count and badges land near there on several surfaces |
| Text block width | ≤ 62% of frame (1190 px) | Leaves the hero visible beside it |
| Cap height | 12–18% of frame height | Below 12% it dies at tile size; above 18% it eats the art |
| Lines | 1–2 (3 only in clean style) | Three lines of shout is a poster |
| Words | 0–3 | Four is a sentence |
| Stroke | 6–9% of cap height | Thicker closes counters and reads as a sticker |
| Shadow | 8 px down, 35% black | Separates from busy art without a box |
| Contrast | ≥ 4.5:1 vs the art under it, 7:1 preferred | The tile is small and often dim |

---

## Style choices

**Shout (Anton, uppercase).** The default for action, horror, PvP, tycoon. Tight leading (0.92), heavy stroke,
one accent word in the accent colour. All caps removes the descender problem and reads at any size.

**Clean (Inter ExtraBold, sentence case).** For cozy, roleplay, simulator, update announcements. Less stroke, more
space, often a soft scrim instead of an outline. It looks like a product, not a poster — use it when the art is
soft.

**None.** A strong image with no words is not a missed opportunity; it is a confident thumbnail. If the action is
already legible and the game name is under the tile, adding "EPIC GAME" makes it worse.

**Kicker (Barlow Condensed ExtraBold, small, letterspaced).** One short line above the title: `UPDATE`, `NEW`,
`CHAPTER 2`. Only if it is true and recent. A permanent "NEW" is a lie players learn to ignore.

---

## Placement

```
┌──────────────────────────────────────────────┐
│  safe 6%                                     │
│   ┌────────────────────────────┐             │
│   │                            │             │
│   │        HERO                │             │
│   │                    ┌───────┴──────┐      │
│   │   TITLE ZONE       │  reserved    │      │
│   │   (lower-left)     │  bottom-right│      │
│   └────────────────────┴──────────────┘      │
└──────────────────────────────────────────────┘
```

- **Lower-left** is the default: it is where the eye finishes, and it is clear of the platform corner.
- **Top-left** when the hero occupies the lower half (Object as Hero, top-down shots).
- **Right** only if the subject is left and the right side is genuinely empty. Keep it out of the bottom-right.
- **Never over the face.** If the only empty space is on the face, the composition is wrong; go back to the prompt.

The script picks the zone from the brief and refuses to place text outside the safe area. If it warns, move the
zone or shorten the words — do not shrink the type to fit a bad layout.

---

## Writing the words

**Do** use a verb, a number, or a two-word hook:

- `SOLD OUT`
- `1V1 ME`
- `NEW PET`
- `DON'T FALL`
- `WAVE 50`
- `200 MPH`

**Don't** use:

- The game's own name (it is already under the tile).
- `BEST GAME EVER`, `100% FREE`, `INSANE` — claims nobody believes.
- Fake numbers (`+9999`) — reads as a scam ad.
- Sentences, punctuation you would not say aloud, or two ideas at once.

**One accent word.** Colour only the word that carries the meaning (`SOLD` white, `OUT` red). Colouring the whole
line removes the hierarchy; colouring three words removes the accent.

---

## Contrast and legibility

Text survives because of *local* contrast, not global brightness.

- White type over a dark, cool image is the safest combination.
- Over a bright sky, either move the block into a shadowed area or use a soft scrim — never a hard black box.
- A scrim is a vertical gradient covering the bottom 40–55%, from 55% black at the edge to transparent. It reads
  as lighting, not as a rectangle.
- If the words need a 20 px stroke to be readable, the placement is wrong.

The compositor writes `thumbnail-grey.png` for exactly this reason: if the type disappears in greyscale, the value
relationship is wrong, and colour will not save it.

---

## Testing

1. Open `thumbnail-256.png` at actual size. Read the title in under a second.
2. Squint. The title should still be a shape, even if the letters blur.
3. Cover the title. Does the image still communicate? If yes, the type is additive — keep it short.
4. Look at the tile beside nine others. Is the type bigger than theirs, or just louder?
