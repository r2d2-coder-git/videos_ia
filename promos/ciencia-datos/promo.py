"""Promo BigDataStack · Ciencia de Datos (formato reel de referencia: cara a pantalla completa + recursos de la plataforma).
Uso: ../../motor/.venv/bin/python promo.py edl|stills <t...>|full|qa"""
import os, sys, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
MOTOR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "motor"); sys.path.insert(0, MOTOR)
import hybrid
from render import eo, pr, mix
from stylef import MO
from render2 import HV

SRC = os.path.join(HERE, "src_prores_mp4.mov")          # SDR ProRes master — video only. Not kept (7 GB); regenerate: swift ../../motor/hdr2prores.swift originales/ciencia_datos_bds.mp4 src_prores_mp4.mov
AUDIO = os.path.join(HERE, "originales", "ciencia_datos_bds.mp4")   # original recording: the voice comes from here
SH = os.path.join(HERE, "shots")                          # platform screenshots
OUT = os.path.join(HERE, "ciencia_datos_bds_editado.mp4")
W, H, FPS = 1080, 1920, 60
BG, PANEL, LINE = (12, 14, 12), (20, 23, 20), (40, 46, 40)
GRN, CYAN, PURP, INK, MUT = (163, 230, 53), (56, 189, 248), (167, 139, 250), (226, 232, 226), (128, 138, 128)

hybrid.A16["bds"] = os.path.join(HERE, "a16.npy")
SEGS = [(3.58, 6.02), (8.45, 10.14), (29.34, 34.24), (34.53, 35.84), (41.80, 47.49, "vs"), (62.91, 66.18), (66.37, 68.45),
        (73.09, 78.30), (78.50, 81.28), (119.97, 123.50, "ve"), (162.50, 169.50)]
EDL = hybrid.build_edl("bds", SEGS)
TL = hybrid.Timeline(EDL)

def img(name):
    return Image.open(os.path.join(SH, name)).convert("RGB")
SHOT = {k: img(f"m_{k}.png") for k in ("home",)}
SHOT.update({k: img(f"L_{k}.png") for k in ("entrena", "mundo", "fibra", "lunes")})          # captured signed in (no "crear cuenta" buttons)

def keys(t, kf):
    """piecewise eased interpolation over [(t, value)], 0.35 s moves (phone-scroll feel)."""
    if t <= kf[0][0]: return kf[0][1]
    if len(kf) == 2:                                             # one slow drift over the whole span
        u = min(1.0, (t - kf[0][0]) / (kf[1][0] - kf[0][0])); u = u * u * (3 - 2 * u)
        return kf[0][1] + (kf[1][1] - kf[0][1]) * u
    for (t0, v0), (t1, v1) in zip(kf, kf[1:]):
        if t < t1:
            d = min(0.45, t1 - t0); p = eo(pr(t, t1 - d, d)); return v0 + (v1 - v0) * p
    return kf[-1][1]

def shot_frame(name, t, ykf, zkf=None):
    im = SHOT[name]; z = keys(t, zkf) if zkf else 1.0
    cw, ch = W / z, H / z
    yc = keys(t, ykf)                                            # y of the crop centre in the screenshot
    dx = 6 * math.sin(t * 1.3); dy = 5 * math.sin(t * 1.7 + 1)      # slight handheld drift
    x0 = (im.width - cw) / 2 + dx; y0 = min(max(yc - ch / 2 + dy, 0), im.height - ch)
    return im.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.Resampling.BICUBIC)

# ------------------------------------------------------------------ graphics
def grid_bg():
    g = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(g)
    for x in range(0, W, 54): d.line((x, 0, x, H), fill=(18, 21, 18))
    for y in range(0, H, 54): d.line((0, y, W, y), fill=(18, 21, 18))
    return g
GRID = grid_bg()

def logo(d, x, y, s=1.0, a=1.0):
    for i, c in enumerate((PURP, (96, 165, 250), (74, 222, 128))):
        yy = y + i * 22 * s
        d.ellipse((x, yy, x + 64 * s, yy + 26 * s), outline=mix(c, BG, a), width=max(2, int(6 * s)))

