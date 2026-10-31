# Prompting

**rxz** · how to ask for the art so it comes back composed, lit and style-consistent.

An image prompt is not a wish. It is a shot list with a lens attached. The models that produce good Roblox art
are not receiving better adjectives — they are receiving a subject, a camera, a light and a boundary.

---

## The formula

```
[STYLE ANCHOR] + [SUBJECT + IDENTITY] + [ACTION/POSE] + [PROP] + [SETTING]
+ [LIGHT] + [CAMERA] + [PALETTE] + [COMPOSITION] + [NEGATIVES]
```

Order is not cosmetic: the first clause sets the rendering language, the middle sets the scene, the end sets the
constraints. Put "no text" early enough that it survives truncation, and repeat it at the end.

**One paragraph. 60–110 words.** Longer prompts dilute; shorter ones leave the model to invent a composition.

---

## Style anchors

Pick exactly one, and keep it for the whole set. Mixing two is how you get an anime face on a plastic body.

| Anchor | Use for | Phrases that hold it |
|---|---|---|
| **Toy-like 3D** | Most Roblox genres; the default | `chunky toy-like 3D render`, `blocky stylized character`, `matte plastic materials`, `soft studio light` |
| **Cel-shaded anime** | Anime, gacha, battlegrounds | `cel-shaded anime illustration`, `clean line art`, `flat colour with hard shadow`, `dynamic perspective` |
| **Painterly cartoon** | Tycoon, simulator, cozy | `painterly cartoon illustration`, `thick brush strokes`, `warm rim light`, `storybook shapes` |
| **Glossy product** | Object as Hero, pets, unboxing | `glossy product render`, `macro lens`, `hard contact shadow`, `studio softbox` |

State the material, not just the style: `matte plastic`, `brushed metal`, `iridescent scales`, `felt`. Materials are
what make an image look rendered rather than filtered.

---

## Three worked prompts

### Horror — Threat Behind

```
Chunky toy-like 3D render, a blocky stylized teenage camper with an oversized head and a
terrified face, matte plastic skin, crouched behind a mossy fallen log and gripping a
flashlight, a tall antlered shadow figure with two small glowing eyes standing between the
pines behind them, cold blue night forest, single hard cyan key from behind the hero, one
warm flashlight pool on the log, 35 mm low angle, hero in the lower-left third, shallow
depth of field, cinematic haze, clean darker space in the upper right, no text, no letters,
no logo, no watermark, no extra characters.
```

### Tycoon — Hero Shot

```
Clean stylized 3D render, a blocky Roblox-style character with a confident grin and raised
eyebrows wearing an open black jacket, one fist holding a thick stack of banknotes, standing
in front of a small red-roofed corner shop with a blank signboard above the door, warm
golden-hour key from camera-left, soft cyan sky fill, saturated gold and deep teal palette,
low angle 35 mm, character in the left third, background softly blurred, clean empty sky in
the upper right, no text, no letters, no logo, no watermark, no extra people.
```

### Pet simulator — Object as Hero

```
Glossy toy-like 3D render, a giant cartoon dragon pet with iridescent scales and tiny wings
bursting out of a cracked egg, shell fragments suspended mid-air, hard contact shadow on a
pastel mint studded floor, three-quarter top-down camera, 50 mm, subject filling the centre
of the frame, candy-bright lighting with a magenta rim light, pastel mint and hot pink
palette, clean space across the top for a title, no text, no letters, no logo, no
watermark, no extra characters.
```

Notice what all three do: one subject, one prop, one light direction, one palette, and a named empty area for the
title. That last clause is what stops the compositor from covering the face.

---

## Negatives

Use the tool's negative field if it has one; otherwise append the block to the prompt. This is the minimum:

```
no text, no letters, no typography, no logo, no watermark, no UI, no frame, no border,
no collage, no split screen, no duplicate character, no extra characters, no extra limbs,
no deformed hands, no blurry face, no low resolution, no watermark
```

Add per genre: `no gore` for horror if the audience is younger, `no real brands` for racing, `no other games'
characters` always.

---

## Settings

| Setting | Value | Why |
|---|---|---|
| Aspect | 16:9 | The only ratio Roblox serves |
| Width | ≥ 1920, ideally 2560 | The experience page shows it big; upscaling ruins the face |
| Batch | 3–4 seeds of one prompt | You are choosing a frame, not a strategy |
| Seed | Record it | Reroll one variable at a time |
| Reference image | Optional, weighted low | Keeps identity without copying composition |
| Upscale | Only from ≥ 1024 | Upscaling a small face produces a soft mask |

---

## Using a reference image

When the user supplies their character, pet or build:

1. Say what to **keep**: `same silhouette, same outfit, same colours as the reference`.
2. Say what to **change**: `new pose, new background, new lighting`.
3. Keep the reference weight low enough that it does not drag the original composition along.
4. Check the identity after generation. If the outfit changed, regenerate — do not ship a stranger.

A real screenshot with bad lighting beats an invented character every time. It is the user's game, and the
thumbnail has to match what the player will see.

---

## When the prompt misbehaves

| Symptom | Cause | Fix |
|---|---|---|
| Garbled letters, signs, UI panels | "Thumbnail" reads as a YouTube template | Describe a scene, add `no text, no UI`, say `16:9 photograph` or `16:9 render` |
| Poster with empty panels | Same | Remove the word "thumbnail" from the prompt entirely |
| Three or more characters | Model fills crowds | `single character, solo, one person` |
| Mushy lighting | "Dramatic lighting" | Name direction, colour and hardness |
| Plastic noise everywhere | "4k, masterpiece, hyperdetailed" | Talk about materials and lens instead |
| Anime face, plastic body | Two style anchors | One anchor, repeated once |
| Subject cropped at the edge | No composition clause | `centred, full body visible, 6% margin` |
| Text on a sign you wanted | Diegetic text request | Ask for a **blank** sign; composite the word |
| Off-model franchise character | Naming a copyrighted character | Describe silhouette, outfit, colours; never name it |
| Different style every seed | Anchor too vague | Add the material and the render type |

---

## The reroll rule

Change **one** thing per reroll, and write down what changed. Three seeds of one prompt tells you which frame
works. Three prompts at once tells you nothing except which one you got lucky with.
