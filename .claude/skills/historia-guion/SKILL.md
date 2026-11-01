---
name: historia-guion
description: Investiga y escribe el guion de un vídeo «Historias de datos» para @r2d2.coder (reels verticales de 60-90 s en español donde Arturo narra a cámara una historia real de data science, IA o datos y animaciones la acompañan). Busca fuentes, verifica cada cifra, escribe la narración con gancho y deja guion.md, fuentes.md y beats.json listos para historia-video. Úsala siempre que pida un guion, una historia o una idea para un vídeo de datos, «cuéntame la historia de…», un nuevo episodio de Historias de datos, ideas de historias virales de data science, o que reescriba o acorte un guion, aunque no diga «skill» ni «guion».
---

# Historia · guion

Escribes el guion de un reel de «Historias de datos» para **@r2d2.coder**: la cuenta de Arturo Lorenzo, que enseña
análisis de datos, Python, SQL, cloud e IA en español. El vídeo lo narra **él a cámara** (~30 % del tiempo) y el
resto son **animaciones que explican** lo que cuenta, sobre todo en **3D** (~40 %), más 2D (~20 %) e híbrido (~10 %). Tu trabajo termina en tres archivos que la skill
`historia-video` convierte en vídeo; el formato exacto está en `historias/CONTRATO.md` (léelo antes de escribir).

## Por qué este formato funciona (y qué lo rompe)

Las historias virales de tech en español (s4vitar, midu, expediente.dev, nuncateloexplicaron) comparten algo: una
paradoja en la primera frase, una explicación técnica en lenguaje llano y un dato que lo hace real. Lo que diferencia
a Arturo es la **autoridad**: datos verificados, fuentes, y una lección que su audiencia puede aplicar en su trabajo.
Un guion con una cifra inventada o mal redondeada destruye justo eso, por eso la verificación no es opcional.

La primera versión del vídeo del Netflix Prize falló porque las imágenes eran abstractas (matrices, puntos en un
globo) y no contaban nada. Por eso cada beat lleva un **visual concreto**: algo que se entiende con el sonido quitado.

## Pasos

### 1. Elegir la historia
Si Arturo no trae tema, propón 5 con este formato: título-gancho · la paradoja en una frase · el dato que la sostiene ·
la lección para un analista. Busca historias reales con giro: un modelo que falló, un dato que engañó, una decisión
millonaria tomada con datos, un sesgo famoso. Ejemplos del tipo que funciona: Netflix Prize, los aviones de Abraham
Wald (sesgo de supervivencia), Target y el embarazo, Zillow Offers, Google Flu Trends, el mapa del cólera de John Snow,
la encuesta del Literary Digest de 1936.

### 2. Investigar y verificar
Busca en la web las fuentes primarias (blog técnico de la empresa, paper, prensa seria de la época). Si la primaria
está de pago o no abre, usa la mejor secundaria seria y dilo. Si dos fuentes no coinciden, usa la primaria y dilo.
Lo que no puedas verificar, quítalo del guion: es preferible perder un dato a arriesgar la credibilidad.

**Historias que circulan como leyenda** (Wald, Target, la cerveza y los pañales…): cuenta la versión real aunque la
viral sea más redonda. Si la versión famosa está simplificada, el guion no la repite como hecho, y en pantalla no se
presentan como datos reales los números o imágenes ilustrativos (la imagen famosa del avión con puntos rojos es una
ilustración moderna: se puede usar como dibujo, nunca como «los datos de Wald»).

`fuentes.md` sigue esta plantilla:

```markdown
# Fuentes · <id>

| Dato (como sale en el guion o en pantalla) | Estado | Fuente |
|---|---|---|
| 60 bombarderos perdidos el 17 de agosto de 1943 | verificado | <url> |
| El reparto de agujeros por zonas | simplificación divulgativa (se cuenta sin cifras) | <url> |

## Descartado o dudoso
- <dato>: <por qué se quitó>

## Decisiones tomadas
- <lo que decidiste sin preguntar y por qué>
```
Estados: `verificado` · `simplificación` (explica cuál) · `dudoso` (no va al guion).

### 3. Escribir `guion.md`
Estructura (cada parte, uno o varios beats):

1. **Gancho** (≤ 3 s, 1-2 frases): la paradoja o la cifra imposible. Sin saludos ni «hoy os cuento».
2. **Contexto**: qué pasaba, quién, cuándo. Lo justo.
3. **Desarrollo**: cómo funcionaba, con 1-2 datos concretos.
4. **Giro**: lo que nadie espera («¿Y por qué no lo usaron?»).
5. **Lección / criterio**: qué significa para alguien que trabaja con datos. Aquí Arturo habla como experto.
6. **CTA** corto: «Sígueme para más historias de datos».

Cómo escribirlo:
- **Objetivo 170-200 palabras**, 220 como máximo. A ~2,6 palabras/s más las pausas, eso son 70-85 s; el
  límite del formato es 60-90 s contando pausas.
- Frases cortas, de oído. Español de España, tuteando al espectador («lo tienes en tu trabajo»), sin
  regionalismos fuertes ni muletillas.
- Escribe los números como se dicen («cien millones», «el diez por ciento»), así la voz y los subtítulos casan.
- `[pausa N]` en su propia línea, N en segundos (0.5-2; lo normal es 1). Úsala antes del giro y antes de la
  lección, no más de 2-3 en todo el guion.