def team_card(t, t0):
    im = GRID.copy(); d = ImageDraw.Draw(im)
    pa = eo(pr(t, t0, 0.35))
    logo(d, 70, 200, 0.8, pa)
    d.text((150, 208), "~/fibranova · tu equipo", font=MO(40, 600), fill=mix(INK, BG, pa))
    d.text((70, 280), "FibraNova · Telecom · Sevilla", font=HV(52, "bold"), fill=mix(GRN, BG, pa))
    people = [("RH", "Raúl Herrera", "Data Lead · tu mentor", CYAN), ("LP", "Lola Prieto", "Responsable de Retención", (251, 146, 60)),
              ("BM", "Bea Montes", "Data Scientist · compañera", PURP), ("IV", "Ignacio Vázquez", "Director de Clientes", (244, 114, 182)),
              ("TÚ", "Tú", "Data Scientist junior", GRN)]
    for i, (ini, name, role, col) in enumerate(people):
        p = eo(pr(t, t0 + 0.15 + i * 0.22, 0.35))
        if p <= 0: continue
        y = 400 + i * 196 + (1 - p) * 40; me = ini == "TÚ"
        box = (70, y, W - 70, y + 176)
        d.rounded_rectangle(box, 18, fill=mix((26, 40, 18) if me else PANEL, BG, p), outline=mix(GRN if me else LINE, BG, p), width=4 if me else 2)
        d.ellipse((110, y + 30, 226, y + 146), fill=mix(col, BG, p * 0.9))
        d.text((168, y + 88), ini, font=HV(40, "bold"), fill=mix(BG, col, p), anchor="mm")
        d.text((262, y + 42), name, font=HV(50, "bold"), fill=mix(GRN if me else INK, BG, p))
        d.text((262, y + 108), role, font=MO(30, 500), fill=mix(MUT, BG, p))
    return im

DISCORD = (851, 16)          # approximate_member_count / presence_count from discord.com/api/v10/invites/qUm7ZHFGQe (2026-10-23)
def discord_card(t, t0):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        u = y / H; d.line((0, y, W, y), fill=(int(30 + 30 * u), int(33 + 20 * u), int(110 + 60 * u)))
    rng = np.random.RandomState(4)
    for _ in range(90):
        x, y, r = rng.randint(0, W), rng.randint(0, H), rng.choice([2, 3, 4])
        tw = 0.5 + 0.5 * math.sin(t * 3 + x)
        d.ellipse((x, y, x + r, y + r), fill=(int(150 + 100 * tw),) * 3)
    p = eo(pr(t, t0, 0.4)); y0 = 560 + (1 - p) * 60
    card = (90, y0, W - 90, y0 + 760)
    d.rounded_rectangle(card, 28, fill=mix((49, 51, 56), (40, 45, 140), p))
    cx = W // 2
    d.ellipse((cx - 85, y0 + 70, cx + 85, y0 + 240), fill=mix(BG, (49, 51, 56), p))
    logo(d, cx - 40, y0 + 120, 1.25, p)
    d.text((cx, y0 + 300), "Te han invitado a unirte a", font=HV(34, "reg"), fill=mix((181, 186, 193), (49, 51, 56), p), anchor="mm")
    d.text((cx, y0 + 370), "BIG DATA STACK", font=HV(64, "bold"), fill=mix((242, 243, 245), (49, 51, 56), p), anchor="mm")
    pc = eo(pr(t, t0 + 0.3, 0.9)); f = HV(32, "reg")
    on, mem = f"{round(DISCORD[1] * pc)} en línea", f"{round(DISCORD[0] * pc)} miembros"
    wa, wb = f.getlength(on), f.getlength(mem); x = cx - (wa + wb + 90) / 2; yy = y0 + 440
    d.ellipse((x, yy - 9, x + 18, yy + 9), fill=mix((35, 165, 90), (49, 51, 56), p)); d.text((x + 28, yy), on, font=f, fill=mix((181, 186, 193), (49, 51, 56), p), anchor="lm")
    x += 28 + wa + 34
    d.ellipse((x, yy - 9, x + 18, yy + 9), fill=mix((128, 132, 142), (49, 51, 56), p)); d.text((x + 28, yy), mem, font=f, fill=mix((181, 186, 193), (49, 51, 56), p), anchor="lm")
    pb = eo(pr(t, t0 + 1.4, 0.15)); press = 1 - 0.04 * math.sin(math.pi * min(1, max(0, (t - t0 - 1.4) / 0.25)))
    bw, bh = 640 * press, 112 * press
    d.rounded_rectangle((cx - bw / 2, y0 + 560, cx + bw / 2, y0 + 560 + bh), 14, fill=mix((88, 101, 242), (49, 51, 56), p))
    d.text((cx, y0 + 560 + bh / 2), "Aceptar invitación" if pb < 0.5 else "¡Te has unido!", font=HV(40, "bold"), fill=(255, 255, 255), anchor="mm")
    return im

