---
name: roblox-thumbnail
description: Art-direct a Roblox experience thumbnail that survives the Discover feed — onboarding interview first (game, genre, theme, promise, hero subject, title words, palette, references), then a composition archetype, an image prompt, a 1920×1080 title composite, and a graded anti-slop pass with a real 256 px legibility proof. Use whenever someone wants a Roblox thumbnail, game art, GFX, Discover art, a thumbnail refresh, a thumbnail for a new game or update, or says their game "isn't getting clicks" — and use it before generating any Roblox image, even when they only ask for "a cool picture for my game".
---

# roblox-thumbnail

**rxz** · v1.0 · no API key, no fixed image tool, no drawing by code.

A Roblox thumbnail is not a picture of your game. It is an advertisement roughly the size of a postage stamp,
seen for a fraction of a second, beside nine competitors. Almost every "AI thumbnail" failure is the same
mistake: making a 1920 px image for a 256 px slot.

This skill builds the 256 px version first — one subject, one promise, one word — then renders it large.

---

## The five laws

**1. One subject.** A viewer's eye needs somewhere to land. Two characters can work only when they are
*against* each other (Versus). Three or more is a poster, not a thumbnail, and at tile size it becomes texture.
Count the focal subjects before you prompt, and again after.

**2. The face carries the click.** At 40 px wide, a face is two eyes, a mouth and a silhouette. Neutral reads as
nothing. Pick one emotion and push it until a stranger could name it from across a room. If the hero has no face
(object, pet, vehicle), the *object's* shape and shine carry it instead — see Object as Hero.

**3. One promise, shown literally.** The image must show the thing a new player does in their first minute. Not
the lore, not the map, not the shop UI — the loop. A thumbnail that promises a boss fight for a game about
selling fish earns one click and one dislike, and Roblox's ranking reads both.

**4. Light before detail.** A single key light and a rim/backlight that separates the subject from the
background do more for perceived quality than any amount of added detail. Flat ambient light is the single
loudest "made by AI" tell.

**5. Text is added, never generated.** Image models cannot spell. One to three words, composited afterwards in
a real font, at a size that survives the tile. No text is often stronger than bad text — but a number, a verb or
a two-word hook can double the read.

These are the same rules the paid Roblox generators quietly follow in their own galleries: one hero, one prop,
one light, one word. The difference between them and slop is not the model. It is the brief.

---

## Step 1 — Onboarding: ask before you draw

**Never generate first and ask later.** A thumbnail is a promise about a specific game; guessing the genre is how
a pet simulator gets an anime boy with a sword, and how "three slop examples" become three copies of one image.

Ask all seven in one message, numbered, with a one-line reason for the ones people find odd. If the host has a
structured question tool, use it; otherwise plain numbered questions work.

| # | Ask | What it decides |
|---|---|---|
| 1 | **Game name and store link** (or paste the description) | I read it myself instead of asking you to summarise |
| 2 | **Genre** — obby, tycoon, simulator, horror, battlegrounds, roleplay, racing, tower defence, anime/gacha, "steal a", other | The archetype, palette and text style |
| 3 | **The one loop a new player does in their first minute** | The promise the image has to show |
| 4 | **Who or what is the hero of the shot** — your character, a pet, a vehicle, a build? Can you send a screenshot or render? | Identity. **Ask for a file or link.** Never invent a cast |
| 5 | **Theme and feeling** — e.g. neon night, sunny cartoon, grimy horror, candy pastel — and one emotion: fear, greed, triumph, chaos, cozy, awe | Palette and light |
| 6 | **Words on the image** — 0 to 3. Or "none" | Whether text exists at all |
| 7 | **References** — two thumbnails you love and two you hate, plus anything that must **not** appear | Taste, and the ban list |

The exact message to send, the branches ("just do it", no art, no genre, refreshing an old thumbnail) and the
answer-to-brief mapping are in `references/onboarding.md`. Read it before the first interview, not after.

Then say the quiet parts out loud, because they change the answer:

- If they name the game for the on-image text, point out the game name already sits under the tile. The words on
  the art should add something the title cannot.
- If the hero is "my avatar" and they have no screenshot, ask for **any** screenshot of their own game first. A
  real, badly lit screenshot beats an invented character every single time, because it is *theirs* and it matches
  what the player will actually see.
- If they answer "just do it", you may infer 1, 2, 3, 5 and 7 from the store page — but you still need 4 and 6.
  Those cannot be guessed, and guessing them is how the thumbnail ends up advertising a different game.

### Write the brief, show the card

