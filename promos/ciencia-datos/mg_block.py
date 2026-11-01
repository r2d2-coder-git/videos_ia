# ------------------------------------------------------------------ motion graphics (output-time driven)
SYN = dict(kw=(198, 120, 221), fn=(97, 175, 239), st=(152, 195, 121), nu=(209, 154, 102), tx=INK, cm=(110, 120, 110))

def _card(d, box, p, hot=False):
    d.rounded_rectangle(box, 14, fill=mix(PANEL, BG, p), outline=mix(GRN if hot else LINE, BG, p), width=2)

def glyph(im, d, kind, box, p):
    """tiny animated illustration for each skill (p: 0..1 after the node lights up)"""
    x0, y0, x1, y1 = box; _card(d, box, min(1, p * 3), p > 0)
    if p <= 0: return
    a = min(1, p * 3); f = MO(24, 600)
    if kind == "logic":
        for i, segs in enumerate([[("if ", "kw"), ("x > 0", "tx"), (":", "tx")], [("    ok", "fn"), ("()", "tx")], [("else", "kw"), (":", "tx")]]):
            if p < 0.15 + i * 0.2: continue
            x = x0 + 22
            for t_, c in segs: d.text((x, y0 + 18 + i * 28), t_, font=f, fill=mix(SYN[c], PANEL, a)); x += f.getlength(t_)
    elif kind == "sql":
        txt = [[("SELECT ", "kw"), ("*", "tx")], [("FROM ", "kw"), ("ventas", "fn")], [("WHERE ", "kw"), ("total", "tx"), (" > ", "tx"), ("0", "nu")]]
        n = int(sum(len("".join(s for s, _ in l)) for l in txt) * min(1, p * 1.6)); k = 0
        for i, l in enumerate(txt):
            x = x0 + 22
            for t_, c in l:
                vis = t_[:max(0, n - k)]; k += len(t_)
                d.text((x, y0 + 18 + i * 28), vis, font=f, fill=SYN[c]); x += f.getlength(t_)
    elif kind == "git":
        ym, yb = y0 + 40, y0 + 80; xs = [x0 + 40 + i * 62 for i in range(5)]
        pl = eo(min(1, p * 1.5))
        d.line((xs[0], ym, xs[0] + (xs[4] - xs[0]) * pl, ym), fill=GRN, width=5)
        if pl > 0.25: d.line((xs[1], ym, xs[2], yb), fill=PURP, width=5)
        if pl > 0.45: d.line((xs[2], yb, xs[3], yb), fill=PURP, width=5)
        if pl > 0.7: d.line((xs[3], yb, xs[4], ym), fill=PURP, width=5)
        for i, x in enumerate(xs):
            if pl * 4.2 >= i: d.ellipse((x - 10, ym - 10, x + 10, ym + 10), fill=GRN)
        for i in (2, 3):
            if pl > 0.3 + 0.2 * (i - 2): d.ellipse((xs[i] - 10, yb - 10, xs[i] + 10, yb + 10), fill=PURP)
    elif kind == "pandas":
        cw, rh = (x1 - x0 - 44) / 3, 22
        for r in range(4):
            for c in range(3):
                q = eo(min(1, max(0, p * 2.2 - (r * 3 + c) * 0.08)))
                if q <= 0: continue
                bx = x0 + 22 + c * cw; by = y0 + 14 + r * (rh + 4)
                d.rounded_rectangle((bx, by, bx + cw - 6, by + rh), 4, fill=mix((40, 70, 110) if r == 0 else (34, 40, 34), PANEL, q))
    elif kind == "viz":
        vals = [0.35, 0.6, 0.45, 0.9, 0.7]; bw = 38
        for i, v in enumerate(vals):
            q = eo(min(1, max(0, p * 2 - i * 0.12))); h = (y1 - y0 - 30) * v * q
            bx = x0 + 30 + i * (bw + 18)
            d.rounded_rectangle((bx, y1 - 14 - h, bx + bw, y1 - 14), 5, fill=GRN if i == 3 else (60, 90, 60))
    elif kind == "ml":
        q = eo(min(1, p * 1.4)); pts = []
        for i in range(int(60 * q) + 1):
            u = i / 60; x = x0 + 22 + u * (x1 - x0 - 44); y = y1 - 16 - (y1 - y0 - 32) / (1 + math.exp(-12 * (u - 0.5)))
            pts.append((x, y))
        if len(pts) > 1: d.line(pts, fill=GRN, width=5, joint="curve")
        d.line((x0 + 22, (y0 + y1) / 2, x1 - 22, (y0 + y1) / 2), fill=(90, 70, 40), width=2)

