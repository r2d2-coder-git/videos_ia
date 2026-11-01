---
name: entrevista-video
description: Edita los vídeos «Entrevista técnica» de @r2d2.coder (Arturo resuelve en voz alta un ejercicio de datos con Python/pandas o SQL como si fuera una entrevista de Data Analyst/Engineer en una empresa) al formato híbrido aprobado — su cara arriba y debajo un panel animado (intro suiza con el logo de la empresa, dataset en vivo con filas reales, pregunta, código que se escribe con una ilustración de lo que hace, resultado, conclusión y CTA) — con cortes quirúrgicos sin huecos, sin subtítulos, más la portada del reel. Úsala siempre que pase una grabación o un vídeo antiguo de un ejercicio de código o datos para editarlo, adaptarlo «al formato nuevo», mejorarlo antes de subirlo, cambiar algo de uno ya editado o hacerle la portada, aunque no diga «skill».
---

# Entrevista técnica · vídeo

Montas un reel vertical (1080×1920, 30 fps) a partir de su grabación: **cara arriba (605 px)** y debajo un **panel
que explica lo que dice**, sincronizado palabra a palabra. Todo sale de código (`entrevistas/hybrid.py`), así que cada
cifra en pantalla tiene que ser la real. El formato está iterado vídeo a vídeo con Arturo: respétalo y no
reintroduzcas lo que ya rechazó (lista al final).

Rutas (desde `videos_ia/`): montador en `entrevistas/hybrid.py`, configuraciones en `entrevistas/configs/`, código común en `motor/`, Python con Whisper en `motor/.venv/bin/python`, datasets y notebooks en
`~/Desktop/codigo_rrss/ejercicios-instagram/data-science/<empresa>/`. Referencia completa de la configuración en
`references/config.md`; ejemplo vivo: `V1` (remoto vs presencial, Stack Overflow) en `entrevistas/configs/configs_lote8.py`.

## Pasos

### 1. Entrada
- La grabación (normalmente en `~/Downloads`). Si es un vídeo **ya editado** por su editor anterior (con música o
  subtítulos), pide o busca el bruto: del editado no salen cortes limpios. Para lotes con bruto + render del editor
  está `entrevistas/brutos/lote8/_analiza.py` + `_alinea.py`, que eligen las mismas tomas que el editor.
- El código del ejercicio (notebook o el que pegue) y el dataset. **Ejecuta su código sobre el CSV real** para sacar
  las cifras; si el CSV no está en la carpeta (a veces solo hay el esquema), busca la fuente oficial y **pide permiso
  antes de descargar** (archivo, origen, tamaño). Si tu resultado no cuadra con lo que dice en voz alta, avísale y
  deja en pantalla sus cifras (las que dice).

### 2. Preparar
```bash
motor/.venv/bin/python motor/prep.py <nombre> "<vídeo>"
```
Deja en `entrevistas/datos/` `<nombre>_a16.npy` y `<nombre>_pieces.json` (trozos de voz VAD con palabras y tiempos en segundos del original)
e imprime cada trozo. Si avisa de **HDR (HLG)** —sus .MOV de iPhone—, saca antes el máster SDR con
`swift hdr2prores.swift in.MOV master.mov` y edita desde el máster (si no, sale lavado y blanco).

### 3. Elegir tomas (`segs`)
Lee los trozos y quédate con la **última toma buena** de cada frase, sin arranques en falso ni repeticiones.
`segs` = lista de `(inicio, fin[, "vs"][, "ve"])` en segundos del original; `"vs"/"ve"` ajustan el corte al valle de
energía cuando cortas dentro de una frase. Recorta lo que sobra (explicaciones redundantes, frases incorrectas) para
que el vídeo quede en **~55-60 s** y el código no se coma más de la mitad.
**Comprueba cada corte que cae a final de palabra**: Whisper fecha mal los finales y es fácil comerse una sílaba
(«2025» se quedó en «2020»). Transcribe el trozo con la frase siguiente pegada y mueve el fin hasta que se oiga entera.

