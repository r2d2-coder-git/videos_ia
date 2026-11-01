// Motor común para "Historias de datos": helpers de dibujo, compositor de escenas, HUD, grano y subtítulos.
// Cada historia define STORY = {title, scenes:[{dur, draw(ctx,t,T)}], narr:[{scene, text, a, b}], events:[...]}.
const W = 1080, H = 1920;
const C = {
  bg: '#09090b', ink: '#f2f1ee', mut: '#8b9099', dim: '#3a3e46', line: '#1d2026',
  red: '#e5383b', redD: '#5c1214', paper: '#eee7d7', cap: '#ff911e',
};
const SANS = '"SF Pro Display", -apple-system, system-ui, sans-serif';
const MONO = '"SF Mono", ui-monospace, Menlo, monospace';

const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const pr = (t, a, d) => clamp((t - a) / d);
const eo = x => 1 - Math.pow(1 - x, 3);
const eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const lerp = (a, b, p) => a + (b - a) * p;
function rng(seed) {
  return function () {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
const font = (w, s, f = SANS) => `${w} ${s}px ${f}`;
function text(ctx, s, x, y, o = {}) {
  ctx.save();
  ctx.globalAlpha *= (o.a ?? 1);
  ctx.font = o.f || font(600, 40); ctx.fillStyle = o.c || C.ink;
  ctx.textAlign = o.al || 'left'; ctx.textBaseline = o.bl || 'alphabetic';
  if (o.ls) ctx.letterSpacing = o.ls + 'px';
  ctx.fillText(s, x, y);
  ctx.restore();
}
function rrect(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
const ramp = (t, a, d) => eio(pr(t, a, d));
const tw = (ctx, s, f) => { ctx.save(); ctx.font = f; const w = ctx.measureText(s).width; ctx.restore(); return w; };
/** Parte `s` en líneas que caben en maxW con la fuente f. */
function wrapLines(ctx, s, f, maxW) {
  ctx.save(); ctx.font = f; const out = []; let l = '';
  for (const w of s.split(' ')) { const tt = l ? l + ' ' + w : w; if (ctx.measureText(tt).width > maxW && l) { out.push(l); l = w; } else l = tt; }
  if (l) out.push(l); ctx.restore(); return out;
}
const hexRGB = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16));
/** Mezcla dos colores '#rrggbb' (atenuar grupos de figuras sin globalAlpha, que dobla opacidad en los solapes). */
const mixColor = (a, b, p) => { const A = hexRGB(a), Bc = hexRGB(b); return `rgb(${A.map((v, i) => Math.round(lerp(v, Bc[i], p))).join(',')})`; };
const L2 = (A, B, p) => ({ x: lerp(A.x, B.x, p), y: lerp(A.y, B.y, p), s: lerp(A.s ?? 1, B.s ?? 1, p) });
/** Parpadeo determinista a partir de a0. */
const blink = (lt, a0 = 0) => lt < a0 ? 0 : 0.55 + 0.45 * Math.cos((lt - a0) * 7);
const fmt = n => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
function bg(ctx, gx, gy, gr, col) {
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  if (col) {
    const gd = ctx.createRadialGradient(gx, gy, 0, gx, gy, gr);
    gd.addColorStop(0, col); gd.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = gd; ctx.fillRect(0, 0, W, H);
  }
}
// Revela una línea de texto subiendo desde una máscara.
function maskLine(ctx, s, x, y, size, p, o = {}) {
  ctx.save();
  ctx.beginPath(); ctx.rect(0, y - size * 1.05, W, size * 1.35); ctx.clip();
  text(ctx, s, x, y + (1 - eo(p)) * size * 1.2, { ...o, a: (o.a ?? 1) * clamp(p * 3) });
  ctx.restore();
}

// ---------------------------------------------------------------- grano + viñeta (precalculados)
const GRAIN = [];
(function () {
  const r = rng(7);
  for (let k = 0; k < 6; k++) {
    const c = mk(540, 960), x = c.getContext('2d'), im = x.createImageData(540, 960);
    for (let i = 0; i < im.data.length; i += 4) {
      const v = 128 + (r() - .5) * 255;
      im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255;
    }
    x.putImageData(im, 0, 0); GRAIN.push(c);
  }
})();
const VIG = (function () {
  const c = mk(W, H), x = c.getContext('2d');
  const gd = x.createRadialGradient(W / 2, H * .45, H * .25, W / 2, H * .45, H * .75);
  gd.addColorStop(0, 'rgba(0,0,0,0)'); gd.addColorStop(1, 'rgba(0,0,0,0.6)');
  x.fillStyle = gd; x.fillRect(0, 0, W, H); return c;
})();

// ---------------------------------------------------------------- subtítulos (estilo reel aprobado)
let CAPS = [];
function buildCaptions(narr, starts) {
  // Reparte cada frase entre a..b proporcional a la longitud, con pausa tras puntuación; trozos de 1-3 palabras.
  CAPS = [];
  for (const n of narr) {
    const t0 = starts[n.scene] + n.a, t1 = starts[n.scene] + n.b;
    const words = n.text.split(/\s+/);
    const wt = words.map(w => w.length + 3 + (/[.,:;?!]$/.test(w) ? 6 : 0));
    const tot = wt.reduce((a, b) => a + b, 0);
    let acc = t0, chunk = [];
    const flush = () => { if (chunk.length) CAPS.push(chunk); chunk = []; };
    words.forEach((w, i) => {
      const d = (t1 - t0) * wt[i] / tot;
      chunk.push({ w, a: acc, b: acc + d }); acc += d;
      if (chunk.length >= 3 || /[.,:;?!]$/.test(w) || (chunk.length >= 2 && w.length > 9)) flush();
    });
    flush();
  }
}
// ---------------------------------------------------------------- voz: anclar planos a palabras (voz.tiempos.json de voz.py)
const _limpia = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9ñ% ]+/g, ' ').trim().split(/\s+/).filter(Boolean);
function crearTiempos(v) {
  const pal = v.palabras.map(w => ({ ...w, l: _limpia(w.p).join(' ') }));
  /** Segundo en que empieza a decirse `texto` (una o varias palabras seguidas), buscando desde `desde`. */
  const en = (texto, desde = 0) => {
    const q = _limpia(texto);
    for (let i = 0; i < pal.length; i++) {
      if (pal[i].ini < desde - 0.01) continue;
      if (q.every((w, k) => pal[i + k] && pal[i + k].l === w)) return pal[i].ini;
    }
    throw new Error(`No encuentro «${texto}» en la voz a partir de ${desde} s`);
  };
  /** Segundo en que termina de decirse `texto`. */
  const fin = (texto, desde = 0) => { const a = en(texto, desde), i = pal.findIndex(w => w.ini === a); return pal[i + _limpia(texto).length - 1].fin; };
  return { en, fin, palabras: v.palabras, frases: v.frases, duracion: v.duracion, provisional: v.provisional };
}
async function cargarVoz(url = 'voz.tiempos.json') { return crearTiempos(await (await fetch(url)).json()); }
// Subtítulos con los tiempos reales: trozos de 1-3 palabras que cortan en la puntuación.
function captionsFromWords(palabras, skip = []) {
  CAPS = []; let chunk = [];
  const flush = () => { if (chunk.length) CAPS.push(chunk); chunk = []; };
  palabras.forEach((w, i) => {
    if (skip.some(([a, b]) => w.ini >= a && w.ini < b)) { flush(); return; }
    if (chunk.length && w.ini - chunk[chunk.length - 1].b > 0.45) flush();
    chunk.push({ w: w.p, a: w.ini, b: Math.max(w.fin, (palabras[i + 1]?.ini ?? w.fin)) });
    if (chunk.length >= 3 || /[.,:;?!…]$/.test(w.p) || (chunk.length >= 2 && w.p.length > 9)) flush();
  });
  flush();
}