SKILLS = [("Lógica", "pensar como programador", "logic", 5.48), ("SQL", "consultar bases de datos", "sql", 6.46),
          ("Git", "trabajar en equipo", "git", 7.52), ("pandas", "limpiar y transformar datos", "pandas", 8.02),
          ("Visualización", "contar historias con gráficos", "viz", 8.44), ("Machine Learning", "modelos que predicen", "ml", 9.96)]
ROUTE = (4.37, 10.80)
def route_card(tn):
    im = GRID.copy(); d = ImageDraw.Draw(im); t0 = ROUTE[0]
    pa = eo(pr(tn, t0, 0.35))
    d.text((60, 190), "// tu ruta en Ciencia de Datos", font=MO(34, 600), fill=mix(GRN, BG, pa))
    d.text((60, 240), "De cero a Machine Learning", font=HV(64, "bold"), fill=mix(INK, BG, pa))
    ys = [430 + i * 156 for i in range(6)]; xn = 120
    for i, (name, sub, kind, ta) in enumerate(SKILLS):
        y = ys[i]; on = tn >= ta; p = eo(pr(tn, ta, 0.3)); pin = eo(pr(tn, t0 + 0.15 + i * 0.06, 0.3))
        if i < 5:                                                    # connector grows towards the next node
            pl = eo(pr(tn, SKILLS[i + 1][3] - 0.3, 0.3))
            d.line((xn, y + 36, xn, y + 156 - 36), fill=mix(LINE, BG, pin), width=4)
            if pl > 0: d.line((xn, y + 36, xn, y + 36 + (120 - 72 + 72) * pl * 0.70), fill=GRN, width=6)
        glow = 0
        if on and tn - ta < 0.6: glow = 1 - (tn - ta) / 0.6
        if glow > 0:
            r = 36 + 26 * (1 - glow); d.ellipse((xn - r, y - r, xn + r, y + r), outline=mix(GRN, BG, glow), width=4)
        d.ellipse((xn - 34, y - 34, xn + 34, y + 34), fill=mix(GRN, BG, p) if on else mix(PANEL, BG, pin), outline=mix(GRN if on else LINE, BG, pin), width=3)
        d.text((xn, y), f"{i + 1:02d}", font=MO(26, 700), fill=BG if on else mix(MUT, BG, pin), anchor="mm")
        d.text((190, y - 34), name, font=HV(46, "bold"), fill=mix(INK, BG, max(p, 0.35 * pin)))
        d.text((190, y + 20), sub, font=MO(24, 500), fill=mix(MUT, BG, max(p, 0.3 * pin)))
        if on: glyph(im, d, kind, (W - 380, y - 58, W - 50, y + 58), min(1, (tn - ta) / 0.9))
    return im

