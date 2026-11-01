import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import pandas as pd
import hybrid
import render2

OUTDIR = os.path.dirname(HERE) + "/entrevistas/finales/"
th = lambda v: f"{int(v):,}".replace(",", ".")
dec = lambda v, n=1: f"{v:.{n}f}".replace(".", ",")

# ------------------------------------------------------------------ DISNEY
ddf = pd.read_csv("/Users/arturolorenzo/Desktop/codigo_rrss/ejercicios-instagram/data-science/disney/datasets/disney_plus.csv")
drows = []
for _, r in ddf.drop_duplicates("titulo").head(14).iterrows():
    drows.append([r.mes, r.franquicia, r.tipo, dec(r.presupuesto_m_usd), dec(r.imdb), r.region, th(r.horas_vistas)])
DISNEY = dict(
    name="disney", out=OUTDIR + "disney_entrevista_editado.mp4",
    segs=[(6.98, 9.22), (9.38, 10.11), (16.48, 19.68), (20.00, 23.07), (23.36, 26.43), (26.75, 29.28), (37.60, 42.94),
          (48.10, 51.14), (51.42, 56.29), (56.54, 58.69), (60.67, 65.70), (65.98, 68.29), (68.45, 72.74), (73.02, 75.78),
          (78.82, 81.50), (81.73, 86.43), (102.85, 107.23), (123.68, 126.37), (128.70, 133.25), (133.54, 133.79),
          (143.17, 149.47), (149.70, 151.68), (151.90, 154.14), (154.46, 157.70), (157.89, 159.42)],
    intro=dict(t0=6.98, t_tecnica=7.4, role="Data Analyst Junior", t_role=7.7, company="en Disney", t_company=9.59,
               info=[("Dataset", "disney_plus.csv · 2.592 filas"), ("Formato", "5 pasos · 60 segundos")]),
    data=dict(t0=16.48, file="disney_plus.csv", count=2592, count_label=" registros · 27 títulos", t_rows=17.65, hl_start=23.87,
              cols=[("Mes", 40, "l", None), ("Franquicia", 165, "l", 23.87), ("Tipo", 410, "l", 25.45), ("Presup. M$", 640, "r", 27.58),
                    ("IMDb", 725, "r", None), ("Región", 755, "l", None), ("Horas vistas", 1040, "r", None)],
              rows=drows, footer_l="… 2.578 filas más", footer_r="10 columnas"),
    question=dict(t0=37.60, size=120, step=126,
                  rows=[("¿Qué franquicia", 38.21), ("lidera las", 39.05), ("horas vistas", 39.91), ("y qué % tiene", 40.93), ("del total?", 41.99)],
                  underlines=[(2, "horas vistas", 40.2), (3, "%", 41.2)]),
    code=dict(t0=48.10, sub="pandas · groupby + sum", file="disney_analysis.ipynb", status_r="n=2592 · disney_plus.csv",
              steps=["csv", "total", "groupby", "sort", "tabla", "print"],
              lines="""import pandas as pd

df = pd.read_csv(
  '../datasets/disney_plus.csv'
)

total = df['horas_vistas'].sum()

r = (
  df
  .groupby('franquicia')
  ['horas_vistas']
  .sum()
  .sort_values(ascending=False)
)

tabla = pd.DataFrame({
  'horas_M': (r / 1e6).round(1),
  '%': (r / total * 100).round(1),
})

print('Horas por franquicia:')
print(tabla)""".split("\n"),
              rev={0: 48.1, 2: 48.5, 3: 48.75, 4: 49.1, 6: 52.43, 8: 60.9, 9: 61.2, 10: 61.98, 11: 69.96, 12: 71.92, 13: 78.9,
                   14: 82.3, 16: 103.06, 17: 105.78, 18: 123.81, 19: 124.3, 21: 128.7, 22: 129.0},
              hl=[(48.07, 0, 4, 0), (51.39, 6, 6, 1), (60.64, 8, 10, 2), (68.42, 11, 12, 2), (78.79, 13, 14, 3), (102.82, 16, 19, 4), (128.67, 21, 22, 5)],
              notes={3: (48.85, "← lee el CSV"), 6: (57.49, "← para calcular el %"), 10: (63.0, "← un grupo por franquicia"),
                     12: (71.92, "← suma de horas"), 13: (82.26, "← de mayor a menor"), 17: (106.56, "← en millones"), 18: (124.6, "← % del total")}),
    result=dict(t0=129.6, file="disney_analysis.ipynb", status_r="n=2592 · disney_plus.csv", title="Horas por franquicia:",
                header=[("franquicia", 36, "l"), ("horas_M", 620, "r"), ("%", 760, "r")], fs=26, rh=50,
                rows=[["Marvel", "7554.9", "38.7"], ["Star Wars", "3268.8", "16.7"], ["Pixar", "2841.2", "14.5"],
                      ["Star / General", "2061.5", "10.6"], ["Disney Classics", "1961.1", "10.0"], ["National Geographic", "1841.8", "9.4"]],
                vals=[[0, 7554.9, 38.7], [0, 3268.8, 16.7], [0, 2841.2, 14.5], [0, 2061.5, 10.6], [0, 1961.1, 10.0], [0, 1841.8, 9.4]],
                bar_col=2, bar_x=800, bar_w=230, hot_row=0, t_hot=133.51, cells=[(0, 1, 143.44), (0, 2, 147.94)], t_bars=130.3,
                note=(143.44, "INSIGHT", ["Marvel: 2,3 veces más horas que Star Wars", "casi 4 de cada 10 horas vistas"])),
    concl=dict(t0=149.67, big="38,7", big_unit="%", lines=["de todas las horas vistas en Disney+", "son de Marvel."],
               thead=[("Franquicia", 40, "l"), ("Horas (M)", 760, "r"), ("%", 1040, "r")],
               trows=[["Marvel", "7.554,9", "38,7 %"], ["Star Wars", "3.268,8", "16,7 %"], ["Pixar", "2.841,2", "14,5 %"]],
               note=("Marvel suma más que Star Wars y Pixar juntas.", "Fuente: disney_plus.csv · 2.592 registros")),
    cta=dict(t0=155.35, sub="Más casos prácticos de datos", rows=[("¿Quieres más", 0.05), ("análisis de", 0.2), ("datos?", 0.35)],
             t_link=155.69, t_es=157.13, t_free=158.0),
)

