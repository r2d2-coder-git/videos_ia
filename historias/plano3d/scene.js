// Plano 3D de prueba: la matriz de 100 M de valoraciones como un relieve de líneas.
// Cada línea es un usuario, cada pico una película que valoró (altura = nota). Casi todo es llano: 98,8 % vacío.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { BokehPass } from 'three/addons/postprocessing/BokehPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const DUR = 8.5;
const ROWS = 200, COLS = 300, DX = 0.18, DZ = 0.45;
const X0 = -COLS * DX / 2, Z0 = -ROWS * DZ / 2;

// ---------------------------------------------------------------- render
const R = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false);
R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.0;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x050507);
scene.fog = new THREE.FogExp2(0x050507, 0.032);
const cam = new THREE.PerspectiveCamera(40, W / H, 0.1, 400);

const rt = new THREE.WebGLRenderTarget(W, H, { samples: 4, type: THREE.HalfFloatType });
const composer = new EffectComposer(R, rt);
composer.addPass(new RenderPass(scene, cam));
const bokeh = new BokehPass(scene, cam, { focus: 12, aperture: 0.0009, maxblur: 0.006 });
composer.addPass(bokeh);
composer.addPass(new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 1.1, 0.55, 0.35));
composer.addPass(new OutputPass());

// ---------------------------------------------------------------- datos (deterministas)
const r = rng(2006);
const base = [], peaks = [];
for (let i = 0; i < ROWS; i++) {
  const row = new Float32Array(COLS), ph = r() * 6.28, amp = 0.04 + r() * 0.06;
  for (let j = 0; j < COLS; j++) row[j] = amp * (Math.sin(j * 0.11 + ph) + 0.6 * Math.sin(j * 0.031 + ph * 2)) + 0.02 * (r() - .5);
  base.push(row);
  const pk = [];
  for (let j = 0; j < COLS; j++) if (r() < 0.012) pk.push({ j, v: 1 + Math.floor(r() * 5), ts: 1.1 + r() * 2.5 });
  peaks.push(pk);
}
const SIG = 1.2;
// cada valoración "cae" en su momento mientras sube el contador
function height(i, j, t) {
  let h = base[i][j], red = 0;
  for (const p of peaks[i]) { const d = j - p.j; if (Math.abs(d) < 6) { const gr = eo(pr(t, p.ts, .45)), g = Math.exp(-d * d / (2 * SIG * SIG)); h += g * p.v * 0.42 * gr; red = Math.max(red, g * gr); } }
  return [h, red];
}

