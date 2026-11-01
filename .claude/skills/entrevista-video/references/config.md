# Configuración de un vídeo (motor/hybrid.py)

Un vídeo es un `dict` que se pasa a `hybrid.run(cfg, modo, args)`. **Todos los tiempos son segundos del vídeo
original** (palabras de `<nombre>_pieces.json`); `Timeline` los recoloca en el montaje. Una escena dura desde su
`t0` hasta el `t0` de la siguiente. Ejemplo completo y actual: `V1` en `motor/configs_lote8.py`.

## Raíz
| clave | qué es |
|---|---|
| `name` | id; nombra stills (`motor/previews/s_<name>_*.jpg`) y audio temporal |
| `src` | vídeo fuente (máster SDR si era HDR) |
| `a16` | ruta del `.npy` de `prep.py` (si no, busca `motor/<name>_a16.npy`) |
| `out` | MP4 final |
| `segs` | tomas `(s, e[, "vs"][, "ve"])`; añade 0,05 s antes / 0,07 s después; `"vs"/"ve"` = cortar en valle de energía (±0,08 s) |
| `emph` | `[(t0, t1), …]` zoom 12 % en la cara (se alterna además un punch-in 1,07 en cada corte) |
| `clean_term` | `True` = terminal sin pestaña de archivo, pasos ni barra de estado |
| `sfx` | `False` para quitar efectos (por defecto: whoosh por escena, clics en resaltados, pop del logo, todo ducked) |
| `cutaways` | existe pero **no usar** (rechazado) |

## Escenas
**intro** (suiza, blanca): `t0`, `t_tecnica` (2.ª línea del título), `title=("Entrevista","técnica.")`, `sub`,
`role` + `t_role`, `company` («en Apple») + `t_company`, `logo=(cx, cy, tamaño, t)` con `logo_kind="so"` para
Stack Overflow (por defecto, glifo de Apple), `info=[]`. Existen `job` (tarjeta de oferta «Solicitar→Postulado») y
`hook` (barras con «?»), pero en la intro actual no se usan.

**data** (suiza): `t0`, `file`, `count` + `count_label` (contador animado), `t_rows`, `scroll_d` (duración del scroll),
`cols=[(cabecera, x, "l"|"r", t_resalte|None)]`, `pool` (filas que pasan) + `rows` (las que quedan), `hl_start`
(999 = sin atenuar columnas), `footer_l`, `footer_r`, `logo` (bool, junto al nombre del archivo).

**question**: `t0`, `rows=[(texto, t)]`, `underlines=[(fila, palabra, t)]`, `size`, `step`.

**code** (terminal): `t0`, `sub`, `lines` (lista de líneas), `rev={línea: t}` (se escribe al decirla),
`hl=[(t, primera, última, paso)]`, `notes={línea: (t, "← texto")}`, `viz=función` + `viz_h` (alto, ~470),
`fs`/`lh` (tamaño/interlineado), `file`, `steps`, `status_r` (solo si `clean_term` es False).
`viz(img, d, t, box)` dibuja en `box=(x0, y0, x1, y1)` con tiempos del original; ver `v1_viz` y los helpers
`viz_frame` / `check` de `configs_lote8.py` (fichas que se agrupan, barras, ordenación — siempre con los datos reales).

**result** (terminal): `t0`, `title`, `header=[(col, x, al)]`, `rows`, `vals` (números por fila, mismas columnas),
`bar_col`, `bar_x`, `bar_w`, `t_bars`, `hot_row` + `t_hot`, `cells=[(fila, col, t)]`, `note=(t, "ETIQUETA", [líneas])`,
`fs`, `rh`, `extra=(t, texto, t_hot)`.

**concl** (suiza): `t0`, `big` («×1,9»), `big_size`, `big_unit`/`unit_dy`, `lines`, `thead`/`trows` (mini tabla),
`note=(línea1, fuente)` (aparece a t0 + 0,5 s). Debe quedar ≥ 5 s.

**cta**: `t0`, `sub`, `rows=[(texto, retardo)]`, `t_link`, `t_free`, `t_es`, `texts` (opcional).

## Utilidades
- `motor/prep.py <nombre> <vídeo>` — audio 16 kHz + trozos VAD con palabras.
- `motor/qa.py <mp4> [--cuts …] [--voz voz.wav] [--expect guion.txt]` — control de calidad; desde el motor:
  `configs*.py <v> qa` (pasa solo los cortes, la voz sin efectos y el audio original para detectar palabras comidas).
- `motor/verify.py <mp4…>` — versión rápida: arranque y hueco máximo entre frases.
- `motor/hdr2prores.swift in out.mov` — máster SDR ProRes con el tone-mapping de Apple (clips HLG del iPhone).
- `motor/cdp_shot.py` — capturas a pantalla completa desde una ventana de Chrome ya abierta (útil si hay que mostrar
  una web con su sesión iniciada; él inicia sesión, tú nunca escribes contraseñas).
- Portadas: PIL con `render2.HV` (Helvetica Neue) — ver la de `entrevistas/finales/01_remoto_vs_presencial_portada.png`.