// ---------------------------------------------------------------- tu cara (hueco hasta que haya grabación)
// Con grabación: cara.mp4 (H.264, 1080×1920) junto a la historia; se dibuja el fotograma del segundo t.
let CARA = null;
async function cargarCara(url = 'cara.mp4') {
  const r = await fetch(url, { method: 'HEAD' }); if (!r.ok) return null;
  const v = document.createElement('video'); v.src = url; v.muted = true; v.preload = 'auto';
  await new Promise(res => v.addEventListener('loadeddata', res, { once: true })); CARA = v; window.CARA = v; return v;
}
async function seekCara(t) {
  if (!CARA) return;
  CARA.currentTime = Math.min(t, CARA.duration - 0.05);
  await new Promise(res => CARA.addEventListener('seeked', res, { once: true }));
}
/** Pinta la cara en el rectángulo (x,y,w,h), recortada tipo "cover". Sin grabación: un hueco marcado. */
function drawCara(ctx, x, y, w, h, o = {}) {
  ctx.save(); rrect(ctx, x, y, w, h, o.r ?? 0); ctx.clip();
  if (CARA) {
    const vw = CARA.videoWidth, vh = CARA.videoHeight, s = Math.max(w / vw, h / vh) * (o.zoom ?? 1);
    ctx.drawImage(CARA, x + (w - vw * s) / 2, y + (h - vh * s) / 2 + (o.dy ?? 0), vw * s, vh * s);
  } else {
    const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#2a2c33'); g.addColorStop(1, '#141519');
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const cx = x + w / 2, cy = y + h * 0.48, s = Math.min(w, h) / 900;
    ctx.fillStyle = 'rgba(255,255,255,0.10)';
    ctx.beginPath(); ctx.arc(cx, cy - 120 * s, 120 * s, 0, 7); ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx, cy + 260 * s, 260 * s, 200 * s, 0, Math.PI, 0); ctx.fill();
    text(ctx, 'TU CARA', cx, y + h * 0.66, { f: font(800, Math.max(28, 54 * s)), c: 'rgba(255,255,255,0.55)', al: 'center', ls: 6 });
    text(ctx, 'hueco para la grabación', cx, y + h * 0.66 + Math.max(26, 44 * s), { f: font(400, Math.max(18, 24 * s), MONO), c: 'rgba(255,255,255,0.35)', al: 'center' });
  }
  ctx.restore();
}