// ---------------------------------------------------------------- geometría: una línea + un oclusor negro por usuario
const lines = [], walls = [];
const lineMat = new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, fog: true });
const wallMat = new THREE.MeshBasicMaterial({ color: 0x050507, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, side: THREE.DoubleSide });
for (let i = 0; i < ROWS; i++) {
  const z = Z0 + i * DZ;
  const lg = new THREE.BufferGeometry();
  lg.setAttribute('position', new THREE.BufferAttribute(new Float32Array(COLS * 3), 3));
  lg.setAttribute('color', new THREE.BufferAttribute(new Float32Array(COLS * 3), 3));
  const ln = new THREE.Line(lg, lineMat); scene.add(ln); lines.push(ln);
  const wg = new THREE.BufferGeometry(), idx = [];
  wg.setAttribute('position', new THREE.BufferAttribute(new Float32Array(COLS * 2 * 3), 3));
  for (let j = 0; j < COLS - 1; j++) { const a = j * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); }
  wg.setIndex(idx);
  const wm = new THREE.Mesh(wg, wallMat); scene.add(wm); walls.push(wm);
  ln.userData.z = z;
}
// puntos brillantes en la cima de cada valoración
const allPeaks = []; peaks.forEach((pk, i) => pk.forEach(p => allPeaks.push({ i, ...p })));
const pg = new THREE.BufferGeometry();
pg.setAttribute('position', new THREE.BufferAttribute(new Float32Array(allPeaks.length * 3), 3));
const dot = (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d'); const g = x.createRadialGradient(32, 32, 0, 32, 32, 32); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.25, 'rgba(255,120,110,.9)'); g.addColorStop(1, 'rgba(229,56,59,0)'); x.fillStyle = g; x.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); })();
const pts = new THREE.Points(pg, new THREE.PointsMaterial({ size: 0.32, map: dot, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, color: 0xff6a5f }));
scene.add(pts);

const RED = new THREE.Color(0xff3b3f), WHITE = new THREE.Color(0xe8eaf2);
function update(t) {
  for (let i = 0; i < ROWS; i++) {
    const P = lines[i].geometry.attributes.position.array, Cc = lines[i].geometry.attributes.color.array, Wp = walls[i].geometry.attributes.position.array;
    const z = lines[i].userData.z;
    for (let j = 0; j < COLS; j++) {
      const [h, red] = height(i, j, t), x = X0 + j * DX;
      P[j * 3] = x; P[j * 3 + 1] = h; P[j * 3 + 2] = z;
      const c = WHITE.clone().lerp(RED, Math.min(1, red * 1.4));
      const k = 0.75 + 0.25 * Math.min(1, red * 2);
      Cc[j * 3] = c.r * k; Cc[j * 3 + 1] = c.g * k; Cc[j * 3 + 2] = c.b * k;
      Wp[j * 6] = x; Wp[j * 6 + 1] = -1; Wp[j * 6 + 2] = z - 0.001;
      Wp[j * 6 + 3] = x; Wp[j * 6 + 4] = h - 0.004; Wp[j * 6 + 5] = z - 0.001;
    }
    lines[i].geometry.attributes.position.needsUpdate = true; lines[i].geometry.attributes.color.needsUpdate = true;
    walls[i].geometry.attributes.position.needsUpdate = true;
  }
  const pp = pg.attributes.position.array;
  allPeaks.forEach((p, k) => { const [h] = height(p.i, p.j, t); pp[k * 3] = X0 + p.j * DX; pp[k * 3 + 1] = t > p.ts ? h + 0.12 : -20; pp[k * 3 + 2] = Z0 + p.i * DZ; });
  pg.attributes.position.needsUpdate = true;
  lineMat.opacity = pr(t, 0, .6);
  // cámara: vuelo rasante que se eleva para mostrar la escala
  const q = eio(clamp(t / DUR)), q2 = eio(pr(t, 4.4, 3.8));
  // vuelo rasante → vista cenital: desde arriba se ve que casi todo está vacío
  const p1 = new THREE.Vector3(lerp(-3.5, 0.5, q), lerp(1.8, 6, q), lerp(42, 40, q)), l1 = new THREE.Vector3(lerp(1.5, 0, q), lerp(0.6, -1, q), lerp(28, 22, q));
  cam.position.copy(p1.lerp(new THREE.Vector3(0, 62, 6), q2));
  const look = l1.lerp(new THREE.Vector3(0, 0, -2), q2);
  scene.fog.density = lerp(0.03, 0.011, q2);
  cam.lookAt(look);
  bokeh.uniforms.focus.value = cam.position.distanceTo(look);
}

// ---------------------------------------------------------------- composición con textos y subtítulos (lib.js)
function world(ctx, t) {
  update(t);
  composer.render();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.drawImage(R.domElement, 0, 0, W, H);
  const sh = ctx.createLinearGradient(0, 0, 0, 620); sh.addColorStop(0, 'rgba(5,5,7,0.92)'); sh.addColorStop(.7, 'rgba(5,5,7,0.6)'); sh.addColorStop(1, 'rgba(5,5,7,0)');
  ctx.fillStyle = sh; ctx.fillRect(0, 0, W, 620);
  text(ctx, 'HISTORIAS DE DATOS · EL NETFLIX PRIZE', 540, 150, { f: font(500, 22, MONO), c: 'rgba(220,224,235,0.6)', al: 'center', ls: 5 });
  const ca = pr(t, 1.2, .5) * (1 - pr(t, 4.6, .4));
  if (ca > 0) {
    text(ctx, fmt(100480507 * eo(pr(t, 1.2, 2.4))), 540, 380, { f: font(200, 118), c: '#fff', al: 'center', a: ca, ls: 2 });
    text(ctx, 'VALORACIONES · CADA PICO ES UNA NOTA DE 1 A 5', 540, 436, { f: font(500, 22, MONO), c: 'rgba(220,224,235,0.75)', al: 'center', ls: 3, a: ca });
  }
  const va = pr(t, 5.0, .5);
  if (va > 0) {
    text(ctx, '98,8 %', 540, 380, { f: font(200, 118), c: '#ff5a5f', al: 'center', a: va, ls: 2 });
    text(ctx, 'DE LA MATRIZ USUARIO × PELÍCULA, VACÍA', 540, 436, { f: font(500, 22, MONO), c: 'rgba(220,224,235,0.75)', al: 'center', ls: 3, a: va });
  }
}

window.STORY = {
  title: '', hud: false, grain: 0.14,
  scenes: [{ dur: DUR, draw: () => { } }],
  world,
  narr: [
    { scene: 0, a: .3, b: 4.2, text: 'Soltaron 100 millones de valoraciones reales de usuarios.' },
    { scene: 0, a: 4.8, b: 7.8, text: 'Y casi toda la matriz estaba vacía.' },
  ],
  events: [
    { scene: 0, at: 1.2, type: 'ticks', dur: 2.4, rate: 26 },
    { scene: 0, at: 5.0, type: 'swell', dur: 1.0 },
  ],
};
setup();
renderFrame(0);
