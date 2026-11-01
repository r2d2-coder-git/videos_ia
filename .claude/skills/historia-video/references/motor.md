# Motor de Historias de datos — referencia

Todo vive en `videos_ia/historias/`. Una historia es una página (`index.html` + `scene.js`) que pinta cada fotograma
en un canvas de 1080×1920; `capture.py` la abre en Chrome sin ventana (servida por HTTP), llama a `renderFrame(t)` por
fotograma, captura la imagen y la pasa a ffmpeg con el audio de `audio.py`.

## Índice
1. lib.js (helpers, STORY, voz, cara, subtítulos)
2. Modo mundo y continuidad
3. Sonido
4. 3D con Three.js
5. Manim
6. Revisión (lista de comprobación)
7. Ejemplos existentes

## 1. lib.js

Globales: `W=1080, H=1920`, colores `C` (`bg, ink, mut, dim, red, cap…`), fuentes `SANS` (SF Pro) y `MONO` (SF Mono).

| Helper | Uso |
|---|---|
| `pr(t, a, d)` | progreso 0→1 entre a y a+d |
| `eo(x)`, `eio(x)` | suavizados (ease-out, ease-in-out) |
| `lerp(a,b,p)`, `clamp` | interpolar, limitar |
| `rng(seed)` | aleatorio determinista (¡nunca Math.random: cada fotograma se pinta por separado!) |
| `text(ctx, s, x, y, {f, c, a, al, bl, ls})` | texto; `f: font(peso, tamaño, MONO?)` |
| `maskLine(ctx, s, x, y, size, p, o)` | línea que sube desde una máscara |
| `rrect`, `bg(ctx, gx, gy, gr, color)`, `mk(w,h)` | rect redondeado, fondo con brillo, canvas auxiliar |
| `fmt(n)` | 100480507 → «100.480.507» |
| `cargarVoz(url)` → `T` | `T.en("palabras")` segundo en que se dicen; `T.fin(...)`; `T.duracion`, `T.palabras` |
| `cargarCara(url)`, `drawCara(ctx,x,y,w,h,{zoom,dy,r})` | su toma (o el hueco «TU CARA» si no hay `cara.mp4`) |
| `ramp(t,a,d)` | `eio(pr(t,a,d))` |
| `tw(ctx,s,f)`, `wrapLines(ctx,s,f,maxW)` | ancho de un texto; partir en líneas |
| `mixColor(a,b,p)`, `hexRGB` | mezclar colores (atenúa grupos de figuras sin `globalAlpha`, que dobla opacidad en los solapes) |
| `L2(A,B,p)` | interpolar `{x,y,s}` (mover un objeto de una posición/escala a otra) |
| `blink(lt,a0)` | parpadeo determinista |

`window.STORY` (lo que lee el motor):

```js
{ title, hud: false,           // hud true = barra de progreso «HISTORIAS DE DATOS»
  scenes: [{dur}, …],          // tramos (beats); su suma es la duración total
  world: (ctx, t) => {…},      // pinta el fotograma completo en t (modo mundo)
  voz: T,                      // con voz: subtítulos con tiempos reales
  sinSubtitulos: [[a,b], …],   // tramos sin subtítulos (p. ej. la lección escrita en pantalla)
  blurSamples: t => 1,         // >1 = desenfoque de movimiento en barridos rápidos
  events: [{t, type, dur, rate}], grain: 0.22, vignette: true }
```
Después de definirlo: `setup(); renderFrame(0);`. Si cargas voz o beats con `fetch`, envuélvelo en una función
`async` (la plantilla ya lo hace); `capture.py` espera a que exista `window.TIMELINE`.

Subtítulos: los pone el motor (1-3 palabras, palabra activa naranja, y≈1490). Deja libre la franja 1400-1580.

## 1b. Plantilla y estilo Notebook

`_plantilla/scene.js` (módulo ES, el patrón de `aviones-wald` + 3D): carga voz + beats, calcula `t0/t1` de cada beat, `rel(n, frase)`
para sub-anclas, y compone con el **telón de su cara** (`tgt(i)` da `lay` y `cur`: 2d/3d = escenario a pantalla completa,
hibrido = franja de cara de 640 px + escenario debajo, cara = telón completo) y **dos capas por beat** (`DRAW[n](ctx,
lt, z, capa, b)`, `capa` = `'under'` | `'over'`). El escenario `z` ya está recortado a y ≤ 1395 (subtítulos debajo).
`HANDOFF` = beats que recogen el objeto de la tarjeta del `cara` anterior en lugar de fundirla.

