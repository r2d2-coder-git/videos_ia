// Plantilla de una historia: beats.json + voz.tiempos.json → cada beat en su tipo de plano.
//   cara    su cara a pantalla completa; lo que va encima en la capa 'over'
//   3d      escena Three.js a pantalla completa (ESC3D[n])
//   2d      animación 2D del estilo (DRAW[n], capa 'under')
//   hibrido su cara en franja arriba + animación 2D debajo
// Su cara es un «telón» que baja (cara), se queda en franja (hibrido) o sube (2d/3d).
// Los beats sin dibujo propio salen como tarjeta (2d) o como escena 3D provisional (3d), para ver el ritmo.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const T = await cargarVoz('voz.tiempos.json');
const E = T.en;
const B = await (await fetch('beats.json')).json();
await cargarCara('cara.mp4');

const beats = B.beats.map(b => ({ ...b, plano: b.plano === 'anim' ? '2d' : b.plano, t0: E(b.ancla) }));
beats[0].t0 = 0;
beats.forEach((b, i) => { b.t1 = i + 1 < beats.length ? beats[i + 1].t0 : T.duracion + 0.8; b.d = b.t1 - b.t0; });
const BN = n => beats[n - 1];
/** Sub-ancla: segundos desde el inicio del beat n hasta que se dice `frase` (para golpes dentro de un beat). */
const rel = (n, frase) => E(frase, BN(n).t0) - BN(n).t0;

// Estilo: para el A (Notebook) carga ../estilos/notebook.js en index.html y descomenta:
// const NB = Notebook('<id>.ipynb'); NB.celdas.add(BN(2).t0, ['codigo()']);
const FONDO = C.bg;
function marco(ctx, t, lay) {
  // lo fijo del estilo detrás de la animación 2D (p. ej. NB.chrome(ctx); return NB.celdas.draw(ctx, t, lay);)
  return null;
}

// ================================================================= 3D
// Un renderizador compartido (con brillo) y una escena por beat 3D. ESC3D[n] = THREE => ({ scene, cam, update(lt, b) }):
// se construye una vez, la primera vez que hace falta; update() mueve cámara y objetos en el segundo lt del beat.
// Varios beats seguidos pueden compartir escena (devuelve el mismo objeto) para que la cámara siga sin corte.
const R3 = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
R3.setPixelRatio(1); R3.setSize(W, H, false);
R3.toneMapping = THREE.ACESFilmicToneMapping;
const RT = new THREE.WebGLRenderTarget(W, H, { samples: 4, type: THREE.HalfFloatType });
const composer = new EffectComposer(R3, RT);
const pase = new RenderPass(new THREE.Scene(), new THREE.PerspectiveCamera());
composer.addPass(pase);
composer.addPass(new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 0.9, 0.5, 0.4));
composer.addPass(new OutputPass());
const ESC3D = {};
const _esc = {};

function provisional3d() {
  // escena 3D de relleno: un poliedro de alambre girando sobre una rejilla, con niebla
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x050507); scene.fog = new THREE.FogExp2(0x050507, 0.06);
  const cam = new THREE.PerspectiveCamera(40, W / H, 0.1, 200);
  const obj = new THREE.Mesh(new THREE.IcosahedronGeometry(2.2, 1), new THREE.MeshBasicMaterial({ color: 0xe5383b, wireframe: true }));
  obj.position.y = 2.5; scene.add(obj);
  scene.add(new THREE.GridHelper(60, 60, 0x333844, 0x1a1d24));
  return { scene, cam, update(lt) {
    obj.rotation.set(lt * 0.4, lt * 0.6, 0);
    cam.position.set(Math.sin(lt * 0.25) * 14, 5, Math.cos(lt * 0.25) * 14); cam.lookAt(0, 2, 0);
  } };
}
function pinta3d(ctx, b, lt) {
  const esc = _esc[b.n] ??= (ESC3D[b.n] ? ESC3D[b.n](THREE) : provisional3d());
  esc.update(lt, b);
  pase.scene = esc.scene; pase.camera = esc.cam;
  composer.render();
  ctx.drawImage(R3.domElement, 0, 0, W, H);
}

// ================================================================= 2D
// DRAW[n] = (ctx, lt, z, capa, b)
//   capa 'under': la animación 2D (escenario z = {x, y, w, h}, ya recortado para no invadir los subtítulos)
//   capa 'over' : lo que va ENCIMA (de su cara en «cara», o de la escena en «3d»): rótulos, cifras, tarjetas.
//                 En «cara», nunca sobre la cara: zona libre ≈ y 180-420 y los laterales; la cara ocupa ≈ x 240-840, y 420-1250.
const DRAW = {};

