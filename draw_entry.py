#!/usr/bin/env python3
"""Draw entry.png v2: a dense newspaper front page summing up
Thursday 19 November 2026 world news (35 stories, 6 sections).

Every story below was checked against real reporting of 19 Nov 2026:
  HERO
  1. Trump, Xi and Putin meet in Shenzhen - first trilateral summit of the
     three great powers, ends with a four-point 'Declaration toward Peace'
     (UN reform, nuclear risk, energy flows; no word on Ukraine).
  2. ICJ rules Myanmar committed genocide against the Rohingya in 2017 -
     the first state ever found guilty of genocide by an international court.
  FEATURED
  3. Anthropic's Nasdaq debut: $81.3bn IPO, biggest listing ever,
     shares open 34% above the $83 offer price, valuation near $1.5tn.
  4. Two tankers hit naval mines in the Strait of Hormuz and catch fire;
     the IEA calls the crisis the greatest threat ever to energy security.
  5. GTA 6 launches at midnight: ~24.6m copies, ~$2.36bn on day one
     (Sensor Tower estimates), biggest entertainment launch ever;
     streams peak at 7.9m concurrent viewers.
  ASIA & PACIFIC
  6. Takaichi meets Putin for 30 minutes at APEC; no talks with Xi, whose
     handshake is all she gets; Taiwan line unchanged.
  7. Cyclone Akvan bears down on India: Odisha lines up 204,070 people
     for possible evacuation across eight districts.
  8. Manila: over 330 arrested in protests against Trump's visit;
     six children still in police custody on 19 Nov.
  9. Japan and India agree to deepen military cooperation, including
     Japanese troops training in India.
  10. Thailand floods expose a waste crisis in Prachinburi province.
  11. South Korea's Supreme Court overturns ex-PM Han Duck-soo's
      15-year sentence over the failed martial law attempt; retrial.
  EUROPE
  12. Berlin 'coalition of the willing' summit: E3 and Kyiv call for a
      winter energy ceasefire; Macron says reopen NATO membership question.
  13. Crimea bridge hit for a second night; EU proposes a 45bn euro loan
      to Ukraine.
  14. Netherlands summons the Russian ambassador after its Kyiv embassy
      is damaged in a strike.
  15. Serbia elects student-movement lecturer Aleksandar Cupic as
      parliamentary speaker, ending the ruling party's 14-year grip.
  16. Denmark's parliament approves a bigger US military role in the
      Arctic under a Greenland defence deal.
  MIDDLE EAST
  17. Houthis hit a tower in Riyadh's King Abdullah Financial District.
  18. US Senate rejects the War Powers bid to end the Iran war, 51-48.
  19. Israel ends its Gaza tank raid after troops crossed the ceasefire
      line; about 6,000 people fled Nuseirat.
  20. Gaza Health Ministry: at least 300 children died waiting for
      Israeli permission to leave for life-saving treatment.
  21. Somalia orders the UAE ambassador to leave within 72 hours,
      accusing Abu Dhabi of violating its sovereignty.
  22. Iraq reaches a compromise with Kataib Hezbollah over control of
      Jurf al-Sakhar south of Baghdad.
  AMERICAS
  23. Trump tells NBC he will meet Kim Jong-un 'at some point'.
  24. A Colorado judge holds ICE officials in contempt for re-arresting
      a man freed by court order.
  25. Guyana alarmed as a former Trump aide floats ceding part of
      Essequibo to Venezuela; US says policy unchanged.
  26. South Florida storm brings flooding and building damage.
  27. Pope Leo XIV condemns the killings of Amazon defenders on a visit
      to Pucallpa, Peru.
  TECH & MARKETS
  28. Markets slide after the Anthropic debut: Nikkei -4.8%, S&P 500 -2.0%.
  29. A London tribunal confirms the UK issued Apple a technical
      capability notice demanding access to customer data.
  30. Rio Tinto commits US$250m over damage from Bougainville's
      Panguna mine.
  31. IEA: data-centre carbon emissions to rise about 70% by 2030.
  CLIMATE & MORE
  32. COP31 draft deal drops all mention of fossil fuels as the deadline
      nears; keeps the '35 by 35' electrification target.
  33. Tonga declares a state of emergency as the El Nino drought worsens.
  34. Category 5 Cyclone Xavier nears the Northern Cook Islands,
      gusts to 170 km/h.
  35. UNHCR: nearly 90 million displaced people live in countries
      highly exposed to climate hazards.
  MARKETS TABLE: Nikkei -4.8%, S&P 500 -2.0%, Brent crude $92.58,
  Anthropic close +17%.
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
PURPLE = (90, 60, 140)
GREEN = (56, 118, 70)
MUTED = (74, 80, 96)
WHITE = (253, 251, 246)
CARD = (255, 255, 255)
BORDER = (200, 192, 175)
HAIR = (220, 214, 200)

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


def text_lines(d, x, y, lines, fnt, color, lh=None):
    lh = lh or int(fnt.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


def globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    d.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
              outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - int(r * 0.5), cx + r, cy + int(r * 0.5)],
          0, 360, fill=color, width=3)


def scales(d, x, y, s, color):
    d.line([x + s // 2, y, x + s // 2, y + int(s * 0.78)], fill=color, width=5)
    d.line([x, y + int(s * 0.16), x + s, y + int(s * 0.16)], fill=color, width=5)
    for cx in (x + int(s * 0.14), x + int(s * 0.86)):
        d.line([cx, y + int(s * 0.16), cx, y + int(s * 0.42)], fill=color, width=3)
        d.polygon([(cx - int(s * 0.16), y + int(s * 0.42)),
                   (cx + int(s * 0.16), y + int(s * 0.42)),
                   (cx, y + int(s * 0.68))], outline=color, width=3)
    d.line([x + int(s * 0.2), y + int(s * 0.9), x + int(s * 0.8), y + int(s * 0.9)],
           fill=color, width=5)


HERO = [
    ("TOP STORY  ·  SHENZHEN, CHINA", RED,
     ["TRUMP, XI & PUTIN", "MEET IN SHENZHEN"],
     "First trilateral summit ends with a four-point "
     "'Declaration toward Peace'", globe, STEEL),
    ("THE HAGUE, NETHERLANDS", TEAL,
     ["WORLD COURT:", "MYANMAR GUILTY"],
     "ICJ: genocide against the Rohingya — first state ever convicted",
     scales, TEAL),
]

FEATURED = [
    ("ANTHROPIC'S", "RECORD DEBUT",
     "Biggest Nasdaq listing ever — $81.3bn IPO, +34% at the open",
     STEEL),
    ("TANKERS BURN", "IN THE GULF",
     "Mines hit two tankers in Hormuz; IEA warns of greatest threat ever",
     RED),
    ("GTA 6: BIGGEST", "LAUNCH EVER",
     "24.6m copies, $2.36bn on day one (estimates)",
     PURPLE),
]

SECTIONS = [
    ("ASIA & PACIFIC", RED, [
        "Takaichi gets 30 minutes with Putin; no Xi talks at APEC",
        "Cyclone Akvan nears India — Odisha to evacuate 204,000",
        "Manila: 330 arrested; six children still held",
        "Japan and India deepen military ties",
        "Thailand floods expose waste crisis in Prachinburi",
        "South Korea court overturns ex-PM Han's 15-year sentence",
    ]),
    ("EUROPE", NAVY, [
        "Berlin: E3 and Kyiv urge winter energy ceasefire",
        "Crimea bridge hit again — EU proposes €45bn loan to Kyiv",
        "Netherlands summons Russian envoy after Kyiv embassy hit",
        "Serbia's students take the speaker's chair",
        "Denmark approves bigger US military role in the Arctic",
    ]),
    ("MIDDLE EAST", TEAL, [
        "Houthis hit Riyadh tower in claimed attack",
        "US Senate rejects bid to end Iran war, 51–48",
        "Israel ends Gaza tank raid after crossing ceasefire line",
        "300 Gaza children died waiting to leave for care",
        "Somalia expels UAE envoy — 72 hours to leave",
        "Iraq strikes deal with Kataib Hezbollah over stronghold",
    ]),
    ("AMERICAS", STEEL, [
        "Trump: I'll meet Kim Jong-un 'at some point'",
        "US judge holds ICE officials in contempt",
        "Guyana alarmed as ex-Trump aide floats Essequibo deal",
        "South Florida storm floods streets, damages buildings",
        "Pope condemns killings of Amazon defenders in Peru",
    ]),
    ("TECH & MARKETS", PURPLE, [
        "Markets slide after Anthropic debut",
        "UK tribunal confirms Apple data-access order",
        "Rio Tinto pays $250m for mine damage in Bougainville",
        "IEA: data-centre emissions to rise 70% by 2030",
    ]),
    ("CLIMATE & MORE", GREEN, [
        "COP31 draft drops fossil-fuel phaseout",
        "Tonga declares drought emergency as El Niño worsens",
        "Category 5 Cyclone Xavier nears Cook Islands",
        "UN: 90m displaced live in climate-risk countries",
    ]),
]

MARKETS = [
    ("Nikkei", "−4.8%"),
    ("S&P 500", "−2.0%"),
    ("Brent crude", "$92.58"),
    ("Anthropic close", "+17%"),
]


def section_height(d, items, fnt, w):
    h = 24 + 6
    for head in items:
        lines = wrap(d, head, fnt, w)
        h += len(lines) * 18 + 9
    return h


def draw_section(d, x, y, w, title, color, items, fnt):
    d.rectangle([x, y, x + w, y + 24], fill=color)
    d.text((x + 8, y + 3), title, font=sans_b(15), fill=WHITE)
    y += 24 + 6
    for head in items:
        lines = wrap(d, head, fnt, w)
        y = text_lines(d, x, y, lines, fnt, INK, lh=18)
        y += 3
        d.line([x, y, x + w, y], fill=HAIR, width=1)
        y += 6
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24

    n_stories = len(HERO) + len(FEATURED) + sum(len(s[2]) for s in SECTIONS)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 116], fill=GOLD)
    kicker = "THE WORLD IN ONE DAY"
    fk = sans_b(19)
    d.text(((W - d.textlength(kicker, font=fk)) / 2, 8), kicker,
           font=fk, fill=GOLD)
    date = "19 NOVEMBER 2026"
    fd = serif_b(58)
    d.text(((W - d.textlength(date, font=fd)) / 2, 30), date,
           font=fd, fill=WHITE)
    sub = (f"THURSDAY  ·  {n_stories} STORIES  ·  ASIA  ·  EUROPE  ·  "
           "MIDDLE EAST  ·  AMERICAS  ·  TECH  ·  CLIMATE")
    fs = sans(17)
    d.text(((W - d.textlength(sub, font=fs)) / 2, 90), sub,
           font=fs, fill=(214, 196, 140))

    # ---------- hero row: 2 cards ----------
    hw = (W - 2 * M - 16) // 2
    hy0, hy1 = 124, 274
    for i, (kicker_t, color, head, sub_t, icon, icol) in enumerate(HERO):
        x0 = M + i * (hw + 16)
        d.rectangle([x0, hy0, x0 + hw, hy1], fill=CARD, outline=BORDER, width=2)
        d.rectangle([x0, hy0, x0 + hw, hy0 + 6], fill=color)
        if icon is globe:
            icon(d, x0 + 76, hy0 + 78, 52, icol)
        else:
            icon(d, x0 + 18, hy0 + 62, 58, icol)
        tx = x0 + 140
        tw = x0 + hw - 14 - tx
        d.text((tx, hy0 + 12), kicker_t, font=sans_b(16), fill=color)
        y = text_lines(d, tx, hy0 + 34, head, sans_b(30), INK, lh=34)
        sub_lines = wrap(d, sub_t, sans(17), tw)
        text_lines(d, tx, y + 4, sub_lines, sans(17), MUTED, lh=21)

    # ---------- featured row: 3 cards ----------
    fw = (W - 2 * M - 24) // 3
    fy0, fy1 = 284, 408
    for i, (h1, h2, sub_t, color) in enumerate(FEATURED):
        x0 = M + i * (fw + 12)
        d.rectangle([x0, fy0, x0 + fw, fy1], fill=CARD, outline=BORDER, width=2)
        d.rectangle([x0, fy0, x0 + fw, fy0 + 6], fill=color)
        tx = x0 + 14
        tw = x0 + fw - 14 - tx
        y = text_lines(d, tx, fy0 + 16, [h1, h2], sans_b(23), INK, lh=26)
        sub_lines = wrap(d, sub_t, sans(16), tw)
        text_lines(d, tx, y + 8, sub_lines, sans(16), MUTED, lh=19)

    # ---------- sections: 3 columns ----------
    sy0, sy1 = 420, 990
    budget = sy1 - sy0
    col_w = (W - 2 * M - 24) // 3
    cols = [SECTIONS[0:2], SECTIONS[2:4], SECTIONS[4:6]]
    size = 18
    while size > 14:
        fnt = sans_b(size)
        ok = True
        for ci, pair in enumerate(cols):
            h = sum(section_height(d, s[2], fnt, col_w) for s in pair) + 12
            if ci == 2:
                h += 24 + 4 + 4 * 26  # markets table
            if h > budget:
                ok = False
        if ok:
            break
        size -= 1
    fnt = sans_b(size)
    for ci, pair in enumerate(cols):
        x0 = M + ci * (col_w + 12)
        y = sy0
        for title, color, items in pair:
            y = draw_section(d, x0, y, col_w, title, color, items, fnt)
            y += 12
        if ci == 2:
            # markets table under the last column's sections
            d.rectangle([x0, y, x0 + col_w, y + 24], fill=(60, 60, 66))
            d.text((x0 + 8, y + 3), "MARKETS", font=sans_b(15), fill=WHITE)
            y += 24 + 4
            for label, val in MARKETS:
                d.text((x0, y), label, font=sans(16), fill=MUTED)
                vw = d.textlength(val, font=sans_b(16))
                d.text((x0 + col_w - vw, y), val, font=sans_b(16), fill=INK)
                y += 22
                d.line([x0, y, x0 + col_w, y], fill=HAIR, width=1)
                y += 4

    # ---------- footer ----------
    foot = "Drawn from the day's reporting  ·  19 November 2026"
    ff = sans(18)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 998), foot,
           font=ff, fill=MUTED)

    img.save("entry.png", optimize=True)
    print(f"saved entry.png, {n_stories} stories, headline size {size}")


if __name__ == "__main__":
    main()