# ---- Spain dot-map with the 8 real "Mundo Real" companies
SPAIN = [(-9.30, 42.90), (-8.95, 43.30), (-8.20, 43.65), (-7.70, 43.75), (-7.0, 43.55), (-5.85, 43.65), (-4.5, 43.42), (-3.8, 43.48),
         (-3.0, 43.35), (-2.0, 43.32), (-1.78, 43.37), (-1.4, 43.05), (-0.7, 42.85), (0.7, 42.85), (1.45, 42.6), (2.2, 42.43), (3.18, 42.43),
         (3.2, 41.9), (2.8, 41.65), (2.2, 41.35), (1.2, 41.08), (0.9, 40.85), (0.5, 40.55), (-0.1, 40.0), (-0.3, 39.5), (0.2, 38.8),
         (-0.4, 38.35), (-0.7, 37.95), (-0.75, 37.6), (-1.3, 37.55), (-1.9, 36.95), (-2.2, 36.72), (-3.0, 36.73), (-4.4, 36.72), (-5.0, 36.45),
         (-5.6, 36.0), (-6.05, 36.3), (-6.4, 36.8), (-6.9, 37.15), (-7.4, 37.18), (-7.5, 37.6), (-7.25, 38.2), (-7.05, 38.85), (-7.3, 39.45),
         (-7.0, 39.7), (-6.9, 40.25), (-6.85, 41.0), (-6.4, 41.5), (-6.6, 41.95), (-7.2, 41.88), (-8.1, 41.82), (-8.85, 41.88), (-8.85, 42.1),
         (-9.0, 42.5)]
ISLES = [((2.95, 39.62), 0.55, 0.30), ((4.08, 39.95), 0.28, 0.12), ((1.42, 38.98), 0.2, 0.15)]
CASES = [("FibraNova", "Sevilla", -5.98, 37.39, (-1, 1)), ("LuzClara", "Sevilla", -5.98, 37.39, (-1, -1)), ("AgroSense", "Murcia", -1.13, 37.99, (1, 1)),
         ("Donare", "Valladolid", -4.72, 41.65, (-1, -1)), ("CoberturaYa", "Zaragoza", -0.88, 41.65, (1, -1)), ("Fichaje Analytics", "Bilbao", -2.93, 43.26, (1, -1)),
         ("Dermia", "Valencia", -0.38, 39.47, (1, 1)), ("Marea", "Madrid", -3.70, 40.42, (1, 1))]
MK = 68; MX0, MY0 = 70, 470
def geo(lon, lat): return (MX0 + (lon + 9.5) * MK, MY0 + (44.0 - lat) * MK * 1.3)
def _dot_map():
    mask = Image.new("L", (W, H)); md = ImageDraw.Draw(mask)
    md.polygon([geo(*p) for p in SPAIN], fill=255)
    for (lon, lat), rx, ry in ISLES:
        cx, cy = geo(lon, lat); md.ellipse((cx - rx * MK, cy - ry * MK * 1.3, cx + rx * MK, cy + ry * MK * 1.3), fill=255)
    pts = [(x, y) for y in range(MY0 - 20, MY0 + 760, 15) for x in range(MX0, W - 40, 15) if mask.getpixel((x, y)) > 0]
    return pts
