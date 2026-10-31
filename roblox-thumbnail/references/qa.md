# QA

**rxz** · the 12-point rubric, and when to throw the concept away.

A thumbnail is judged by a stranger in under a second. You cannot reproduce that by staring at a 1920 px file in
a chat window. So the rubric is split: six checks a script can measure, six a human has to look at, and one rule
for when to stop polishing.

---

## Automated (`python scripts/thumb.py check thumbnail.png`)

| # | Check | Pass | Why |
|---|---|---|---|
| 1 | Resolution and ratio | 1920×1080, or same ratio ≥ 1280×720 | Anything else is cropped or soft |
| 2 | Title inside safe zone | 6% margin, out of the bottom-right corner | Platform chrome and crop |
| 3 | Title word count | ≤ 3 | Read at 256 px |
| 4 | Edge clutter | Border detail not busier than the centre | Borders should be quiet |
| 5 | Tonal range | Enough light-to-dark spread | Flat images read as screenshots |
| 6 | Hue spread | ≤ 4 dominant hues | Rainbow mush at tile size |
| 7 | Focal concentration | One region dominates the luminance field | No focal point = no click |
| 8 | Title contrast | ≥ 4.5:1 against the art beneath it | Legibility, not taste |

FAIL blocks. WARN is a question, not a verdict — answer it by looking, and note the answer.

---

## Human (the part that decides)

| # | Check | How |
|---|---|---|
| 9 | **Promise** | Name what the player does, from the image alone. If it does not match the first minute, fail |
| 10 | **Emotion** | Shrink the face to 40 px. Can you still name the feeling? |
| 11 | **Style unity** | One rendering language? Any element from a different one is a fail |
| 12 | **Ownership** | Name one thing that could only belong to this game. If you cannot, it is generic |

---

## The 256 px protocol

1. Open `thumbnail-256.png` at actual size — not zoomed, not in a chat bubble.
2. Hold it at arm's length for one second, then look away.
3. Write down what you remember. That is what the thumbnail is.
4. Repeat with `thumbnail-grey.png`.
5. Compare against `compare.png`, which renders the candidates at real tile width.

If the memory is "a guy" or "some blue", the image is not doing its job, no matter how good it looks full-size.

---

## Severity

**Critical — re-concept, do not polish:**

- Two or more focal subjects, or the same character twice.
- The promise is not in the game.
- Model-generated letters anywhere.
- The hero's face is cropped, hidden, or unreadable.
- Style collision (anime face on a plastic body, painted sky behind a 3D car).

**Major — fix before shipping:**

- Title over three words, in the reserved corner, or below 4.5:1 contrast.
- Flat lighting, no rim, no contact shadow.
- Subject touching the frame edge.
- More than four hues, or a rainbow gradient.
- Anything important in the outer 6%.

**Minor — note it, ship anyway:**

- A single prop that is slightly off-model.
- Background detail that is busier than ideal but still reads.
- A colour that is a shade off the game's palette.

Two criticals, or five majors, means the concept is wrong. One more polish pass will not save it; a new prompt
with a different archetype might.

---

## What to change, based on what failed

| Failure | Change | Not this |
|---|---|---|
| No focal point | Different archetype, fewer subjects | More contrast in post |
| Weak emotion | New pose and expression in the prompt | Bigger face crop |
| Flat light | Named key + rim in the prompt | A vignette in the compositor |
| Style collision | Re-prompt with one anchor | Repaint one element |
| Text unreadable | Shorter words, new zone | Thicker stroke |
| Promise mismatch | New concept | New colourway |
| Cluttered edges | Reframe, move camera | Blur the border in post |
| Subject floats | Contact shadow in the prompt | A drawn shadow |

The pattern: almost every fix belongs in the **brief or the prompt**, not in post. Post-processing a weak frame is
how a thumbnail becomes technically clean and completely forgettable.

---

## Sign-off

Before you call it done, state these five, in one line each:

1. The promise, in one sentence.
2. The archetype.
3. The measured cap height and contrast ratio.
4. What the 256 px test remembered.
5. The one thing that could only belong to this game.

If any line is hard to write, the thumbnail is not finished.