function tarjeta(ctx, lt, z, capa, b) {
  const p = eo(pr(lt, 0, .4));
  if (capa === 'over' && b.plano !== 'cara' && b.plano !== '3d') return;
  if (capa === 'under' && b.plano === '3d') return;
  const small = capa === 'over';
  const r = small ? { x: 560, y: 200, w: 460, h: 320 } : { x: z.x, y: z.y + 20, w: z.w, h: Math.min(z.h - 40, 640) };
  ctx.save(); ctx.globalAlpha *= p;
  rrect(ctx, r.x, r.y, r.w, r.h, 20); ctx.fillStyle = 'rgba(20,22,27,0.88)'; ctx.fill();
  ctx.strokeStyle = 'rgba(255,255,255,0.12)'; ctx.lineWidth = 2; ctx.stroke();
  text(ctx, `BEAT ${b.n} · ${b.plano.toUpperCase()}`, r.x + 30, r.y + 50, { f: font(600, 20, MONO), c: C.red, ls: 2 });
  const f = font(600, small ? 26 : 32);
  wrapLines(ctx, b.visual || b.idea || '', f, r.w - 60).slice(0, 8).forEach((s, i) => text(ctx, s, r.x + 30, r.y + 100 + i * (small ? 34 : 42), { f, c: C.ink }));
  if (b.dato) text(ctx, b.dato, r.x + 30, r.y + r.h - 28, { f: font(400, 20, MONO), c: C.mut });
  ctx.restore();
}
const draw = (b, ctx, lt, z, capa) => (DRAW[b.n] || tarjeta)(ctx, lt, z, capa, b);

// ================================================================= composición
// lay: 0 = escenario arriba (2d/3d), 1 = escenario bajo la franja (hibrido) · cur: altura del telón de la cara
const tgt = i => {
  const b = beats[i];
  if (b.plano === '2d' || b.plano === '3d') return { lay: 0, cur: 0 };
  if (b.plano === 'hibrido') return { lay: 1, cur: 640 };
  return { lay: i > 0 ? tgt(i - 1).lay : 0, cur: H };
};
const HANDOFF = new Set([]);   // beats que recogen el objeto de la tarjeta del beat «cara» anterior (no se funde)
const beatAt = t => { const i = beats.findIndex(b => t >= b.t0 && t < b.t1); return i < 0 ? beats.length - 1 : i; };

function fondoBeat(ctx, k, lt, z, lay, t) {
  // lo que hay debajo del telón: la escena 3D o la animación 2D del beat k
  const b = beats[k];
  if (b.plano === '3d') { pinta3d(ctx, b, lt); return; }
  marco(ctx, t, lay);
  ctx.save(); ctx.beginPath(); ctx.rect(0, z.y - 24, W, 1395 - z.y + 24); ctx.clip();
  draw(b, ctx, lt, z, 'under');
  ctx.restore();
}
function world(ctx, t) {
  const i = beatAt(t), b = beats[i], lt = t - b.t0;
  const A = i > 0 ? tgt(i - 1) : tgt(0), Bt = tgt(i), p = eio(pr(lt, 0, 0.42));
  const lay = lerp(A.lay, Bt.lay, p), cur = lerp(A.cur, Bt.cur, p);
  const z = { x: 60, y: lerp(410, 850, lay), w: 960 }; z.h = 1390 - z.y;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillStyle = FONDO; ctx.fillRect(0, 0, W, H);
  if (cur < H - 1) {
    // en un plano «cara» se congela debajo el último plano animado (para que el telón suba sobre algo)
    let k = i; if (b.plano === 'cara') { k = i - 1; while (k >= 0 && beats[k].plano === 'cara') k--; }
    if (k >= 0) fondoBeat(ctx, k, k === i ? lt : beats[k].d - 0.001, z, lay, t);
  }
  if (cur > 1) {
    const q = clamp((cur - 640) / 1280);
    drawCara(ctx, 0, 0, W, cur, { zoom: lerp(1.15, 1, q), dy: lerp(120, 0, q) });
    if (cur < H - 1) { ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fillRect(0, cur - 2, W, 3); }
  }
  // la tarjeta del beat «cara» anterior se va (salvo que el siguiente recoja su objeto)
  if (i > 0 && beats[i - 1].plano === 'cara' && !HANDOFF.has(b.n) && lt < 0.35) {
    ctx.save(); ctx.globalAlpha = 1 - lt / 0.35; draw(beats[i - 1], ctx, beats[i - 1].d, z, 'over'); ctx.restore();
  }
  draw(b, ctx, lt, z, 'over');
}

// ================================================================= sonido (t en segundos de vídeo)
const at = (n, s = 0) => BN(n).t0 + s;
const events = [];   // p. ej. { t: at(3, rel(3, 'sesenta')), type: 'thud' }

window.STORY = {
  title: B.titulo, hud: false, grain: 0.08, vignette: false,
  scenes: beats.map(b => ({ dur: b.d, draw: () => { } })),
  world, voz: T, events,
};
setup();
renderFrame(0);