MAPDOTS = _dot_map()
MAP = (13.50, 19.96); ZOOM_T = 17.20; PIN_T = 14.68
def map_card(tn):
    im = GRID.copy(); d = ImageDraw.Draw(im); t0 = MAP[0]
    pa = eo(pr(tn, t0, 0.35))
    z = 1 + 1.6 * eo(pr(tn, ZOOM_T, 0.8)); fx, fy = geo(-5.98, 37.39)
    def S(x, y): return (fx + (x - fx) * z + (W / 2 - fx) * (z - 1) / 1.6 * eo(pr(tn, ZOOM_T, 0.8)) * 1.0,
                         fy + (y - fy) * z + (900 - fy) * (z - 1) / 1.6)
    fade = 1 - 0.75 * eo(pr(tn, ZOOM_T, 0.6))
    for x, y in MAPDOTS:
        q = eo(pr(tn, t0 + 0.05 + (x - MX0) / 2600, 0.3))
        if q <= 0: continue
        sx, sy = S(x, y); r = 2.6 * min(z, 1.8)
        if -10 < sx < W + 10 and -10 < sy < H + 10:
            d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=mix((70, 110, 60), BG, q * fade))
    ph = eo(pr(tn, t0 + 0.1, 0.35)) * (1 - eo(pr(tn, ZOOM_T, 0.4)))
    d.text((60, 190), "// mundo real", font=MO(34, 600), fill=mix(GRN, BG, ph))
    d.text((60, 240), "8 empresas simuladas", font=HV(64, "bold"), fill=mix(INK, BG, ph))
    for i, (name, city, lon, lat, (dx, dy)) in enumerate(CASES):
        p = eo(pr(tn, PIN_T + i * 0.14, 0.3))
        if p <= 0: continue
        sx, sy = S(*geo(lon, lat)); main = name == "FibraNova"
        k = 1 if not (tn >= ZOOM_T) or main else 1 - eo(pr(tn, ZOOM_T, 0.4))
        if k <= 0.01: continue
        drop = (1 - p) * 40
        r = 13 if main and tn >= ZOOM_T else 10
        d.ellipse((sx - r, sy - r - drop, sx + r, sy + r - drop), fill=mix(GRN if (main and tn >= ZOOM_T) else (255, 145, 30), BG, p * k))
        if main and tn >= ZOOM_T:
            u = (tn - ZOOM_T) % 1.0; rr = 14 + 40 * u
            d.ellipse((sx - rr, sy - rr, sx + rr, sy + rr), outline=mix(GRN, BG, 1 - u), width=3)
        if tn < ZOOM_T or not main:
            lx = sx + dx * 22; ly = sy + dy * 30 - drop
            d.text((lx, ly), name, font=MO(26, 700), fill=mix(INK, BG, p * k), anchor="lm" if dx > 0 else "rm")
    # FibraNova case card after the zoom
    pc = eo(pr(tn, ZOOM_T + 0.5, 0.4))
    if pc > 0:
        y = 1100 + (1 - pc) * 50
        d.rounded_rectangle((60, y, W - 60, y + 250), 20, fill=mix(PANEL, BG, pc), outline=mix(GRN, BG, pc), width=3)
        d.text((100, y + 34), "caso 01 · nivel junior", font=MO(28, 600), fill=mix(GRN, PANEL, pc))
        d.text((100, y + 80), "FibraNova", font=HV(72, "bold"), fill=mix(INK, PANEL, pc))
        pt = eo(pr(tn, 18.40, 0.3))
        d.text((100, y + 176), "Telecomunicaciones · Sevilla", font=HV(38, "reg"), fill=mix(MUT, PANEL, pc * max(0.0, pt)))
    return im

# ---- end card: the three-ring logo assembles, then the URL
END = 38.64
def end_card(tn):
    im = GRID.copy(); d = ImageDraw.Draw(im); cx, cy = W / 2, 640
    for i, c in enumerate((PURP, (96, 165, 250), (74, 222, 128))):
        p = pr(tn, END + 0.05 + i * 0.16, 0.45)
        if p <= 0: continue
        e = 1 - (1 - p) ** 3; bounce = math.sin(min(1, p) * math.pi) * 0.12 * (1 - p)
        y = cy - 120 + i * 92 - (1 - e) * 500 + bounce * 60
        d.ellipse((cx - 150, y, cx + 150, y + 112), outline=mix(c, BG, min(1, p * 2)), width=22)
    pt = pr(tn, END + 0.75, 0.6); s = "~/bigdatastack"; n = int(len(s) * pt)
    if pt > 0:
        f = MO(74, 700); w = f.getlength(s); x = cx - w / 2
        d.text((x, 1000), s[:n], font=f, fill=INK)
        if n > len("~/bigdata"): d.text((x + f.getlength("~/bigdata"), 1000), s[len("~/bigdata"):n], font=f, fill=GRN)
    pu = eo(pr(tn, END + 1.3, 0.35))
    if pu > 0:
        f = MO(56, 700); s = "bigdatastack.dev"; w = f.getlength(s) + 80; y = 1130 + (1 - pu) * 30
        d.rounded_rectangle((cx - w / 2, y, cx + w / 2, y + 110), 22, fill=mix(GRN, BG, pu))
        d.text((cx, y + 55), s, font=f, fill=BG, anchor="mm")
    return im

MG_SFX = [ROUTE[0], MAP[0], ZOOM_T, END]                      # whooshes (output time)
MG_POPS = [s[3] for s in SKILLS] + [PIN_T + i * 0.14 for i in range(8)] + [END + 0.05 + i * 0.16 + 0.4 for i in range(3)]