- Un título `# …` arriba con el titular del vídeo (no se lee en voz alta).

### 4. Escribir `beats.json`
Divide el guion en 12-20 beats. Para cada uno: `plano`, `ancla`, `idea`, `visual`, `dato`.

- `ancla`: las 2-6 primeras palabras **literales** del beat, **únicas** en el guion (si una frase se repite, alarga
  el ancla hasta que no se repita) y en orden. El vídeo arranca el beat cuando la voz dice esas palabras.
- Duración: entre ~2 y ~6 s por beat (palabras ÷ 2,6). Un beat corto (2 s) está bien para un golpe; uno de más de
  ~6 s en animación necesita un cambio dentro o partirse.
- `dato`: lo que aparece escrito en pantalla en ese beat (una cifra, una fecha, un nombre como «Statistical
  Research Group · Columbia»). Todo lo que salga en pantalla tiene que estar en `fuentes.md`. Vacío si no hay.
- En la cabecera de `beats.json`, `duracion_objetivo` = la duración estimada en segundos (con pausas).

Cuatro tipos de plano, con un reparto objetivo del **tiempo** que Arturo ha fijado:

| `plano` | Tiempo | Qué es | Para qué momentos |
|---|---|---|---|
| `cara` | ~30 % | Él a cámara a pantalla completa (pueden entrar objetos a su lado) | Gancho, giro, lección/criterio, CTA: donde una persona transmite más que un dibujo |
| `3d` | ~40 % | Escena 3D (Three.js) a pantalla completa: objetos con volumen, cámara que se mueve, luz | Escala («sesenta no vuelven»), el objeto protagonista, la acción de la historia, el impacto |
| `2d` | ~20 % | Animación 2D del estilo: celdas, tablas, cifras exactas, diagramas | Datos que hay que leer, mecanismo paso a paso, texto en pantalla |
| `hibrido` | ~10 % | Su cara en franja arriba + animación 2D debajo | Puentes: justo tras un `cara`, cuando la explicación sigue y conviene que se le vea |

Por qué este reparto: el 3D es lo que da el aspecto de cine que retiene en el feed; la cara da la autoridad; el 2D
se reserva para lo que hay que **leer** (una cifra exacta, una tabla), que en 3D se lee peor. Por eso, al decidir
el plano de un beat, pregúntate primero: ¿esto se puede **mostrar** como un objeto o una acción en el espacio? → `3d`.
¿Hay que leer algo? → `2d`.

- Un `visual` de `3d` describe objetos físicos y lo que hace la cámara: «una formación de B-17 en 3D vuela hacia
  cámara; la cámara la acompaña de lado; uno a uno, sesenta se apagan y caen dejando humo». Piensa en objetos que
  se puedan construir con piezas simples (cajas, cilindros, esferas, líneas, partículas) y luz.
- Beats `3d` seguidos pueden compartir escena para que la cámara no corte (anótalo: «misma escena que el beat 3»).
- Evita dos `cara` de más de 5 s seguidos; si la lección y el CTA quedan juntos, deja el CTA corto (~2 s).
- El validador comprueba el reparto (±8-10 puntos de margen).
- Cada `visual` debe poder **dibujarse** y **entenderse sin voz**: un cheque con un sello, dos tickets con la hora de
  envío, un contador que llega a 100.480.507, una matriz que se rellena. Evita «gráfico», «animación de datos»,
  «visualización abstracta».
- Encadena: piensa cómo sale cada visual del anterior (el contador se convierte en la matriz, la matriz se aleja y es
  la pantalla de un portátil…). Anótalo dentro de `visual`.

### 5. Validar y entregar
Guarda todo en `historias/<id>/` y comprueba con el validador del motor (anclas únicas y en orden, duración de cada
beat, reparto de cara, duración total):

```bash
python3 historias/validar.py <id>
```
Corrige lo que marque, sobre todo el reparto de planos. Si Arturo no está para decidir algo, decide tú y apúntalo en «Decisiones tomadas» de
`fuentes.md`. Al terminar dile a Arturo en pocas líneas: titular, duración estimada, reparto
cara / 3d / 2d / híbrido, y qué datos quedaron dudosos. Ofrece pasar a `historia-video`.

## Ejemplo de beats (fragmento)

```json
{"n": 4, "nombre": "Los datos", "plano": "3d", "ancla": "Soltaron cien millones",
 "idea": "La escala del dataset", "visual": "Un relieve 3D de líneas (una por usuario) se extiende hasta el horizonte; los picos rojos (valoraciones) brotan mientras la cámara vuela rasante y sube hasta verlo desde arriba",
 "dato": "100.480.507 valoraciones · Netflix Prize dataset"},
{"n": 5, "nombre": "Vacía", "plano": "2d", "ancla": "Y casi toda",
 "idea": "La matriz está casi vacía", "visual": "Celda de notebook: ratings.pivot(...) → una tabla de NaN con el 98,8 % resaltado en rojo",
 "dato": "98,8 % de celdas vacías"},
{"n": 9, "nombre": "Giro", "plano": "cara", "ancla": "Y por qué no lo usaron",
 "idea": "La pregunta que da la vuelta a la historia", "visual": "Él a cámara, serio; el cheque del gancho reaparece en una esquina", "dato": ""}
```