Save the answers as `brief.json` (copy `assets/brief.template.json`, or run `python scripts/thumb.py init`).
Then show a seven-line art-direction card and get a yes before generating. It takes ten seconds to read and
saves a whole generation cycle:

```
GAME      Neon District (tycoon)
PROMISE   Buy your first shop, watch the queue form
HERO      your avatar grinning, cash in hand  (screenshot supplied)
FEELING   greedy triumph
THEME     magenta night, cyan neon, one warm gold
WORDS     "SOLD OUT"  (2)
NOT       other games' characters, default noob, anything the model writes
```

If any line is wrong, fix the brief — not the prompt.

---

## Step 2 — Pick one archetype

Six shapes cover almost everything. Pick **one**; a frame that tries two has no focal point. Across a set of ten
thumbnails, alternate archetypes so the gallery does not look like one image recoloured.

| Archetype | Shape | Best for | Fails when |
|---|---|---|---|
| **Hero Shot** | Subject fills 55–70%, low angle, one prop, background pushed back | Tycoon, simulator, battlegrounds, shop | Background is as loud as the subject |
| **Threat Behind** | Foreground hero reacting; antagonist looming; three depth planes | Horror, survival, "escape the..." | The threat is cropped or too small to read |
| **Versus** | Two subjects on a diagonal, facing each other | PvP, fighting, "1v1" | A third character sneaks in |
| **Object as Hero** | The reward at giant scale, 3/4 top-down, hard contact shadow | Pet sim, trading, "steal a", unboxing | No scale cue, so it reads as a sticker |
| **Action Freeze** | Mid-motion, streaks/debris, subject entering frame | Racing, obby, sports | Motion blur hides the face |
| **Before / After** | Same subject twice, split frame, visible transformation | Upgrades, "noob to pro", progression | The two halves differ in style, not just state |

Genre-specific shot ideas, palettes and failure modes are in `references/genre-playbook.md`; text zones and
safe areas are in `references/typography.md`.

---

## Step 3 — Write the prompt

One paragraph, in this order. Order matters: models weight the beginning hardest, and the style anchor fixes the
rendering language before any subject detail can fight it.

```
[STYLE ANCHOR] + [SUBJECT + IDENTITY] + [ACTION/POSE] + [PROP] + [SETTING]
+ [LIGHT] + [CAMERA] + [PALETTE] + [COMPOSITION] + [NEGATIVES]
```

- **Style anchor** — pick exactly one from `references/prompting.md`: toy-like 3D, cel-shaded anime, painterly
  cartoon, glossy product. Mixing two is the "AI collage" look.
- **Light** — name a direction and a colour: "single hard key from camera-left, cyan rim from behind". Never write
  "dramatic lighting"; it means nothing and returns mush.
- **Camera** — "35 mm, low angle, subject in the left third, shallow depth of field". Camera terms buy you
  composition, which is the thing you actually need.
- **Negatives** — always include: no text, no letters, no logos, no watermark, no extra characters, no collage,
  no split screen (unless the archetype *is* split), no UI.
- **Reference image** — if the user supplied one, say what to keep (silhouette, outfit, colours) and what to
  change (pose, background, lighting). Never let the model "improve" the identity.

Save the finished prompt as `prompt.txt` beside the brief, with the model and seed, so a reroll is one variable and
not a rebuild. Three fully written prompts, a negatives block and model settings are in `references/prompting.md`.

---

## Step 4 — Generate

Use whatever image tool this session can reach. If it has none, hand the user the prompt and stop there.

**Do not draw the thumbnail art in code.** Procedural art is fine as small filler inside a mock UI; as the hero
of a thumbnail it reads as placeholder, and placeholder is the one thing a thumbnail cannot be. This is the
single most common way an otherwise good agent produces a bad thumbnail.

- Generate **three seeds of one prompt**, not three different concepts. You are choosing a frame, not a strategy.
- **Look at all three before choosing.** Judge them at tile size, not full-screen — a frame that is impressive in
  the chat and illegible in the feed is the normal failure, not the rare one.
- If the model writes letters, reject that image. Regenerate with the no-text clause moved to the front; if it
  persists, crop or repaint the area. Garbled text is worse than no text.
- Keep the best candidate at full resolution. Do not upscale a 512 px image "because it is only a thumbnail" —
  Roblox serves large sizes on the experience page and hover states.
- Record the model, seed and prompt in the brief. You will want to reroll one variable, not start over.

---

## Step 5 — Composite the title

