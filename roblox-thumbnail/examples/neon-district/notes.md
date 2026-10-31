# Why this brief looks like this

A worked example of the onboarding answers turning into a shot. The game is invented; the reasoning is not.

| Question | Answer |
|---|---|
| Game | Neon District — a night-market tycoon |
| Genre | Tycoon |
| First minute | Buy a stall, stock it, watch customers queue |
| Hero | The player's avatar, grinning, cash in hand (screenshot supplied) |
| Theme / feeling | Magenta night, cyan neon, one warm gold; greedy triumph |
| Words | "SOLD OUT" |
| References | Two tycoon thumbnails with a clear hero and one prop; two AI ones with five characters and gibberish text |
| Ban list | Other games' characters, default noob, any text from the model |

## The choices

- **Hero Shot**, not Object as Hero: the promise is ownership, and a face sells that faster than a cash register.
- **"SOLD OUT"**, not the game name: the name is already under the tile. "Sold out" is the fantasy.
- **Accent on OUT**: the joke lives in the second word.
- **Lower-left type**: the shop and the queue sit right, so the type gets the empty street corner.
- **Blank signboard in the prompt**: the model cannot spell. The sign stays empty; if a word belongs on it,
  composite it later or crop it out.
- **No plate**: the night street is dark enough that white type carries on its own. Add `"plate": true` only if the
  greyscale proof shows the type sinking.

## What to check after generating

1. `thumb.py compose brief.json art.png` — the title lands lower-left, cap height 12–18%.
2. `thumb.py check thumbnail.png` — no fails.
3. `thumbnail-256.png` — can you tell it is a shop game, and that the shop just sold out?
4. `thumbnail-grey.png` — does the character still separate from the street?