### 4. Configurar
Copia la estructura de `V1` en `entrevistas/configs/configs_lote8.py` (o un archivo nuevo con el mismo patrón) y rellena las
escenas con tiempos de palabra **del original** (el motor los mapea al montaje):
`intro → data → question → code (+ viz) → result → concl → cta`, más `emph` y `clean_term=True`.
Detalle de cada clave en `references/config.md`. Reglas que ya están decididas:
- **Intro**: solo «Entrevista técnica.», «Data Analyst Junior **en <Empresa>**» y el **logo de la empresa** animado
  (Apple: glifo; Stack Overflow: `logo_kind="so"`, dibujado). `info=[]`, sin tarjetas extra: dura ~2-3 s y no da
  tiempo a leer más.
- **Dataset**: tabla «en vivo» con **filas reales** del CSV (pool que hace scroll + filas finales), contador de filas
  reales; si hay nulos, déjalos visibles y explica `NaN` en el pie.
- **Código**: líneas que se escriben al decirlas (`rev`), resaltado por pasos (`hl`), notas cortas (`notes`, p. ej.
  «← mediana, no media») y una **ilustración animada con datos reales** debajo (`viz`) que cambie cada pocos
  segundos. `clean_term=True` (sin pestaña del notebook, ni pasos, ni barra «python 3.11»).
- **Resultado**: tabla con barras, fila ganadora resaltada al decirla y nota (si dice «media» y es mediana, la nota lo
  aclara en ese momento).
- **Conclusión**: la cifra grande (p. ej. «×1,9») **≥ 5 s en pantalla**; mueve `cta.t0` lo necesario.
- **`emph`**: zoom de énfasis en su cara en 3-5 frases clave (pregunta, resultado y algún paso del código).

### 5. Revisar y renderizar
```bash
motor/.venv/bin/python entrevistas/configs/configs_lote8.py <v> edl            # cortes y duración
motor/.venv/bin/python entrevistas/configs/configs_lote8.py <v> stills 1.5 6 14 …   # fotogramas → entrevistas/previews/
motor/.venv/bin/python entrevistas/configs/configs_lote8.py <v> full           # MP4 final (en segundo plano: tarda varios minutos)
motor/.venv/bin/python entrevistas/configs/configs_lote8.py <v> qa             # control de calidad (obligatorio antes de entregar)
```
Mira una hoja de fotogramas (una por escena) **antes** del render completo. Tras el render, `qa` revisa formato y
color, arranque y pausas de voz, **palabras comidas en cada corte** (compara cada final de toma con el original),
planos de menos de 0,5 s, deja la hoja `<vídeo>_hoja.jpg` y la transcripción completa.
Arregla cada AVISO y vuelve a pasarlo.

### 6. Portada
PNG 1080×1920 junto al vídeo: su cara (fotograma expresivo de la grabación) arriba, título en el estilo suizo del
vídeo («Data Analyst / **en <Empresa>**» con el color de la marca o la pregunta gancho) y, si encaja, la tarjeta
gancho (barras con «?»). Todo el texto dentro del recorte 4:5 de la cuadrícula del perfil (y ≈ 285-1635).

### 7. Entregar
Envía el MP4 (y la portada) con `SendUserFile`; los pasa al móvil por AirDrop.
Resume qué cambiaste y lo que no pudiste arreglar (p. ej. una palabra mal dicha). Recuérdale que la **música** la
ponga desde Instagram al publicar.

## Lo que Arturo ya rechazó (no lo vuelvas a hacer)
- Subtítulos en este formato, y la etiqueta «Entrevista técnica · Empresa» encima de su cara.
- Cortes con huecos, arranques lentos o restos de tomas («quirúrgico»: que no se note ningún corte).
- La «lupa»/cutaway que tapa su cara con un trozo ampliado del panel (parece un bug).
- Whoosh de ruido blanco («alguien soplando al micro»): solo el barrido filtrado del motor, bajo y debajo de la voz.
- Contenido pegado a los bordes: el motor ya encoge el panel a 60 px izq. / 90 px der. por la interfaz de IG/TikTok.
- Intro cargada (dataset, formato, tarjetas, barras): en 2-3 s solo cabe título + puesto + logo.
- Cabecera del notebook, lista de pasos y barra de estado en el terminal.
- Conclusiones que se van en 2 s.
- Datos inventados en pantalla: si no hay CSV real, no hay filas.
