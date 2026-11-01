# videos_ia · reels de @r2d2.coder

Arturo (r2d2.coder) publica reels verticales en español sobre análisis/ingeniería de datos, Python, SQL y cloud, y
promociona su plataforma gratuita **BigDataStack** (bigdatastack.dev). Aquí se editan con código: nada de editores
de vídeo ni generadores por IA, así que cada cifra en pantalla tiene que ser real. Háblale en español.

## Formatos y su skill
| formato | skill | dónde |
|---|---|---|
| Entrevista técnica (cara arriba + panel suizo/terminal con código, sin subtítulos) | `entrevista-video` | `entrevistas/` (`hybrid.py`, `configs/`, `datos/`, `brutos/`, `finales/`) |
| Promos a cámara (cara completa, subtítulos karaoke, capturas y motion graphics) | `promo-video` | `promos/<id>/` (plantilla: `promos/ciencia-datos/promo.py`) |
| Historias de datos (narración + animaciones) | `historia-guion`, `historia-video` | `historias/` |

Otros: `entrevistas/brutos/lote8/` (brutos + renders de su antiguo editor, `_analiza.py`/`_alinea.py`), `referencias/estilos/`, `archivo/` (pruebas y versiones descartadas). `motor/` es el código común (qa, prep, cdp_shot, hdr2prores, render) y, como `historias/`, lleva un entorno virtual: no los muevas.
Datasets y notebooks de los ejercicios: `~/Desktop/codigo_rrss/ejercicios-instagram/data-science/<empresa>/`.
Python con Whisper y PIL: `motor/.venv/bin/python` (Python 3.14; `faster_whisper.decode_audio` falla con el PyAV
nuevo: decodifica el audio con ffmpeg a f32le).

## Cómo le gusta
- Estilo **profesional, de autoridad**, no cartoon; le gustan el **suizo minimal** y el **terminal**.
- Cortes **quirúrgicos**: ni huecos, ni arranques lentos, ni restos de tomas, ni palabras comidas. Método: Silero VAD +
  transcribir cada trozo + cortar en valles de energía + fundidos de 12-15 ms + punch-in 1,07 alterno.
- Menos es más: si un elemento no da tiempo a leerlo (intro de 2 s, contador sobre un plano corto), fuera.
- Su cara manda en el gancho y en el CTA; nada encima de su cara.
- Calidad de imagen del iPhone: ver `.claude/rules/calidad-iphone.md`.

## Reglas de trabajo
- **Datos reales o nada**: ejecuta su código sobre el CSV real; si falta el CSV, busca la fuente oficial y pide
  permiso antes de descargar (archivo, origen, tamaño). Si lo que sale no cuadra con lo que dice, avísale.
- Renders largos en segundo plano y espera la notificación; nunca bucles de espera en primer plano.
- Antes de entregar cualquier vídeo, pásale **`motor/qa.py`** (entrevistas: `configs*.py <v> qa`; promos:
  `promo.py qa`) y arregla los avisos: palabras cortadas en los cortes, planos < 0,5 s (microframes), pausas,
  color sin etiqueta. Mira la hoja de fotogramas.
- Entrega con `SendUserFile`: el vídeo, la copia `_movil.mp4` si pesa > 30 MB (si no, no le llega al móvil) y la
  portada. Recuérdale que la música la pone desde Instagram.
- Él inicia sesión en las webs; tú nunca escribes contraseñas. Las capturas con sesión se hacen desde su ventana
  abierta (`motor/cdp_shot.py`).
