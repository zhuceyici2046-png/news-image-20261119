#!/usr/bin/env python3
"""Draw entry.png: one image summing up Thursday 19 November 2026 world news.

Stories (all reported on 19 Nov 2026, cross-checked across several outlets):
  1. Trump, Xi and Putin meet in Shenzhen - first trilateral summit of the
     three great powers, ends with a four-point 'Declaration toward Peace'.
  2. ICJ rules Myanmar committed genocide against the Rohingya in 2017 -
     the first state ever found guilty of genocide by an international court.
  3. Anthropic's Nasdaq debut: ~$2 trillion valuation, biggest listing ever,
     shares open 34% above the IPO price.
  4. Tanker attacks mount in the Gulf as US-Iran strikes escalate; the IEA
     calls the crisis the greatest threat ever to energy security.
  5. Crimea bridge hit for a second night; EU proposes a 45bn euro loan
     to Ukraine.
  6. Bangladesh in turmoil: Yunus's ancestral home set on fire amid
     violence in 28 districts.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (22, 35, 58)
NAVY = (18, 30, 54)
RED = (178, 39, 30)
GOLD = (212, 172, 60)
STEEL = (46, 94, 140)
TEAL = (31, 122, 109)
MUTED = (74, 80, 96)
WHITE = (253, 251, 246)
CARD = (255, 255, 255)
BORDER = (200, 192, 175)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(f"{FD}/{name}", size)


def serif_b(s):
    return F("DejaVuSerif-Bold.ttf", s)


def sans_b(s):
    return F("DejaVuSans-Bold.ttf", s)


def sans(s):
    return F("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(d, lines, name, size, max_w):
    """Shrink bold font until every line fits max_w."""
    while size > 18:
        fnt = F(name, size)
        if all(d.textlength(t, font=fnt) <= max_w for t in lines):
            return fnt
        size -= 2
    return F(name, size)


def text_lines(d, x, y, lines, fnt, color, lh=None):
    lh = lh or int(fnt.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


# ---- icons (simple geometric glyphs) ----
def globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=6)
    d.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
              outline=color, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=4)
    d.arc([cx - r, cy - int(r * 0.5), cx + r, cy + int(r * 0.5)],
          0, 360, fill=color, width=4)


def scales(d, x, y, s, color):
    d.line([x + s // 2, y, x + s // 2, y + int(s * 0.78)], fill=color, width=6)
    d.line([x, y + int(s * 0.16), x + s, y + int(s * 0.16)], fill=color, width=6)
    for cx in (x + int(s * 0.14), x + int(s * 0.86)):
        d.line([cx, y + int(s * 0.16), cx, y + int(s * 0.42)], fill=color, width=4)
        d.polygon([(cx - int(s * 0.16), y + int(s * 0.42)),
                   (cx + int(s * 0.16), y + int(s * 0.42)),
                   (cx, y + int(s * 0.68))], outline=color, width=4)
    d.line([x + int(s * 0.2), y + int(s * 0.9), x + int(s * 0.8), y + int(s * 0.9)],
           fill=color, width=6)


def chart(d, x, y, s, color):
    d.rectangle([x, y + int(s * 0.58), x + int(s * 0.2), y + s], fill=color)
    d.rectangle([x + int(s * 0.32), y + int(s * 0.36), x + int(s * 0.52), y + s],
                fill=color)
    d.rectangle([x + int(s * 0.64), y + int(s * 0.12), x + int(s * 0.84), y + s],
                fill=color)
    d.line([x, y + int(s * 0.52), x + int(s * 0.48), y + int(s * 0.22),
            x + s, y], fill=color, width=6)
    d.polygon([(x + s, y), (x + int(s * 0.8), y + 2), (x + s - 2, y + int(s * 0.2))],
              fill=color)


def ship(d, x, y, s, color):
    d.polygon([(x, y + int(s * 0.42)), (x + s, y + int(s * 0.42)),
               (x + int(s * 0.82), y + int(s * 0.72)),
               (x + int(s * 0.18), y + int(s * 0.72))], fill=color)
    d.rectangle([x + int(s * 0.34), y + int(s * 0.12), x + int(s * 0.58),
                 y + int(s * 0.42)], fill=color)
    d.line([x + int(s * 0.44), y, x + int(s * 0.44), y + int(s * 0.12)],
           fill=color, width=4)
    d.line([x, y + int(s * 0.88), x + s, y + int(s * 0.88)], fill=color, width=5)
    d.line([x + int(s * 0.1), y + s, x + int(s * 0.9), y + s], fill=color, width=5)


def bridge(d, x, y, s, color):
    d.rectangle([x + int(s * 0.14), y + int(s * 0.18), x + int(s * 0.24),
                 y + int(s * 0.78)], fill=color)
    d.rectangle([x + int(s * 0.76), y + int(s * 0.18), x + int(s * 0.86),
                 y + int(s * 0.78)], fill=color)
    d.arc([x, y - int(s * 0.08), x + s, y + int(s * 0.8)], 180, 360,
          fill=color, width=6)
    d.line([x, y + int(s * 0.78), x + s, y + int(s * 0.78)], fill=color, width=6)


def flame(d, x, y, s, color):
    cx = x + s // 2
    d.polygon([(cx, y),
               (cx + int(s * 0.32), y + int(s * 0.45)),
               (cx + int(s * 0.22), y + int(s * 0.72)),
               (cx + int(s * 0.12), y + int(s * 0.95)),
               (cx, y + s),
               (cx - int(s * 0.12), y + int(s * 0.95)),
               (cx - int(s * 0.22), y + int(s * 0.72)),
               (cx - int(s * 0.32), y + int(s * 0.45))], fill=color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---------- header band ----------
    d.rectangle([0, 0, W, 160], fill=NAVY)
    d.rectangle([0, 160, W, 166], fill=GOLD)
    kicker = "THE WORLD IN ONE DAY"
    fk = sans_b(25)
    d.text(((W - d.textlength(kicker, font=fk)) / 2, 22), kicker,
           font=fk, fill=GOLD)
    date = "19 NOVEMBER 2026"
    fd = serif_b(78)
    d.text(((W - d.textlength(date, font=fd)) / 2, 50), date,
           font=fd, fill=WHITE)
    sub = "THURSDAY  ·  THE WORLD'S NEWS IN A SINGLE PICTURE"
    fs = sans(24)
    d.text(((W - d.textlength(sub, font=fs)) / 2, 128), sub,
           font=fs, fill=(214, 196, 140))

    # ---------- hero: Shenzhen summit ----------
    hx0, hy0, hx1, hy1 = M, 182, W - M, 408
    d.rectangle([hx0, hy0, hx1, hy1], fill=CARD, outline=BORDER, width=2)
    d.rectangle([hx0, hy0, hx1, hy0 + 7], fill=RED)
    globe(d, hx0 + 108, hy0 + 116, 86, STEEL)
    tx = hx0 + 232
    tw = hx1 - 18 - tx
    d.text((tx, hy0 + 16), "TOP STORY  ·  SHENZHEN, CHINA",
           font=sans_b(25), fill=RED)
    hero_head = ["TRUMP, XI & PUTIN", "MEET IN SHENZHEN"]
    fh = fit_font(d, hero_head, "DejaVuSans-Bold.ttf", 52, tw)
    y = text_lines(d, tx, hy0 + 44, hero_head, fh, INK, lh=56)
    hero_sub = wrap(d, "First trilateral summit of the three great powers "
                       "— ends with a \u2018Declaration toward Peace\u2019",
                    sans(27), tw)
    text_lines(d, tx, y + 8, hero_sub, sans(27), MUTED, lh=31)

    # ---------- 2x2 story grid ----------
    cards = [
        ("WORLD COURT:", "MYANMAR GUILTY",
         "Rohingya genocide, 2017 — first state ever convicted",
         TEAL, scales),
        ("ANTHROPIC'S", "$2 TRILLION DEBUT",
         "Biggest Nasdaq listing ever — shares +34% on debut",
         STEEL, chart),
        ("TANKERS HIT AS", "GULF CRISIS GROWS",
         "IEA: the greatest threat ever to energy security",
         RED, ship),
        ("CRIMEA BRIDGE", "HIT AGAIN",
         "Second night of strikes — EU proposes a €45bn loan to Kyiv",
         NAVY, bridge),
    ]
    cw = (W - 2 * M - 16) // 2
    ch = 232
    rows_y = [424, 672]
    for i, (h1, h2, sub, color, icon) in enumerate(cards):
        cx0 = M + (i % 2) * (cw + 16)
        cy0 = rows_y[i // 2]
        d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=CARD,
                    outline=BORDER, width=2)
        d.rectangle([cx0, cy0, cx0 + cw, cy0 + 7], fill=color)
        icon(d, cx0 + 20, cy0 + 88, 76, color)
        tx = cx0 + 112
        tw = cx0 + cw - 16 - tx
        head = [h1, h2]
        fh = fit_font(d, head, "DejaVuSans-Bold.ttf", 34, tw)
        y = text_lines(d, tx, cy0 + 24, head, fh, INK, lh=40)
        sub_lines = wrap(d, sub, sans(24), tw)
        text_lines(d, tx, y + 10, sub_lines, sans(24), MUTED, lh=30)

    # ---------- bottom strip: Bangladesh ----------
    sx0, sy0, sx1, sy1 = M, 920, W - M, 996
    d.rectangle([sx0, sy0, sx1, sy1], fill=CARD, outline=BORDER, width=2)
    d.rectangle([sx0, sy0, sx0 + 7, sy1], fill=RED)
    flame(d, sx0 + 22, sy0 + 16, 44, RED)
    tx = sx0 + 84
    d.text((tx, sy0 + 12), "ALSO · BANGLADESH IN TURMOIL",
           font=sans_b(26), fill=INK)
    d.text((tx, sy0 + 44),
           "Yunus's ancestral home set on fire amid violence in 28 districts",
           font=sans(23), fill=MUTED)

    # ---------- footer ----------
    foot = "Drawn from the day's reporting  ·  19 November 2026"
    ff = sans(19)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1004), foot,
           font=ff, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