function drawCaptions(ctx, t) {
  const ch = CAPS.find(c => t >= c[0].a && t < c[c.length - 1].b + 0.12);
  if (!ch) return;
  let size = 78;
  ctx.font = font(900, size);
  const sp = size * .28;
  const ws = ch.map(c => c.w.toUpperCase());
  let tw = ws.reduce((s, w) => s + ctx.measureText(w).width, 0) + sp * (ws.length - 1);
  if (tw > 940) { size = Math.floor(size * 940 / tw); ctx.font = font(900, size); tw = ws.reduce((s, w) => s + ctx.measureText(w).width, 0) + size * .28 * (ws.length - 1); }
  const pop = 0.92 + 0.08 * eo(pr(t, ch[0].a, 0.09));
  ctx.save();
  ctx.translate(W / 2, 1490); ctx.scale(pop, pop);
  ctx.textBaseline = 'middle'; ctx.lineJoin = 'round'; ctx.lineWidth = 14; ctx.strokeStyle = '#000';
  let x = -tw / 2;
  ws.forEach((w, i) => {
    const wd = ctx.measureText(w).width;
    ctx.strokeText(w, x, 0);
    ctx.fillStyle = (t >= ch[i].a && t < ch[i].b) ? C.cap : '#fff';
    ctx.fillText(w, x, 0);
    x += wd + size * .28;
  });
  ctx.restore();
}

