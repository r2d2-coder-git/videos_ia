---
name: historia-video
description: Convierte un guion de «Historias de datos» (guion.md + beats.json en historias/<id>/) en el reel vertical final de @r2d2.coder: la voz de Arturo (o una provisional), su cara a cámara en los momentos clave y animaciones por código (escenas 3D con Three.js, 2D en canvas y, si hace falta, Manim) ancladas palabra a palabra, con subtítulos estilo reel y sonido. Úsala siempre que pida montar, animar, renderizar o rehacer un vídeo de Historias de datos, probar un estilo o un plano, meter su grabación o su voz en una historia, o ver cómo quedaría un guion en vídeo, aunque no diga «skill».
---

# Historia · vídeo

Montas el reel de una historia que ya tiene guion. Arturo narra a cámara y las animaciones **explican** lo que dice:
cada plano tiene que entenderse con el sonido quitado y nacer del anterior. Todo se hace con código que renderiza a
MP4: no hay generadores de vídeo por IA, así que cada cifra en pantalla es exacta.

Antes de nada lee `historias/CONTRATO.md` (archivos y formato) y, cuando vayas a escribir código,
`references/motor.md` (API del motor). Para elegir o aplicar un estilo, `references/estilos.md`.

Comandos (desde `videos_ia/historias/`; el Python con Whisper está en `../motor/.venv`):

```bash
../motor/.venv/bin/python voz.py provisional <id>        # voz sintética + tiempos (si aún no hay grabación)
../motor/.venv/bin/python voz.py tiempos <id> [audio]    # tiempos de su voz real
python3 validar.py <id>                                  # comprueba guion + beats (y tiempos si hay voz)
../motor/.venv/bin/python capture.py <id> stills 1.0 4.5 …  # fotogramas sueltos → <id>/out/still_*.png
../motor/.venv/bin/python capture.py <id> hoja           # un fotograma por beat → <id>/out/hoja.png
../motor/.venv/bin/python capture.py <id> full 30        # MP4 final con voz, música y efectos → <id>/out/<id>.mp4
```

## Pasos

### 1. Comprobar la entrada
En `historias/<id>/` tiene que haber `guion.md` y `beats.json`. Si falta el guion, ofrece usar `historia-guion`.
Pasa `python3 validar.py <id>` (anclas únicas y en orden, duración de beats, reparto de cara); corrige lo que
marque en `beats.json` antes de seguir. Vuelve a pasarlo tras sacar la voz: con `voz.tiempos.json` usa los tiempos
reales.

### 2. La voz manda
- Si Arturo ha dejado su grabación (`voz.wav`, o un audio que te indique), saca los tiempos con `voz.py tiempos`.
- Si no, genera la provisional con `voz.py provisional` y díselo: suele ir algo más rápida que él (el vídeo
  provisional dura menos que la estimación de `validar.py`), así que algunos beats quedarán más cortos.
  Cuando grabe, se rehacen los tiempos y el vídeo se recoloca solo porque todo está anclado a palabras.
- Mira el `acierto` que imprime: los números escritos en letra («dos mil seis») no cuentan como oídos y es normal quedarse en ~80-90 %; por debajo de ~70 % la voz no dice el guion (frases cambiadas): avísale.
- Si hay `cara.mp4` (su toma a cámara, H.264), el motor la usa; si no, pinta el hueco «TU CARA». No lo trates como
  error: es lo normal mientras prueba.

### 3. Estilo
Si la historia o Arturo no fijan estilo, pregúntale con las opciones de `references/estilos.md` (o usa el que ya
eligió en otra historia). Un vídeo, un estilo: el 2D sigue el estilo, y el 3D comparte su paleta y su acento para
que todo parezca de la misma pieza.