# ------------------------------------------------------------------ APPLE 2
APPLE2 = dict(
    name="apple_2", out=OUTDIR + "apple_comision_entrevista_editado.mp4",
    segs=[(10.91, 14.05), (16.93, 21.31), (29.44, 32.32), (35.36, 38.85), (41.86, 47.04), (56.86, 60.45), (60.61, 61.22), (61.44, 63.97),
          (95.49, 101.73), (102.11, 106.46), (107.84, 109.50), (111.58, 119.30), (119.65, 122.62), (122.94, 126.08), (132.22, 138.30),
          (138.62, 139.08, "ve"), (163.10, 165.95), (166.14, 166.53), (166.72, 167.55, "ve"), (169.60, 171.01, "vs"),
          (171.33, 176.06), (178.85, 180.99), (181.34, 185.06), (185.22, 185.66), (185.82, 189.02), (189.38, 190.11), (196.42, 201.82)],
    intro=dict(t0=10.91, t_tecnica=11.26, role="Data Engineer Junior", t_role=11.78, company="en Apple", t_company=13.62, logo=(875, 690, 200, 12.76),
               info=[("Dataset", "app_store_apps.csv · 1.200 apps"), ("Formato", "5 pasos · 60 segundos")]),
    data=dict(t0=16.93, logo=True, file="app_store_apps.csv", count=1200, count_label=" apps · App Store", t_rows=17.44, hl_start=29.83,
              cols=[("App", 40, "l", None), ("Precio $", 420, "r", 29.83), ("Gratis", 510, "r", 31.27), ("Descargas", 660, "r", 35.61),
                    ("Rating", 760, "r", 36.35), ("Valoraciones", 920, "r", 37.59), ("MB", 1040, "r", None)],
              rows=render2.TROWS, footer_l="… 1.186 filas más", footer_r="10 columnas"),
    question=dict(t0=41.86, size=116, step=124,
                  rows=[("Consigue el", 42.49), ("top 10 de apps", 43.37), ("con las que", 44.75), ("Apple gana", 45.35), ("más dinero.", 46.31)],
                  underlines=[(1, "top 10", 43.6), (4, "más dinero", 46.5)]),
    code=dict(t0=56.86, sub="pandas · filtrar + nlargest", file="apple_analysis.ipynb", status_r="n=1200 · app_store_apps.csv",
              steps=["csv", "pago", "bruto", "30%", "top10", "1e6", "print"],
              lines="""import pandas as pd

df = pd.read_csv(
  '../datasets/app_store_apps.csv'
)

pago = df[~df['es_gratis']].copy()

pago['ingreso_bruto'] = (
  pago['precio_usd']
  * pago['descargas']
)

# Comisión Apple 30%
pago['corte_apple'] = (
  pago['ingreso_bruto'] * 0.30
)

top = (
  pago
  .nlargest(10, 'ingreso_bruto')
  [['app', 'categoria',
    'precio_usd', 'corte_apple']]
)

top['corte_apple'] = (
  (top['corte_apple'] / 1e6).round(2)
)

print('Top 10 (corte Apple en M USD):')
print(top.to_string(index=False))""".split("\n"),
              rev={0: 56.9, 2: 57.2, 3: 57.5, 4: 57.8, 6: 60.58, 8: 96.8, 9: 102.22, 10: 104.62, 11: 105.9, 13: 116.83, 14: 113.79,
                   15: 123.53, 16: 124.0, 18: 133.11, 19: 133.4, 20: 133.47, 21: 135.35, 22: 135.6, 23: 135.9, 25: 163.2, 26: 163.71,
                   27: 164.3, 29: 179.32, 30: 179.6},
              hl=[(56.83, 0, 4, 0), (59.23, 6, 6, 1), (95.46, 8, 11, 2), (111.55, 13, 16, 3), (132.19, 18, 23, 4), (163.05, 25, 27, 5), (178.82, 29, 30, 6)],
              notes={6: (62.2, "← ~ = no gratis"), 10: (104.62, "← precio × descargas"), 15: (124.91, "← 30 % para Apple"),
                     20: (135.35, "← las 10 que más ingresan"), 26: (166.7, "← 1e6 = 1.000.000")}),
    result=dict(t0=180.5, file="apple_analysis.ipynb", status_r="n=1200 · app_store_apps.csv", title="Top 10 (corte Apple en M USD):",
                header=[("app", 36, "l"), ("categoria", 420, "l"), ("precio", 745, "r"), ("corte", 860, "r")], fs=23, rh=44,
                rows=[["Pulse Productividad Pro", "Productividad", "6.99", "14.81"], ["Vibe Juegos Lite", "Juegos", "4.99", "13.66"],
                      ["Prism Productividad Plus", "Productividad", "9.99", "7.14"], ["Drift Finanzas Lite", "Finanzas", "6.99", "5.74"],
                      ["Quartz Educacion Lite", "Educacion", "19.99", "5.12"], ["Quartz Juegos Pro", "Juegos", "14.99", "4.24"],
                      ["Volt Juegos 360", "Juegos", "14.99", "4.14"], ["Nova Juegos HD", "Juegos", "4.99", "2.60"],
                      ["Flow Juegos 360", "Juegos", "4.99", "2.56"], ["Glow Salud HD", "Salud y Fitness", "19.99", "2.33"]],
                vals=[[0, v] for v in (14.81, 13.66, 7.14, 5.74, 5.12, 4.24, 4.14, 2.60, 2.56, 2.33)],
                bar_col=1, bar_x=880, bar_w=165, hot_row=0, t_hot=183.67, cells=[(0, 3, 186.41)], t_bars=181.0,
                note=None),
    concl=dict(t0=185.79, big="14,81", big_unit="M$", lines=["se lleva Apple solo con", "Pulse Productividad Pro."],
               thead=[("App", 40, "l"), ("Precio", 780, "r"), ("Corte Apple", 1040, "r")],
               trows=[["Pulse Productividad Pro", "6,99 $", "14,81 M$"], ["Vibe Juegos Lite", "4,99 $", "13,66 M$"],
                      ["Prism Productividad Plus", "9,99 $", "7,14 M$"]],
               note=("Precio bajo + muchas descargas = más comisión.", "Comisión del 30 % sobre el ingreso bruto.")),
    cta=dict(t0=198.15, sub="Más casos prácticos de datos", rows=[("¿Quieres más", 0.05), ("ingeniería", 0.2), ("de datos?", 0.35)],
             t_link=198.41, t_es=201.13, t_free=199.67),
)


