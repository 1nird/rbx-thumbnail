# Onboarding

**rxz** · the exact interview, the branches, and how answers become a brief.

The single most common failure in AI thumbnail tools is that they generate before they ask. This file exists so
every agent running the skill asks the same seven things, in the same order, and stops at the same gate.

---

## The message to send

Send this as one message. Numbered, short, no preamble longer than a line. If the host has a structured question
tool, put each number in it; otherwise plain text.

```
Before I make anything, seven quick ones — the answers decide the whole shot:

1. Game name + store link (or paste the description). I'll read it.
2. Genre — obby / tycoon / simulator / horror / battlegrounds / roleplay / racing /
   tower defence / anime-gacha / steal-a / other?
3. The one thing a new player does in their first minute that's fun.
4. Who or what is the hero of the shot — your character, a pet, a vehicle, a build?
   Send a screenshot or render if you have one; I'd rather use yours than invent one.
5. Theme and feeling — e.g. neon night, sunny cartoon, grimy horror, candy pastel —
   plus one emotion: fear, greed, triumph, chaos, cozy or awe.
6. Words on the image, 0 to 3. "None" is a real answer.
7. Two thumbnails you love, two you hate, and anything that must NOT appear.
```

Why each one matters, in case the agent has to explain:

- **1** saves the user from summarising their own game, and gives you the promise in their words.
- **2** picks the archetype before taste gets involved.
- **3** is the only answer the image actually has to communicate.
- **4** cannot be guessed. Inventing a cast is the fastest way to a thumbnail for a different game.
- **5** gives you one palette and one emotion. Two emotions is no emotion.
- **6** decides whether typography exists at all.
- **7** is where "I hate AI thumbnails with five characters" becomes a constraint you can obey.

---

## Branches

**"Just do it, I don't care."**
Infer 1, 2, 3, 5 and 7 from the store page. Reply with one short message asking only 4 and 6:

```
Fine — two things I can't guess: who's the hero (send a screenshot if you have one), and
what words, if any, go on the image?
```

Do not generate before those two exist. This is the whole point of the gate.

**"I don't have any art."**
Ask for **any** screenshot of their game — a phone photo of the screen is fine. If there is genuinely nothing,
use Object as Hero (the reward, rendered large) or a described original character, and say in the card that the
hero is invented. Never quietly substitute a stock avatar.

**"I don't know the genre."**
Read the store page and offer two, with a recommendation: *"It reads as a simulator with a tycoon loop — I'd shoot
it as simulator, because the hatching is the promise."* One question, not a taxonomy lesson.

**"Make it like [a famous thumbnail]."**
Extract the structure: archetype, subject scale, light direction, palette, word count. Never copy the character,
the logo, or the composition beat for beat. Say which part you are borrowing, so the user can veto it.

**"No words."**
Set `"text": {"style": "none"}`. Do not add a title because a thumbnail "should" have one. Then make sure the
image carries the promise on its own — that is the trade.

**"I want all ten thumbnails."**
Interview once, then build a set: one archetype per slot from `genre-playbook.md`'s ten-slot table. Do not
recolour one image ten times; that is a set-level slop tell.

**Refreshing an existing thumbnail.**
Ask for the current image and, if they have it, which slot underperforms. Keep the hero's identity and the
palette; change the archetype or the promise. Recolouring a thumbnail that does not convert changes nothing a
player can see.

---

## Answers → brief

| Answer | Field | Note |
|---|---|---|
| 1 | `game` | Also seeds `source.prompt` context |
| 2 | archetype choice | Use `genre-playbook.md`, not vibes |
| 3 | `promise` in the card | Becomes the first clause of the prompt's action |
| 4 | hero description / reference | Ask for a file; put the keep/change clauses in the prompt |
| 5 | palette + emotion | One dominant hue, one accent, one warm spot |
| 6 | `title`, `kicker`, `text.style` | 0 words → `"style": "none"` |
| 7 | ban list + references | Negative prompt and archetype cues |

The brief itself is `assets/brief.template.json`. Fill only the fields you need:

```json
{
  "game": "Bubble Pets",
  "title": "NEW PET",
  "kicker": "UPDATE 3",
  "text": {
    "style": "shout",
    "color": "#FFFFFF",
    "accent": "#FF3B1F",
    "accent_word": "NEW",
    "plate": "auto",
    "align": "left",
    "zone": "lower-left",
    "max_width": 0.62
  },
  "art": { "focus": [0.6, 0.4] },
  "source": { "model": "", "seed": "", "prompt": "see prompt.txt" }
}
```

---

## The art-direction card

Seven lines, shown before generation, approved before generation. It is cheaper to fix a line here than a render.

```
GAME      Bubble Pets (pet simulator)
PROMISE   Hatch your first pet and watch it follow you
HERO      your bubble dragon (screenshot supplied)
FEELING   greedy awe
THEME     candy pastel, mint + hot pink, one gold
WORDS     "NEW PET"  (2)
NOT       other games' pets, default noob, anything the model writes
```

If the user changes one line, change the brief, not the prompt. The prompt is downstream.

---

## Anti-patterns

- **Fifteen questions.** Seven is the budget. More feels like a form and gets abandoned.
- **Asking for "vibe" with no examples.** "What feeling?" plus six options is answerable; "describe the vibe" is not.
- **Averaging five references.** Ask which one is closest, and what specifically they like about each. A mood board
  is not a brief.
- **Generating while waiting for an answer.** The gate exists because a wrong hero wastes every later step.
- **Asking again after the card is approved.** That is the point to build.
