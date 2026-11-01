# Historias de datos — contrato entre piezas

Las dos skills (`historia-guion`, `historia-video`) y el motor (`historias/`) solo se hablan a través de estos
archivos. Si cambia algo aquí, cambia en las tres piezas.

## Carpeta de una historia: `historias/<id>/`

`<id>` en minúsculas con guiones (`netflix-prize`, `aviones-wald`).

| Archivo | Lo escribe | Qué es |
|---|---|---|
| `guion.md` | historia-guion | La narración exacta, párrafos + marcas `[pausa N]` en su propia línea. Títulos `#` y comentarios `<!-- -->` no se leen en voz alta. |
| `fuentes.md` | historia-guion | Cada cifra o hecho del guion con su fuente (URL) y si está verificado. |
| `beats.json` | historia-guion | Los momentos del vídeo: tipo de plano + qué se ve (abajo). |
| `voz.wav` | voz.py / el usuario | La voz. Provisional (Mónica, macOS) o la grabación real. |
| `voz.tiempos.json` | voz.py | Cada palabra del guion con su segundo (`{duracion, provisional, palabras:[{p,ini,fin}], frases}`). |
| `cara.mp4` | el usuario (opcional) | Su grabación a cámara, H.264 1080×1920, sincronizada con `voz.wav` desde el segundo 0. Sin ella se pinta un hueco «TU CARA». |
| `index.html`, `scene.js` | historia-video | El vídeo en código (usa `../lib.js`). |
| `out/` | capture.py | Fotogramas de revisión, `<id>.mp4` y audio. |
| `publicar.txt` | historia-video | 1.ª línea título; luego el caption y las fuentes. |

## `beats.json`

```json
{
  "id": "netflix-prize",
  "titulo": "Netflix pagó 1 millón por un algoritmo… y no lo usó",
  "duracion_objetivo": 75,
  "beats": [
    {
      "n": 1,
      "nombre": "Gancho",
      "plano": "cara",
      "ancla": "Netflix pagó un millón",
      "idea": "La paradoja: pagar un millón por algo que no usas",
      "visual": "Él a cámara; a su lado entra un cheque de 1.000.000 $ y le cae un sello «NUNCA SE USÓ»",
      "dato": "1.000.000 $ · Netflix Prize 2009"
    }
  ]
}
```

- `plano` (reparto objetivo en tiempo entre paréntesis):
  - `cara` (~30 %): su cara a pantalla completa, con elementos que entran sobre ella.
  - `3d` (~40 %): escena 3D (Three.js) a pantalla completa con su voz: objetos reales con volumen, cámara que se mueve,
    luz, brillo. Es el plano «cine»: ganchos, escala, el objeto protagonista, los momentos de impacto.
  - `2d` (~20 %): animación 2D del estilo (celdas, tablas, cifras, diagramas): datos exactos, texto, mecanismo paso a paso.
  - `hibrido` (~10 %): su cara en una franja arriba + animación 2D debajo.
  `anim` (versiones antiguas) cuenta como `2d`.
- `ancla`: las primeras palabras del beat, copiadas literalmente del guion. El vídeo arranca ese beat con `E(ancla)`.
- `visual`: un objeto o acción concreta que se entiende sin oír la voz. Nunca «gráfico abstracto».
- `dato`: la cifra que aparece en pantalla en ese beat, si la hay (tiene que estar en `fuentes.md`).

## Formato del vídeo

Vertical 1080×1920, 30 fps, 60-90 s. Él narra: ~30 % `cara`, ~40 % `3d`, ~20 % `2d`, ~10 % `hibrido`. Subtítulos
estilo reel (1-3 palabras, mayúsculas, blanco con contorno, palabra activa naranja, y≈1490). Cambio visual cada 3-4 s.