# ------------------------------------------------------------------ DISNEY: animated illustration under the code
import math as _m
from PIL import Image as _Img, ImageDraw as _Draw
from render import eo as _eo, pr as _pr, mix as _mix
from stylef import MO as _MO
_FR = ["Marvel", "Star Wars", "Pixar", "Star / General", "Disney Classics", "National Geographic"]          # sorted by hours
_SHORT = {"Marvel": "Marvel", "Star Wars": "Star Wars", "Pixar": "Pixar", "Star / General": "Star",
          "Disney Classics": "Classics", "National Geographic": "Nat Geo"}
_COL = {"Marvel": (226, 54, 54), "Star Wars": (255, 214, 64), "Pixar": (61, 165, 217), "Star / General": (155, 93, 229),
        "Disney Classics": (241, 91, 181), "National Geographic": (244, 162, 97)}
_titles = ddf.drop_duplicates("titulo")[["titulo", "franquicia"]].values.tolist()          # 27 tokens, 1 per title (96 rows)
_hours = ddf.groupby("franquicia")["horas_vistas"].sum()
_total = ddf["horas_vistas"].sum()
_ALPHA = sorted(_FR)                                                                       # groupby default order
T_GRID, T_TOTAL, T_GROUP, T_SUM, T_SORT, T_MILL, T_PCT = 48.6, 52.43, 61.98, 71.92, 82.26, 105.78, 123.81
_TB, _TP, _INK, _MUT, _ACC = (10, 12, 15), (15, 18, 22), (220, 226, 234), (110, 120, 135), (88, 166, 255)