### 4. Montar
1. Copia `historias/_plantilla/index.html` y `scene.js` en `historias/<id>/`. Con eso ya renderiza: su cara es un
   «telón» (baja en `cara`, se queda en franja en `hibrido`, sube en `2d`/`3d`), los beats `3d` salen como escena 3D
   provisional y los `2d` como tarjeta, todo anclado a la voz. Saca la `hoja` para ver el ritmo antes de dibujar.
   Si `validar.py` marca el reparto de planos (objetivo ~30 % cara, ~40 % 3d, ~20 % 2d, ~10 % híbrido), corrige el
   `plano` de los beats en `beats.json` antes de dibujar: Arturo quiere ese reparto.
2. **Beats `3d`**: escribe `ESC3D[n]` (escena Three.js con su cámara y su `update(lt)`), siguiendo
   `references/motor.md` → «3D». Son el 40 % del vídeo y lo que más se ve: dedícales el mayor esfuerzo (modelo
   reconocible, luz, cámara con intención, brillo en lo importante). Los rótulos y cifras van encima en `DRAW[n]`
   capa `'over'`.
3. **Beats `2d`/`hibrido`/`cara`**: carga las piezas del estilo (Notebook: `../estilos/notebook.js`) y rellena
   `DRAW[n]` con el `visual` de `beats.json`: capa `'under'` = la animación 2D; capa `'over'` = lo que va encima de su
   cara (o de la escena 3D). Usa `rel(n, 'frase')` para los golpes dentro de un beat. Escribe y comprueba en
   bloques de 3-4 beats (hoja o fotogramas de cada uno): un error se arregla mejor pronto.
   La historia `aviones-wald/` es el ejemplo completo de referencia: cópiale los patrones.
4. **Continuidad**: el visual de un beat sale del anterior (el contador se convierte en matriz, la matriz se aleja y es
   la pantalla de un portátil). Sustituye el fundido de la plantilla por la transformación real donde se pueda.
5. En planos `cara`, los elementos entran **sobre** su toma (capa `'over'`) en la zona libre: arriba (y 180-420)
   o en los laterales; la cara ocupa ≈ x 240-840, y 420-1250. Los objetos pueden pasar de la tarjeta al escenario
   del beat siguiente (`HANDOFF` en la plantilla) en vez de fundirse.
6. Añade `events` de sonido en los golpes (sello, contador, revelación). La voz va encima; la música queda debajo.

Un mismo objeto puede vivir en 3D y en 2D (el avión 3D del gancho y su silueta 2D en el notebook): que tengan la
misma forma y colores para que el paso de uno a otro se lea como continuidad. Manim, si hace falta, va como un clip
dentro de un beat `2d` (ver `references/motor.md`).

### 5. Revisar antes del render
Saca la hoja (`capture.py <id> hoja`, un fotograma en el centro de cada beat) y revísala contra la lista de
`references/motor.md` → «Revisión». Arregla lo que veas y enséñale la hoja a Arturo antes del
render completo: un render son varios minutos y un fotograma son segundos.

### 6. Render y entrega
`capture.py <id> full 30` (tarda ~10 min por minuto de vídeo: lánzalo en segundo plano), comprueba duración y
sonoridad y entrégaselo (con `SendUserFile` si lo tienes; si no, la ruta). Escribe `publicar.txt`
(título, caption con la lección en 2-3 líneas, fuentes de `fuentes.md`). Si la voz era provisional, recuérdaselo.

## Lo que hemos aprendido (y por qué importa)
- El primer vídeo hecho con la skill (aviones-wald) salió todo en 2D y Arturo lo echó en falta: el 3D es
  el ~40 % del formato, no un extra opcional.
- Las animaciones abstractas no cuentan nada: en la v1 del Netflix Prize nadie entendía la historia. Objetos y acciones
  concretas, una idea por plano.
- Sin continuidad parece un PowerPoint: cada escena tiene que nacer de la anterior.
- No copiar la estética de otro canal (el tablero con papeles y sellos era demasiado expediente.dev): ideas sí, look no.
- Autoridad, no cartoon: movimiento sobrio, rigor en los datos (fuente en pantalla al final). Un acento principal;
  si hacen falta más colores, que signifiquen algo y siempre lo mismo (Notebook: rojo = datos/errores, naranja =
  la idea clave, verde = «ok»).