`estilos/notebook.js` (estilo A), cargado en `index.html` tras `lib.js`:
```js
const NB = Notebook('aviones_wald.ipynb');           // NB.N = paleta
NB.celdas.add(BN(2).t0, ['flota = bombarderos(año=1943)']);   // una celda por beat (o en una sub-ancla)
// en marco(): NB.chrome(ctx); const cell = NB.celdas.draw(ctx, t, lay); NB.out(ctx, cell, t, z.y - 4);
NB.card(ctx, x, y, w, h, a, 'Out[ ]: impactos'); NB.errBox(…); NB.check(ctx, x, y, a, temblor, 'ok', t);
```

## 2. Modo mundo y continuidad

Para que cada escena nazca de la anterior hay dos recursos probados:
- **Cámara sobre un mundo**: todos los elementos viven en coordenadas de mundo y la cámara viaja (`ctx.setTransform`
  con zoom y centro interpolados). Ejemplo completo: `netflix2/scene.js` (`camAt`, `CAMK`, `world`).
- **Transformación de objetos**: el mismo objeto cambia de forma o de papel (un contador que se convierte en la
  primera fila de una matriz, puntos que se reordenan). Interpola posiciones de los mismos elementos entre beats.
Evita encadenar fundidos: se nota a PowerPoint.

## 3. Sonido

`audio.py` genera una cama ambiental, barridos entre `scenes` y efectos por `events`: `thud` (golpe), `ticks`
(contador; `dur`, `rate`), `ding`, `swell` (subida hacia `t`), `fall`. Si existe `voz.wav`, la voz va encima y la
cama baja ~15 dB. Sonoridad final −14 LUFS (lo hace `capture.py`).

## 4. 3D con Three.js (~40 % del vídeo)

La plantilla ya es un módulo ES con Three.js (importmap a `../node_modules/three`), un renderizador compartido con
brillo (`UnrealBloomPass`) y la función `pinta3d`. Cada beat `3d` define su escena:

```js
ESC3D[3] = THREE => {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x050507); scene.fog = new THREE.FogExp2(0x050507, 0.035);
  const cam = new THREE.PerspectiveCamera(38, W / H, 0.1, 400);
  scene.add(new THREE.HemisphereLight(0xdfe6ff, 0x0b0b10, 0.9));
  const sol = new THREE.DirectionalLight(0xffffff, 2.2); sol.position.set(5, 10, 6); scene.add(sol);
  const flota = construyeFlota(THREE);            // tus objetos
  scene.add(flota.grupo);
  return { scene, cam, update(lt, b) {            // lt = segundos desde que empieza el beat; determinista
    const q = eio(clamp(lt / b.d));
    cam.position.set(lerp(-6, 4, q), 2.5, lerp(14, 9, q)); cam.lookAt(0, 0, 0);
    flota.caer(lt, rel(3, 'sesenta'));           // golpes anclados a palabras
  } };
};
// beats 3d seguidos que comparten escena (la cámara no corta):  ESC3D[4] = ESC3D[3]  y en update usa el t global
```

Claves:
- **Modelos**: construye con primitivas (`BoxGeometry`, `CylinderGeometry`, `SphereGeometry`, `ExtrudeGeometry` de
  una silueta 2D, `LatheGeometry`), agrupados en `THREE.Group`. Una silueta de `Shape` extruida da objetos
  reconocibles (aviones, edificios, logotipos) con poco código. Usa la misma forma que su versión 2D.
- **Materiales**: `MeshStandardMaterial` con `roughness`/`metalness` y una luz principal + una de relleno.
  El acento (`emissive` rojo/naranja) solo en lo importante: el brillo lo realza y guía la mirada.
- **Muchos objetos** (formaciones, partículas, datos): `InstancedMesh` (un solo dibujo para cientos).
- **Líneas y relieves** (el look del plano de Netflix): `THREE.Line` con colores por vértice + muros negros
  para ocultar lo de detrás. Ejemplo: `plano3d/scene.js`.
- **Cámara con intención**: acompaña, revela escala (subir y abrir), se acerca al detalle. Movimientos con
  `eio`, nunca bruscos. Niebla (`FogExp2`) para dar profundidad.
