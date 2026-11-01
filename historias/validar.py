"""Comprueba guion.md + beats.json de una historia antes de pasarla a vídeo.
Uso: python3 validar.py <id>
Tipos de plano: cara · 3d · 2d · hibrido («anim», de versiones antiguas, cuenta como 2d).
Duraciones estimadas a 2,6 palabras/s + las [pausa N]; con voz.tiempos.json usa los tiempos reales."""
import json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
WPS = 2.6
# reparto objetivo del tiempo por tipo de plano: (porcentaje, tolerancia)
OBJ = {"cara": (30, 8), "3d": (40, 10), "2d": (20, 8), "hibrido": (10, 7)}


def limpia(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ% ]+", " ", s).split()


def main(id_):
    d = os.path.join(HERE, id_)
    src = re.sub(r"<!--.*?-->", "", open(os.path.join(d, "guion.md"), encoding="utf-8").read(), flags=re.S)
    lines = [l.strip() for l in src.splitlines() if l.strip() and not l.strip().startswith(("#", ">"))]
    pausas = sum(float(x) for l in lines for x in re.findall(r"\[pausa ([\d.]+)\]", l))
    words = [w for l in lines for w in re.sub(r"\[pausa [\d.]+\]", " ", l).split()]
    flat = limpia(" ".join(words))
    total = len(words) / WPS + pausas
    beats = json.load(open(os.path.join(d, "beats.json"), encoding="utf-8"))["beats"]
    voz = os.path.join(d, "voz.tiempos.json")
    real = json.load(open(voz, encoding="utf-8")) if os.path.exists(voz) else None
    problemas = []

    # posición de cada ancla (en palabras) y unicidad
    pos = []
    for b in beats:
        q = limpia(b["ancla"])
        hits = [i for i in range(len(flat)) if flat[i:i + len(q)] == q]
        if not hits: problemas.append(f"beat {b['n']}: el ancla «{b['ancla']}» no está literal en el guion"); pos.append(None); continue
        if len(hits) > 1: problemas.append(f"beat {b['n']}: el ancla «{b['ancla']}» aparece {len(hits)} veces; alárgala hasta que sea única")
        if len(q) < 2: problemas.append(f"beat {b['n']}: ancla de una sola palabra; usa 2-6 palabras")
        pos.append(hits[0])
    ok = [p for p in pos if p is not None]
    if ok != sorted(ok): problemas.append("las anclas no van en el orden del guion")

    # duración de cada beat
    if real:
        tw = [w["ini"] for w in real["palabras"]]; total = real["duracion"]
        t_at = lambda i: tw[i] if i < len(tw) else total
    else:
        t_at = lambda i: i / WPS
    filas, tiempo = [], {"cara": 0.0, "3d": 0.0, "2d": 0.0, "hibrido": 0.0}
    for k, b in enumerate(beats):
        if pos[k] is None: continue
        nxt = next((p for p in pos[k + 1:] if p is not None), None)
        a = 0.0 if k == 0 else t_at(pos[k]); e = t_at(nxt) if nxt is not None else total
        dur = e - a
        plano = "2d" if b["plano"] == "anim" else b["plano"]
        filas.append((b["n"], plano, dur, b["ancla"]))
        if plano not in tiempo: problemas.append(f"beat {b['n']}: plano «{b['plano']}» no válido (cara, 3d, 2d, hibrido)"); continue
        tiempo[plano] += dur
        limite = 8.0 if plano == "3d" else 6.5   # en 3D la cámara ya se mueve, aguanta algo más
        if dur > limite and plano != "cara": problemas.append(f"beat {b['n']}: {dur:.1f} s sin cambio de plano; divídelo o añade un cambio dentro")
    for (n1, p1, d1, _), (n2, p2, d2, _) in zip(filas, filas[1:]):
        if p1 == p2 == "cara" and d1 > 5 and d2 > 5: problemas.append(f"beats {n1}-{n2}: dos «cara» de más de 5 s seguidos")

    fuente = "voz real" if real and not real.get("provisional") else "voz provisional" if real else "estimación"
    pct = {k: 100 * v / max(total, 1) for k, v in tiempo.items()}
    print(f"{id_}: {len(words)} palabras · {pausas:g} s de pausas · {total:.0f} s ({fuente}) · {len(beats)} beats")
    print("  reparto: " + " · ".join(f"{k} {pct[k]:.0f} % (objetivo {OBJ[k][0]} %)" for k in OBJ))
    for n, p, dur, a in filas: print(f"  {n:>2} {p:<8} {dur:4.1f} s  {a}")
    if not 60 <= total <= 90: problemas.append(f"duración {total:.0f} s fuera de 60-90 s")
    for k, (obj, tol) in OBJ.items():
        if abs(pct[k] - obj) > tol: problemas.append(f"{k} al {pct[k]:.0f} % (objetivo {obj} % ± {tol})")
    print("\n".join(["PROBLEMAS:"] + ["  - " + p for p in problemas]) if problemas else "OK")
    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main(sys.argv[1])
