"""Batch of 8 old-format videos (lote8) re-edited in the approved hybrid format.
Sources: raw clips concatenated per video (entrevistas/brutos/lote8/<v>/raw.mp4); takes chosen to reproduce the editor's render (lote8/_alinea.py)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); ENT = os.path.dirname(HERE); sys.path.insert(0, ENT)
LOTE = os.path.join(ENT, "brutos", "lote8")
sys.path.insert(0, LOTE)
import hybrid
from render import eo, pr, mix
from stylef import MO
from render2 import HV
from _alinea import align

OUTDIR = os.path.join(ENT, "finales") + "/"
os.makedirs(OUTDIR, exist_ok=True)
TB, TP, INK, MUT, ACC = (10, 12, 15), (15, 18, 22), (220, 226, 234), (110, 120, 135), (88, 166, 255)
GREEN, RED_, YEL = (86, 211, 140), (240, 90, 90), (255, 214, 64)

def base(v, name, out):
    chain = align(v, show=False)
    return dict(name=name, src=f"{LOTE}/{v}/raw.mp4", a16=f"{LOTE}/{v}/raw_a16.npy", out=OUTDIR + out,
                segs=[(p["s"], p["e"]) for p in chain])

def viz_frame(d, box, t, t0, cap):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=TP); d.line((x0, y0, x1, y0), fill=(34, 39, 48), width=2)
    if t < t0 - 0.3: return False
    d.text((36, y0 + 18), "# lo que hace el código", font=MO(19, 500), fill=MUT)
    if cap: d.text((x1 - 36, y0 + 18), cap, font=MO(19, 500), fill=INK, anchor="ra")
    return True

def check(d, x, y, ok, a, s=22):
    col = mix(GREEN if ok else RED_, TP, a)
    if ok: d.line([(x, y + s * 0.55), (x + s * 0.38, y + s * 0.9), (x + s, y + s * 0.1)], fill=col, width=4, joint="curve")
    else:
        d.line([(x, y), (x + s, y + s)], fill=col, width=4); d.line([(x + s, y), (x, y + s)], fill=col, width=4)

# ====================================================================== VIDEO 4 · contraseña segura
V4 = base("video4", "lote8_v4", "04_contrasena_segura.mp4")
PW4 = [("hola123", 7, False, True), ("Python2024!", 11, True, True), ("abc", 3, False, False), ("Segura99", 8, True, True)]
V4.update(
    intro=dict(t0=127.46, t_tecnica=128.34, role="Ciencia de datos", t_role=129.2, company="para cualquier perfil", t_company=130.0,
               info=[("Lenguaje", "Python · sin librerías"), ("Formato", "4 pasos · 60 segundos")],
               job=dict(t_in=127.9, t_apply=130.3, tile_text="Py", tile_bg=(55, 118, 171), title="Data Analyst · Scientist · Engineer",
                        company="Pregunta típica de entrevista técnica", meta="Python · Nivel junior")),
    question=dict(t0=133.51, size=104, step=112,
                  rows=[("¿Es una contraseña", 134.6), ("segura?", 136.07), ("8+ caracteres", 137.19), ("1 mayúscula", 138.77), ("1 número", 139.73)],
                  underlines=[(2, "8+ caracteres", 137.5), (3, "1 mayúscula", 139.0), (4, "1 número", 139.9)]),
    data=dict(t0=140.96, file="contrasenas  (list)", count=4, count_label=" contraseñas de ejemplo", t_rows=142.0, hl_start=999, scroll_d=0.6,
              cols=[("Contraseña", 40, "l", None), ("Caracteres", 1040, "r", None)],
              rows=[[p, str(n)] for p, n, _, _ in PW4], pool=[], footer_l="", footer_r="Python · list[str]"),
    code=dict(t0=146.85, sub="Python · any() + generadores", file="python_entrevistas.ipynb", status_r="Python 3.12",
              steps=["def", "len≥8", "mayús.", "número", "print"],
              lines='''contrasenas = ["hola123", "Python2024!",
               "abc", "Segura99"]

def es_segura(clave : str) -> bool:
    return (len(clave) >= 8
            and any(c.isupper() for c in clave)
            and any(c.isdigit() for c in clave))

print([es_segura(c) for c in contrasenas])'''.split("\n"),
              rev={0: 147.0, 1: 147.3, 3: 147.79, 4: 225.97, 5: 239.15, 6: 254.85, 8: 270.03},
              hl=[(146.85, 3, 3, 0), (219.17, 4, 4, 1), (237.31, 5, 5, 2), (252.13, 6, 6, 3), (266.95, 8, 8, 4)],
              notes={3: (153.3, "← str → bool"), 4: (230.55, "← 8+ caracteres"), 5: (248.45, "← mayúscula"),
                     6: (260.8, "← número"), 8: (271.15, "← una por contraseña")}),
    result=dict(t0=289.44, file="python_entrevistas.ipynb", status_r="Python 3.12", title="Out[1]:",
                header=[("contraseña", 36, "l"), ("es_segura", 720, "l")], fs=30, rh=60,
                rows=[[p, str(ok)] for p, n, u, dg in PW4 for ok in [n >= 8 and u and dg]],
                vals=[[0, 1]] * 4, bar_col=1, bar_x=1100, bar_w=0, hot_row=99, t_hot=999, t_bars=999,
                cells=[(0, 1, 291.66), (1, 1, 293.83), (2, 1, 298.95), (3, 1, 299.89)],
                extra=(289.7, "[False, True, False, True]", 999)),
    concl=dict(t0=299.75, big="2 de 4", big_size=200, lines=["contraseñas cumplen las 3 reglas:", "8+ caracteres, mayúscula y número."],
               thead=[("Contraseña", 40, "l"), ("¿Segura?", 1040, "r")],
               trows=[["Python2024!", "Sí"], ["Segura99", "Sí"], ["hola123 · abc", "No"]],
               note=("any() + generador: una línea por regla.", "Corto, legible y típico de entrevista.")),
    cta=dict(t0=320.97, sub="Más ejercicios de entrevista", rows=[("¿Quieres más", 0.05), ("profesiones", 0.2), ("de data?", 0.35)],
             t_link=320.97, t_es=322.79, t_free=323.11),
    emph=[(133.5, 139.95), (293.7, 297.0)],
)
T4 = dict(list=147.0, c1=228.83, c2=247.49, c3=259.2, res=273.89)
def v4_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    cap = "4 contraseñas de la lista"
    if t >= T4["c1"]: cap = "len(clave) >= 8"
    if t >= T4["c2"]: cap = "any(c.isupper() for c in clave)"
    if t >= T4["c3"]: cap = "any(c.isdigit() for c in clave)"
    if t >= T4["res"]: cap = "and: tienen que cumplirse las 3"
    if not viz_frame(d, box, t, T4["list"], cap): return
    cols = [("8+ car.", 520, T4["c1"]), ("mayús.", 680, T4["c2"]), ("número", 830, T4["c3"]), ("segura", 990, T4["res"])]
    for lab, x, tt in cols:
        a = eo(pr(t, tt, 0.35))
        d.text((x, y0 + 64), lab, font=MO(19, 600), fill=mix(MUT, TP, max(a, 0.35)), anchor="ma")
    for k, (pwd, n, up, dg) in enumerate(PW4):
        y = y0 + 110 + k * 78; a = eo(pr(t, T4["list"] + k * 0.12, 0.3))
        d.text((60, y), f'"{pwd}"', font=MO(28, 600), fill=mix((165, 214, 255), TP, a))
        d.text((360, y + 4), f"{n} car.", font=MO(20, 500), fill=mix(MUT, TP, a))
        for (lab, x, tt), ok in zip(cols[:3], (n >= 8, up, dg)):
            pc = eo(pr(t, tt + k * 0.1, 0.3))
            if pc > 0: check(d, x - 11, y + 4, ok, pc)
        pr_ = eo(pr(t, T4["res"] + k * 0.15, 0.35))
        if pr_ > 0:
            ok = n >= 8 and up and dg
            d.rounded_rectangle((935, y - 4, 1045, y + 36), 10, fill=mix(GREEN if ok else RED_, TP, pr_ * 0.25), outline=mix(GREEN if ok else RED_, TP, pr_), width=2)
            d.text((990, y + 16), "True" if ok else "False", font=MO(22, 700), fill=mix(GREEN if ok else RED_, TP, pr_), anchor="mm")
V4["code"]["viz"] = v4_viz; V4["code"]["viz_h"] = 470

# ====================================================================== VIDEO 5 · suscripciones fantasma
V5 = base("video5", "lote8_v5", "05_suscripciones_fantasma.mp4")
G5 = [("Netflix", 12.99), ("Supermercado", 45.20), ("Netflix", 12.99), ("Spotify", 9.99),
      ("Gasolina", 60.0), ("Spotify", 9.99), ("Netflix", 12.99), ("Spotify", 9.99)]
eur = lambda v: f"{v:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
V5.update(
    intro=dict(t0=156.35, t_tecnica=156.69, role="Data Engineer Junior", t_role=159.63, company="40.000 € al año", t_company=158.63,
               info=[("Lenguaje", "Python · collections.Counter"), ("Formato", "5 pasos · 60 segundos")],
               job=dict(t_in=156.7, t_apply=160.2, tile_text="DE", tile_bg=(30, 64, 175), title="Data Engineer Junior",
                        company="40.000 € brutos/año", meta="Prueba técnica · 15 minutos")),
    question=dict(t0=169.19, size=112, step=118,
                  rows=[("Detecta las", 169.93), ("suscripciones", 170.77), ("y cuánto te", 172.41), ("cuestan al año", 173.21)],
                  underlines=[(1, "suscripciones", 171.0), (3, "al año", 173.9)]),
    data=dict(t0=191.27, file="gastos  (list[tuple])", count=8, count_label=" movimientos de la cuenta", t_rows=192.41, hl_start=999, scroll_d=0.8,
              cols=[("Concepto", 40, "l", None), ("Importe", 1040, "r", None)],
              rows=[[c, eur(v)] for c, v in G5], pool=[], footer_l="como un extracto del banco", footer_r="8 movimientos"),
    code=dict(t0=210.11, sub="Python · Counter + dict comprehension", file="python_entrevistas.ipynb", status_r="Python 3.12",
              steps=["def", "Counter", "dict", "≥2", "×12", "print"],
              lines='''from collections import Counter

gastos = [
  ("Netflix", 12.99), ("Supermercado", 45.20),
  ("Netflix", 12.99), ("Spotify", 9.99),
  ("Gasolina", 60.0), ("Spotify", 9.99),
  ("Netflix", 12.99), ("Spotify", 9.99)]

def suscripciones(gastos : list) -> dict:
    conteo = Counter(gastos)
    return { concepto: round(importe * 12,2)
        for (concepto, importe), veces in conteo.items()
        if veces >=2
        }

print(suscripciones(gastos))'''.split("\n"),
              rev={0: 210.2, 2: 210.3, 3: 210.4, 4: 210.5, 5: 210.6, 6: 210.7, 8: 211.33, 9: 243.61, 10: 349.44, 11: 353.6, 12: 379.34, 13: 380.0, 15: 402.83},
              hl=[(210.11, 8, 8, 0), (242.91, 9, 9, 1), (349.06, 10, 11, 2), (378.66, 12, 12, 3), (383.30, 10, 10, 4), (402.47, 15, 15, 5)],
              notes={8: (223.83, "← list → dict"), 9: (250.0, "← cuenta repeticiones"), 12: (380.2, "← suscripción"), 10: (385.42, "← al año")}),
    result=dict(t0=409.38, file="python_entrevistas.ipynb", status_r="Python 3.12", title="Out[1]:",
                header=[("suscripción", 36, "l"), ("€ al año", 760, "r")], fs=32, rh=62,
                rows=[["Netflix", "155.88"], ["Spotify", "119.88"]], vals=[[0, 1]] * 2, bar_col=1, bar_x=1100, bar_w=0,
                hot_row=99, t_hot=999, t_bars=999, cells=[(0, 1, 413.73), (1, 1, 414.81)],
                extra=(409.6, "{'Netflix': 155.88, 'Spotify': 119.88}", 999)),
    concl=dict(t0=414.81, big="275,76", big_unit="€/año", big_size=220, lines=["en suscripciones que se repiten", "cada mes sin que te des cuenta."],
               thead=[("Suscripción", 40, "l"), ("Cargos", 700, "r"), ("Al año", 1040, "r")],
               trows=[["Netflix", "3 × 12,99 €", "155,88 €"], ["Spotify", "3 × 9,99 €", "119,88 €"]],
               note=("Counter cuenta tuplas repetidas en una línea.", "Supermercado y gasolina: solo una vez, no son suscripción.")),
    cta=dict(t0=436.23, sub="Más ejercicios de entrevista", rows=[("¿Quieres más", 0.05), ("ingeniería", 0.2), ("de datos?", 0.35)],
             t_link=436.23, t_es=439.59, t_free=437.91),
    emph=[(169.9, 173.95), (411.5, 416.7)],
)
COL5 = {"Netflix": (229, 9, 20), "Spotify": (30, 215, 96), "Supermercado": (120, 130, 150), "Gasolina": (240, 150, 60)}
T5 = dict(cards=210.3, counter=246.72, filt=379.34, x12=385.42)
def v5_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    cap = "8 movimientos (concepto, importe)"
    if t >= T5["counter"]: cap = "Counter: cuántas veces se repite cada tupla"
    if t >= T5["filt"]: cap = "if veces >= 2 → suscripción"
    if t >= T5["x12"]: cap = "importe × 12 = coste al año"
    if not viz_frame(d, box, t, T5["cards"], cap): return
    order = ["Netflix", "Spotify", "Supermercado", "Gasolina"]
    pc = eo(pr(t, T5["counter"], 1.0)); pf = eo(pr(t, T5["filt"], 0.5)); px = eo(pr(t, T5["x12"], 0.5))
    seen = {k: 0 for k in order}
    for k, (c, v) in enumerate(G5):
        a = eo(pr(t, T5["cards"] + k * 0.08, 0.3))
        if a <= 0: continue
        gx, gy = 50 + (k % 4) * 248, y0 + 70 + (k // 4) * 76
        col_i = order.index(c); j = seen[c]; seen[c] += 1
        sx, sy = 50 + col_i * 248, y0 + 70 + j * 14
        x, y = gx + (sx - gx) * pc, gy + (sy - gy) * pc
        single = c in ("Supermercado", "Gasolina")
        aa = a * (1 - 0.8 * pf if single else 1)
        d.rounded_rectangle((x, y, x + 228, y + 62), 10, fill=mix((26, 30, 38), TP, aa), outline=mix(COL5[c], TP, aa), width=2)
        d.text((x + 14, y + 10), c, font=MO(20, 700), fill=mix(COL5[c], TP, aa))
        d.text((x + 14, y + 36), eur(v), font=MO(18, 500), fill=mix(INK, TP, aa))
    if pc > 0.5:
        a = eo((pc - 0.5) * 2)
        for c in order:
            n = sum(1 for g, _ in G5 if g == c); x = 50 + order.index(c) * 248
            single = n < 2
            col = mix(RED_ if (single and pf > 0.5) else (YEL if n >= 2 else MUT), TP, a)
            d.text((x + 114, y0 + 200), f"× {n}", font=MO(30, 700), fill=col, anchor="ma")
            if single and pf > 0: d.line((x + 10, y0 + 100, x + 218, y0 + 100), fill=mix(RED_, TP, pf), width=3)
    if px > 0:
        for i, c in enumerate(["Netflix", "Spotify"]):
            v = dict(G5)[c]; y = y0 + 280 + i * 60
            d.text((60, y), f"{c}: {eur(v)} × 12 = ", font=MO(26, 600), fill=mix(INK, TP, px))
            d.text((60 + MO(26, 600).getlength(f"{c}: {eur(v)} × 12 = "), y - 4), eur(round(v * 12, 2)), font=MO(30, 700), fill=mix(YEL, TP, px))
V5["code"]["viz"] = v5_viz; V5["code"]["viz_h"] = 470

# ====================================================================== VIDEO 6 · racha más larga (Duolingo)
V6 = base("video6", "lote8_v6", "06_racha_duolingo.mp4")
V6.update(
    intro=dict(t0=157.76, t_tecnica=158.58, role="Data Engineer Junior", t_role=159.42, company="Prueba técnica · Python", t_company=159.95,
               info=[("Lenguaje", "Python · datetime"), ("Formato", "5 pasos · 60 segundos")],
               job=dict(t_in=158.1, t_apply=160.1, tile_text="DE", tile_bg=(30, 64, 175), title="Data Engineer Junior",
                        company="Prueba técnica · Python", meta="Fechas, bucles y rachas")),
    question=dict(t0=201.92, size=112, step=118,
                  rows=[("Calcula la racha", 203.58), ("más larga de", 204.70), ("días seguidos", 205.46), ("(estilo Duolingo)", 206.38)],
                  underlines=[(2, "días seguidos", 205.9)]),
    code=dict(t0=210.05, sub="Python · fechas + bucle", file="python_entrevistas.ipynb", status_r="Python 3.12",
              steps=["def", "sort", "init", "for", "+1", "reset", "ret", "print"],
              lines='''from datetime import date

dias = ["2025-01-01", "2025-01-02",
        "2025-01-03", "2025-01-05",
        "2025-01-06"]

def racha_maxima(dias: list) -> int:
    fechas = sorted(date.fromisoformat(d)
                    for d in dias)
    mejor = actual = 1

    for i in range(1, len(fechas)):
        if (fechas[i] - fechas[i-1]).days == 1:
            actual += 1
            mejor = max(mejor,actual)
        else:
            actual = 1
    return mejor

print(f"Racha: {racha_maxima(dias)} días")'''.split("\n"),
              rev={0: 210.15, 2: 210.3, 3: 210.45, 4: 210.6, 6: 211.05, 7: 226.57, 8: 227.2, 9: 274.91, 11: 309.96, 12: 358.23,
                   13: 368.28, 14: 370.64, 15: 390.72, 16: 394.67, 17: 406.58, 19: 432.49},
              hl=[(210.05, 6, 6, 0), (225.89, 7, 8, 1), (270.79, 9, 9, 2), (309.70, 11, 11, 3), (357.83, 12, 12, 3),
                  (367.68, 13, 14, 4), (390.66, 15, 16, 5), (405.54, 17, 17, 6), (431.11, 19, 19, 7)],
              notes={7: (230.27, "← str → date"), 9: (277.13, "← empiezan en 1"), 11: (313.38, "← desde el 2º"),
                     12: (363.49, "← seguido"), 14: (374.40, "← guarda la mejor"), 16: (398.83, "← se rompe")}),
    result=dict(t0=444.26, file="python_entrevistas.ipynb", status_r="Python 3.12", title="Out[1]:",
                header=[("", 36, "l")], fs=40, rh=72, rows=[["Racha: 3 días"]], vals=[[0, 1]], bar_col=1, bar_x=1100, bar_w=0,
                hot_row=0, t_hot=447.06, t_bars=999, cells=[],
                note=(449.63, "DETALLE", ["1, 2 y 3 de enero: 3 días seguidos", "el 4 se rompe · 5 y 6: racha de 2"])),
    concl=dict(t0=454.53, big="3", big_unit="días", big_size=260, unit_dy=170, lines=["es la racha más larga:", "del 1 al 3 de enero."],
               thead=[("Racha", 40, "l"), ("Días", 1040, "r")], trows=[["1 – 3 de enero", "3"], ["5 – 6 de enero", "2"]],
               note=("Ordenar + una sola pasada por la lista.", "Patrón clásico de entrevista con fechas.")),
    cta=dict(t0=471.95, sub="Más ejercicios de entrevista", rows=[("¿Quieres más", 0.05), ("ingeniería", 0.2), ("de datos?", 0.35)],
             t_link=471.95, t_es=474.95, t_free=474.11),
    emph=[(203.5, 206.75), (444.9, 447.4)],
)
D6 = [1, 2, 3, 5, 6]
T6 = dict(cal=210.3, date=226.57, sort=263.97, init=274.91, loop=309.96, s1=368.28, s2=371.81, s3=390.88, s4=396.0, ret=405.78)
def v6_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    steps = [(T6["s1"], 2, 2, 2, False), (T6["s2"], 3, 3, 3, False), (T6["s3"], 5, 1, 3, True), (T6["s4"], 6, 2, 3, False)]
    cur = None
    for st in steps:
        if t >= st[0]: cur = st
    cap = "5 fechas (texto)" if t < T6["date"] else ("date.fromisoformat + sorted" if t < T6["init"] else "mejor = actual = 1")
    if t >= T6["loop"]: cap = "bucle desde el 2º día"
    if cur: cap = "gap → actual = 1" if cur[4] else "día seguido → actual + 1"
    if t >= T6["ret"]: cap = "return mejor"
    if not viz_frame(d, box, t, T6["cal"], cap): return
    cw = 128; cx0 = 70
    for k in range(7):
        day = k + 1; x = cx0 + k * (cw + 8); y = y0 + 80
        present = day in D6; a = eo(pr(t, T6["cal"] + k * 0.06, 0.3))
        in_streak = cur is not None and present and ((day <= 3 and day <= cur[1]) or (day >= 5 and cur[1] >= day and cur[1] >= 5))
        gap = cur is not None and day == 4 and cur[1] >= 5
        fill = (26, 30, 38)
        if in_streak: fill = mix((240, 140, 40), TP, 0.35)
        if gap: fill = mix(RED_, TP, 0.3)
        d.rounded_rectangle((x, y, x + cw, y + 110), 12, fill=mix(fill, TP, a), outline=mix((240, 140, 40) if in_streak else ((70, 78, 92) if present else (40, 44, 52)), TP, a), width=2)
        d.text((x + cw / 2, y + 16), "ene", font=MO(16, 500), fill=mix(MUT, TP, a), anchor="ma")
        d.text((x + cw / 2, y + 40), str(day), font=MO(40, 700), fill=mix(INK if present else (60, 66, 78), TP, a), anchor="ma")
        if not present: d.text((x + cw / 2, y + 88), "—", font=MO(18), fill=mix((60, 66, 78), TP, a), anchor="ma")
        elif cur is not None and day == cur[1]:
            d.polygon([(x + cw / 2 - 10, y + 126), (x + cw / 2 + 10, y + 126), (x + cw / 2, y + 112)], fill=ACC)
    pi = eo(pr(t, T6["init"], 0.3))
    if pi > 0:
        a_v = cur[2] if cur else 1; m_v = cur[3] if cur else 1
        d.text((70, y0 + 240), f"actual = {a_v}", font=MO(34, 700), fill=mix(INK, TP, pi))
        d.text((480, y0 + 240), f"mejor = {m_v}", font=MO(34, 700), fill=mix(YEL, TP, pi))
    pr_ = eo(pr(t, T6["ret"], 0.4))
    if pr_ > 0:
        d.text((70, y0 + 320), "racha máxima = 3 días", font=MO(36, 700), fill=mix((240, 140, 40), TP, pr_))
V6["code"]["viz"] = v6_viz; V6["code"]["viz_h"] = 470

# ====================================================================== VIDEO 7 · PySpark junior vs senior (última compra)
V7 = base("video7", "lote8_v7", "07_pyspark_junior_vs_senior.mp4")
V7["segs"] = sorted(V7["segs"] + [(106.34, 106.97, "ve")])          # keep "row_number" (editor took it from another take)
VENTAS = [("u1", "2025-01-05", "Madrid", 120), ("u1", "2025-03-10", "Madrid", 80), ("u2", "2025-02-01", "Barna", 200),
          ("u2", "2025-02-15", "Barna", 50), ("u3", "2025-01-20", "Sevilla", 300)]
V7.update(
    intro=dict(t0=1.47, title=("Junior", "vs Senior."), sub="Data Engineering · PySpark", t_tecnica=2.37, role="Data Engineer",
               t_role=1.85, company="PySpark · Window functions", t_company=3.0,
               info=[("Tecnología", "PySpark · Spark SQL"), ("Formato", "2 soluciones · 1 resultado")]),
    data=dict(t0=11.49, file="ventas  (Spark DataFrame)", count=5, count_label=" compras", t_rows=12.49, hl_start=15.43, scroll_d=0.8,
              cols=[("usuario", 40, "l", 15.43), ("fecha", 330, "l", 17.41), ("ciudad", 640, "l", 16.57), ("importe", 1040, "r", None)],
              rows=[[u, f, c, str(i)] for u, f, c, i in VENTAS], pool=[], footer_l="", footer_r="5 filas · 4 columnas"),
    question=dict(t0=19.52, size=118, step=124,
                  rows=[("Quédate con", 20.45), ("la última compra", 21.11), ("de cada usuario", 22.05)],
                  underlines=[(1, "última", 21.4), (2, "cada usuario", 22.4)]),
    code=dict(t0=32.80, sub="PySpark · groupBy vs Window", file="pyspark_junior_vs_senior.ipynb", status_r="Spark 3.5",
              steps=["groupBy", "join", "Window", "row_number"],
              lines='''# JUNIOR · groupBy + join de vuelta
ult = (
  ventas
  .groupBy('usuario')
  .agg(F.max('fecha').alias('fecha'))
)

ventas.join(
  ult, ['usuario','fecha']).show()

# SENIOR · Window (una sola pasada)
w = (
  Window
  .partitionBy('usuario')
  .orderBy(F.col('fecha').desc())
)

(ventas
 .withColumn('rk', F.row_number().over(w))
 .filter(F.col('rk') == 1)
 .drop('rk')
 .show())'''.split("\n"),
              rev={0: 32.92, 1: 34.3, 2: 34.5, 3: 34.68, 4: 38.16, 5: 38.5, 7: 55.99, 8: 56.5, 10: 96.69, 11: 98.05, 12: 98.3,
                   13: 99.49, 14: 101.57, 15: 104.5, 17: 105.0, 18: 106.34, 19: 111.66, 20: 112.4, 21: 113.0},
              hl=[(32.80, 0, 5, 0), (55.33, 7, 8, 1), (96.51, 10, 15, 2), (104.71, 17, 21, 3)],
              notes={4: (38.16, "← fecha máx."), 8: (58.99, "← 2ª pasada"), 13: (100.95, "← por usuario"),
                     14: (103.45, "← reciente 1º"), 18: (106.6, "← 1, 2, 3…"), 19: (111.92, "← solo la última")}),
    result=dict(t0=115.49, file="pyspark_junior_vs_senior.ipynb", status_r="Spark 3.5", title="Out[5]: .show()",
                header=[("usuario", 36, "l"), ("fecha", 260, "l"), ("ciudad", 560, "l"), ("importe", 860, "r")], fs=28, rh=56,
                rows=[["u1", "2025-03-10", "Madrid", "80"], ["u2", "2025-02-15", "Barna", "50"], ["u3", "2025-01-20", "Sevilla", "300"]],
                vals=[[0, 1]] * 3, bar_col=1, bar_x=1100, bar_w=0, hot_row=99, t_hot=999, t_bars=999, cells=[],
                note=(116.25, "SENIOR", ["mismo resultado, una sola pasada", "escala a millones de filas"])),
    concl=dict(t0=118.05, big="1", big_unit="pasada", big_size=260, unit_dy=170, lines=["en vez de 2: la Window function", "evita el join de vuelta."],
               thead=[("Enfoque", 40, "l"), ("Pasadas", 740, "r"), ("Escala", 1040, "r")],
               trows=[["Junior · groupBy + join", "2", "Peor"], ["Senior · Window", "1", "Millones"]],
               note=("Mismo resultado, menos shuffle.", "Pregunta clásica de entrevista PySpark.")),
    cta=dict(t0=132.83, sub="Más ingeniería de datos", rows=[("¿Quieres más", 0.05), ("ingeniería", 0.2), ("de datos?", 0.35)],
             t_link=132.83, t_es=135.53, t_free=134.11),
    emph=[(20.4, 22.95), (118.0, 120.95)],
)
T7 = dict(rows=33.0, grp=34.68, ult=38.16, join=55.99, win=98.05, part=99.49, order=101.57, rk=106.34, keep=111.66)
def v7_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    senior = t >= T7["win"]
    cap = "ventas: 5 compras"
    if t >= T7["grp"]: cap = "junior: groupBy + max(fecha)"
    if t >= T7["join"]: cap = "junior: join de vuelta (2ª pasada)"
    if senior: cap = "senior: ventana por usuario"
    if t >= T7["order"]: cap = "senior: ordenada por fecha desc"
    if t >= T7["rk"]: cap = "row_number() → 1, 2…"
    if t >= T7["keep"]: cap = "rk == 1 → la última compra"
    if not viz_frame(d, box, t, T7["rows"], cap): return
    last = {"u1": "2025-03-10", "u2": "2025-02-15", "u3": "2025-01-20"}
    UC = {"u1": (88, 166, 255), "u2": (240, 150, 60), "u3": (190, 120, 255)}
    if not senior:
        for k, (u, f, c, i) in enumerate(VENTAS):
            a = eo(pr(t, T7["rows"] + k * 0.06, 0.3)); y = y0 + 64 + k * 50
            hit = t >= T7["join"] and last[u] == f
            fill = mix(GREEN, TP, 0.22 * eo(pr(t, T7["join"] + 0.6, 0.4))) if hit else (26, 30, 38)
            d.rounded_rectangle((50, y, 470, y + 40), 8, fill=mix(fill, TP, a), outline=mix(UC[u], TP, a * (0.9 if t >= T7["grp"] else 0.3)), width=2)
            d.text((66, y + 9), f"{u}  {f}  {c}", font=MO(19, 600), fill=mix(INK, TP, a))
        pu = eo(pr(t, T7["ult"], 0.4))
        if pu > 0:
            d.text((600, y0 + 64), "ult = max(fecha)", font=MO(19, 600), fill=mix(MUT, TP, pu))
            for k, u in enumerate(["u1", "u2", "u3"]):
                y = y0 + 100 + k * 50
                d.rounded_rectangle((600, y, 1020, y + 40), 8, fill=mix((26, 30, 38), TP, pu), outline=mix(UC[u], TP, pu), width=2)
                d.text((616, y + 9), f"{u}  {last[u]}", font=MO(19, 700), fill=mix(INK, TP, pu))
        pj = eo(pr(t, T7["join"] + 0.3, 0.6))
        if pj > 0:
            for k, (u, f, c, i) in enumerate(VENTAS):
                if last[u] != f: continue
                ku = ["u1", "u2", "u3"].index(u)
                d.line((600, y0 + 120 + ku * 50, 600 - (130 * pj), y0 + 84 + k * 50), fill=mix(GREEN, TP, pj), width=3)
            d.text((50, y0 + 330), "2 pasadas por los datos + shuffle del join", font=MO(22, 700), fill=mix(RED_, TP, pj))
    else:
        po = eo(pr(t, T7["order"], 0.6)); prk = eo(pr(t, T7["rk"], 0.4)); pk = eo(pr(t, T7["keep"], 0.5))
        parts = [("u1", [("2025-03-10", 1), ("2025-01-05", 2)]), ("u2", [("2025-02-15", 1), ("2025-02-01", 2)]), ("u3", [("2025-01-20", 1)])]
        pp = eo(pr(t, T7["part"], 0.5))
        for pi_, (u, rows) in enumerate(parts):
            bx = 50 + pi_ * 330; a = eo(pr(t, T7["win"] + pi_ * 0.1, 0.4))
            d.rounded_rectangle((bx - 10, y0 + 60, bx + 300, y0 + 200), 12, outline=mix(UC[u], TP, a * pp), width=2)
            d.text((bx, y0 + 68), f"partición {u}", font=MO(17, 600), fill=mix(UC[u], TP, a))
            for j, (f, rk) in enumerate(rows):
                y = y0 + 100 + j * 46; drop = rk != 1
                aa = a * (1 - 0.75 * pk if drop else 1)
                d.rounded_rectangle((bx, y, bx + 280, y + 38), 8, fill=mix(mix(GREEN, TP, 0.22) if (not drop and pk > 0) else (26, 30, 38), TP, aa))
                d.text((bx + 12, y + 8), f, font=MO(19, 600), fill=mix(INK, TP, aa))
                if prk > 0: d.text((bx + 268, y + 8), f"rk {rk}", font=MO(19, 700), fill=mix(YEL if rk == 1 else MUT, TP, prk * aa), anchor="ra")
        if pk > 0: d.text((50, y0 + 330), "1 sola pasada: mismo resultado", font=MO(24, 700), fill=mix(GREEN, TP, pk))
V7["code"]["viz"] = v7_viz; V7["code"]["viz_h"] = 470

# ====================================================================== VIDEO 8 · ETL clásico (día a día de un data engineer junior)
V8 = base("video8", "lote8_v8", "08_etl_dia_a_dia.mp4")
_s8 = [x for x in V8["segs"] if not (149.0 < x[0] < 151.6)]                     # drop "cruzamos las ventas por..." (incomplete take)
V8["segs"] = sorted(_s8 + [(152.13, 154.78, "ve"), (165.95, 166.55, "ve"), (289.79, 291.95, "ve")])
RAW8 = [("1", "P001", "2025-01-05", "120€"), ("2", "P002", "2025-01-05", "80€"), ("2", "P002", "2025-01-05", "80€"),
        ("3", "P003", "2025-02-10", "300€"), ("4", "P001", "2025-02-11", "NULL"), ("5", "P002", "2025-03-01", "50€")]
PROD8 = {"P001": ("Camiseta", "Ropa"), "P002": ("Café", "Alimentación"), "P003": ("Portátil", "Electrónica")}
V8.update(
    intro=dict(t0=1.41, title=("Su día", "a día."), sub="Data Engineering · ETL", t_tecnica=3.45, role="Data Engineer Junior", t_role=2.17,
               company="Un pipeline ETL con PySpark", t_company=4.07,
               info=[("Fases", "Extract · Clean · Join · Transform · Load"), ("Tecnología", "PySpark")],
               job=dict(t_in=1.8, t_apply=3.7, tile_text="DE", tile_bg=(30, 64, 175), title="Data Engineer Junior",
                        company="Equipo de datos", meta="Pipelines ETL · PySpark")),
    data=dict(t0=7.14, file="1 · EXTRACT  ventas (crudas)", count=6, count_label=" filas con basura típica", t_rows=8.1, hl_start=999, scroll_d=0.8,
              cols=[("id", 40, "l", None), ("producto", 200, "l", None), ("fecha", 480, "l", None), ("importe", 1040, "r", None)],
              rows=[list(r) for r in RAW8], pool=[], footer_l="+ productos: Camiseta · Café · Portátil", footer_r="2 tablas de origen"),
    code=dict(t0=54.72, sub="PySpark · pipeline ETL", file="01_etl_clasico.ipynb", status_r="Spark 3.5",
              steps=["extract", "clean", "join", "transform", "load"],
              lines='''# 2 · CLEAN
ventas_limpias = (
  ventas
  .withColumn('importe',
    F.regexp_replace('importe', '€', '')
     .cast('int'))
  .withColumn('fecha', F.to_date('fecha'))
  .filter(F.col('importe').isNotNull())
  .dropDuplicates()
)

# 3 · JOIN
ventas_enriq = ventas_limpias.join(
  F.broadcast(productos), 'producto', 'left')

# 4 · TRANSFORM
resumen = (
  ventas_enriq
  .withColumn('mes', F.month('fecha'))
  .groupBy('categoria')
  .agg(F.sum('importe').alias('total'),
       F.count('*').alias('n_ventas'))
)

# 5 · LOAD
(ventas_enriq.write.mode('overwrite')
  .partitionBy('categoria').parquet(ruta))'''.split("\n"),
              rev={0: 55.0, 1: 55.3, 2: 55.5, 3: 62.0, 4: 64.71, 5: 66.47, 6: 69.13, 7: 72.30, 8: 78.24, 9: 78.5,
                   11: 101.9, 12: 105.28, 13: 153.0, 15: 166.0, 16: 195.41, 17: 195.8, 18: 241.81, 19: 269.0, 20: 270.48, 21: 271.3, 22: 273.7,
                   24: 282.0, 25: 282.65, 26: 286.31},
              hl=[(54.72, 0, 9, 1), (61.43, 3, 5, 1), (68.99, 6, 6, 1), (71.14, 7, 7, 1), (77.76, 8, 8, 1), (101.86, 11, 13, 2),
                  (165.92, 15, 22, 3), (240.29, 18, 18, 3), (268.48, 19, 21, 3), (281.63, 24, 26, 4)],
              notes={4: (65.55, "← quita el €"), 5: (67.35, "← a entero"), 6: (70.23, "← a fecha"), 7: (75.86, "← fuera nulos"),
                     8: (78.6, "← sin duplicados"), 13: (159.07, "← + categoría"), 18: (243.13, "← mes"), 20: (272.08, "← por categoría"),
                     26: (287.45, "← data lake")}),
    concl=dict(t0=289.76, big="5", big_unit="fases", big_size=260, unit_dy=170, lines=["de un pipeline ETL, listo para", "un dashboard o un analista."],
               thead=[("Fase", 40, "l"), ("Qué hace", 1040, "r")],
               trows=[["Extract", "leer ventas y productos"], ["Clean", "€ → int, fechas, nulos, duplicados"], ["Join", "+ nombre y categoría"],
                      ["Transform", "total por categoría"], ["Load", "parquet en el data lake"]],
               note=("El join es la fase más costosa del pipeline.", "Broadcast de la tabla pequeña: sin shuffle.")),
    cta=dict(t0=316.2, sub="Más ingeniería de datos", rows=[("¿Quieres más", 0.05), ("ingeniería", 0.2), ("de datos?", 0.35)],
             t_link=316.2, t_es=318.6, t_free=317.78),
    emph=[(101.86, 105.4), (281.6, 285.0)],
)
T8 = dict(clean=55.0, euro=64.71, cast=66.47, null=75.86, dup=78.24, join=101.9, joincols=159.07, tr=195.41, agg=270.48, load=282.65, path=286.31)
def v8_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    stage = "clean" if t < T8["join"] else ("join" if t < T8["tr"] else ("transform" if t < T8["load"] else "load"))
    caps = {"clean": "CLEAN: limpiamos las ventas crudas", "join": "JOIN: + nombre y categoría (broadcast)",
            "transform": "TRANSFORM: total por categoría", "load": "LOAD: parquet particionado"}
    if not viz_frame(d, box, t, T8["clean"], caps[stage]): return
    if stage == "clean":
        pe, pc, pn, pd_ = (eo(pr(t, T8[k], 0.4)) for k in ("euro", "cast", "null", "dup"))
        for k, (i, p, f, imp) in enumerate(RAW8):
            y = y0 + 62 + k * 50; a = eo(pr(t, T8["clean"] + k * 0.05, 0.3))
            drop = (imp == "NULL" and pn > 0) or (k == 2 and pd_ > 0)
            fade = (pn if imp == "NULL" else (pd_ if k == 2 else 0))
            aa = a * (1 - 0.7 * fade)
            d.text((60, y), f"{i}  {p}  {f}", font=MO(22, 500), fill=mix(INK, TP, aa))
            val = imp if imp == "NULL" else (imp.replace("€", "") if pe > 0.5 else imp)
            col = RED_ if imp == "NULL" else (GREEN if pc > 0.5 else (240, 150, 60))
            d.text((560, y), val if not (pc > 0.5 and imp != "NULL") else str(int(imp.replace("€", ""))), font=MO(24, 700), fill=mix(col, TP, aa))
            if pc > 0.5 and imp != "NULL": d.text((700, y + 2), "int", font=MO(18, 500), fill=mix(MUT, TP, aa))
            if drop: d.line((50, y + 13, 50 + 640 * fade, y + 13), fill=mix(RED_, TP, a), width=3)
        lab = []
        if pn > 0: lab.append("NULL fuera")
        if pd_ > 0: lab.append("duplicado fuera")
        if lab: d.text((760, y0 + 140), "\n".join(lab), font=MO(22, 700), fill=RED_)
        if pd_ > 0.9: d.text((760, y0 + 230), "6 → 4 filas", font=MO(30, 700), fill=YEL)
    elif stage == "join":
        pj = eo(pr(t, T8["joincols"], 0.5))
        clean = [r for k, r in enumerate(RAW8) if r[3] != "NULL" and k != 2]
        for k, (i, p, f, imp) in enumerate(clean):
            y = y0 + 70 + k * 56
            d.text((60, y), f"{i}  {p}  {imp.replace('€', '')}", font=MO(24, 600), fill=INK)
            if pj > 0:
                nm, cat = PROD8[p]
                d.text((420, y), f"+ {nm}", font=MO(24, 600), fill=mix(ACC, TP, pj))
                d.text((700, y), cat, font=MO(24, 700), fill=mix(YEL, TP, pj))
        d.text((60, y0 + 330), "productos (3 filas) viaja a cada nodo: sin shuffle", font=MO(20, 500), fill=mix(MUT, TP, eo(pr(t, T8["join"] + 1, 0.5))))
    elif stage == "transform":
        pa = eo(pr(t, T8["agg"], 0.8))
        bars = [("Electrónica", 300, 1), ("Alimentación", 130, 2), ("Ropa", 120, 1)]
        for k, (c, tot, n) in enumerate(bars):
            y = y0 + 80 + k * 80
            d.text((60, y + 8), c, font=MO(24, 600), fill=INK)
            d.rounded_rectangle((330, y + 6, 330 + 520 * tot / 300 * pa, y + 40), 6, fill=ACC if k == 0 else (55, 64, 80))
            if pa > 0.3: d.text((x1 - 50, y + 8), f"{tot} € · {n}", font=MO(24, 700), fill=mix(INK, TP, pa), anchor="ra")
        d.text((60, y0 + 330), "groupBy('categoria') + sum + count", font=MO(20, 500), fill=MUT)
    else:
        pp = eo(pr(t, T8["path"], 0.5))
        d.text((60, y0 + 70), "/tmp/ventas_procesadas/", font=MO(26, 700), fill=INK)
        for k, c in enumerate(["Alimentación", "Electrónica", "Ropa"]):
            a = eo(pr(t, T8["load"] + 0.3 + k * 0.25, 0.4))
            d.text((100, y0 + 130 + k * 56), f"categoria={c}/  part-0000{k}.parquet", font=MO(22, 500), fill=mix(ACC, TP, a))
        d.text((60, y0 + 330), "Guardadas 4 filas · lista para el data lake", font=MO(22, 700), fill=mix(GREEN, TP, pp))
V8["code"]["viz"] = v8_viz; V8["code"]["viz_h"] = 470

# ====================================================================== VIDEO 1 · remoto vs presencial (Stack Overflow 2025)
V1 = base("video_1", "lote8_v1", "01_remoto_vs_presencial.mp4")
# tightened for publishing (2026-10-26): shorter dataset/import lines, drop the wrong "dos grupos, los que sí y los que no"
# and the cut-off "La diferencia es más"
V1["segs"] = [(202.50, 204.83, "vs"), (211.84, 214.76, "ve"), (228.96, 233.70), (237.15, 243.40, "ve"), (246.24, 250.66), (250.91, 254.69),
              (254.98, 256.22), (263.01, 265.86), (276.70, 280.86), (297.76, 300.83), (311.49, 314.50, "ve"), (319.17, 323.04),
              (336.16, 345.63), (345.86, 347.40, "ve"), (376.96, 382.53)]
RW = [("Remote", 88718, 7120), ("Hybrid (some in-person, leans…", 80966, 3811), ("Your choice (very flexible…", 75410, 2752),
      ("Hybrid (some remote, leans…", 72958, 4202), ("In-person", 46406, 3195)]
import json as _json
_SO_ROWS = _json.load(open(f"{LOTE}/video_1/survey_sample_rows.json"))
RW_SHORT = ["Remoto", "Híbrido flex.", "A elegir", "Híbrido pres.", "Presencial"]
V1.update(
    intro=dict(t0=202.50, t_tecnica=202.78, role="Data Analyst Junior", t_role=203.38, company="en Stack Overflow", t_company=203.9, logo=(540, 1040, 340, 203.3), logo_kind="so",
               info=[]),          # intro is only ~2.4 s: title + role + logo only (user found the rest too busy)
    data=dict(t0=211.81, file="survey_results_public.csv", count=49191, count_label=" respuestas · 172 columnas", t_rows=212.3, hl_start=999, scroll_d=2.6,
              cols=[("Age", 40, "l", None), ("WorkExp", 330, "r", None), ("RemoteWork", 390, "l", None), ("ConvertedCompYearly", 1040, "r", None)],
              rows=_SO_ROWS[-13:], pool=_SO_ROWS[:-13],          # real rows from the official 2025 results.csv
              footer_l="NaN = el encuestado no respondió", footer_r="Developer Survey 2025"),
    question=dict(t0=228.93, size=118, step=124,
                  rows=[("¿Cuánto cobra", 229.85), ("un dev remoto", 231.41), ("vs presencial?", 232.99)],
                  underlines=[(1, "remoto", 231.6), (2, "presencial", 233.2)]),
    code=dict(t0=237.12, sub="pandas · groupby + agg", file="stackoverflow_tiktok.ipynb", status_r="n=21.080 · survey 2025",
              steps=["csv", "notna", "groupby", "agg", "sort", "print"],
              lines='''import pandas as pd

df = pd.read_csv(
  '../datasets/survey_results_public.csv'
)

df = df[
  df['ConvertedCompYearly'].notna()
  & df['RemoteWork'].notna()
]

result = (
  df.groupby('RemoteWork')
  ['ConvertedCompYearly']
  .agg(['median','count'])
  .sort_values('median', ascending=False)
)

print("Salario por modalidad")
print(result.round(0))'''.split("\n"),
              rev={0: 237.70, 2: 240.48, 3: 241.0, 4: 241.36, 6: 246.81, 7: 251.70, 8: 255.31, 9: 255.8, 11: 279.35, 12: 279.6,
                   13: 280.0, 14: 298.21, 15: 312.20, 16: 312.5, 18: 319.22, 19: 320.60},
              hl=[(237.12, 0, 4, 0), (246.21, 6, 9, 1), (276.67, 11, 13, 2), (297.73, 14, 14, 3), (311.46, 15, 16, 4), (319.14, 18, 19, 5)],
              notes={7: (253.84, "← salario bruto anual"), 8: (264.56, "← remoto o no"), 12: (279.9, "← 5 modalidades"),
                     14: (298.83, "← mediana, no media"), 15: (313.74, "← mayor a menor")}),
    result=dict(t0=321.62, file="stackoverflow_tiktok.ipynb", status_r="n=21.080 · survey 2025", title="Salario por modalidad",
                header=[("RemoteWork", 36, "l"), ("median", 760, "r"), ("count", 900, "r")], fs=23, rh=52,
                rows=[[n, f"{m:.1f}", str(c)] for n, m, c in RW], vals=[[0, m] for _, m, _ in RW], bar_col=1, bar_x=920, bar_w=120,
                hot_row=0, t_hot=337.17, t_bars=322.5, cells=[(0, 1, 338.03), (4, 1, 345.83)],
                note=(337.6, "OJO: ES LA MEDIANA", ["remoto: 88.718 $ · presencial: 46.406 $", "casi el doble (× 1,9)"])),
    concl=dict(t0=343.71, big="×1,9", big_size=240, lines=["cobra de mediana un dev en remoto", "frente a uno 100 % presencial."],
               thead=[("Modalidad", 40, "l"), ("Salario (p50)", 760, "r"), ("Devs", 1040, "r")],
               trows=[["Remoto", "88.718 $", "7.120"], ["Presencial", "46.406 $", "3.195"]],
               note=("Ojo: es la mediana, no la media.", "Fuente: Stack Overflow Developer Survey 2025 · 21.080 devs")),
    cta=dict(t0=378.6, sub="Más casos prácticos de datos", rows=[("¿Quieres más", 0.05), ("profesiones", 0.2), ("de data?", 0.35)],
             t_link=378.65, t_es=381.91, t_free=380.97),
    emph=[(229.0, 233.2), (249.2, 250.6), (279.3, 280.8), (313.0, 314.4), (336.1, 342.2)],
    clean_term=True,
)
T1 = dict(grid=241.36, notna=249.79, grp=279.35, agg=298.21, sort=312.20)
def v1_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    cap = "1 ficha ≈ 400 devs" if t < T1["notna"] else "quitamos filas sin salario o sin modalidad"
    if t >= T1["grp"]: cap = "groupby('RemoteWork'): 5 grupos"
    if t >= T1["agg"]: cap = "agg: mediana del salario y nº de devs"
    if t >= T1["sort"]: cap = "sort_values: de mayor a menor"
    if not viz_frame(d, box, t, T1["grid"], cap): return
    COLS = [(255, 150, 60), (190, 120, 255), (88, 166, 255), (86, 211, 140), (240, 90, 90)]
    toks = []
    for gi, (_, _, c) in enumerate(RW): toks += [gi] * round(c / 400)
    toks = [toks[i] for i in sorted(range(len(toks)), key=lambda i: (i * 37) % len(toks))]
    alpha = sorted(range(5), key=lambda i: RW[i][0])
    ps = eo(pr(t, T1["sort"], 1.0)); pg = eo(pr(t, T1["grp"], 1.0)); pa = eo(pr(t, T1["agg"], 0.8))
    colw = (x1 - x0 - 80) / 5
    def cx(gi): return x0 + 40 + colw * ((alpha.index(gi)) * (1 - ps) + gi * ps + 0.5)
    base = y1 - 70; cnt = [0] * 5
    for k, gi in enumerate(toks):
        a = eo(pr(t, T1["grid"] + k * 0.012, 0.3)) * (1 - pa)
        if a <= 0.02: continue
        gx = x0 + 60 + (k % 18) * 54; gy = y0 + 70 + (k // 18) * 34
        j = cnt[gi]; cnt[gi] += 1
        bx = cx(gi) - 2 * 30 + (j % 4) * 30; by = base - 30 - (j // 4) * 22
        x = gx + (bx - gx) * pg; y = gy + (by - gy) * pg
        d.rounded_rectangle((x, y, x + 26, y + 16), 4, fill=mix(COLS[gi], TP, a))
    if pa > 0:
        mmax = max(m for _, m, _ in RW)
        for gi, (_, m, c) in enumerate(RW):
            h = (base - y0 - 130) * m / mmax * pa; x = cx(gi)
            d.rounded_rectangle((x - 40, base - h, x + 40, base), 6, fill=COLS[gi])
            d.text((x, base - h - 10), f"{m / 1000:.1f}k $".replace(".", ","), font=MO(19, 700), fill=mix(INK, TP, pa), anchor="mb")
    if pg > 0.3:
        for gi in range(5):
            d.text((cx(gi), base + 14), RW_SHORT[gi], font=MO(16, 600), fill=mix(COLS[gi], TP, eo((pg - 0.3) / 0.7)), anchor="ma")
V1["code"]["viz"] = v1_viz; V1["code"]["viz_h"] = 470

# ====================================================================== VIDEO 2 · lista de espera por profesión (SQL sobre BigDataStack)
V2 = base("video_2", "lote8_v2", "02_sql_lista_de_espera.mp4")
_s2 = [x for x in V2["segs"] if not (203.0 < x[0] < 204.0)]
V2["segs"] = sorted(_s2 + [(203.49, 205.45, "ve"), (207.52, 209.06), (289.31, 291.55, "ve")])
TR2 = [("Análisis de Datos", 366), ("Ciencia de Datos", 251), ("Ingeniería de IA", 186), ("MLOps", 146), ("Data Governance", 127), ("Ingeniería de Datos", 0)]
V2.update(
    intro=dict(t0=131.04, title=("Analítica", "con SQL."), sub="Caso real · mi plataforma BigDataStack", t_tecnica=131.77, role="Datos reales de BigDataStack",
               t_role=131.29, company="Analítica de producto con SQL", t_company=132.25,
               info=[("Base de datos", "PostgreSQL"), ("Formato", "1 consulta · 60 segundos")]),
    question=dict(t0=143.59, size=112, step=118,
                  rows=[("¿Cuántas personas", 143.99), ("hay en lista de", 145.09), ("espera por", 145.47), ("profesión?", 146.17)],
                  underlines=[(2, "espera", 145.6)]),
    data=dict(t0=157.83, file="bigdatastack  (PostgreSQL)", count=2, count_label=" tablas", t_rows=158.3, hl_start=159.05, scroll_d=0.6,
              cols=[("Tabla", 40, "l", 159.05), ("Columnas", 470, "l", 162.56), ("Qué guarda", 1040, "r", None)],
              rows=[["tracks", "id · title", "las profesiones"], ["track_interests", "id · track_id · …", "interés de cada alumno"]],
              pool=[], footer_l="", footer_r="relación 1 → N"),
    code=dict(t0=181.57, sub="SQL · LEFT JOIN + GROUP BY", file="queries-tiktok.sql", status_r="PostgreSQL",
              steps=["SELECT", "JOIN", "GROUP", "count", "ORDER"],
              lines='''SELECT t.title as profesion,
       count(ti.id) as interesados
FROM tracks t
LEFT JOIN track_interests ti on ti.track_id = t.id
GROUP BY t.id
ORDER BY interesados DESC;'''.split("\n"),
              rev={2: 195.64, 3: 196.98, 4: 219.31, 0: 233.33, 1: 260.31, 5: 268.21},
              hl=[(181.57, 0, 0, 0), (193.12, 2, 3, 1), (215.81, 4, 4, 2), (222.08, 0, 0, 3), (259.91, 1, 1, 3), (267.81, 5, 5, 4)],
              notes={2: (205.0, "← profesiones"), 4: (221.11, "← 1 grupo por profesión"), 1: (264.65, "← nº de interesados"),
                     5: (271.43, "← más esperada 1º")}),
    result=dict(t0=272.35, file="queries-tiktok.sql", status_r="PostgreSQL", title="Result · Total 6",
                header=[("profesion", 36, "l"), ("interesados", 760, "r")], fs=27, rh=56,
                rows=[[n, str(c)] for n, c in TR2], vals=[[0, c] for _, c in TR2], bar_col=1, bar_x=800, bar_w=230,
                hot_row=0, t_hot=283.76, t_bars=273.0, cells=[(0, 1, 284.88), (1, 1, 287.82)],
                note=(286.0, "INSIGHT", ["Análisis de Datos lidera con 366", "Ing. de Datos sale con 0 gracias al LEFT JOIN"])),
    concl=dict(t0=289.31, big="366", big_unit="personas", big_size=240, unit_dy=150, lines=["esperan Análisis de Datos:", "la próxima profesión de la plataforma."],
               thead=[("Profesión", 40, "l"), ("En lista de espera", 1040, "r")],
               trows=[["Análisis de Datos", "366"], ["Ciencia de Datos", "251"], ["Ingeniería de IA", "186"]],
               note=("LEFT JOIN + GROUP BY + COUNT: el trío clave.", "Datos reales de BigDataStack.")),
    cta=dict(t0=318.47, sub="Más casos prácticos de datos", rows=[("¿Quieres más", 0.05), ("análisis de", 0.2), ("datos?", 0.35)],
             t_link=318.47, t_es=321.49, t_free=320.59),
    emph=[(143.6, 147.4), (281.9, 288.0)],
)
T2 = dict(rows=195.64, join=197.18, grp=219.31, count=260.31, order=268.21)
def v2_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    cap = "FROM tracks: 6 profesiones"
    if t >= T2["join"]: cap = "LEFT JOIN: cada interés con su profesión"
    if t >= T2["grp"]: cap = "GROUP BY t.id"
    if t >= T2["count"]: cap = "count(ti.id): interesados por profesión"
    if t >= T2["order"]: cap = "ORDER BY interesados DESC"
    if not viz_frame(d, box, t, T2["rows"], cap): return
    alpha = sorted(range(6), key=lambda i: TR2[i][0])
    po = eo(pr(t, T2["order"], 1.0)); pj = eo(pr(t, T2["join"], 1.2)); pc = eo(pr(t, T2["count"], 0.6))
    for i, (n, c) in enumerate(TR2):
        a = eo(pr(t, T2["rows"] + i * 0.08, 0.3))
        r = alpha.index(i) * (1 - po) + i * po
        y = y0 + 62 + r * 52
        d.text((50, y), n, font=MO(22, 700 if i == 0 and po > 0.5 else 500), fill=mix(INK, TP, a))
        dots = round(c / 20)
        for k in range(dots):
            pk = eo(pr(t, T2["join"] + k * 0.03, 0.3)) * (1 - pc)
            if pk > 0: d.ellipse((420 + k * 26, y + 6, 436 + k * 26, y + 22), fill=mix(ACC, TP, pk))
        if pc > 0:
            d.rounded_rectangle((420, y + 4, 420 + 470 * c / 366 * pc, y + 24), 5, fill=ACC if i == 0 else (55, 64, 80))
            d.text((x1 - 40, y), str(c), font=MO(24, 700), fill=mix(YEL if i == 0 else INK, TP, pc), anchor="ra")
        if c == 0 and pj > 0.8:
            d.text((420, y + 2), "0 · sigue en la lista (LEFT JOIN)", font=MO(18, 600), fill=mix(RED_, TP, eo((pj - 0.8) * 5) * (1 - pc)))
V2["code"]["viz"] = v2_viz; V2["code"]["viz_h"] = 470

# ====================================================================== VIDEO 3 · delitos sexuales por origen (INE, normalizado)
V3 = base("video3", "lote8_v3", "03_delitos_por_origen_ine.mp4")
_s3 = [x for x in V3["segs"] if not (21.0 < x[0] < 21.1) and not (427.8 < x[0] < 428.0) and not (435.5 < x[0] < 435.6)]
V3["segs"] = sorted(_s3 + [(12.00, 15.81), (16.00, 17.54), (130.18, 131.20), (186.62, 188.91, "ve"),
                           (430.59, 431.74), (435.55, 436.72, "ve"), (448.19, 448.51)])
D3 = [("Total", 6111), ("Española", 4131), ("UE27 sin España", 320), ("Europa no UE", 52), ("De África", 651),
      ("De América", 844), ("De Asia", 113), ("De Oceanía", 0)]
F3 = [("África", 2100.7, 4.9, 651), ("América", 2988.2, 3.4, 844), ("Asia", 4984.9, 2.1, 113), ("Europa", 6583.8, 1.6, 372),
      ("Española", 10219.4, 1.0, 4131)]
def _es(x, dec=0): return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
V3.update(
    intro=dict(t0=3.81, title=("Datos", "del INE."), sub="¿Qué origen tiene más delitos sexuales per cápita?", t_tecnica=4.2,
               role="Datos oficiales del INE", t_role=5.0, company="Análisis con Python · pandas", t_company=6.4,
               info=[("Datasets", "delitos + población"), ("Año", "2025")]),
    data=dict(t0=12.00, file="delicuencia_nacionalidad.csv", count=7930, count_label=" filas · INE", t_rows=13.4, hl_start=55.6, scroll_d=0.8,
              cols=[("Nacionalidad", 40, "l", None), ("Delitos sexuales 2025", 1040, "r", 55.6)],
              rows=[[n, _es(c)] for n, c in D3], pool=[], footer_l="Filtro: delitos sexuales · 2025", footer_r="Fuente: INE"),
    question=dict(t0=61.15, size=118, step=124,
                  rows=[("¿Más delitos…", 61.5), ("o más", 62.6), ("población?", 63.6)],
                  underlines=[(2, "población", 64.4)]),
    code=dict(t0=70.53, sub="pandas · tasa normalizada", file="delitos_sexuales_tiktok.ipynb", status_r="INE · 2025",
              steps=["población", "filtro", "continente", "1 de cada X", "tabla"],
              lines='''# 2 · población por nacionalidad
pob = pd.read_csv(
  '../datasets/evolucion_migracion.csv',
  sep=';')
pob = pob[
  pob['Periodo'] == '1 de enero de 2025'
]

# 3 · cálculo normalizado según origen
d = delitos_cont(delitos)
p = pob_cont(total)

# 1 delito por cada X habitantes
factor = pd.Series({
  k: p[k] / d[k] for k in d
}).sort_values()

tabla = pd.DataFrame({
  '1 de cada': factor,
  'factor': factor['Española'] / factor,
})
print(tabla.round(1))'''.split("\n"),
              rev={0: 70.6, 1: 71.4, 2: 71.6, 3: 71.8, 4: 82.3, 5: 84.4, 6: 84.6, 8: 90.3, 9: 176.4, 10: 181.5,
                   12: 194.9, 13: 195.4, 14: 195.6, 15: 195.8, 17: 197.3, 18: 197.5, 19: 197.7, 20: 197.9, 21: 198.3},
              hl=[(70.53, 0, 3, 0), (82.14, 4, 6, 1), (90.21, 8, 8, 2), (176.29, 9, 10, 2), (194.85, 12, 15, 3), (197.2, 17, 21, 4)],
              notes={2: (74.3, "← población INE"), 5: (85.0, "← 1 ene 2025"), 9: (178.0, "← delitos (CSV 1)"),
                     10: (183.5, "← habitantes (CSV 2)"), 14: (196.5, "← hab. / delitos")}),
    result=dict(t0=391.74, file="delitos_sexuales_tiktok.ipynb", status_r="INE · 2025", title="1 delito por cada X habitantes",
                header=[("origen", 36, "l"), ("1 de cada", 620, "r"), ("factor", 800, "r")], fs=27, rh=56,
                rows=[[n, f"{x:.1f}", f"{f:.1f}"] for n, x, f, _ in F3], vals=[[0, x, f] for _, x, f, _ in F3], bar_col=2, bar_x=840, bar_w=200,
                hot_row=0, t_hot=400.4, t_bars=392.4, cells=[(4, 1, 396.6), (0, 1, 403.9)],
                note=(404.6, "INSIGHT", ["Española: 1 de cada 10.219 habitantes", "África: 1 de cada 2.101 habitantes"])),
    concl=dict(t0=422.75, big="×4,9", big_size=240, lines=["más delitos sexuales registrados por habitante", "de origen africano que de origen español."],
               thead=[("Origen", 40, "l"), ("1 delito por cada", 760, "r"), ("Factor", 1040, "r")],
               trows=[["África", "2.101 hab.", "4,9"], ["América", "2.988 hab.", "3,4"], ["Española", "10.219 hab.", "1,0"]],
               note=("Tasa bruta: aún no ajusta por edad ni sexo.", "Fuente: INE · delitos sexuales 2025 y población a 1/1/2025")),
    cta=dict(t0=465.89, sub="Más casos prácticos de datos", rows=[("¿Quieres más", 0.05), ("análisis de", 0.2), ("datos?", 0.35)],
             t_link=465.89, t_es=467.69, t_free=466.6),
    emph=[(57.4, 60.8), (422.75, 427.55)],
)
T3 = dict(pob=71.6, filt=84.4, grp=176.29, pcol=181.41, fac=194.85, sort=197.3)
def v3_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    cap = "población por nacionalidad"
    if t >= T3["filt"]: cap = "nos quedamos con 1 ene 2025"
    if t >= T3["grp"]: cap = "delitos y población por continente"
    if t >= T3["fac"]: cap = "habitantes ÷ delitos = 1 de cada X"
    if t >= T3["sort"]: cap = "ordenado: menos habitantes por delito arriba"
    if not viz_frame(d, box, t, T3["pob"], cap): return
    order = ["Española", "Europa", "América", "Asia", "África"]
    po = eo(pr(t, T3["sort"], 1.0)); pg = eo(pr(t, T3["grp"], 0.6)); pp = eo(pr(t, T3["pob"] + 0.6, 0.8)); pf = eo(pr(t, T3["fac"], 0.9))
    hy = y0 + 64
    for lab, x, al in (("origen", 50, "la"), ("delitos", 380, "ra"), ("habitantes", 600, "ra"), ("1 de cada", x1 - 40, "ra")):
        a = 1 if lab == "origen" else (pg if lab == "delitos" else pp if lab == "habitantes" else pf)
        d.text((x, hy), lab, font=MO(17, 600), fill=mix(MUT, TP, a), anchor=al)
    xmax = max(x for _, x, _, _ in F3)
    for i, (n, x, f, dl) in enumerate(F3):
        a = eo(pr(t, T3["pob"] + order.index(n) * 0.1, 0.3))
        r = order.index(n) * (1 - po) + i * po
        y = hy + 44 + r * 62
        hot = n == "África" and po > 0.5
        d.text((50, y), n, font=MO(23, 700 if hot else 500), fill=mix(YEL if hot else INK, TP, a))
        pop = x * dl
        d.text((380, y), _es(dl * pg), font=MO(23, 500), fill=mix(RED_, TP, pg), anchor="ra")
        d.text((600, y), _es(pop * pp / 1e6, 1) + " M", font=MO(23, 500), fill=mix(ACC, TP, pp), anchor="ra")
        if pf > 0:
            w = (x1 - 40 - 640 - 110) * x / xmax * pf
            d.rounded_rectangle((640, y + 4, 640 + w, y + 24), 5, fill=YEL if hot else (55, 64, 80))
            d.text((x1 - 40, y), _es(x * pf), font=MO(23, 700), fill=mix(YEL if hot else INK, TP, pf), anchor="ra")
V3["code"]["viz"] = v3_viz; V3["code"]["viz_h"] = 470

VIDEOS = {"v1": V1, "v3": V3, "v2": V2, "v4": V4, "v5": V5, "v6": V6, "v7": V7, "v8": V8}

if __name__ == "__main__":
    hybrid.run(VIDEOS[sys.argv[1]], sys.argv[2], sys.argv[3:])
