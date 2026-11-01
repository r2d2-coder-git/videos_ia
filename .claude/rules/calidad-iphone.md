---
paths:
  - "**/*.MOV"
  - "**/*.mov"
  - "**/*.mp4"
  - "motor/**"
  - "entrevistas/**"
  - "promos/**"
  - "historias/**"
---

# Calidad de imagen de las grabaciones del iPhone

Sus clips del iPhone vienen en **HDR**: HEVC 10 bits, BT.2020, transferencia **HLG** (`arib-std-b67`), 60 fps,
~13 Mbps, girados (`rotation=-90`). Antes de editar cualquier vídeo suyo mira el color con
`ffprobe -show_entries stream=color_transfer,color_primaries,pix_fmt,r_frame_rate`.

Si es HLG:
1. **No** lo conviertas con un `scale`/re-encode normal de ffmpeg: sale «muy blanco», lavado.
2. **No** uses un tone-mapping casero (LUT propia): él lo nota («el color sigue mal») aunque en el visor parezca bien.
   El ffmpeg de esta máquina no tiene `zscale` ni `libplacebo`.
3. **Sí**: saca un máster SDR con el tone-mapping de Apple —
   `swift motor/hdr2prores.swift <in.MOV> <master.mov>` (ProRes 422 HQ, BT.709, conserva el giro y los 60 fps;
   el máster no lleva audio: la voz se toma del original). `avconvert -p Preset1920x1080` también convierte bien el
   color pero se queda en ~15 Mbps H.264 y él vio pérdida de calidad; `--multiPass` falla.
4. Lee los fotogramas del máster con `-vf fps=60` (el iPhone graba con fps variable) y renderiza a **60 fps**,
   x264 `-preset slow -crf 12 -tune film`; nada de proxies intermedios recomprimidos.
5. Etiqueta el resultado como SDR: `-bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1`
   (el motor y `qa.py` ya lo hacen/comprueban).

Si él exporta un MP4 «para facilitar», compruébalo: el último seguía en HLG y a ~3,7 Mbps (peor que el MOV). Úsalo si lo
pide, pero aplicándole el mismo paso 3 y avisándole de que el MOV tiene más calidad.