def disney_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=_TP); d.line((x0, y0, x1, y0), fill=(34, 39, 48), width=2)
    if t < T_GRID - 0.3: return
    d.text((36, y0 + 18), "# lo que hace el código", font=_MO(19, 500), fill=_MUT)
    base = y1 - 70; colw = (x1 - x0 - 80) / 6
    def colx(name, t):
        ia, isorted = _ALPHA.index(name), _FR.index(name)
        ps = _eo(_pr(t, T_SORT, 1.0))
        i = ia + (isorted - ia) * ps
        return x0 + 40 + colw * (i + 0.5)
    pg = t >= T_GROUP
    tw, th_ = 64, 26
    psum = _eo(_pr(t, T_SUM, 0.8))
    # bars (after .sum())
    hmax = _hours.max()
    if psum > 0:
        for name in _FR:
            cx = colx(name, t); h = (base - y0 - 110) * _hours[name] / hmax * psum
            d.rounded_rectangle((cx - 46, base - h, cx + 46, base), 6, fill=_COL[name])
            lab = f"{_hours[name] / 1e6:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".") if t >= T_MILL else f"{int(_hours[name] / 1e6):,} M".replace(",", ".")
            if t >= T_MILL: lab += " M"
            d.text((cx, base - h - 10), lab, font=_MO(18, 600), fill=_mix(_INK, _TP, psum), anchor="mb")
            pp = _eo(_pr(t, T_PCT, 0.4))
            if pp > 0:
                pct = f"{_hours[name] / _total * 100:.1f} %".replace(".", ",")
                d.text((cx, base - h - 34), pct, font=_MO(20, 700), fill=_mix(_ACC, _TP, pp), anchor="mb")
    # tokens: grid -> buckets -> fade into bars
    if psum < 1:
        stack = {f: 0 for f in _FR}
        for k, (tit, fr) in enumerate(_titles):
            pa = _eo(_pr(t, T_GRID + k * 0.035, 0.3))
            if pa <= 0: continue
            gx = x0 + 70 + (k % 9) * 104; gy = y0 + 80 + (k // 9) * 44
            j = stack[fr]; stack[fr] += 1
            bx = colx(fr, t) - tw / 2; by = base - (j + 1) * (th_ + 6)
            pmv = _eo(_pr(t, T_GROUP + _FR.index(fr) * 0.18, 0.9))
            x = gx + (bx - gx) * pmv; y = gy + (by - gy) * pmv
            a = pa * (1 - psum)
            d.rounded_rectangle((x, y, x + tw, y + th_), 6, fill=_mix(_COL[fr], _TP, a))
    # total counter
    pt = _pr(t, T_TOTAL, 1.4)
    if pt > 0 and t < T_GROUP:
        v = _total * _eo(pt) / 1e6
        d.text((x1 - 36, y0 + 18), f"total = {v:,.0f} M horas".replace(",", "."), font=_MO(22, 700), fill=_ACC, anchor="ra")
    # bucket labels
    pl = _eo(_pr(t, T_GROUP + 0.4, 0.4))
    if pl > 0:
        for name in _FR:
            d.text((colx(name, t), base + 16), _SHORT[name], font=_MO(18, 600), fill=_mix(_COL[name], _TP, pl), anchor="ma")
    # caption of current step
    cap = None
    if T_GRID <= t < T_TOTAL: cap = "27 títulos · 1 ficha = 96 filas"
    elif T_GROUP <= t < T_SUM: cap = "groupby: un grupo por franquicia"
    elif T_SUM <= t < T_SORT: cap = ".sum(): horas totales de cada grupo"
    elif T_SORT <= t < T_MILL: cap = "sort_values: de mayor a menor"
    elif t >= T_MILL: cap = "tabla: horas en millones y % del total"
    if cap: d.text((x1 - 36, y0 + 18), cap, font=_MO(19, 500), fill=_INK, anchor="ra")

DISNEY["code"]["viz"] = disney_viz
DISNEY["code"]["viz_h"] = 470


# ------------------------------------------------------------------ APPLE 2: animated illustration under the code
_adf = pd.read_csv("/Users/arturolorenzo/Desktop/codigo_rrss/ejercicios-instagram/data-science/apple/datasets/app_store_apps.csv")
_pago = _adf[~_adf["es_gratis"]].copy()
_pago["ingreso_bruto"] = _pago["precio_usd"] * _pago["descargas"]
_pago["corte_apple"] = _pago["ingreso_bruto"] * 0.30
_atop = _pago.nlargest(10, "ingreso_bruto")
_ex = _atop.iloc[0]
A_GRID, A_FILT, A_BRUTO, A_PRECIO, A_DESC, A_EQ, A_CORTE, A_30, A_X03, A_TOP, A_NORM, A_1E6 = \
    57.5, 60.58, 100.32, 102.22, 104.62, 105.9, 113.79, 118.39, 124.9, 133.11, 163.71, 166.7
_GREEN, _GREY = (86, 211, 140), (60, 66, 78)
_money = lambda v: f"{int(round(v)):,}".replace(",", ".") + " $"

def apple_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=_TP); d.line((x0, y0, x1, y0), fill=(34, 39, 48), width=2)
    if t < A_GRID - 0.3: return
    d.text((36, y0 + 18), "# lo que hace el código", font=_MO(19, 500), fill=_MUT)
    cap = None
    # --- phase A/B: 60 tokens (1 = 20 apps), 15 of pago (297/1200 ~ 25 %)
    out_tok = _eo(_pr(t, A_BRUTO - 0.2, 0.4))
    if t < A_BRUTO + 0.3:
        pf = _eo(_pr(t, A_FILT, 0.8))
        paid_i = 0
        for k in range(60):
            pa = _eo(_pr(t, A_GRID + k * 0.02, 0.3)) * (1 - out_tok)
            if pa <= 0: continue
            paid = k % 4 == 1
            gx = x0 + 75 + (k % 15) * 62; gy = y0 + 80 + (k // 15) * 40
            if paid:
                tx_, ty_ = x0 + 75 + paid_i * 62, y0 + 170; paid_i += 1
                x = gx + (tx_ - gx) * pf; y = gy + (ty_ - gy) * pf
                d.rounded_rectangle((x, y, x + 52, y + 24), 6, fill=_mix(_ACC, _TP, pa))
            else:
                a = pa * (1 - pf)
                if a > 0.02: d.rounded_rectangle((gx, gy, gx + 52, gy + 24), 6, fill=_mix(_mix(_GREY, _GREEN, pf), _TP, a))
        if t < A_FILT: cap = "1.200 apps · 1 ficha = 20 apps"
        else:
            cap = "~es_gratis: nos quedamos con las de pago"
            pc = _eo(_pr(t, A_FILT + 0.6, 0.4))
            d.text((x0 + 75, y0 + 230), f"{len(_pago)} apps de pago", font=_MO(26, 700), fill=_mix(_ACC, _TP, pc * (1 - out_tok)))
    # --- phase C/D: worked example with the top app
    if A_BRUTO <= t < A_TOP:
        po = 1 - _eo(_pr(t, A_TOP - 0.35, 0.3))
        pc = _eo(_pr(t, A_BRUTO, 0.4)) * po
        d.text((60, y0 + 70), "Ejemplo: " + _ex["app"], font=_MO(22, 700), fill=_mix(_INK, _TP, pc))
        items = [(f"{_ex['precio_usd']:.2f} $".replace(".", ","), "precio", A_PRECIO), ("×", None, A_DESC - 0.1),
                 (f"{int(_ex['descargas']):,}".replace(",", "."), "descargas", A_DESC)]
        x = 60
        for txt, lab, tt in items:
            pi = _eo(_pr(t, tt, 0.35)) * po
            f = _MO(30, 700); w = f.getlength(txt)
            if lab:
                d.rounded_rectangle((x - 12, y0 + 112, x + w + 12, y0 + 160), 10, outline=_mix(_ACC, _TP, pi), width=2)
                d.text((x, y0 + 166), lab, font=_MO(16, 500), fill=_mix(_MUT, _TP, pi))
            d.text((x, y0 + 118), txt, font=f, fill=_mix(_INK if lab else _MUT, _TP, pi)); x += w + 40
        pe = _eo(_pr(t, A_EQ, 0.35)) * po
        d.text((60, y0 + 200), "= " + _money(_ex["ingreso_bruto"]), font=_MO(30, 700), fill=_mix(_GREEN, _TP, pe))
        d.text((60 + _MO(30, 700).getlength("= " + _money(_ex["ingreso_bruto"])) + 20, y0 + 210), "ingreso bruto", font=_MO(18, 500), fill=_mix(_MUT, _TP, pe))
        cap = "ingreso_bruto = precio × descargas"
        if t >= A_CORTE:
            pb = _eo(_pr(t, A_CORTE, 0.5)) * po; ps = _eo(_pr(t, A_30, 0.6))
            bx0, bx1, by = 60, x1 - 60, y0 + 270
            d.rounded_rectangle((bx0, by, bx0 + (bx1 - bx0) * pb, by + 44), 8, fill=_mix(_GREY, _TP, pb))
            if ps > 0:
                d.rounded_rectangle((bx0, by, bx0 + (bx1 - bx0) * 0.30 * ps, by + 44), 8, fill=_mix(_ACC, _TP, po))
                d.text((bx0, by + 58), "Apple 30 %", font=_MO(18, 700), fill=_mix(_ACC, _TP, ps * po))
                d.text((bx0, by + 82), _money(_ex["corte_apple"]), font=_MO(22, 700), fill=_mix(_INK, _TP, ps * po))
                d.text((bx1, by + 58), "desarrollador 70 %", font=_MO(18, 600), fill=_mix(_MUT, _TP, ps * po), anchor="ra")
                d.text((bx1, by + 82), _money(_ex["ingreso_bruto"] * 0.7), font=_MO(22, 600), fill=_mix(_MUT, _TP, ps * po), anchor="ra")
            cap = "corte_apple = ingreso_bruto × 0,30"
    # --- phase E/F: top 10 ranking, then values to millions
    if t >= A_TOP:
        vmax = _atop["corte_apple"].max(); pn = _eo(_pr(t, A_1E6, 0.5)); phl = _eo(_pr(t, A_NORM, 0.3))
        if phl > 0:
            d.rounded_rectangle((870, y0 + 56, x1 - 30, y0 + 64 + 10 * 37), 8, outline=_mix(_ACC, _TP, phl * (1 - pn * 0.6)), width=2)
        for i, (_, r) in enumerate(_atop.iterrows()):
            pi = _eo(_pr(t, A_TOP + 0.3 + i * 0.08, 0.35))
            if pi <= 0: continue
            y = y0 + 64 + i * 37
            hot = i == 0
            d.text((50, y + 4), f"{i + 1:>2}", font=_MO(17, 600), fill=_mix(_MUT, _TP, pi))
            d.text((88, y + 4), r["app"], font=_MO(17, 600 if hot else 400), fill=_mix(_INK, _TP, pi))
            w = (840 - 360) * r["corte_apple"] / vmax * pi
            d.rounded_rectangle((360, y + 6, 360 + w, y + 26), 5, fill=_ACC if hot else (55, 64, 80))
            raw, mil = _money(r["corte_apple"]), f"{r['corte_apple'] / 1e6:.2f} M".replace(".", ",")
            if pn < 1: d.text((x1 - 40, y + 4), raw, font=_MO(17, 600), fill=_mix(_INK, _TP, pi * (1 - pn)), anchor="ra")
            if pn > 0: d.text((x1 - 40, y + 4), mil, font=_MO(19, 700), fill=_mix(_ACC if hot else _INK, _TP, pi * pn), anchor="ra")
        cap = "nlargest(10): las 10 que más ingresan" if t < A_NORM else ("÷ 1e6 → en millones" if t >= A_1E6 else "normalizamos: números muy largos")
    if cap: d.text((x1 - 36, y0 + 18), cap, font=_MO(19, 500), fill=_INK, anchor="ra")

APPLE2["code"]["viz"] = apple_viz
APPLE2["code"]["viz_h"] = 470


# ------------------------------------------------------------------ dynamism: job card, emphasis zoom, live dataset
APPLE2["intro"]["job"] = dict(t_in=11.4, t_apply=12.95, tile_logo=True, tile_bg=(242, 242, 242),
                              title="Data Engineer Junior", company="Apple · Cupertino, California", meta="Jornada completa · Híbrido")
APPLE2["emph"] = [(42.4, 46.95), (183.6, 190.0)]
_apool = []
for _, r in _adf.iloc[14:44].iterrows():
    _apool.append([r.app, (f"{r.precio_usd:.2f}".replace(".", ",") if r.precio_usd else "0,00"), "Sí" if r.es_gratis else "No",
                   th(r.descargas), dec(r.rating), th(r.num_valoraciones), dec(r.tamano_mb)])
APPLE2["data"]["pool"] = _apool

DISNEY["intro"]["job"] = dict(t_in=7.3, t_apply=8.75, tile_text="D+", tile_bg=(16, 36, 98),
                              title="Data Analyst Junior", company="Disney · Burbank, California", meta="Jornada completa · Híbrido")
DISNEY["emph"] = [(38.1, 42.9), (143.1, 148.6)]
_dpool = []
for _, r in ddf.sample(30, random_state=7).iterrows():
    _dpool.append([r.mes, r.franquicia, r.tipo, dec(r.presupuesto_m_usd), dec(r.imdb), r.region, th(r.horas_vistas)])
DISNEY["data"]["pool"] = _dpool


# ------------------------------------------------------------------ APPLE 1 (apps gratis vs pago)
APPLE1 = dict(
    name="apple_1", src=os.path.dirname(HERE) + "/entrevistas/brutos/2026-10-04 15-40-48.mp4",
    out=OUTDIR + "apple_gratis_vs_pago_editado.mp4",
    segs=[(3.42, 6.43), (15.17, 22.62), (24.80, 30.72, "ve"), (37.82, 42.21), (42.78, 43.49), (49.76, 53.63), (53.95, 55.36),
          (55.55, 60.48), (60.74, 61.82, "ve"), (64.00, 66.58, "ve"), (85.25, 88.10), (88.26, 90.94), (104.99, 109.34), (132.93, 135.74),
          (140.38, 145.54), (145.70, 149.41), (149.60, 153.70), (153.95, 158.98), (167.52, 169.97), (173.79, 179.01)],
    intro=dict(t0=3.42, t_tecnica=3.78, role="Data Analyst Junior", t_role=4.32, company="en Apple", t_company=5.95,
               logo=(875, 690, 200, 4.95), info=[("Dataset", "app_store_apps.csv · 1.200 apps"), ("Formato", "5 pasos · 60 segundos")],
               job=dict(t_in=3.75, t_apply=5.6, tile_logo=True, tile_bg=(242, 242, 242), title="Data Analyst Junior",
                        company="Apple · Cupertino, California", meta="Jornada completa · Híbrido")),
    data=dict(t0=15.17, logo=True, file="app_store_apps.csv", count=1200, count_label=" apps · App Store", t_rows=16.0, hl_start=25.66,
              cols=[("App", 40, "l", None), ("Precio $", 420, "r", None), ("Gratis", 510, "r", None), ("Descargas", 660, "r", 25.66),
                    ("Rating", 760, "r", 27.10), ("Valoraciones", 920, "r", 28.34), ("MB", 1040, "r", 29.16)],
              rows=render2.TROWS, pool=_apool, footer_l="… 1.186 filas más", footer_r="10 columnas"),
    question=dict(t0=37.82, size=120, step=126,
                  rows=[("¿Las apps", 38.46), ("gratis se", 38.9), ("descargan", 39.62), ("mucho más que", 40.22), ("las de pago?", 41.38)],
                  underlines=[(1, "gratis", 38.95), (4, "pago", 41.74)]),
    code=dict(t0=49.76, sub="pandas · groupby + agg", file="apple_analysis.ipynb", status_r="n=1200 · app_store_apps.csv",
              steps=["csv", "groupby", "agg", "ratio", "print"],
              lines="""import pandas as pd

df = pd.read_csv(
  '../datasets/app_store_apps.csv'
)

r = (
  df
  .groupby('es_gratis')
  .agg(
    descargas_med=('descargas',
                   'median'),
    rating_med=('rating', 'median'),
    apps=('app', 'count'),
  )
  .round(1)
)

ratio = (
  r.loc[True, 'descargas_med']
  / r.loc[False, 'descargas_med']
)

print(r)
print(f'\\nLas gratis x{ratio:.1f} descargas')""".split("\n"),
              rev={0: 50.1, 2: 50.4, 3: 50.8, 4: 51.2, 6: 54.4, 7: 54.7, 8: 56.26, 9: 64.94, 14: 65.1, 15: 65.3, 16: 65.5,
                   10: 86.16, 11: 86.4, 12: 87.56, 13: 88.56, 18: 105.06, 19: 105.4, 20: 106.0, 21: 106.5, 23: 134.48, 24: 134.8},
              hl=[(49.76, 0, 4, 0), (54.02, 6, 8, 1), (64.0, 9, 16, 2), (85.25, 10, 11, 2), (86.56, 12, 12, 2), (88.42, 13, 13, 2),
                  (104.99, 18, 21, 3), (132.93, 23, 24, 4)],
              notes={3: (51.1, "← lee el CSV"), 8: (58.5, "← 2 grupos: True | False"), 10: (86.0, "← mediana"),
                     12: (87.56, "← mediana"), 13: (89.0, "← nº de apps"), 19: (106.8, "← gratis ÷ pago")}),
    result=dict(t0=140.38, file="apple_analysis.ipynb", status_r="n=1200 · app_store_apps.csv", title="Out[1]: print(r)",
                header=[("es_gratis", 36, "l"), ("descargas_med", 500, "r"), ("rating_med", 700, "r"), ("apps", 820, "r")], fs=26, rh=54,
                rows=[["False", "34014.0", "4.1", "297"], ["True", "93607.0", "4.2", "903"]],
                vals=[[0, 34014.0], [0, 93607.0]], bar_col=1, bar_x=860, bar_w=180, hot_row=1, t_hot=140.94,
                cells=[(1, 1, 141.0), (0, 1, 145.8), (1, 3, 150.46), (0, 3, 152.16)], t_bars=141.0,
                extra=(140.6, "Las gratis x2.8 descargas", 168.5),
                note=(153.46, "OJO: SESGO", ["903 apps gratis vs 297 de pago (3:1)", "el ratio x2.8 hay que leerlo con cautela"])),
    concl=dict(t0=167.47, big="×2,8", big_size=240, lines=["más descargas (mediana) tienen las", "apps gratis que las de pago."],
               thead=[("Grupo", 40, "l"), ("Descargas (p50)", 760, "r"), ("Apps", 1040, "r")],
               trows=[["Gratis", "93.607", "903"], ["De pago", "34.014", "297"]],
               note=("Ojo: hay 3 apps gratis por cada una de pago.", "El ratio hay que leerlo con cautela.")),
    cta=dict(t0=175.58, sub="Más casos prácticos de datos", rows=[("¿Quieres más", 0.05), ("análisis de", 0.2), ("datos?", 0.35)],
             t_link=175.24, t_es=176.62, t_free=177.32),
    emph=[(38.4, 42.2), (167.5, 169.97)],
)

B_GRID, B_GROUP, B_AGG, B_D, B_R, B_N, B_RATIO, B_EQ = 50.6, 56.26, 64.94, 86.16, 87.56, 88.56, 105.06, 107.36
def apple1_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=_TP); d.line((x0, y0, x1, y0), fill=(34, 39, 48), width=2)
    if t < B_GRID - 0.3: return
    d.text((36, y0 + 18), "# lo que hace el código", font=_MO(19, 500), fill=_MUT)
    cap = None
    out_tok = _eo(_pr(t, B_AGG, 0.4))
    cxs = {True: x0 + 290, False: x0 + 790}
    if t < B_AGG + 0.5:
        pg = _eo(_pr(t, B_GROUP, 1.0)); cnt = {True: 0, False: 0}
        for k in range(60):
            pa = _eo(_pr(t, B_GRID + k * 0.02, 0.3)) * (1 - out_tok)
            if pa <= 0: continue
            free = k % 4 != 1
            gx = x0 + 75 + (k % 15) * 62; gy = y0 + 80 + (k // 15) * 40
            j = cnt[free]; cnt[free] += 1; cols = 9 if free else 5
            bx = cxs[free] - cols * 54 / 2 + (j % cols) * 54; by = y0 + 110 + (j // cols) * 34
            x = gx + (bx - gx) * pg; y = gy + (by - gy) * pg
            d.rounded_rectangle((x, y, x + 46, y + 22), 6, fill=_mix(_GREEN if free else _ACC, _TP, pa))
        pl = _eo(_pr(t, B_GROUP + 0.5, 0.4)) * (1 - out_tok)
        if pl > 0:
            d.text((cxs[True], y0 + 330), "True · gratis (903)", font=_MO(22, 700), fill=_mix(_GREEN, _TP, pl), anchor="ma")
            d.text((cxs[False], y0 + 330), "False · pago (297)", font=_MO(22, 700), fill=_mix(_ACC, _TP, pl), anchor="ma")
        cap = "1.200 apps · 1 ficha = 20 apps" if t < B_GROUP else "groupby('es_gratis'): 2 grupos"
    if t >= B_AGG:
        pt = _eo(_pr(t, B_AGG + 0.2, 0.4))
        d.text((560, y0 + 70), "gratis", font=_MO(22, 700), fill=_mix(_GREEN, _TP, pt), anchor="ra")
        d.text((x1 - 60, y0 + 70), "pago", font=_MO(22, 700), fill=_mix(_ACC, _TP, pt), anchor="ra")
        rows = [("mediana descargas", "93.607", "34.014", 93607, 34014, B_D), ("mediana rating", "4,2", "4,1", 4.2, 4.1, B_R),
                ("nº de apps", "903", "297", 903, 297, B_N)]
        for k, (lab, a, b, va, vb, tt) in enumerate(rows):
            pr_ = _eo(_pr(t, tt, 0.35))
            if pr_ <= 0: continue
            y = y0 + 120 + k * 62
            d.text((60, y), lab, font=_MO(21, 500), fill=_mix(_INK, _TP, pr_))
            d.text((560, y), a, font=_MO(24, 700), fill=_mix(_INK, _TP, pr_), anchor="ra")
            d.text((x1 - 60, y), b, font=_MO(24, 700), fill=_mix(_INK, _TP, pr_), anchor="ra")
            m = max(va, vb)
            d.rounded_rectangle((600, y + 6, 600 + 150 * va / m * pr_, y + 14), 3, fill=_GREEN)
            d.rounded_rectangle((600, y + 18, 600 + 150 * vb / m * pr_, y + 26), 3, fill=_ACC)
        cap = ".agg(): 3 métricas por grupo"
        if t >= B_RATIO:
            pe = _eo(_pr(t, B_RATIO, 0.4)); y = y0 + 330
            d.text((60, y), "ratio = 93.607 / 34.014", font=_MO(26, 600), fill=_mix(_INK, _TP, pe))
            pq = _eo(_pr(t, B_EQ, 0.4))
            d.text((x1 - 60, y - 6), "= ×2,75 → x2.8", font=_MO(32, 700), fill=_mix((255, 214, 64), _TP, pq), anchor="ra")
            cap = "ratio: cuántas veces más se descargan"
    if cap: d.text((x1 - 36, y0 + 18), cap, font=_MO(19, 500), fill=_INK, anchor="ra")

APPLE1["code"]["viz"] = apple1_viz
APPLE1["code"]["viz_h"] = 470


# ------------------------------------------------------------------ AIRBNB MADRID 1 (+1 año sin actividad) — re-edit of an old-format video
import json as _json
_bdf = pd.read_csv("/Users/arturolorenzo/Desktop/codigo_rrss/ejercicios-instagram/data-science/airbnb/datasets/airbnb_madrid.csv")
_bdf["last_review"] = pd.to_datetime(_bdf["last_review"])
_HOY = pd.Timestamp("2026-07-21")                       # recording day: reproduces the 3,434 / 18.0 % shown on screen
_bact = _bdf[_bdf["last_review"].notna()]
_bold = _bact[(_HOY - _bact["last_review"]).dt.days > 365]
def _brow(r):
    lr = r.last_review.strftime("%Y-%m-%d") if pd.notna(r.last_review) else "—"
    return [r.neighbourhood_group, r.neighbourhood[:18], r.room_type.replace("Entire home/apt", "Piso entero").replace("Private room", "Habitación").replace("Shared room", "Compartida").replace("Hotel room", "Hotel"),
            f"{int(r.price)}" if pd.notna(r.price) else "—", th(r.number_of_reviews), lr]
_brows = [_brow(r) for _, r in _bdf.head(14).iterrows()]
_bpool = [_brow(r) for _, r in _bdf.sample(30, random_state=5).iterrows()]
_bsp = _json.load(open(os.path.join(HERE, "airbnb_madrid_1.json")))["speech"]
_ex = _bact[_bact["last_review"].dt.year.isin([2022, 2024, 2026])].groupby(_bact["last_review"].dt.year).head(1).sort_values("last_review").head(3)

AIRBNB1 = dict(
    name="airbnb_madrid_1", out=OUTDIR + "airbnb_madrid_1_editado.mp4",
    segs=[(a, b) for a, b in _bsp],
    intro=dict(t0=0.0, t_tecnica=0.48, role="Data Analyst Junior", t_role=1.84, company="40.000 € brutos al año", t_company=3.04,
               info=[("Dataset", "airbnb_madrid.csv · 22.835 alojamientos"), ("Formato", "5 pasos · 60 segundos")],
               job=dict(t_in=0.9, t_apply=3.68, tile_text="€", tile_bg=(22, 101, 52), title="Data Analyst Junior",
                        company="40.000 € brutos/año · Madrid", meta="Jornada completa · Híbrido")),
    data=dict(t0=4.68, file="airbnb_madrid.csv", count=22835, count_label=" alojamientos · Madrid", t_rows=5.3, hl_start=999, scroll_d=1.6,
              cols=[("Distrito", 40, "l", None), ("Barrio", 250, "l", None), ("Tipo", 470, "l", None), ("€/noche", 720, "r", None),
                    ("Reviews", 830, "r", None), ("Última review", 1040, "r", None)],
              rows=_brows, pool=_bpool, footer_l="… 22.821 filas más", footer_r="19 columnas"),
    question=dict(t0=8.58, size=124, step=128,
                  rows=[("¿Cuántos pisos", 9.54), ("llevan más", 10.36), ("de un año", 10.92), ("sin actividad?", 11.54)],
                  underlines=[(2, "un año", 11.2), (3, "sin actividad", 11.88)]),
    code=dict(t0=12.64, sub="pandas · fechas + filtros", file="airbnb_madrid.ipynb", status_r="n=22835 · airbnb_madrid.csv",
              steps=["csv", "fecha", "hoy", "dias", "filtro", "%", "print"],
              lines="""import pandas as pd

df = pd.read_csv(
  'airbnb_madrid.csv'
)

df['last_review'] = pd.to_datetime(
  df['last_review']
)

hoy = pd.Timestamp.today()

df['dias'] = (
  (hoy - df['last_review']).dt.days
)

activos = df[df['last_review'].notna()]
viejos = activos[activos['dias']>365]

pct = len(viejos)/len(activos)*100

print(f"{len(viejos):,} pisos")
print(f"con +1 año sin review")
print(f"({pct:.1f}% del total)")""".split("\n"),
              rev={0: 13.46, 2: 17.1, 3: 17.6, 4: 18.3, 6: 20.72, 7: 21.4, 8: 22.0, 10: 25.36, 12: 31.36, 13: 32.4, 14: 33.0,
                   16: 38.74, 17: 44.94, 19: 52.12, 21: 56.08, 22: 56.5, 23: 56.9},
              hl=[(12.64, 0, 0, 0), (16.68, 2, 4, 0), (20.52, 6, 8, 1), (24.96, 10, 10, 2), (30.60, 12, 14, 3), (38.12, 16, 16, 4),
                  (44.44, 17, 17, 4), (51.68, 19, 19, 5), (55.40, 21, 23, 6)],
              notes={3: (18.26, "← lee el CSV"), 7: (23.28, "← texto → fecha"), 10: (28.4, "← fecha de hoy"),
                     13: (35.12, "← días sin review"), 16: (43.3, "← quita nulos"), 17: (49.16, "← +1 año")}),
    result=dict(t0=58.42, file="airbnb_madrid.ipynb", status_r="n=22835 · airbnb_madrid.csv", title="Out[2]:",
                header=[("", 36, "l")], fs=34, rh=64,
                rows=[["3,434 pisos"], ["con +1 año sin review"], ["(18.0% del total)"]],
                vals=[[0, 1], [0, 1], [0, 1]], bar_col=1, bar_x=1100, bar_w=0, hot_row=0, t_hot=58.98, cells=[(2, 0, 64.32)], t_bars=999,
                note=(59.6, "CONTEXTO", ["18 % de los 19.105 pisos con alguna review", "y 3.730 anuncios no tienen ninguna"])),
    concl=dict(t0=63.16, big="18,0", big_unit="%", lines=["de los pisos con reviews lleva", "más de un año sin actividad."],
               thead=[("Alojamientos", 40, "l"), ("Nº", 1040, "r")],
               trows=[["Con alguna review", "19.105"], ["+1 año sin review", "3.434"], ["Sin ninguna review", "3.730"]],
               note=("Probablemente anuncios inactivos.", "Fuente: airbnb_madrid.csv · 22.835 alojamientos")),
    cta=dict(t0=67.30, sub="Más casos prácticos de datos", rows=[("¿Quieres más", 0.05), ("análisis de", 0.2), ("datos?", 0.35)],
             t_link=68.80, t_es=69.80, t_free=69.85, texts=("Sígueme", "y dale a me gusta.", "Hasta mañana.")),
    emph=[(9.5, 11.95), (58.9, 61.0)],
    cutaways=[(8.7, 12.6, 440), (12.6, 14.6, 330), (21.7, 24.9, 540), (24.9, 26.6, 680), (33.7, 38.1, 660), (45.1, 51.1, 1010), (58.9, 62.0, 470)],
)

C_GRID, C_CAST, C_HOY, C_DIAS, C_ACT, C_NULL, C_OLD, C_OLD2, C_PCT = 17.1, 20.72, 25.36, 31.36, 38.74, 43.3, 44.94, 49.16, 52.12
def airbnb_viz(img, d, t, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=_TP); d.line((x0, y0, x1, y0), fill=(34, 39, 48), width=2)
    if t < C_GRID - 0.3: return
    d.text((36, y0 + 18), "# lo que hace el código", font=_MO(19, 500), fill=_MUT)
    cap = None; ORANGE = (206, 145, 120); RED_ = (240, 90, 90)
    # tokens: 60 fichas, 10 sin review (16 %), of the 50 with review 9 are +1 año (18 %)
    tok_vis = 1 - _eo(_pr(t, C_CAST - 0.2, 0.3)) if t < C_ACT else _eo(_pr(t, C_ACT, 0.4))
    if tok_vis > 0.01:
        pn = _eo(_pr(t, C_NULL, 0.6)); po = _eo(_pr(t, C_OLD2, 0.6))
        k_old = 0
        for k in range(60):
            pa = _eo(_pr(t, C_GRID + k * 0.02, 0.3)) * tok_vis
            if pa <= 0: continue
            noreview = k % 6 == 0; old = (not noreview) and (k % 11 == 3 or k % 13 == 5)
            x = x0 + 75 + (k % 15) * 62; y = y0 + 80 + (k // 15) * 40
            col = (150, 156, 168)
            if noreview: col = _mix((90, 96, 108), _TP, 1 - pn); pa *= (1 - pn)
            elif old: col = _mix(RED_, col, po)
            if pa > 0.02: d.rounded_rectangle((x, y, x + 52, y + 24), 6, fill=_mix(col, _TP, pa))
        if t < C_CAST: cap = "22.835 alojamientos · 1 ficha ≈ 380"
        elif t < C_NULL: cap = "activos: solo los que tienen review"
        elif t < C_OLD2: cap = "quitamos 3.730 sin ninguna review"; d.text((x0 + 75, y0 + 260), "19.105 activos", font=_MO(26, 700), fill=_mix(_INK, _TP, pn))
        else:
            cap = "viejos: +365 días sin review"
            d.text((x0 + 75, y0 + 260), "3.434 con +1 año sin actividad", font=_MO(26, 700), fill=_mix(RED_, _TP, po))
        if t >= C_PCT:
            pp = _eo(_pr(t, C_PCT, 0.4))
            d.text((x0 + 75, y0 + 320), "pct = 3.434 / 19.105 = ", font=_MO(28, 600), fill=_mix(_INK, _TP, pp))
            d.text((x0 + 75 + _MO(28, 600).getlength("pct = 3.434 / 19.105 = "), y0 + 314), "18,0 %", font=_MO(34, 700), fill=_mix((255, 214, 64), _TP, pp))
            cap = "porcentaje sobre los activos"
    # worked example: string -> datetime -> hoy -> days
    if C_CAST <= t < C_ACT:
        pv = _eo(_pr(t, C_CAST, 0.4)) * (1 - _eo(_pr(t, C_ACT - 0.35, 0.3)))
        pdt = _eo(_pr(t, C_CAST + 1.2, 0.5)); ph = _eo(_pr(t, C_HOY, 0.4)); pdd = _eo(_pr(t, C_DIAS, 0.4))
        d.text((60, y0 + 64), "last_review", font=_MO(19, 600), fill=_mix(_MUT, _TP, pv))
        for k, (_, r) in enumerate(_ex.iterrows()):
            y = y0 + 100 + k * 64; ds = r.last_review.strftime("%Y-%m-%d")
            if pdt < 0.5:
                d.text((60, y), f"'{ds}'", font=_MO(28, 600), fill=_mix(ORANGE, _TP, pv * (1 - pdt * 2)))
            else:
                d.rounded_rectangle((52, y - 6, 52 + _MO(28, 600).getlength(ds) + 22, y + 38), 8, outline=_mix(_ACC, _TP, pv), width=2)
                d.text((63, y), ds, font=_MO(28, 600), fill=_mix(_INK, _TP, pv))
            if pdd > 0:
                days = (_HOY - r.last_review).days
                col = RED_ if days > 365 else (86, 211, 140)
                d.text((x1 - 60, y), f"{days:,} días".replace(",", "."), font=_MO(28, 700), fill=_mix(col, _TP, pv * pdd), anchor="ra")
        if ph > 0:
            d.rounded_rectangle((x1 - 330, y0 + 60, x1 - 60, y0 + 92), 16, fill=_mix(_ACC, _TP, ph * pv))
            d.text((x1 - 195, y0 + 76), "hoy = 2026-07-21", font=_MO(18, 700), fill=_mix(_TB, _TP, ph * pv), anchor="mm")
        cap = "to_datetime: texto → fecha" if t < C_HOY else ("Timestamp.today(): fecha de hoy" if t < C_DIAS else "dias = hoy − last_review")
    if cap: d.text((x1 - 36, y0 + 18), cap, font=_MO(19, 500), fill=_INK, anchor="ra")

AIRBNB1["code"]["viz"] = airbnb_viz
AIRBNB1["code"]["viz_h"] = 470

if __name__ == "__main__":
    cfg = {"disney": DISNEY, "apple_2": APPLE2, "apple_1": APPLE1, "airbnb_madrid_1": AIRBNB1}[sys.argv[1]]
    hybrid.run(cfg, sys.argv[2], sys.argv[3:])
