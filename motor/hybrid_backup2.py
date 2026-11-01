"""Generic r2d2.coder interview-exercise editor: surgical cuts + hybrid (Swiss + Terminal) panel.
All event times are ORIGINAL-video seconds (word timestamps); the renderer maps new time -> original time."""
import os, sys, math, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "previews"); sys.path.insert(0, HERE); os.makedirs(ROOT, exist_ok=True)
import numpy as np, av
from PIL import Image, ImageDraw
import render as R
from render import eo, pr, mix, cl
from render2 import HV, WH, BK, GR, LG, RED
from stylef import MO, BSYN

W, H, CAM, FPS = 1080, 1920, 605, 30
PW, PH = W, H - CAM
TB, TP, INK, MUT, DIM, RUL = (10, 12, 15), (15, 18, 22), (220, 226, 234), (110, 120, 135), (70, 78, 92), (34, 39, 48)
ACC, OK, WARN, CMT = (88, 166, 255), (86, 211, 140), (240, 190, 80), (120, 130, 145)

def tx(d, xy, s, f, col, a=1.0, bg=WH, anchor="la"):
    if a > 0.01: d.text(xy, s, font=f, fill=mix(col, bg, a), anchor=anchor)
def slide(t, t0, d=0.35, dist=24):
    p = eo(pr(t, t0, d)); return p, dist * (1 - p)

# ------------------------------------------------------------------ EDL
def build_edl(name, segs, pre=0.05, post=0.07):
    a = np.load(os.path.join(HERE, f"{name}_a16.npy"))
    fr = 160; rms = np.sqrt(np.convolve(a ** 2, np.ones(fr) / fr, "same"))[::fr]
    def valley(t, w):
        i0, i1 = int((t - w) * 100), int((t + w) * 100); return (i0 + int(np.argmin(rms[i0:i1]))) / 100
    out = []
    for s, e, *flags in segs:
        if "vs" in flags: s = valley(s, 0.08)
        if "ve" in flags: e = valley(e, 0.08)
        s -= 0 if "vs" in flags else pre; e += 0 if "ve" in flags else post
        if out and s - out[-1][1] < 0.10: out[-1] = (out[-1][0], e)
        else: out.append((s, e))
    return out

class Timeline:
    def __init__(self, edl):
        self.edl = edl; self.starts = []; acc = 0.0
        for s, e in edl: self.starts.append(acc); acc += e - s
        self.dur = acc
    def locate(self, tn):
        for i, (s, e) in enumerate(self.edl):
            if tn < self.starts[i] + (e - s) or i == len(self.edl) - 1: return i, s + tn - self.starts[i]

# ------------------------------------------------------------------ Swiss pieces
def swiss_header(d, num, label, sub, t, t0):
    d.rectangle((0, 0, PW, 200), fill=WH)
    p, dx = slide(t, t0, 0.35, 30)
    tx(d, (40 - dx, 38), num, HV(120, "bold"), RED, p)
    tx(d, (300, 56), label, HV(30, "bold"), BK, p)
    tx(d, (300, 98), sub, HV(26, "reg"), GR, p)
    d.line((40, 196, PW - 40, 196), fill=BK, width=3)


# ------------------------------------------------------------------ brand logo (Apple glyph from SF Pro, U+F8FF)
_logo_cache = {}
def logo_parts(size):
    """Body and leaf of the Apple glyph as separate RGBA sprites (so the leaf can be animated on its own)."""
    if size in _logo_cache: return _logo_cache[size]
    from PIL import ImageFont
    f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", size)
    l, tp, r, bt = f.getbbox("\uf8ff")
    w, h = r - l + 4, bt - tp + 4
    mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).text((2 - l, 2 - tp), "\uf8ff", font=f, fill=255)
    rows = [sum(mask.crop((0, y, w, y + 1)).getdata()) for y in range(h)]
    lo, hi = int(h * 0.12), int(h * 0.45)
    split = min(range(lo, hi), key=lambda y: rows[y])          # thinnest row between leaf and body
    leaf_m = mask.crop((0, 0, w, split)); body_m = mask.crop((0, split, w, h))
    def sprite(mk):
        im = Image.new("RGBA", mk.size, BK + (0,)); im.putalpha(mk); return im
    _logo_cache[size] = (sprite(body_m), sprite(leaf_m), split, mask)
    return _logo_cache[size]