// ---------------------------------------------------------------- HUD superior
function drawHUD(ctx, t, idx, sp, title) {
  const a = clamp(t / 0.6);
  text(ctx, 'HISTORIAS DE DATOS', 70, 142, { f: font(600, 24, MONO), c: C.ink, ls: 4, a });
  text(ctx, title, 1010, 142, { f: font(400, 24, MONO), c: C.mut, ls: 2, al: 'right', a });
  const n = STORY.scenes.length, gap = 10, w = (940 - gap * (n - 1)) / n;
  for (let i = 0; i < n; i++) {
    const x = 70 + i * (w + gap);
    ctx.globalAlpha = a;
    ctx.fillStyle = 'rgba(255,255,255,0.16)'; ctx.fillRect(x, 166, w, 4);
    const f = i < idx ? 1 : i === idx ? sp : 0;
    ctx.fillStyle = C.red; ctx.fillRect(x, 166, w * f, 4);
    ctx.globalAlpha = 1;
  }
}

// ---------------------------------------------------------------- compositor
const S = [mk(W, H), mk(W, H)];
let STARTS = [], TOTAL = 0;
function setup() {
  let acc = 0; STARTS = STORY.scenes.map(s => { const a = acc; acc += s.dur; return a; }); TOTAL = acc;
  if (STORY.voz) captionsFromWords(STORY.voz.palabras, STORY.sinSubtitulos || []);
  else buildCaptions(STORY.narr || [], STARTS);
  window.TIMELINE = {
    total: TOTAL, starts: STARTS, fps: 30,
    events: (STORY.events || []).map(e => ({ ...e, t: e.t ?? (STARTS[e.scene] + e.at) })),
    voz: !!STORY.voz, provisional: !!STORY.voz?.provisional,
  };
}
function drawScene(ctx, buf, i, t, alpha) {
  const sc = STORY.scenes[i], lt = Math.max(0, t - STARTS[i]);
  const b = buf.getContext('2d');
  b.setTransform(1, 0, 0, 1, 0, 0); b.globalAlpha = 1; b.globalCompositeOperation = 'source-over';
  sc.draw(b, lt, sc.dur);
  // empuje de cámara lento
  const z = 1 + 0.03 * clamp(lt / sc.dur);
  ctx.save(); ctx.globalAlpha = alpha;
  ctx.translate(W / 2, H * .42); ctx.scale(z, z); ctx.translate(-W / 2, -H * .42);
  ctx.drawImage(buf, 0, 0); ctx.restore();
}
function renderFrame(t, frame = 0) {
  const ctx = document.getElementById('c').getContext('2d');
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
  let i = STARTS.findIndex((s, k) => t >= s && t < s + STORY.scenes[k].dur);
  if (i < 0) i = STORY.scenes.length - 1;
  if (STORY.world) {
    // modo mundo continuo: la historia define cámara + mundo; desenfoque de movimiento en los barridos
    const k = STORY.blurSamples ? STORY.blurSamples(t) : 1;
    if (k <= 1) STORY.world(ctx, t);
    else {
      const b = S[0].getContext('2d');
      for (let s = 0; s < k; s++) {
        b.setTransform(1, 0, 0, 1, 0, 0); b.globalAlpha = 1;
        STORY.world(b, t - 0.05 * s / (k - 1));
        ctx.globalAlpha = 1 / (s + 1); ctx.drawImage(S[0], 0, 0);
      }
      ctx.globalAlpha = 1;
    }
  } else {
    const XF = 0.22;
    drawScene(ctx, S[0], i, t, 1);
    const nx = i + 1 < STARTS.length ? STARTS[i + 1] : Infinity;
    if (t > nx - XF) drawScene(ctx, S[1], i + 1, t, eio(pr(t, nx - XF, XF)));
  }
  // grano y viñeta
  ctx.save(); ctx.globalCompositeOperation = 'soft-light'; ctx.globalAlpha = STORY.grain ?? 0.22;
  ctx.drawImage(GRAIN[frame % GRAIN.length], 0, 0, W, H); ctx.restore();
  if (STORY.vignette !== false) ctx.drawImage(VIG, 0, 0);
  const sp = clamp((t - STARTS[i]) / STORY.scenes[i].dur);
  if (STORY.hud !== false) drawHUD(ctx, t, i, sp, STORY.title);
  drawCaptions(ctx, t);
  // fundido de salida
  const fo = pr(t, TOTAL - 0.5, 0.5);
  if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return true;
}
window.renderFrame = renderFrame;