```bash
python scripts/thumb.py compose brief.json art.png -o thumbnail.png
```

The script guarantees the things models and humans both get wrong:

- **1920×1080**, cover-cropped from any input size, with the crop biased to the brief's `art.focus`.
- **Real typography**, never model lettering: Anton uppercased and tightly led for shout, Inter sentence case
  for clean, Barlow Condensed for the kicker. A stroke sized as a fraction of cap height, and optional one
  accent word.
- **Auto-fit**, so a long title shrinks or wraps instead of running off the edge, with the measured cap height
  printed as a percentage of frame height.
- **Safe zone**, keeping text out of the outer 6% and the bottom-right platform-chrome corner.
- **Proofs**, always: `thumbnail-256.png` (phone-class tile), `thumbnail-grey.png` (value check) and, with
  `--debug`, a safe-area overlay.
- **A text layer**, with `--text-only`, for anyone who wants to finish in Canva or Photopea.

Typography rules and the reasoning behind the numbers: `references/typography.md`.

---

## Step 6 — Grade it

```bash
python scripts/thumb.py check thumbnail.png
```

It prints numbers, not taste: resolution, whether the title is inside the safe zone, title word count, edge
clutter, tonal range, hue spread, focal concentration and title contrast. Treat FAIL as a blocker and WARN as a
question to answer by looking.

Then do the two looks the script cannot do:

1. **The 256 px look.** Open `thumbnail-256.png` at actual size, arm's length away. Can you tell what the game is
   and what you do in it, without reading the game name? If not, the concept is wrong, not the polish.
2. **The grey look.** `thumbnail-grey.png`. If the subject disappears into the background in greyscale, the
   lighting is too even — go back to the prompt, not the compositor.

Score it against `references/qa.md`. Two or more critical failures means **new concept**, not another polish pass.
Polishing a bad concept is how a thumbnail ends up technically clean and completely forgettable.

---

## Step 7 — Compare the set, then rotate

```bash
python scripts/thumb.py sheet a.png b.png c.png -o compare.png
```

That renders every candidate at true tile width, in colour and greyscale, side by side. Choose the one that wins
at that size — not the one that looks best full-screen in the chat.

Roblox allows up to ten thumbnails per experience. Use them: one hero shot, one gameplay proof, one reward, one
"what just happened" moment. Rotating the first slot over a week is the cheapest A/B test a Roblox game has, and
it costs nothing but a re-upload.

---

## Step 8 — Deliver

Give the user:

- `thumbnail.png` — 1920×1080, ready to upload.
- `thumbnail-256.png` — the proof, attached so they can judge it as players will.
- `brief.json`, `prompt.txt` — so the next one takes minutes, not a re-interview.
- One line of provenance: model, seed, prompt.
- The honest caveat: upload it, then look at the real tile on a phone. Roblox's crop and overlays are the only
  test that counts.

Do not add a watermark or a maker's mark unless asked. It costs clicks and reads amateur.

---

## The slop tells

If you see two or more of these, stop polishing and re-concept:

- Three or more characters, or the same face twice.
- A default blocky avatar in a neutral pose, mid-frame.
- Flat ambient light, no contact shadow, subject pasted on a background.
- Six saturated hues, or a rainbow gradient behind everything.
- Letters in the artwork — misspelled, doubled, or floating.
- Four or more words, or text in the bottom-right corner.
- The promise is not in the game (fake rewards, fake numbers, borrowed characters).
- Every element rendered in a different style: anime face, plastic body, painted sky.
- The subject is cropped by the frame edge, or the head touches the top.
- Ten thumbnails that are the same image in ten colourways.

The full catalogue, with why each one reads as slop and its fix, is `references/slop-tells.md`.

---

## Files

```
SKILL.md                  this file
README.md                 install and first run, for the person you hand it to
scripts/thumb.py          compose · check · sheet · init
assets/brief.template.json
assets/fonts/             Anton, Barlow Condensed, Inter (SIL OFL)
references/onboarding.md the exact seven questions, branches, answer-to-brief map
references/slop-tells.md  the diagnostic catalogue
references/genre-playbook.md  genre → promise, archetype, palette, failure mode
references/prompting.md   the prompt formula, three worked examples, negatives
references/typography.md  title rules, zones, numbers, fonts
references/qa.md          the 12-point rubric and the kill rule
examples/neon-district/   a filled brief and its prompt, no borrowed art
```

Requires Python 3.10+ and Pillow (`pip install pillow`). No network, no keys.

If `python` is not the command on the machine, use `py` (Windows) or `python3`.
