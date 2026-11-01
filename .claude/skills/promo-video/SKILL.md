---
name: promo-video
description: Edita los reels promocionales de @r2d2.coder (sobre todo de su plataforma BigDataStack: «aprende <profesión> gratis y en español») en el formato del reel que funcionó — su cara a pantalla completa con cortes rápidos, subtítulos karaoke (blanco con contorno negro, palabra activa en naranja), capturas reales de la plataforma con su sesión iniciada y motion graphics (ruta de habilidades, mapa, tarjetas de equipo, modelo, Discord) — más la portada. Úsala siempre que pase una grabación para promocionar la plataforma, una profesión, un curso, la comunidad o cualquier vídeo «a cámara» con guion corto que no sea un ejercicio de código, o que quiera cambiar algo de una promo ya editada, aunque no diga «skill».
---

# Promo · vídeo

Reel vertical de ~35-45 s (1080×1920, **60 fps** como su grabación): **su cara a pantalla completa**, cortes sin
huecos y, mientras habla, planos que **enseñan lo que dice** (capturas de la plataforma o motion graphics). Referencia
viva: `promos/ciencia-datos/promo.py` (promo de Ciencia de Datos, aprobada) y su reel de referencia
`https://www.instagram.com/p/DcjaNyWM5yO/`. Para una promo nueva copia `promos/ciencia-datos/promo.py` a `promos/<id>/promo.py` y
adapta las secciones marcadas; el código común está en `motor/` y `entrevistas/hybrid.py` (Python: `motor/.venv/bin/python`).

## Pasos

### 1. Entrada y color
- La grabación suele ser un **.MOV del iPhone en HDR (HLG)**: sigue la regla `.claude/rules/calidad-iphone.md`
  (máster ProRes SDR con `motor/hdr2prores.swift`, edita desde el máster, 60 fps, crf 12). Si él te pasa un MP4
  exportado, comprueba con `ffprobe` que no siga siendo HLG y de menos bitrate que el MOV; díselo si es peor.
- El guion (lo que dice) y el objetivo (qué profesión, qué CTA).

### 2. Tomas
`motor/prep.py <id> <vídeo> promos/<id>` y elige la **última toma buena** de cada frase (suele repetir mucho: en la de Ciencia de
Datos el Discord tenía 8 tomas). `SEGS` en segundos del original con `"vs"/"ve"` para cortar en valle. Comprueba que
ningún corte se coma el final de una palabra (`qa` lo detecta, ver paso 6).

### 3. Planos
Haz una tabla frase → plano antes de dibujar:
- **Su cara** en el gancho («Aprende X gratis y en español»), en los planos donde hace algo distinto (p. ej. de pie
  señalando el monitor) y **en el CTA final** («lo tienes en mi perfil»): no los tapes.
- **Capturas de la plataforma** con su sesión iniciada (sin «crear cuenta gratis» ni candados): abre Chrome con un
  perfil aparte en la página de login (`open -na "Google Chrome" --args --user-data-dir=<carpeta> --remote-debugging-port=9333 <url>`),
  **él inicia sesión** (tú nunca escribes contraseñas), no cierres esa ventana (la sesión se pierde) y captura con
  `motor/cdp_shot.py 9333 <url> <png> 540 2` (ancho móvil 540 css ×2 = 1080 px; el layout de escritorio se corta en
  vertical). Scroll **lento** y suave (~400-500 px/s), no saltos.
- **Motion graphics** (en su estética oscura de la plataforma: fondo de rejilla, verde lima, mono) cuando la idea es
  abstracta o hay datos: ruta de habilidades que se enciende al nombrarlas, mapa de puntos con las empresas reales,
  tarjeta del equipo, curva/modelo, código que se ejecuta con cursor y salida. Patrones en `promos/ciencia-datos/promo.py`
  (`route_card`, `map_card`, `team_card`, `model_card`, `run_code`, `discord_card`).
- **Datos reales o nada**: nombres, ciudades, cifras y contadores salen de la web o de una API pública
  (p. ej. miembros de Discord con `discord.com/api/v10/invites/<código>?with_counts=true`). Si algo es ilustrativo
  (ids de clientes inventados), díselo al entregar.

### 4. Subtítulos (estilo de su reel)
1-3 palabras por bloque en una línea, MAYÚSCULAS, SF Pro peso ~900 (~78 px), **blanco con contorno negro de ~7 px**,
la **palabra que está diciendo en naranja** (#FF911E), centrados a ~77 % de alto (y≈1480), pequeño «pop» al entrar.
Tiempos de palabra con faster-whisper sobre el audio montado (`words_out.json`). Sin cajas. Ojo: la portada del
reel de referencia lleva cajas negras con texto blanco, pero eso es la portada, no los subtítulos.

### 5. Revisar
Fotogramas de prueba (`promo.py stills t1 t2 …`) de cada plano nuevo antes del render completo; render en segundo
plano (`promo.py full`).

### 6. QA y entrega
`promo.py qa` → formato y color BT.709, arranque y pausas de voz, **palabras cortadas en los cortes**, **planos de
menos de 0,5 s** (el «microframe» de su cara entre dos gráficos: haz que cada gráfico empiece/acabe exactamente en el
corte o en el siguiente plano), hoja de fotogramas y copia `_movil.mp4` < 30 MB. Arregla los avisos y vuelve a pasar.
Envía con `SendUserFile` el vídeo (y la copia móvil si el original pesa > 30 MB) y la **portada** (su fotograma más
expresivo + «APRENDE X GRATIS Y EN ESPAÑOL 🔥» en cajas negras redondeadas, texto blanco, dentro del recorte 4:5,
y ≈ 285-1635). Recuérdale poner la música desde Instagram.

## Lo que ya rechazó
- Datos encima de su cara (contadores sobre el plano del monitor): tapan y no da tiempo a leerlos.
- Planos demasiado cortos para procesarlos (un scroll de 2 s por 8 casos, seguido del mapa).
- Cierres con logo animado en lugar de su cara en el CTA.
- Zooms de énfasis en planos sin intención (el de «vida real»); sí en «gratis», «tu encargo», «mi perfil».
- Color lavado / pérdida de calidad (ver la regla del iPhone).
- Mensajes o cifras inventadas (chats de Discord, nº de miembros sin consultar).
