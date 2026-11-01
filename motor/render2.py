"""Swiss palette, Helvetica Neue helper and the App Store sample rows."""
from PIL import ImageFont
HN = "/System/Library/Fonts/HelveticaNeue.ttc"
_c = {}
def HV(size, w="bold"):
    idx = {"reg": 0, "bold": 1, "light": 7, "med": 10}[w]
    k = (size, idx)
    if k not in _c: _c[k] = ImageFont.truetype(HN, size, index=idx)
    return _c[k]
WH, BK, GR, LG, RED = (255, 255, 255), (0, 0, 0), (120, 120, 120), (225, 225, 225), (227, 6, 19)
ROWS_CSV = """Spark Educacion Lite,0.0,True,523979,4.6,39595,109.1
Prism Entretenimiento Plus,0.0,True,871,4.8,34,512.2
Mint Educacion AI,6.99,False,410981,4.0,17791,702.4
Volt Finanzas,0.0,True,110128,4.2,3781,577.6
Quartz Redes X,0.0,True,129418,3.5,3246,128.9
Vibe Educacion Plus,0.0,True,58383,5.0,4491,184.1
Prism Musica Plus,0.0,True,244215,4.6,10620,246.9
Nova Juegos Lite,0.0,True,10948,3.6,708,696.5
Glow Juegos Go,0.0,True,164400,4.4,4416,280.5
Orbit Juegos HD,0.0,True,368814,3.4,23390,433.3
Glow Viajes HD,0.0,True,94171,4.0,3980,33.1
Zen Entretenimiento 360,0.0,True,171606,3.6,3021,678.2
Mint Fotografia,0.0,True,348651,4.1,18283,306.1
Nova Juegos AI,1.99,False,11396,3.9,435,585.5""".split("\n")
def _fmt_row(r):
    a, p, g, dl, rt, nv, mb = r.split(",")
    th = lambda v: f"{int(v):,}".replace(",", ".")
    return [a, p.replace(".", ",") if p != "0.0" else "0,00", "Sí" if g == "True" else "No", th(dl),
            rt.replace(".", ","), th(nv), mb.replace(".", ",")]
TROWS = [_fmt_row(r) for r in ROWS_CSV]