def draw_logo(img, cx, cy, size, t, t0):
    body, leaf, split, mask = logo_parts(size)
    from render import eback
    pb = pr(t, t0, 0.5)
    if pb <= 0: return
    w, h = mask.size
    s = max(0.01, eback(pb, 1.9))
    b = body.resize((max(1, int(body.width * s)), max(1, int(body.height * s))), Image.LANCZOS)
    by = cy - h / 2 + split
    img.paste(b, (int(cx - b.width / 2), int(by + body.height / 2 - b.height / 2)), b)
    pl = eo(pr(t, t0 + 0.3, 0.55))
    if pl > 0:
        lf = leaf.rotate(-35 * (1 - pl), resample=Image.BICUBIC, expand=True)
        a = lf.split()[3].point(lambda v: int(v * min(1, pl * 2))); lf.putalpha(a)
        ly = cy - h / 2 - 70 * (1 - pl)
        img.paste(lf, (int(cx - w / 2 + (leaf.width - lf.width) / 2), int(ly + (leaf.height - lf.height) / 2)), lf)
    ps = pr(t, t0 + 0.85, 0.6)
    if 0 < ps < 1:                                   # glint sweeping across the logo
        band = Image.new("L", (w, h), 0); bd = ImageDraw.Draw(band)
        x = -w * 0.6 + ps * w * 2.2
        bd.polygon([(x, 0), (x + w * 0.22, 0), (x + w * 0.22 - h * 0.5, h), (x - h * 0.5, h)], fill=150)
        from PIL import ImageChops
        sh = Image.new("RGBA", (w, h), (255, 255, 255, 0)); sh.putalpha(ImageChops.multiply(band, mask))
        img.paste(sh, (int(cx - w / 2), int(cy - h / 2)), sh)

def check_mark(d, x, y, s, col, w=4):
    d.line([(x, y + s * 0.5), (x + s * 0.38, y + s * 0.88), (x + s, y + s * 0.1)], fill=col, width=w, joint="curve")