CHART = Image.open(os.path.join(SH, "chart_desk.png")).convert("RGB")
CHART = CHART.resize((W - 80, int(CHART.height * (W - 80) / CHART.width)), Image.Resampling.LANCZOS)
RISK = [("C-48213", 0.91), ("C-10577", 0.86), ("C-33902", 0.79), ("C-27145", 0.64), ("C-51830", 0.22), ("C-09114", 0.07)]
def model_card(t, t0):
    im = GRID.copy(); d = ImageDraw.Draw(im)
    pa = eo(pr(t, t0, 0.35))
    d.text((40, 222), "Regresión logística", font=HV(76, "bold"), fill=mix(INK, BG, pa))
    d.text((40, 318), "¿qué clientes se van a ir?", font=HV(46, "reg"), fill=mix(MUT, BG, pa))
    y = 420; pw = eo(pr(t, t0 + 0.2, 1.6))                         # chart wipes in left -> right
    if pw > 0:
        cw = int(CHART.width * pw); im.paste(CHART.crop((0, 0, max(1, cw), CHART.height)), (40, y))
    ty = y + CHART.height + 70
    pt = eo(pr(t, t0 + 2.4, 0.3))
    d.text((40, ty), "cliente_id", font=MO(30, 600), fill=mix(MUT, BG, pt)); d.text((W - 40, ty), "prob. de baja", font=MO(30, 600), fill=mix(MUT, BG, pt), anchor="ra")
    for i, (cid, pb) in enumerate(RISK):
        p = eo(pr(t, t0 + 2.6 + i * 0.18, 0.3))
        if p <= 0: continue
        yy = ty + 60 + i * 74; hot = pb > 0.6; col = (248, 113, 113) if hot else GRN
        d.rounded_rectangle((40, yy, W - 40, yy + 64), 10, fill=mix(PANEL, BG, p), outline=mix((90, 40, 40) if hot else LINE, BG, p), width=2)
        d.text((70, yy + 32), cid, font=MO(36, 600), fill=mix(INK, BG, p), anchor="lm")
        bx0, bx1 = 420, W - 200
        d.rounded_rectangle((bx0, yy + 22, bx0 + (bx1 - bx0) * pb * p, yy + 42), 6, fill=col)
        d.text((W - 70, yy + 32), f"{pb:.2f}".replace(".", ","), font=MO(36, 700), fill=mix(col, BG, p), anchor="rm")
    ph = eo(pr(t, t0 + 4.2, 0.3))
    if ph > 0:
        yy = ty + 60 + 6 * 74 + 10
        d.text((W // 2, yy + 30), "↑ a estos llama primero Retención", font=MO(34, 700), fill=mix((248, 113, 113), BG, ph), anchor="mm")
    out = GRID.copy(); out.paste(im.crop((0, 0, W, H - 40)), (0, 40))       # centre the block vertically
    return out

# ------------------------------------------------------------------ overlays
def pill_text(d, cx, y, text, f, p, fg=(10, 10, 10), bg=(255, 255, 255)):
    w = f.getlength(text); pad = 26
    d.rounded_rectangle((cx - w / 2 - pad, y, cx + w / 2 + pad, y + f.size * 1.45), 18, fill=bg)
    d.text((cx, y + f.size * 0.72), text, font=f, fill=fg, anchor="mm")

def hook(im, t):
    """reel-style opener: white boxes, black bold text"""
    d = ImageDraw.Draw(im); f = HV(76, "bold")
    for txt, tt, y in (("Aprende ciencia de datos", 3.62, 330), ("gratis y en español", 4.38, 450)):
        p = eo(pr(t, tt, 0.25))
        if p <= 0: continue
        lay = Image.new("RGBA", (W, H)); ld = ImageDraw.Draw(lay); pill_text(ld, W // 2, y + (1 - p) * 20, txt, f, p)
        a = lay.split()[3].point(lambda v: int(v * p)); im.paste(lay, (0, 0), a)

def url_overlay(im, t, t0):
    d = ImageDraw.Draw(im); p = eo(pr(t, t0, 0.3))
    if p <= 0: return
    full = "bigdatastack.dev"; n = int(len(full) * eo(pr(t, t0 + 0.1, 0.6)))
    f = MO(70, 700); y = 1180 + (1 - p) * 30
    w = f.getlength(full) + 80
    d.rounded_rectangle((W / 2 - w / 2, y, W / 2 + w / 2, y + 130), 22, fill=GRN)
    d.text((W / 2 - f.getlength(full) / 2, y + 65), full[:n] + ("▍" if int(t * 3) % 2 == 0 and n < len(full) else ""), font=f, fill=BG, anchor="lm")

def chip(im, t, t0, text, y=1180):
    d = ImageDraw.Draw(im); p = eo(pr(t, t0, 0.3))
    if p <= 0: return
    f = MO(46, 700); w = f.getlength(text) + 70; y = y + (1 - p) * 30
    d.rounded_rectangle((W / 2 - w / 2, y, W / 2 + w / 2, y + 100), 18, fill=mix(GRN, BG, p))
    d.text((W / 2, y + 50), text, font=f, fill=BG, anchor="mm")

CODE = (30.50, 35.33)          # output-time window (orig 119.92-123.57 + 162.45-163.62)
def run_code(im, t, t0):
    """simulated [ejecutar ▶] press + output panel sliding up"""
    d = ImageDraw.Draw(im)
    if t < t0 - 0.8: return
    pk = max(0.0, 1 - abs(t - t0) / 0.2)
    if pk > 0: d.rounded_rectangle((25, 1208, 335, 1285), 10, outline=GRN, width=5)
    pm = eo(pr(t, t0 - 0.7, 0.6)); cx_, cy_ = 760 + (175 - 760) * pm, 980 + (1262 - 980) * pm     # pointer glides to [ejecutar ▶]
    if t > t0 + 0.1: cx_, cy_ = 175, 1262
    if t < t0 + 1.2:
        k = 1.4 * (0.85 if abs(t - t0) < 0.08 else 1)
        arrow = [(0, 0), (0, 34), (9, 26), (16, 42), (23, 39), (16, 24), (28, 24)]
        pts = [(cx_ + x * k, cy_ + y * k) for x, y in arrow]
        d.polygon(pts, fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    if t0 <= t < t0 + 0.35:
        r = 20 + 90 * (t - t0) / 0.35; a_ = 1 - (t - t0) / 0.35
        d.ellipse((175 - r, 1247 - r, 175 + r, 1247 + r), outline=mix(GRN, (20, 24, 20), a_), width=4)
    p = eo(pr(t, t0 + 0.25, 0.35))
    if p <= 0: return
    y = 230 - (1 - p) * 60
    d.rounded_rectangle((40, y, W - 40, y + 420), 16, fill=(16, 22, 14), outline=GRN, width=3)
    d.text((80, y + 40), "▶ salida  ·  ejecutado en tu navegador", font=MO(30, 600), fill=GRN)
    for i, line in enumerate(["clientes: (12000, 9)", "consumo: (72000, 5)", "tickets: (18253, 4)", "bajas: (600, 3)"]):
        pl = eo(pr(t, t0 + 0.45 + i * 0.12, 0.2))
        d.text((80, y + 110 + i * 70), line, font=MO(40, 500), fill=mix(INK, (16, 22, 14), pl))

# ---- subtitles in the reference reel style: 1-3 words, heavy UPPERCASE, white with black outline,
#      the word being spoken painted orange; lower third
import json
from PIL import ImageFont
ORANGE = (255, 145, 30)
SUBF = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 78); SUBF.set_variation_by_axes([100, 96, 400, 900])
FIX = {"bigdatastack": "BIGDATASTACK.DEV", "ocho": "8"}
def _chunks():
    ws = [w for w in json.load(open(os.path.join(HERE, "words_out.json"))) if w[2].strip(".") != "dev"]
    words = []
    for s_, e_, w in ws:
        key = w.strip(".,").lower()
        txt = FIX.get(key, w.strip(".,").upper())
        words.append([s_, e_, txt, w[-1] in ".,?!"])
    out, cur = [], []
    for w in words:
        if cur and (len(cur) == 3 or len(" ".join(x[2] for x in cur + [w])) > 17 or w[0] - cur[-1][1] > 0.35): out.append(cur); cur = []
        cur.append(w)
        if w[3]: out.append(cur); cur = []
    if cur: out.append(cur)
    for i in range(len(out) - 1): out[i][-1][1] = max(out[i][-1][1], min(out[i + 1][0][0], out[i][-1][1] + 0.3))
    return out
SUBS = _chunks()
def subs(im, tn):
    cur = [c for c in SUBS if c[0][0] - 0.04 <= tn < c[-1][1]]
    if not cur: return
    ch = cur[0]
    pop = 1 + 0.08 * (1 - eo(pr(tn, ch[0][0] - 0.04, 0.12)))          # small pop when a chunk appears
    lay = Image.new("RGBA", (W, 260)); d = ImageDraw.Draw(lay)
    sp = SUBF.getlength(" ") * 0.75
    widths = [SUBF.getlength(w[2]) for w in ch]; total = sum(widths) + sp * (len(ch) - 1)
    x = W / 2 - total / 2
    for w, wd in zip(ch, widths):
        col = ORANGE if w[0] - 0.04 <= tn < w[1] + 0.06 else (255, 255, 255)
        d.text((x, 130), w[2], font=SUBF, fill=col, anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
        x += wd + sp
    if pop != 1: lay = lay.resize((int(W * pop), int(260 * pop)), Image.Resampling.BICUBIC)
    im.paste(lay, (int(W / 2 - lay.width / 2), int(1480 - lay.height / 2)), lay)

def cta(im, t, t0):
    d = ImageDraw.Draw(im)
    p = eo(pr(t, t0, 0.3))
    if p <= 0: return
    url_overlay(im, t, t0 + 0.4)

# ------------------------------------------------------------------ B-roll plan (original seconds)
BROLL = [  # (t0, t1, kind, args)
    (66.27, 68.55, "team", ()),
    (75.05, 81.40, "model", ()),
    (163.50, 166.80, "discord", ()),          # starts under the code shot so no face frame slips between them
]

def face_frame(fr, piece):
    z = 1.07 if piece % 2 else 1.0
    if z == 1.0: return fr
    cw, ch = W / z, H / z; x0 = (W - cw) / 2; y0 = (H - ch) * 0.4
    return fr.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.Resampling.BICUBIC)

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
ROUTE = (4.37, 10.82)          # ends exactly on the cut (no stray face frames)
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
    zp = eo(pr(tn, ZOOM_T, 0.8)); z = 1 + 0.9 * zp; fx, fy = geo(-5.98, 37.39)
    ccx, ccy = fx + (W / 2 - fx) * zp, fy + (820 - fy) * zp       # Sevilla glides to the centre while zooming in
    def S(x, y): return (ccx + (x - fx) * z, ccy + (y - fy) * z)
    fade = 1 - 0.45 * eo(pr(tn, ZOOM_T, 0.6))
    for x, y in MAPDOTS:
        q = eo(pr(tn, t0 + 0.05 + (x - MX0) / 2600, 0.3))
        if q <= 0: continue
        sx, sy = S(x, y); r = 2.6 * z
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
END = 999.0          # end card disabled: the user wants his face for the CTA
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

STATS = [(6.6, "K", "ALUMNOS APRENDIENDO", GRN), (31.4, "K", "LECCIONES COMPLETADAS", CYAN), (127.4, "K", "EJERCICIOS EJECUTADOS", (251, 146, 60))]
STATS_T = (2.57, 4.39)          # "Se llama bigdatastack.dev" (pointing at the monitor); numbers from the site's home page
def stats_overlay(im, tn):
    lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay)
    for i, (v, u, lab, col) in enumerate(STATS):
        p = eo(pr(tn, STATS_T[0] + 0.15 + i * 0.15, 0.25))
        if p <= 0: continue
        val = v * eo(pr(tn, STATS_T[0] + 0.15 + i * 0.15, 0.6)); y = 230 + i * 190 + (1 - p) * 30
        box = (60, y, 640, y + 160)
        d.rounded_rectangle(box, 22, fill=(10, 12, 10, int(215 * p)), outline=col + (int(255 * p),), width=3)
        txt = "+" + f"{val:.1f}".replace(".", ",") + u
        d.text((95, y + 70), txt, font=HV(80, "bold"), fill=col + (int(255 * p),), anchor="lm")
        d.text((97, y + 128), lab, font=MO(24, 600), fill=(200, 205, 200, int(255 * p)), anchor="lm")
    im.paste(lay, (0, 0), lay)

EMPH = [(0.70, 1.75), (22.30, 23.40), (40.55, 41.30)]   # gratis · tu encargo · mi perfil
def emph(im, tn):
    for a, b in EMPH:
        if a <= tn < b:
            k = eo(pr(tn, a, 0.14)) * (1 - eo(pr(tn, b - 0.18, 0.18))); z = 1 + 0.12 * k
            if z <= 1.001: return im
            cw, ch = W / z, H / z; x0 = (W - cw) / 2; y0 = (H - ch) * 0.38
            return im.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.Resampling.BICUBIC)
    return im

def compose(fr, tn):
    piece, T = TL.locate(tn)
    im = emph(face_frame(fr, piece), tn)
    for t0, t1, kind, args in BROLL:
        if t0 <= T < t1:
            if kind == "shot": im = shot_frame(args[0], T, args[1], args[2])
            elif kind == "team": im = team_card(T, t0)
            elif kind == "discord": im = discord_card(T, t0)
            elif kind == "model": im = model_card(T, t0)
    if CODE[0] <= tn < CODE[1]:                                   # in-browser code: whole sentence + start of the next one
        im = shot_frame("lunes", tn, [(CODE[0], 2290), (CODE[1], 2330)], [(CODE[0], 1.0), (CODE[1], 1.04)])
        run_code(im, tn, CODE[0] + 0.9)
    if ROUTE[0] <= tn < ROUTE[1]: im = route_card(tn)
    if MAP[0] <= tn < MAP[1]: im = map_card(tn)
    if tn >= END: im = end_card(tn)

    subs(im, tn)
    # progress bar
    d = ImageDraw.Draw(im); d.rectangle((0, H - 8, W * tn / TL.dur, H), fill=GRN)
    return im

def frames(times):
    """yield (tn, PIL frame) reading the proxy piece by piece"""
    times = sorted(times)
    for i, (s, e) in enumerate(EDL):
        ts = [tn for tn in times if TL.locate(tn)[0] == i]
        if not ts: continue
        p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{s:.3f}", "-i", SRC, "-t", f"{e - s + 0.2:.3f}",
                              "-vf", f"fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        k = 0; buf = None
        for tn in ts:
            want = int(round((TL.locate(tn)[1] - s) * FPS))
            while k <= want:
                raw = p.stdout.read(W * H * 3)
                if len(raw) < W * H * 3: break
                buf = raw; k += 1
            yield tn, Image.frombytes("RGB", (W, H), buf)
        p.stdout.close(); p.wait()

def sfx(wav):
    with wave.open(wav) as w:
        sr = w.getframerate(); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2) / 32767
    n = len(v); fx = np.zeros((n, 2), np.float32); rng = np.random.RandomState(3)
    def whoosh(d=0.5, vol=0.045):
        N = int(d * sr); hop, win = 128, 1024; noise = rng.randn(N + win); out = np.zeros(N + win); norm = np.zeros(N + win)
        wn = np.hanning(win); fq = np.fft.rfftfreq(win, 1 / sr)
        for i in range(0, N, hop):
            fc = 260 + 1100 * np.sin(np.pi * i / N) ** 1.5
            band = np.exp(-0.5 * (np.log2(np.maximum(fq, 1) / fc) / 0.45) ** 2); band[fq > 3200] = 0
            out[i:i + win] += np.fft.irfft(np.fft.rfft(noise[i:i + win] * wn) * band) * wn; norm[i:i + win] += wn ** 2
        out = (out / np.maximum(norm, 1e-6))[:N]; tt = np.arange(N) / N
        s = out * np.sin(np.pi * tt) ** 2; s = s / (np.abs(s).max() + 1e-9) * vol; pan = 0.5 - 0.5 * np.cos(np.pi * tt)
        return np.stack([s * np.sqrt(1 - pan), s * np.sqrt(pan)], 1)
    def click(f=2400, vol=0.05):
        tt = np.arange(int(0.03 * sr)) / sr; s = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 160) * vol; return np.stack([s, s], 1)
    def to_new(T):
        for (s, e), st in zip(TL.edl, TL.starts):
            if s <= T <= e: return st + T - s
            if T < s: return st
    def put(T, sig, lead=0.0, new=False):
        tn = T if new else to_new(T)
        if tn is None: return
        i = int(max(0, tn - lead) * sr); m = min(len(sig), n - i)
        if m > 0: fx[i:i + m] += sig[:m]
    for t0, *_ in BROLL: put(t0, whoosh(), lead=0.25)
    for t in MG_SFX: put(t, whoosh(), lead=0.25, new=True)
    for t in MG_POPS: put(t, click(1500, vol=0.035), new=True)
    put(120.80, click(1800)); put(165.02, click(2200)); put(166.9, click(2600))
    env = np.convolve(np.abs(v.mean(1)), np.ones(int(0.05 * sr)) / int(0.05 * sr), "same")
    out = np.clip(v + fx * (1 - 0.55 * np.clip(env / 0.08, 0, 1))[:, None], -1, 1)
    o = wav.replace(".wav", "_sfx.wav")
    with wave.open(o, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out * 32767).astype(np.int16).tobytes())
    return o

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "edl":
        for (s, e), st in zip(TL.edl, TL.starts): print(f"orig {s:7.2f}-{e:7.2f}  new {st:6.2f}")
        print("dur", round(TL.dur, 2))
    elif mode == "qa":
        import qa
        qa.check(OUT, cuts=TL.starts[1:], voice=os.path.join(HERE, "audio.wav"), src_a16=np.load(hybrid.A16["bds"]), edl=TL.edl)
    elif mode == "stills":
        for tn, fr in frames([float(x) for x in sys.argv[2:]]):
            compose(fr, tn).save(os.path.join(HERE, f"s_{tn:05.1f}.jpg"), quality=85)
    else:
        wav = os.path.join(HERE, "audio.wav"); mov = AUDIO
        fc = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={e - s - 0.015:.3f}:d=0.015[a{i}];"
                     for i, (s, e) in enumerate(EDL)) + "".join(f"[a{i}]" for i in range(len(EDL))) + f"concat=n={len(EDL)}:v=0:a=1,aformat=channel_layouts=stereo[a]"
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", mov, "-filter_complex", fc, "-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", wav], check=True)
        wav = sfx(wav)
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-tune", "film", "-pix_fmt", "yuv420p",
                              "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
        N = int(TL.dur * FPS)
        for k, (tn, fr) in enumerate(frames([i / FPS for i in range(N)])):
            p.stdin.write(compose(fr, tn).tobytes())
            if k % 300 == 0: print(k, N, flush=True)
        p.stdin.close(); p.wait(); print("done", N, round(TL.dur, 2))