- **Determinista**: nada de `Math.random()` ni relojes: todo sale de `lt` y `rng(seed)`.
- **Texto**: no metas texto en 3D; rótulos y cifras en `DRAW[n]` capa `'over'` (2D, nítido, en la paleta del estilo).
- Profundidad de campo (`BokehPass`) es opcional: queda bien en primeros planos pero cuesta tiempo de render.
- **Texturas de canvas** (humo, nubes, halos): `tex.colorSpace = THREE.SRGBColorSpace`; sin eso salen mucho más
  claras y el brillo las convierte en manchas blancas. Humo oscuro y poco opaco; nubes casi transparentes.
- **Transparencias**: un objeto «fantasma» necesita cuerpo ~0,25 de opacidad + aristas claras (`EdgesGeometry`)
  para leerse sobre fondo oscuro. Lo que cae o se aleja, que se aleje de cámara (no hacia ella).
- **Continuidad 3D ↔ 2D**: construye el modelo 3D desde las mismas siluetas que el 2D (misma unidad y origen) y
  termina/empieza el plano 3D con una cámara cenital que deja el objeto en el mismo píxel y tamaño que el 2D
  (distancia = focal / tamaño en px). Así el corte 3D → notebook no se nota. Ver `cenital()` en `aviones-wald`.
- **Rótulos pegados a objetos 3D**: proyecta la posición (`v.project(cam)`) y pinta el rótulo en 2D en `'over'`.
- **Brillo**: el `emissive` de lo que debe destacar, contenido (~0,2-0,5): con el bloom, más se quema.

Ejemplo completo: `aviones-wald/scene.js`, bloque «3D»: B-17 hecho con extrusiones de la silueta 2D, formación de
80 con `InstancedMesh` y 60 que caen con humo, Manhattan en bloques con baliza en Columbia, el avión que vuelve
(agujeros instanciados, motores con «0» proyectados) y los fantasmas que caen mientras las placas vuelan a los motores.

## 5. Manim

Para explicar un concepto paso a paso (fórmulas, matrices, distribuciones). Entorno: `historias/.venv-manim`
(sin LaTeX: usa `Text`, no `MathTex`). Render vertical:
```bash
../.venv-manim/bin/python -m manim -qh --fps 30 -r 1080,1920 --disable_caching archivo.py Escena
```
Con `config.frame_width, config.frame_height = 7.2, 12.8` los textos salen a buen tamaño. Lánzalo como
`../.venv-manim/bin/python -m manim …` (el ejecutable `manim` del entorno guarda la ruta antigua de la carpeta). Ejemplo:
`manim/factorizacion.py`. Para meterlo en una historia como beat `anim`, carga el MP4 como `<video>` (igual que
`cargarCara`) y dibuja el fotograma del segundo `lt`.

## 6. Revisión (antes de enseñar fotogramas)

- ¿Se entiende cada beat **sin voz**? Si no, el visual es demasiado abstracto.
- ¿El visual del beat nace del anterior?
- Textos: nada se solapa, nada se corta en los bordes, márgenes ≥ 60 px a los lados, nada entre y 1400-1580
  (subtítulos) en `anim`/`hibrido`, nada importante por encima de y 120 ni por debajo de y 1750 (interfaz de IG).
- Cifras en pantalla = las de `fuentes.md`.
- En `cara`: la cara no queda tapada; en `hibrido`: la franja de cara y el panel no se pisan.
- Ritmo: ningún tramo de más de ~4 s sin cambio visual.
- Fuente de los datos visible al final.

## 7. Ejemplos existentes

| Carpeta | Qué enseña |
|---|---|
| `netflix/` | v1 en escenas sueltas (lo que NO funcionó: visuales abstractos) |
| `netflix2/` | mundo continuo con cámara y desenfoque de movimiento (look demasiado parecido a expediente.dev) |
| `estilos/` | los 4 estilos candidatos en un fotograma |
| `plano3d/` | Three.js: relieve de líneas con bloom y DOF |
| `manim/` | Manim: factorización de matrices |
| `aviones-wald/` | **referencia completa**: estilo Notebook + ~40 % en 3D (formación, Manhattan, el avión con volumen), telón de cara, un objeto que cruza toda la historia en 3D y 2D, celdas, sonidos |
| `_plantilla/` | punto de partida: beats + voz + telón de cara + capas |