def draw_job_card(img, d, t, J):
    p = eo(pr(t, J["t_in"], 0.5))
    if p <= 0: return
    x0, y0, x1, y1 = 40, J.get("y", 1030), PW - 40, J.get("y", 1030) + 210
    dx = (1 - p) * 700
    from PIL import ImageFilter
    sh = Image.new("RGBA", (x1 - x0 + 60, y1 - y0 + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((30, 36, 30 + x1 - x0, 36 + y1 - y0), 18, fill=(0, 0, 0, int(38 * p)))
    sh = sh.filter(ImageFilter.GaussianBlur(12)); img.paste(sh, (int(x0 - 30 + dx), y0 - 30), sh)
    d.rounded_rectangle((x0 + dx, y0, x1 + dx, y1), 18, fill=WH, outline=(222, 222, 222), width=2)
    # company tile
    tx0, ty0 = x0 + 28 + dx, y0 + 28
    d.rounded_rectangle((tx0, ty0, tx0 + 96, ty0 + 96), 16, fill=J["tile_bg"])
    if J.get("tile_logo"):
        draw_logo(img, tx0 + 48, ty0 + 50, 62, t, J["t_in"] - 1)
    else:
        d.text((tx0 + 48, ty0 + 50), J["tile_text"], font=HV(40, "bold"), fill=WH, anchor="mm")
    lx = tx0 + 124
    d.text((lx, y0 + 30), J["title"], font=HV(36, "bold"), fill=BK)
    d.text((lx, y0 + 78), J["company"], font=HV(26, "reg"), fill=(80, 80, 80))
    d.text((lx, y0 + 116), J["meta"], font=HV(22, "reg"), fill=(140, 140, 140))
    # button: "Solicitar" -> "Postulado ✓"
    q = eo(pr(t, J["t_apply"], 0.35))
    bw, bh = 250, 58; bx1 = x1 - 28 + dx; bx0 = bx1 - bw; by0 = y1 - 28 - bh
    blue, green = (10, 102, 194), (21, 128, 61)
    col = mix(green, blue, q)
    if q < 0.5:
        d.rounded_rectangle((bx0, by0, bx1, by0 + bh), 29, fill=blue)
        d.text(((bx0 + bx1) / 2, by0 + bh / 2), "Solicitar", font=HV(26, "bold"), fill=WH, anchor="mm")
    else:
        d.rounded_rectangle((bx0, by0, bx1, by0 + bh), 29, fill=col)
        d.text((bx0 + 40, by0 + bh / 2), "Postulado", font=HV(26, "bold"), fill=WH, anchor="lm")
        check_mark(d, bx1 - 62, by0 + 17, 24, WH, 4)

def sc_intro(cfg):
    I = cfg["intro"]
    def fn(img, d, t):
        d.rectangle((0, 0, PW, PH), fill=WH)
        swiss_header(d, "01", "Introducción", "Caso práctico · Entrevista técnica", t, I["t0"])
        for k, (s, t0) in enumerate([("Entrevista", I["t0"] + 0.05), ("técnica.", I["t_tecnica"])]):
            p, dy = slide(t, t0, 0.4, 30); tx(d, (40, 260 + k * 150 + dy), s, HV(160, "bold"), BK, p)
        y = 620; p, _ = slide(t, I["t_role"], 0.4)
        if p > 0: d.rectangle((40, y, 40 + 80 * p, y + 12), fill=RED)
        tx(d, (40, y + 50), I["role"], HV(54, "med"), BK, eo(pr(t, I["t_role"], 0.35)))
        tx(d, (40, y + 120), I["company"], HV(54, "light"), BK, eo(pr(t, I["t_company"], 0.35)))
        if I.get("logo"): draw_logo(img, I["logo"][0], I["logo"][1], I["logo"][2], t, I["logo"][3])
        if I.get("job"): draw_job_card(img, d, t, I["job"])
        for k, (a, b) in enumerate(I["info"]):
            pa = eo(pr(t, I["t_role"] + 0.3 + k * 0.25, 0.35))
            yy = y + 230 + k * 82
            if pa > 0: d.line((40, yy - 14, 40 + (PW - 80) * pa, yy - 14), fill=LG, width=2)
            tx(d, (40, yy), a, HV(24, "bold"), BK, pa); tx(d, (220, yy), b, HV(24, "reg"), GR, pa)
    return fn

def sc_data(cfg):
    D = cfg["data"]
    def fn(img, d, t):
        d.rectangle((0, 0, PW, PH), fill=WH)
        swiss_header(d, "01", "El dataset", "Qué datos nos dan", t, D["t0"])
        p, dy = slide(t, D["t0"] + 0.05, 0.4)
        tx(d, (40, 236 + dy), D["file"], MO(44, 600), BK, p)
        if D.get("logo"): draw_logo(img, 40 + MO(44, 600).getlength(D["file"]) + 42, 262, 64, t, D["t0"] + 0.15)
        n = int(D["count"] * eo(pr(t, D["t_rows"], D.get("scroll_d", 1.4))))
        tx(d, (40, 300 + dy), f"{n:,}".replace(",", ".") + D["count_label"], HV(28, "reg"), GR, p)
        ty = 380; ph = eo(pr(t, D["t_rows"], 0.35))
        hl_on = t >= D["hl_start"]; fh, fr_ = HV(18, "bold"), HV(22, "reg")
        for lab, x, al, ht in D["cols"]:
            act = ht is not None and t >= ht
            col = RED if act else (GR if not hl_on else (190, 190, 190))
            tx(d, (x, ty), lab, fh, col, ph, WH, "ls" if al == "l" else "rs")
            if act:
                q = eo(pr(t, ht, 0.3)); w = fh.getlength(lab); x0 = x if al == "l" else x - w
                d.rectangle((x0, ty + 10, x0 + w * q, ty + 15), fill=RED)
        if ph > 0: d.line((40, ty + 22, 40 + (PW - 80) * ph, ty + 22), fill=BK, width=2)
        seq = D.get("pool", []) + D["rows"]; n_extra = len(D.get("pool", []))
        off = n_extra * eo(pr(t, D["t_rows"], D.get("scroll_d", 1.4)))          # rows still to scroll past
        area_top, area_bot = ty + 30, ty + 66 + len(D["rows"]) * 54
        lay = Image.new("RGB", (PW, area_bot - area_top), WH); ld = ImageDraw.Draw(lay)
        speed = 1 - eo(pr(t, D["t_rows"], D.get("scroll_d", 1.4)))
        for k, row in enumerate(seq):
            y = ty + 66 + (k - off) * 54 - area_top
            if y < -40 or y > lay.height + 10 or ph <= 0: continue
            final = k >= n_extra
            for (lab, x, al, ht), v in zip(D["cols"], row):
                act = final and ht is not None and t >= ht
                col = (BK if lab == D["cols"][0][0] else (60, 60, 60)) if not hl_on else (BK if act else (185, 185, 185))
                col = mix(col, WH, 1 - 0.45 * speed)                                # motion: lighter while flying past
                ld.text((x, y), v, font=HV(22, "med") if act else fr_, fill=mix(col, WH, ph), anchor="ls" if al == "l" else "rs")
            ld.line((40, y + 18, PW - 40, y + 18), fill=LG, width=1)
        img.paste(lay, (0, area_top))
        pf = eo(pr(t, D["t_rows"] + 1.2, 0.35)); fy = ty + 66 + len(D["rows"]) * 54 + 20
        tx(d, (40, fy), D["footer_l"], HV(22, "reg"), GR, pf); tx(d, (PW - 40, fy), D["footer_r"], HV(22, "reg"), GR, pf, WH, "ra")
    return fn

def sc_question(cfg):
    Q = cfg["question"]
    def fn(img, d, t):
        d.rectangle((0, 0, PW, PH), fill=WH)
        swiss_header(d, "02", "La pregunta", "Lo que nos piden en la entrevista", t, Q["t0"])
        f = HV(Q.get("size", 128), "bold"); y0 = 250; step = Q.get("step", 128)
        for k, (s, t0) in enumerate(Q["rows"]):
            p, dy = slide(t, t0, 0.35, 28); tx(d, (40, y0 + k * step + dy), s, f, BK, p)
        for (row, word, t0) in Q["underlines"]:
            pg = eo(pr(t, t0, 0.4))
            if pg <= 0: continue
            line = Q["rows"][row][0]; i = line.index(word)
            x0 = 40 + f.getlength(line[:i]); w = f.getlength(word)
            yy = y0 + row * step + int(step * 1.12)
            d.rectangle((x0, yy, x0 + w * pg, yy + 12), fill=RED)
    return fn

# ------------------------------------------------------------------ Terminal code panel
def tokens(line):
    if line.strip().startswith("#"):
        return [(line, CMT)]
    return [(s, BSYN.get(c, c)) for s, c in R.tokens(line)]

def sc_code(cfg):
    C = cfg["code"]; CODE = C["lines"]; TOK = [tokens(l) for l in CODE]
    LH, CF = C.get("lh", 38), MO(C.get("fs", 27)); TOP = 290; BOT = PH - 60 - C.get("viz_h", 0)
    cap = int((BOT - TOP) / LH)
    def hl_at(t):
        cur = None
        for h in C["hl"]:
            if t >= h[0]: cur = h
        return cur
    def target(t):
        h = hl_at(t); need = h[2] if h else 0
        return max(0, need - cap + 2)
    def fn(img, d, t):
        d.rectangle((0, 0, PW, PH), fill=TB)
        swiss_header(d, "03", "El código", C["sub"], t, C["t0"])
        h = hl_at(t); step = h[3] if h else 0
        y = 200
        d.rectangle((0, y, PW, y + 66), fill=TP); d.line((0, y + 66, PW, y + 66), fill=RUL, width=2)
        d.text((36, y + 33), C["file"], font=MO(22, 500), fill=INK, anchor="lm")
        x = PW - 36
        for k in range(len(C["steps"]) - 1, -1, -1):
            s = C["steps"][k]; ff = MO(19, 650 if k == step else 400); fw = ff.getlength(s)
            col = ACC if k == step else (OK if k < step else DIM)
            d.text((x - fw, y + 34), s, font=ff, fill=col, anchor="lm"); x -= fw + 20
        d.rectangle((0, PH - 52, PW, PH), fill=TP); d.line((0, PH - 52, PW, PH - 52), fill=RUL, width=2)
        d.text((36, PH - 26), "python 3.11 · pandas 2.3", font=MO(19), fill=MUT, anchor="lm")
        d.text((PW - 36, PH - 26), C["status_r"], font=MO(19), fill=MUT, anchor="rm")
        off = sum(target(t - k * 0.04) for k in range(10)) / 10
        layer = Image.new("RGB", (PW, (BOT - TOP) if C.get("viz") else (PH - 52 - TOP)), TB); ld = ImageDraw.Draw(layer)
        if h:
            i = C["hl"].index(h); pv = C["hl"][i - 1] if i > 0 else h; kk = eo(pr(t, h[0], 0.3))
            a1 = (pv[1] * (1 - kk) + h[1] * kk - off) * LH - 5; a2 = ((pv[2] + 1) * (1 - kk) + (h[2] + 1) * kk - off) * LH - 3
            ld.rectangle((0, a1, PW, a2), fill=(20, 32, 50)); ld.rectangle((0, a1, 5, a2), fill=ACC)
        for i, toks in enumerate(TOK):
            if i not in C["rev"] or t < C["rev"][i]: continue
            yy = (i - off) * LH
            if yy < -LH or yy > layer.height: continue
            act = h is None or h[1] <= i <= h[2]; a = 1.0 if act else 0.33
            n = int((t - C["rev"][i]) * 70)
            ld.text((40, yy + 4), f"{i + 1:>2}", font=MO(19), fill=mix(ACC if (act and h) else DIM, TB, a))
            x = 96; left = n
            for s, col in toks:
                if left <= 0: break
                part = s[:left]; ld.text((x, yy), part, font=CF, fill=mix(col, TB, a)); x += CF.getlength(part); left -= len(s)
            if n < len(CODE[i]) + 3 and t - C["rev"][i] < 1.0 and int(t * 4) % 2 == 0:
                ld.rectangle((x + 2, yy + 3, x + 14, yy + 33), fill=INK)
            if i in C["notes"] and t >= C["notes"][i][0] and act:
                pa = eo(pr(t, C["notes"][i][0], 0.3))
                ld.text((x + 20 + 10 * (1 - pa), yy + 3), C["notes"][i][1], font=MO(22, 500), fill=mix(ACC, TB, pa))
        img.paste(layer, (0, TOP))
        d.rectangle((0, PH - 52, PW, PH), fill=TP); d.line((0, PH - 52, PW, PH - 52), fill=RUL, width=2)
        d.text((36, PH - 26), "python 3.11 · pandas 2.3", font=MO(19), fill=MUT, anchor="lm")
        d.text((PW - 36, PH - 26), C["status_r"], font=MO(19), fill=MUT, anchor="rm")
        if C.get("viz"):
            C["viz"](img, d, t, (0, BOT, PW, PH - 52))
    return fn

# ------------------------------------------------------------------ Terminal result panel
def sc_result(cfg):
    O = cfg["result"]
    def fn(img, d, t):
        d.rectangle((0, 0, PW, PH), fill=TB)
        swiss_header(d, "04", "Resultado", "Lo que imprime el notebook", t, O["t0"])
        y = 200
        d.rectangle((0, y, PW, y + 66), fill=TP); d.line((0, y + 66, PW, y + 66), fill=RUL, width=2)
        d.text((36, y + 33), O["file"], font=MO(22, 500), fill=INK, anchor="lm")
        d.text((PW - 36, y + 34), "print", font=MO(19, 650), fill=ACC, anchor="rm")
        y = 296; pa = eo(pr(t, O["t0"] + 0.05, 0.3))
        tx(d, (36, y), O["title"], MO(24, 500), MUT, pa, TB)
        f = MO(O.get("fs", 26)); fb = MO(O.get("fs", 26), 650)
        for (s, x, al) in O["header"]:
            tx(d, (x, y + 52), s, MO(O.get("fs", 26) - 2, 600), MUT, pa, TB, "la" if al == "l" else "ra")
        if pa > 0: d.line((36, y + 92, PW - 36, y + 92), fill=RUL, width=2)
        vmax = max(r[O["bar_col"]] for r in O["vals"])
        for k, row in enumerate(O["rows"]):
            yy = y + 108 + k * O.get("rh", 50)
            pk = eo(pr(t, O["t0"] + 0.15 + k * 0.07, 0.3))
            hot = k == O["hot_row"] and t >= O["t_hot"]
            if hot:
                q = eo(pr(t, O["t_hot"], 0.3)); d.rectangle((24, yy - 8, 24 + (PW - 48) * q, yy + O.get("rh", 50) - 14), fill=(20, 32, 50))
                d.rectangle((24, yy - 8, 29, yy + O.get("rh", 50) - 14), fill=ACC)
            for j, (s, (_, x, al)) in enumerate(zip(row, O["header"])):
                cell_hot = any(k == r_ and j == c_ and t >= tc for (r_, c_, tc) in O["cells"])
                col = ACC if cell_hot else (INK if hot or j else (OK if k == O["hot_row"] else INK))
                tx(d, (x, yy), s, fb if cell_hot or hot else f, col, pk, TB, "la" if al == "l" else "ra")
            # inline bar
            bt = O["t_bars"] + k * 0.08
            pb = eo(pr(t, bt, 0.6))
            if pb > 0:
                v = O["vals"][k][O["bar_col"]]; bx, bw = O["bar_x"], O["bar_w"]
                d.rectangle((bx, yy + 6, bx + bw * v / vmax * pb, yy + 22), fill=ACC if k == O["hot_row"] else (55, 64, 80))
        ny_extra = 0
        if O.get("extra"):
            pe = eo(pr(t, O["extra"][0], 0.3)); ey = y + 108 + len(O["rows"]) * O.get("rh", 50) + 14
            hot_e = t >= O["extra"][2]
            if hot_e: d.rectangle((24, ey - 8, 24 + MO(28, 650).getlength(O["extra"][1]) + 30, ey + 40), fill=(20, 32, 50))
            tx(d, (36, ey), O["extra"][1], MO(28, 650), ACC if hot_e else INK, pe, TB); ny_extra = 70
        if O.get("note") and t >= O["note"][0]:
            pn = eo(pr(t, O["note"][0], 0.35)); ny = y + 108 + len(O["rows"]) * O.get("rh", 50) + 30 + ny_extra
            d.rectangle((36, ny, PW - 36, ny + 150), outline=mix((120, 96, 40), TB, pn), width=2)
            tx(d, (64, ny + 28), O["note"][1], MO(25, 700), WARN, pn, TB)
            for k, s in enumerate(O["note"][2]):
                n = int((t - O["note"][0] - 0.3 - k * 0.6) * 55)
                if n > 0: tx(d, (64, ny + 72 + k * 36), s[:n], MO(24), INK, 1, TB)
        d.rectangle((0, PH - 52, PW, PH), fill=TP); d.line((0, PH - 52, PW, PH - 52), fill=RUL, width=2)
        d.text((36, PH - 26), "python 3.11 · pandas 2.3", font=MO(19), fill=MUT, anchor="lm")
        d.text((PW - 36, PH - 26), O["status_r"], font=MO(19), fill=MUT, anchor="rm")
    return fn

def sc_concl(cfg):
    K = cfg["concl"]
    def fn(img, d, t):
        d.rectangle((0, 0, PW, PH), fill=WH)
        swiss_header(d, "05", "Conclusión", "Respuesta a la pregunta", t, K["t0"])
        p, dx = slide(t, K["t0"] + 0.05, 0.4, 40)
        tx(d, (40 - dx, 220), K["big"], HV(K.get("big_size", 260), "bold"), BK, p)
        if K.get("big_unit"):
            tx(d, (40 - dx + HV(K.get("big_size", 260), "bold").getlength(K["big"]) + 12, 220 + K.get("unit_dy", 150)), K["big_unit"], HV(70, "bold"), RED, p)
        pa = eo(pr(t, K["t0"] + 0.35, 0.35))
        for k, s in enumerate(K["lines"]): tx(d, (40, 560 + k * 48), s, HV(36, "med"), BK, pa)
        y = 680; pt = eo(pr(t, K["t0"] + 0.7, 0.35))
        if pt > 0:
            d.line((40, y, 40 + (PW - 80) * pt, y), fill=BK, width=2)
            for s, x, al in K["thead"]: tx(d, (x, y + 30), s, HV(24, "bold"), GR, pt, WH, "la" if al == "l" else "ra")
            for k, row in enumerate(K["trows"]):
                yy = y + 80 + k * 66
                for j, (s, (_, x, al)) in enumerate(zip(row, K["thead"])):
                    tx(d, (x, yy), s, HV(36, "bold" if j == 0 else "reg"), RED if (k == 0 and j == len(row) - 1) else BK, pt, WH, "la" if al == "l" else "ra")
                d.line((40, yy + 56, PW - 40, yy + 56), fill=LG, width=2)
        if K.get("note"):
            pn, dx2 = slide(t, K["t0"] + 0.5, 0.35); ny = y + 80 + len(K["trows"]) * 66 + 40
            if pn > 0:
                d.rectangle((40, ny, 52, ny + 92), fill=RED)
                tx(d, (76 + dx2, ny), K["note"][0], HV(28, "med"), BK, pn); tx(d, (76 + dx2, ny + 44), K["note"][1], HV(28, "reg"), GR, pn)
    return fn

def sc_cta(cfg):
    T0 = cfg["cta"]["t0"]; L = cfg["cta"]
    def fn(img, d, t):
        d.rectangle((0, 0, PW, PH), fill=WH)
        swiss_header(d, "+", "Sigue aprendiendo", L["sub"], t, T0)
        for k, (s, dt) in enumerate(L["rows"]):
            p, dy = slide(t, T0 + dt, 0.35, 28); tx(d, (40, 250 + k * 118 + dy), s, HV(112, "bold"), BK, p)
        pl, _ = slide(t, L["t_link"], 0.35)
        if pl > 0:
            f = HV(48, "med"); w = f.getlength("Link en mi perfil") + 60
            d.rectangle((40, 650, 40 + w * pl, 740), fill=BK); tx(d, (70, 695), "Link en mi perfil", f, WH, pl, BK, "lm")
        tx(d, (40, 800), "Plataforma en español.", HV(44, "reg"), BK, eo(pr(t, L["t_es"], 0.35)))
        p, dy = slide(t, L["t_free"], 0.35, 28); tx(d, (40, 870 + dy), "100% gratis.", HV(110, "bold"), RED, p)
    return fn

# ------------------------------------------------------------------ render
SAFE_L, SAFE_R = 60, 90            # Instagram / TikTok UI safe margins (buttons live on the right)
def safe(p):
    """Shrink the panel into the safe area and extend its own edge colours to the borders."""
    w = PW - SAFE_L - SAFE_R; h = int(PH * w / PW)
    small = p.resize((w, h), Image.LANCZOS)
    out = Image.new("RGB", (PW, PH))
    out.paste(small, (SAFE_L, 0))
    out.paste(small.crop((8, 0, 9, h)).resize((SAFE_L, h)), (0, 0))
    out.paste(small.crop((w - 1, 0, w, h)).resize((SAFE_R, h)), (SAFE_L + w, 0))
    out.paste(out.crop((0, h - 1, PW, h)).resize((PW, PH - h)), (0, h))
    return out

def make(cfg):
    edl = build_edl(cfg["name"], cfg["segs"]); TL = Timeline(edl)
    scenes = [(cfg["intro"]["t0"], sc_intro(cfg)), (cfg["data"]["t0"], sc_data(cfg)), (cfg["question"]["t0"], sc_question(cfg)),
              (cfg["code"]["t0"], sc_code(cfg)), (cfg["result"]["t0"], sc_result(cfg)), (cfg["concl"]["t0"], sc_concl(cfg)),
              (cfg["cta"]["t0"], sc_cta(cfg))]
    def panel(T):
        idx = max([i for i, (s, _) in enumerate(scenes) if T >= s] or [0])
        img = Image.new("RGB", (PW, PH), WH); d = ImageDraw.Draw(img); scenes[idx][1](img, d, T); return img
    def frame(src, tn):
        piece, T = TL.locate(tn)
        cam = src.crop((0, 0, W, CAM))
        z = 1.07 if piece % 2 == 1 else 1.0
        for (e0, e1) in cfg.get("emph", []):                 # soft punch-in on key phrases
            k = min(eo(pr(T, e0, 0.45)), 1 - eo(pr(T, e1, 0.45)))
            if k > 0: z *= 1 + 0.12 * k
        if z > 1.0001:
            cw, ch = W / z, CAM / z
            cy = min(max(300, ch / 2), CAM - ch / 2)
            cam = cam.crop((int(W / 2 - cw / 2), int(cy - ch / 2), int(W / 2 + cw / 2), int(cy + ch / 2))).resize((W, CAM), Image.LANCZOS)
        out = Image.new("RGB", (W, H), WH); out.paste(cam, (0, 0)); out.paste(safe(panel(T)), (0, CAM))
        d = ImageDraw.Draw(out)
        d.rectangle((0, CAM, W, CAM + 8), fill=BK); d.rectangle((0, CAM, int(W * tn / TL.dur), CAM + 8), fill=RED)
        return out
    return TL, frame

def frames_iter(src, TL, times):
    c = av.open(src); v = c.streams.video[0]
    tg = [(tn, TL.locate(tn)[1]) for tn in times]; k = 0
    for fr in c.decode(v):
        tt = float(fr.pts * v.time_base)
        while k < len(tg) and tt >= tg[k][1] - 1 / 120:
            yield tg[k][0], fr.to_image(); k += 1
        if k >= len(tg): break

def add_sfx(cfg, TL, wav):
    import wave
    def to_new(T):
        for (s, e), st in zip(TL.edl, TL.starts):
            if s <= T <= e: return st + T - s
            if T < s: return st
        return None
    with wave.open(wav) as w:
        sr = w.getframerate(); ch = w.getnchannels()
        voice = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, ch) / 32767
    mono = voice.mean(1); n = len(mono); fx = np.zeros((n, 2), np.float32)
    rng = np.random.RandomState(3)
    def whoosh(d=0.55, vol=0.05):
        """Swipe: noise shaped by a narrow band-pass whose centre sweeps up then down (no hiss above ~3 kHz)."""
        N = int(d * sr); hop, win = 128, 1024
        noise = rng.randn(N + win)
        out = np.zeros(N + win); norm = np.zeros(N + win); w = np.hanning(win)
        freqs = np.fft.rfftfreq(win, 1 / sr)
        for i in range(0, N, hop):
            u = i / N
            fc = 260 + 1100 * np.sin(np.pi * u) ** 1.5                     # 260 Hz -> ~1.4 kHz -> back
            band = np.exp(-0.5 * (np.log2(np.maximum(freqs, 1) / fc) / 0.45) ** 2)
            band[freqs > 3200] = 0
            seg = np.fft.irfft(np.fft.rfft(noise[i:i + win] * w) * band)
            out[i:i + win] += seg * w; norm[i:i + win] += w ** 2
        out = (out / np.maximum(norm, 1e-6))[:N]
        t = np.arange(N) / N
        env = np.sin(np.pi * t) ** 2 * (1 - 0.35 * t)                       # smooth swell, gentle tail
        sig = out * env; sig = sig / (np.abs(sig).max() + 1e-9) * vol
        pan = 0.5 - 0.5 * np.cos(np.pi * t)                                  # left -> right
        return np.stack([sig * np.sqrt(1 - pan), sig * np.sqrt(pan)], 1).astype(np.float32)
    def click(f=2400, d=0.03, vol=0.05):
        t = np.arange(int(d * sr)) / sr
        return (np.sin(2 * np.pi * f * t) * np.exp(-t * 160) * vol).astype(np.float32)
    def pop(vol=0.07):
        t = np.arange(int(0.12 * sr)) / sr
        return (np.sin(2 * np.pi * (300 + 900 * t) * t) * np.exp(-t * 30) * vol).astype(np.float32)
    def put(T, sig, orig=True, lead=0.0):
        tn = to_new(T) if orig else T
        if tn is None: return
        i = int(max(0, tn - lead) * sr); m = min(len(sig), n - i)
        if sig.ndim == 1: sig = np.stack([sig, sig], 1)
        if m > 0: fx[i:i + m] += sig[:m]
    for key in ("data", "question", "code", "result", "concl", "cta"):
        put(cfg[key]["t0"], whoosh(), lead=0.28)
    for (_, _, _, ht) in cfg["data"]["cols"]:
        if ht is not None: put(ht, click())
    for h in cfg["code"]["hl"]: put(h[0], click(1800, vol=0.035))
    put(cfg["result"]["t_hot"], click(2600, vol=0.05))
    I = cfg["intro"]
    if I.get("logo"): put(I["logo"][3], pop())
    if I.get("job"):
        put(I["job"]["t_in"], whoosh(0.45, 0.035)); put(I["job"]["t_apply"], click(2000, vol=0.05)); put(I["job"]["t_apply"] + 0.06, click(3000, vol=0.04))
    # duck effects under the voice so they never compete with it
    env = np.convolve(np.abs(mono), np.ones(int(0.05 * sr)) / int(0.05 * sr), "same")
    gain = 1 - 0.55 * np.clip(env / 0.08, 0, 1)
    fxg = fx * gain[:, None]
    if ch == 1: fxg = fxg.mean(1, keepdims=True)
    mixd = np.clip(voice + fxg, -1, 1)
    out = wav.replace(".wav", "_sfx.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mixd * 32767).astype(np.int16).tobytes())
    return out

def run(cfg, mode, args):
    src = cfg.get("src") or f"/Users/arturolorenzo/Downloads/{cfg['name']}.mp4"
    TL, frame = make(cfg)
    if mode == "edl":
        for (s, e), st in zip(TL.edl, TL.starts): print(f"orig {s:7.2f}-{e:7.2f} new {st:6.2f}")
        print("dur", round(TL.dur, 2)); return
    if mode == "stills":
        for tn, img in frames_iter(src, TL, sorted(float(x) for x in args)):
            frame(img, tn).save(os.path.join(ROOT, f"s_{cfg['name']}_{tn:05.1f}.jpg"), quality=85)
        return
    wav = os.path.join(ROOT, f"{cfg['name']}_audio.wav")
    fc = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={e - s - 0.015:.3f}:d=0.015[a{i}];"
                 for i, (s, e) in enumerate(TL.edl)) + "".join(f"[a{i}]" for i in range(len(TL.edl))) + f"concat=n={len(TL.edl)}:v=0:a=1[a]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", fc, "-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", wav], check=True)
    if cfg.get("sfx", True): wav = add_sfx(cfg, TL, wav)
    out = cfg["out"]
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    n = 0
    for tn, img in frames_iter(src, TL, [k / FPS for k in range(int(TL.dur * FPS))]):
        p.stdin.write(frame(img, tn).tobytes()); n += 1
    p.stdin.close(); p.wait(); print("done", n, round(TL.dur, 2))
