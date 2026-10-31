#!/usr/bin/env python3
"""rxz - roblox-thumbnail tooling.

    python thumb.py init "Game Name" [-o brief.json]
    python thumb.py compose brief.json art.png [-o thumbnail.png] [--text-only] [--debug] [--punch 0.2]
    python thumb.py check thumbnail.png [--json]
    python thumb.py sheet a.png b.png c.png [-o compare.png]

Compose turns generated art plus a brief into a 1920x1080 thumbnail with real
typography, a 256 px proof and a sidecar of measurements. Check reads those
measurements and the image itself, and prints PASS / WARN / FAIL. Sheet puts
candidates side by side at true tile size.

Pillow only. No network, no keys.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required:  pip install pillow")

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
ASSETS = ROOT / "assets"

W, H = 1920, 1080
MARGIN = round(W * 0.06)            # 115 px
RESERVED = (0.82, 0.86, 1.0, 1.0)   # bottom-right platform chrome, fractions

FONTS = {
    "shout": "Anton-Regular.ttf",
    "clean": "Inter-ExtraBold.ttf",
    "kicker": "BarlowCondensed-ExtraBold.ttf",
}

ZONES = ("lower-left", "upper-left", "upper-right", "lower-center", "center")


# ------------------------------- helpers -------------------------------

def die(msg: str) -> None:
    sys.exit(f"error: {msg}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"no such brief: {path}")
    except json.JSONDecodeError as exc:
        die(f"{path} is not valid JSON: {exc}")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_DIR / FONTS[name]
    if not path.exists():
        die(f"missing font {path}. Re-copy assets/fonts from the skill folder.")
    return ImageFont.truetype(str(path), size=size)


def hex_rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        die(f"bad colour {value!r}; use #RRGGBB")
    return (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16), alpha)


def lum(rgb) -> float:
    def ch(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b) -> float:
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def cover(img: Image.Image, focus=(0.5, 0.5)) -> Image.Image:
    """Scale to cover 1920x1080, crop with the focal point kept in view."""
    img = img.convert("RGB")
    scale = max(W / img.width, H / img.height)
    nw, nh = max(W, round(img.width * scale)), max(H, round(img.height * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    fx = min(max(float(focus[0]), 0.0), 1.0)
    fy = min(max(float(focus[1]), 0.0), 1.0)
    left = min(max(round(fx * nw - W / 2), 0), nw - W)
    top = min(max(round(fy * nh - H / 2), 0), nh - H)
    return img.crop((left, top, left + W, top + H))


def wrap(words: list[str], font_obj, stroke: int, max_width: float) -> list[list[str]]:
    lines, cur = [], []
    for word in words:
        trial = cur + [word]
        box = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), " ".join(trial),
                                                               font=font_obj, stroke_width=stroke)
        if box[2] - box[0] <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = [word]
    if cur:
        lines.append(cur)
    return lines


def fit(words: list[str], kind: str, max_width: float, max_height: float,
        max_lines: int) -> tuple[int, list[list[str]], int, int]:
    """Largest size whose wrapped block fits the box and the cap-height ceiling.

    The ceiling matters more than the box: a two-word title will always fit at
    poster size, and poster size is what makes a thumbnail look like an ad for
    a different product. 18% of frame height is the cap.
    """
    lo, hi = 40, 460
    cap_ceiling = H * 0.18
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        f = font(kind, mid)
        stroke = max(3, round(mid * 0.062))
        lines = wrap(words, f, stroke, max_width)
        bbox = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), "Hg", font=f)
        cap = bbox[3] - bbox[1]
        lead = mid * (0.98 if kind == "shout" else 1.12)
        total_h = lead * len(lines)
        widths = []
        for line in lines:
            b = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), " ".join(line),
                                                                  font=f, stroke_width=stroke)
            widths.append(b[2] - b[0])
        ok = (len(lines) <= max_lines and max(widths) <= max_width
              and total_h <= max_height and cap <= cap_ceiling)
        if ok:
            best = (mid, lines, stroke, cap)
            lo = mid + 1
        else:
            hi = mid - 1
    if best is None:
        f = font(kind, 40)
        lines = wrap(words, f, 3, max_width)
        return 40, lines, 3, 28
    return best


def measure_line(draw, line, f, stroke):
    return draw.textbbox((0, 0), " ".join(line), font=f, stroke_width=stroke)


def draw_tracked(draw, xy, text, f, fill, tracking, stroke=0, stroke_fill=None):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill, stroke_width=stroke,
                  stroke_fill=stroke_fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def tracked_width(draw, text, f, tracking) -> float:
    return sum(draw.textlength(ch, font=f) for ch in text) + tracking * max(0, len(text) - 1)


def mean_colour(img: Image.Image):
    return img.convert("RGB").resize((1, 1), Image.LANCZOS).getpixel((0, 0))


# ------------------------------- compose -------------------------------

def compose(args) -> int:
    brief = load_json(Path(args.brief))
    art_path = Path(args.art)
    if not art_path.exists():
        die(f"no such art file: {art_path}")

    title = str(brief.get("title", "")).strip()
    kicker = str(brief.get("kicker", "")).strip()
    text = brief.get("text", {}) or {}
    style = str(text.get("style", "shout")).lower()
    if style not in ("shout", "clean", "none"):
        die("text.style must be shout, clean or none")
    zone = str(text.get("zone", "lower-left")).lower()
    if zone not in ZONES:
        die(f"text.zone must be one of {', '.join(ZONES)}")
    align = str(text.get("align", "left")).lower()
    if align not in ("left", "center", "right"):
        die("text.align must be left, center or right")

    focus = (brief.get("art") or {}).get("focus", [0.5, 0.5])
    base = cover(Image.open(art_path), focus)

    punch = max(0.0, min(1.0, float(args.punch or 0.0)))
    if punch > 0:
        base = ImageEnhance.Color(base).enhance(1.0 + 0.35 * punch)
        base = ImageEnhance.Contrast(base).enhance(1.0 + 0.22 * punch)

    meta = {
        "tool": "rxz roblox-thumbnail",
        "version": 1,
        "canvas": [W, H],
        "art": str(art_path),
        "game": brief.get("game", ""),
        "title": title,
        "kicker": kicker,
        "zone": zone,
        "lines": [],
        # measured on the art alone: type would flatter every metric it touches
        "art_stats": stats(base),
    }

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if style != "none" and title:
        words = title.split()
        max_w = W * float(text.get("max_width", 0.62))
        max_h = H * (0.34 if style == "shout" else 0.30)
        max_lines = 2 if style == "shout" else 3
        size, lines, stroke, cap = fit(words, style, max_w, max_h, max_lines)
        f = font(style, size)
        leading = size * (0.98 if style == "shout" else 1.12)

        main = hex_rgba(text.get("color", "#FFFFFF"))
        accent = hex_rgba(text.get("accent", "#FF3B1F"))
        stroke_fill = hex_rgba(text.get("stroke", "#0B0B12"))
        accent_word = str(text.get("accent_word", "")).strip().upper()

        draw = ImageDraw.Draw(overlay)
        line_h = [measure_line(draw, ln, f, stroke) for ln in lines]
        title_w = max(b[2] - b[0] for b in line_h)
        block_h = leading * len(lines)

        # kicker sits above the block when present, with an accent bar
        k_font = None
        k_track = 0
        k_h = 0
        k_w = 0
        if kicker:
            k_size = max(34, round(size * 0.30))
            k_font = font("kicker", k_size)
            k_track = round(k_size * 0.16)
            k_w = tracked_width(draw, kicker.upper(), k_font, k_track) + round(k_size * 0.9)
            kb = draw.textbbox((0, 0), kicker.upper(), font=k_font)
            k_h = (kb[3] - kb[1]) + round(k_size * 1.05)
            block_h += k_h

        block_w = max(title_w, k_w)
        x, y = place(zone, block_w, block_h, align)
        box = (max(0, int(x)), max(0, int(y)),
               min(W, int(x + block_w)), min(H, int(y + block_h)))

        # Scrim: on by request, or automatically when the art under the type is too bright.
        plate = text.get("plate", "auto")
        ratio = contrast(main, mean_colour(base.crop(box)))
        if plate is True or (str(plate).lower() == "auto" and ratio < 4.5):
            add_scrim(overlay, y, block_h)
            ratio = contrast(main, mean_colour(
                Image.alpha_composite(base.convert("RGBA"), overlay).crop(box)))

        draw = ImageDraw.Draw(overlay)
        cy = y
        if kicker:
            kx = x if align == "left" else (x + (block_w - k_w) / 2
                                            if align == "center" else x + block_w - k_w)
            bar_w = max(5, round(k_font.size * 0.10))
            draw.rectangle([kx, cy + round(k_font.size * 0.16), kx + bar_w,
                            cy + round(k_font.size * 0.92)], fill=accent)
            draw_tracked(draw, (kx + bar_w + round(k_font.size * 0.42), cy),
                         kicker.upper(), k_font, main, k_track)
            cy += k_h

        for i, line in enumerate(lines):
            lb = line_h[i]
            lw = lb[2] - lb[0]
            lx = x if align == "left" else (x + (block_w - lw) / 2 if align == "center"
                                            else x + block_w - lw)
            # shadow for separation on busy art
            shadow_off = max(4, round(size * 0.035))
            for wi, word in enumerate(line):
                prefix = " ".join(line[:wi]) + (" " if wi else "")
                wx = lx + draw.textlength(prefix, font=f)
                fill = accent if accent_word and word.upper().strip(".,!?") == accent_word else main
                draw.text((wx + shadow_off, cy + shadow_off), word, font=f,
                          fill=(0, 0, 0, 90), stroke_width=stroke,
                          stroke_fill=(0, 0, 0, 90))
                draw.text((wx, cy), word, font=f, fill=fill, stroke_width=stroke,
                          stroke_fill=stroke_fill)
            cy += leading

        margin_ok = (box[0] >= MARGIN - 2 and box[1] >= MARGIN - 2 and
                     box[2] <= W - MARGIN + 2 and box[3] <= H - MARGIN + 2)
        rx0, ry0 = int(W * RESERVED[0]), int(H * RESERVED[1])
        hits_reserved = not (box[2] <= rx0 or box[0] >= W or box[3] <= ry0 or box[1] >= H)

        meta.update({
            "style": style,
            "font_size": size,
            "cap_height": cap,
            "cap_pct": round(100 * cap / H, 1),
            "stroke": stroke,
            "lines": [" ".join(ln) for ln in lines],
            "words": len(words),
            "box": [int(v) for v in box],
            "margin_ok": bool(margin_ok),
            "hits_reserved_corner": bool(hits_reserved),
            "contrast": round(ratio, 2),
            "title_color": text.get("color", "#FFFFFF"),
        })

    out = Image.alpha_composite(base.convert("RGBA"), overlay)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.text_only:
        overlay.save(out_path)
        print(f"text layer  {out_path}  ({overlay.width}x{overlay.height}, transparent)")
        return 0

    out.convert("RGB").save(out_path, quality=95)

    # proofs: the only sizes anyone should judge it at
    small = out.convert("RGB").resize((256, 144), Image.LANCZOS)
    small.save(out_path.with_name(out_path.stem + "-256.png"))
    out.convert("L").save(out_path.with_name(out_path.stem + "-grey.png"))

    if args.debug:
        dbg = out.copy()
        d = ImageDraw.Draw(dbg)
        d.rectangle([MARGIN, MARGIN, W - MARGIN, H - MARGIN], outline=(0, 255, 120, 255), width=4)
        d.rectangle([int(W * RESERVED[0]), int(H * RESERVED[1]), W, H],
                    outline=(255, 60, 60, 255), width=4)
        dbg.convert("RGB").save(out_path.with_name(out_path.stem + "-safe.png"))

    out_path.with_name(out_path.stem + ".json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8")

    if meta.get("lines"):
        print(f"wrote       {out_path}  ({W}x{H})")
        print(f"title       {' / '.join(meta['lines'])}")
        print(f"cap height  {meta['cap_height']} px  ({meta['cap_pct']}% of frame)")
        print(f"contrast    {meta['contrast']}:1")
        print(f"safe zone   {'ok' if meta['margin_ok'] else 'OUTSIDE'}  - reserved corner "
              f"{'HIT' if meta['hits_reserved_corner'] else 'clear'}")
        print(f"proofs      {out_path.stem}-256.png - {out_path.stem}-grey.png")
    else:
        print(f"wrote       {out_path}  ({W}x{H})  (no title)")
    return 0


def place(zone: str, block_w: float, block_h: float, align: str):
    if zone == "lower-left":
        return MARGIN, H - MARGIN - block_h
    if zone == "upper-left":
        return MARGIN, MARGIN
    if zone == "upper-right":
        return W - MARGIN - block_w, MARGIN
    if zone == "lower-center":
        return (W - block_w) / 2, H - MARGIN - block_h
    return (W - block_w) / 2, (H - block_h) / 2


def add_scrim(overlay: Image.Image, top: float, height: float) -> None:
    """Soft vertical gradient behind type. Reads as lighting, not a box."""
    band_top = max(0, int(top - height * 0.55))
    band_h = min(H - band_top, int(height * 1.55))
    if band_h <= 0:
        return
    grad = Image.new("L", (1, band_h))
    for i in range(band_h):
        p = i / max(1, band_h - 1)
        grad.putpixel((0, i), int(150 * (p ** 1.6)))
    grad = grad.resize((W, band_h))
    layer = Image.new("RGBA", (W, band_h), (8, 8, 12, 255))
    overlay.paste(layer, (0, band_top), grad)


# ------------------------------- check -------------------------------

def stats(img: Image.Image):
    g = img.convert("L")
    small = g.resize((240, 135), Image.LANCZOS)
    px = list(small.tobytes())
    mean = sum(px) / len(px)
    lo = sorted(px)[int(len(px) * 0.02)]
    hi = sorted(px)[int(len(px) * 0.98)]

    edge = small.filter(ImageFilter.FIND_EDGES)
    ep = list(edge.tobytes())
    ew, eh = edge.size
    border, center = [], []
    # inset by 2 px: the edge filter itself lights up the outermost row/column
    for y in range(2, eh - 2):
        for x in range(2, ew - 2):
            v = ep[y * ew + x]
            if x < ew * 0.06 or x > ew * 0.94 or y < eh * 0.06 or y > eh * 0.94:
                border.append(v)
            elif ew * 0.30 < x < ew * 0.70 and eh * 0.30 < y < eh * 0.70:
                center.append(v)
    b = sum(border) / max(1, len(border))
    c = sum(center) / max(1, len(center))
    clutter = b / max(1.0, c)

    hsv = img.convert("RGB").resize((240, 135), Image.LANCZOS).convert("HSV")
    raw = hsv.tobytes()
    bins = [0] * 12
    total = len(raw) // 3
    for i in range(0, len(raw), 3):
        h, s, v = raw[i], raw[i + 1], raw[i + 2]
        if s > 80 and v > 40:
            bins[h * 12 // 256] += 1
    hues = sum(1 for n in bins if n / total > 0.03)

    cells = g.resize((48, 27), Image.LANCZOS)
    cp = [abs(v - mean) for v in cells.tobytes()]
    cp.sort(reverse=True)
    top = sum(cp[:max(1, len(cp) // 10)]) / max(1, len(cp) // 10)
    focal = top / max(1.0, (sum(cp) / len(cp)))

    return {
        "mean": round(mean, 1),
        "range": int(hi - lo),
        "border_edge": round(b, 2),
        "center_edge": round(c, 2),
        "clutter": round(clutter, 2),
        "hues": hues,
        "focal": round(focal, 2),
    }


def check(args) -> int:
    path = Path(args.path)
    if not path.exists():
        die(f"no such file: {path}")
    img = Image.open(path).convert("RGB")
    side_path = path.with_suffix(".json")
    meta = json.loads(side_path.read_text(encoding="utf-8")) if side_path.exists() else None
    # judge the art, not the type: a big title would fake tonal range and a focal point
    s = (meta or {}).get("art_stats") or stats(img)

    rows, notes = [], []

    def add(name, ok, detail, level="FAIL"):
        rows.append({"check": name, "level": "PASS" if ok else level, "detail": detail})

    ratio = img.width / img.height
    ok_size = img.width >= 1280 and abs(ratio - 16 / 9) < 0.01
    add("resolution", ok_size, f"{img.width}x{img.height}, ratio {ratio:.3f} (want 16:9, >=1280 wide)")

    if meta and meta.get("lines"):
        add("title safe zone", meta.get("margin_ok", False),
            f"box {meta.get('box')} inside 6% margin; reserved corner "
            f"{'hit' if meta.get('hits_reserved_corner') else 'clear'}")
        add("title words", meta.get("words", 99) <= 3,
            f"{meta.get('words')} words: {' / '.join(meta.get('lines', []))}", "WARN")
        add("title contrast", meta.get("contrast", 0) >= 4.5,
            f"{meta.get('contrast')}:1 (want >=4.5)", "WARN")
        add("cap height", 12.0 <= meta.get("cap_pct", 0) <= 18.0,
            f"{meta.get('cap_pct')}% of frame (want 12-18%)", "WARN")
    elif meta is None:
        notes.append("no compose sidecar: title checks skipped (run compose, not a raw image)")

    add("edge clutter", s["clutter"] <= 1.25,
        f"border/centre detail {s['clutter']} (want <=1.25)", "WARN")
    add("tonal range", s["range"] >= 110, f"p2-p98 luminance spread {s['range']} (want >=110)", "WARN")
    add("hue spread", s["hues"] <= 4, f"{s['hues']} dominant hues (want <=4)", "WARN")
    add("focal point", s["focal"] >= 1.55, f"concentration {s['focal']} (want >=1.55)", "WARN")

    fails = [r for r in rows if r["level"] == "FAIL"]
    warns = [r for r in rows if r["level"] == "WARN"]

    if args.json:
        print(json.dumps({"file": str(path), "stats": s, "meta": meta, "checks": rows,
                          "notes": notes, "fails": len(fails), "warns": len(warns)},
                         indent=2))
    else:
        print(f"{path}  {img.width}x{img.height}")
        for r in rows:
            print(f"  {r['level']:<4}  {r['check']:<18} {r['detail']}")
        for n in notes:
            print(f"  note  {n}")
        print()
        if fails:
            print(f"{len(fails)} fail - {len(warns)} warn - fix the fails, then look at the 256 px proof.")
        elif warns:
            print(f"0 fail - {len(warns)} warn - answer each warn by looking, not by guessing.")
        else:
            print("0 fail - 0 warn - now do the two human looks (256 px, greyscale).")
    return 1 if fails else 0


# ------------------------------- sheet -------------------------------

def sheet(args) -> int:
    paths = [Path(p) for p in args.images]
    if not paths:
        die("give at least one image")
    for p in paths:
        if not p.exists():
            die(f"no such file: {p}")

    cell_w, pad, label_h, big_h = 360, 28, 40, 203
    small_w, small_h, gap = 256, 144, 10
    cols = len(paths)
    width = pad + cols * (cell_w + pad)
    height = pad + 34 + big_h + 16 + small_h + gap + small_h + 12 + label_h + pad
    board = Image.new("RGB", (width, height), (18, 18, 22))
    d = ImageDraw.Draw(board)
    f = font("clean", 20)
    fs = font("clean", 15)

    d.text((pad, pad), "at true tile size - 360 wide, then 256 colour / 256 grey", font=f,
           fill=(235, 235, 240))

    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB")
        x = pad + i * (cell_w + pad)
        y = pad + 34
        board.paste(im.resize((cell_w, big_h), Image.LANCZOS), (x, y))
        y += big_h + 16
        small = im.resize((small_w, small_h), Image.LANCZOS)
        board.paste(small, (x, y))
        d.text((x + small_w + 10, y + 58), "256", font=fs, fill=(150, 150, 160))
        y += small_h + gap
        board.paste(small.convert("L").convert("RGB"), (x, y))
        d.text((x + small_w + 10, y + 58), "grey", font=fs, fill=(150, 150, 160))
        d.text((x, height - pad - label_h + 6), p.name[:40], font=fs, fill=(210, 210, 220))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    board.save(out, quality=95)
    print(f"wrote {out}  ({width}x{height})")
    return 0


# ------------------------------- init -------------------------------

def init(args) -> int:
    tmpl = ASSETS / "brief.template.json"
    data = json.loads(tmpl.read_text(encoding="utf-8")) if tmpl.exists() else {}
    data["game"] = args.game
    out = Path(args.out)
    if out.exists() and not args.force:
        die(f"{out} exists; pass --force to overwrite")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"wrote {out} - fill in title, theme and hero, then compose.")
    return 0


# ------------------------------- cli -------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(prog="thumb.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("compose", help="art + brief -> 1920x1080 thumbnail")
    p.add_argument("brief")
    p.add_argument("art")
    p.add_argument("-o", "--out", default="thumbnail.png")
    p.add_argument("--text-only", action="store_true", help="write the transparent text layer")
    p.add_argument("--debug", action="store_true", help="also write a safe-area overlay proof")
    p.add_argument("--punch", type=float, default=0.0, help="0-1 colour/contrast lift")
    p.set_defaults(fn=compose)

    p = sub.add_parser("check", help="measure a finished thumbnail")
    p.add_argument("path")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=check)

    p = sub.add_parser("sheet", help="compare candidates at true tile size")
    p.add_argument("images", nargs="+")
    p.add_argument("-o", "--out", default="compare.png")
    p.set_defaults(fn=sheet)

    p = sub.add_parser("init", help="write a fresh brief.json")
    p.add_argument("game")
    p.add_argument("-o", "--out", default="brief.json")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=init)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
