// Historia 01 · El Netflix Prize (v2): un tablero de investigación continuo.
// Cada momento es una "evidencia" clavada en el tablero; la cámara viaja de una a otra siguiendo un hilo rojo.

const INK = '#1c1a17', SOFT = '#76695a', PAPER = '#ece5d4', PAPER2 = '#e4dcc8';
const BEATS = [4.4, 10.5, 9.4, 7.6, 9.8, 8.0, 9.2, 8.0];
const B = []; { let a = 0; for (const d of BEATS) { B.push(a); a += d; } }

// ---------------------------------------------------------------- texturas
function noiseCanvas(n, seed, lo, hi, alpha) {
  const c = mk(n, n), x = c.getContext('2d'), im = x.createImageData(n, n), r = rng(seed);
  for (let i = 0; i < im.data.length; i += 4) { const v = lo + r() * (hi - lo); im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = alpha; }
  x.putImageData(im, 0, 0); return c;
}
const PAPER_TEX = noiseCanvas(256, 2, 150, 255, 255);
const BOARD_TEX = noiseCanvas(256, 9, 0, 40, 255);
let PAPER_PAT = null, BOARD_PAT = null;

// ---------------------------------------------------------------- piezas reutilizables
function wrap(ctx, s, maxW) {
  const out = []; let line = '';
  for (const w of s.split(' ')) { const tt = line ? line + ' ' + w : w; if (ctx.measureText(tt).width > maxW && line) { out.push(line); line = w; } else line = tt; }
  if (line) out.push(line); return out;
}
function para(ctx, s, x, y, maxW, lh, o) {
  ctx.save(); ctx.font = o.f; const ls = wrap(ctx, s, maxW); ctx.restore();
  ls.forEach((l, i) => text(ctx, l, x, y + i * lh, o)); return ls.length;
}
function pin(ctx, x, y) {
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.5)'; ctx.shadowBlur = 6; ctx.shadowOffsetY = 4;
  const g = ctx.createRadialGradient(x - 3, y - 3, 1, x, y, 10);
  g.addColorStop(0, '#ff8a8a'); g.addColorStop(.5, C.red); g.addColorStop(1, '#7a1214');
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, 10, 0, 7); ctx.fill(); ctx.restore();
}
function tape(ctx, x, y, w, rot) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.fillStyle = 'rgba(232,214,160,0.75)'; ctx.fillRect(-w / 2, -14, w, 28); ctx.restore();
}
// Papel con sombra y textura. contenido en coords locales centradas. p = progreso de aparición (cae sobre el tablero).
function paper(ctx, x, y, w, h, rot, p, draw, o = {}) {
  if (p <= 0) return;
  const q = eo(p);
  ctx.save(); ctx.translate(x, y - 30 * (1 - q)); ctx.rotate(rot + (1 - q) * 0.06); const s = lerp(1.1, 1, q); ctx.scale(s, s);
  ctx.globalAlpha *= clamp(p * 2.5);
  ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = lerp(60, 26, q); ctx.shadowOffsetY = lerp(40, 14, q);
  ctx.fillStyle = o.col || PAPER; ctx.fillRect(-w / 2, -h / 2, w, h);
  ctx.shadowColor = 'transparent';
  if (!o.dark) { ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha *= .35; ctx.fillStyle = PAPER_PAT; ctx.fillRect(-w / 2, -h / 2, w, h); ctx.restore(); }
  if (o.band) { ctx.fillStyle = o.band; ctx.fillRect(-w / 2, -h / 2, w, o.bandH || 46); }
  draw && draw(ctx);
  if (o.tape) { tape(ctx, -w / 2 + 30, -h / 2 + 4, 110, -0.6); tape(ctx, w / 2 - 30, -h / 2 + 4, 110, 0.6); }
  else if (o.pin !== false) pin(ctx, 0, -h / 2 + 22);
  ctx.restore();
}
function tag(ctx, x, y, s, p) {
  if (p <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.rotate(-0.02); ctx.globalAlpha *= clamp(p * 2);
  ctx.font = font(600, 22, MONO); ctx.letterSpacing = '3px'; const w = ctx.measureText(s).width + 36;
  ctx.fillStyle = '#f2efe8'; ctx.fillRect(0, -22, w * eo(p), 44);
  ctx.beginPath(); ctx.rect(0, -22, w * eo(p), 44); ctx.clip();
  text(ctx, s, 18, 1, { f: font(600, 22, MONO), c: INK, bl: 'middle', ls: 3 });
  ctx.restore();
}
function stamp(ctx, x, y, s, rot, p, size = 64, col = C.red) {
  if (p <= 0) return;
  const q = pr(p, 0, 1), sc = lerp(2.4, 1, Math.min(1, q * q * 4));
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc); ctx.globalAlpha *= clamp(q * 5) * .92;
  ctx.font = font(900, size); ctx.letterSpacing = '4px'; const w = ctx.measureText(s).width + 50, h = size * 1.45;
  ctx.strokeStyle = col; ctx.lineWidth = 7; ctx.strokeRect(-w / 2, -h / 2, w, h);
  text(ctx, s, 0, 4, { f: font(900, size), c: col, al: 'center', bl: 'middle', ls: 4 });
  ctx.restore();
}
// trazo de rotulador que se dibuja
function marker(ctx, pts, p, col = C.red, w = 9) {
  if (p <= 0) return;
  ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.globalAlpha *= .9;
  let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  ctx.setLineDash([L, L]); ctx.lineDashOffset = L * (1 - eio(p));
  ctx.beginPath(); ctx.moveTo(...pts[0]); for (let i = 1; i < pts.length; i++) ctx.lineTo(...pts[i]); ctx.stroke(); ctx.restore();
}

// ---------------------------------------------------------------- iconos de línea (sobrios)
function icon(ctx, kind, x, y, s, col = INK) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 3.5; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  const person = (px, py) => { ctx.beginPath(); ctx.arc(px, py - 34, 14, 0, 7); ctx.stroke(); ctx.beginPath(); ctx.moveTo(px - 26, py + 20); ctx.quadraticCurveTo(px, py - 22, px + 26, py + 20); ctx.stroke(); };
  if (kind === 'math') {
    ctx.strokeRect(-56, -48, 112, 70); text(ctx, 'Σ x²', 0, -12, { f: font(600, 30, MONO), c: col, al: 'center', bl: 'middle' });
    ctx.beginPath(); ctx.moveTo(-30, 22); ctx.lineTo(-40, 48); ctx.moveTo(30, 22); ctx.lineTo(40, 48); ctx.stroke();
  } else if (kind === 'student') {
    person(0, 18);
    ctx.beginPath(); ctx.moveTo(-34, -46); ctx.lineTo(0, -60); ctx.lineTo(34, -46); ctx.lineTo(0, -32); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(26, -46); ctx.lineTo(26, -28); ctx.stroke();
  } else if (kind === 'garage') {
    ctx.beginPath(); ctx.moveTo(-58, -6); ctx.lineTo(0, -52); ctx.lineTo(58, -6); ctx.moveTo(-48, -14); ctx.lineTo(-48, 46); ctx.lineTo(48, 46); ctx.lineTo(48, -14); ctx.stroke();
    for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.moveTo(-34, -6 + i * 10); ctx.lineTo(34, -6 + i * 10); ctx.stroke(); }
    ctx.strokeRect(-20, 22, 40, 18); ctx.beginPath(); ctx.moveTo(-28, 44); ctx.lineTo(28, 44); ctx.stroke();
  } else if (kind === 'engineer') {
    ctx.strokeRect(14, -40, 62, 44); ctx.beginPath(); ctx.moveTo(45, 4); ctx.lineTo(45, 16); ctx.moveTo(-70, 16); ctx.lineTo(90, 16); ctx.stroke();
    ctx.beginPath(); ctx.arc(-34, -24, 14, 0, 7); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-58, 16); ctx.quadraticCurveTo(-34, -20, -10, 16); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-54, -2); ctx.lineTo(-50, -34); ctx.moveTo(-14, -2); ctx.lineTo(-18, -34); ctx.stroke();
    ctx.lineWidth = 2.5; for (const [a, b] of [[-52, -52], [-34, -58], [-16, -52]]) { ctx.beginPath(); ctx.moveTo(a, b); ctx.lineTo(a + (a + 34) * .15, b - 8); ctx.stroke(); }
  }
  ctx.restore();
}

// ---------------------------------------------------------------- mapa de puntos (precalculado)
const LAND = [
  [[-168, 66], [-140, 70], [-100, 72], [-80, 70], [-62, 60], [-55, 50], [-66, 44], [-76, 37], [-81, 30], [-81, 25], [-97, 26], [-105, 21], [-95, 16], [-85, 11], [-78, 8], [-90, 14], [-106, 21], [-113, 31], [-119, 34], [-124, 41], [-126, 49], [-136, 58], [-152, 60], [-166, 60]],
  [[-55, 60], [-44, 60], [-22, 70], [-20, 80], [-60, 82], [-72, 77]],
  [[-78, 9], [-60, 11], [-50, 1], [-35, -6], [-40, -22], [-49, -29], [-58, -38], [-66, -55], [-73, -50], [-72, -30], [-71, -18], [-81, -5]],
  [[-10, 36], [-1, 43], [-5, 48], [1, 50], [8, 54], [10, 58], [5, 62], [15, 70], [30, 71], [42, 66], [42, 45], [28, 41], [22, 40], [13, 38], [15, 45], [8, 44], [-2, 36]],
  [[-6, 50], [2, 51], [0, 58], [-6, 58]],
  [[-17, 21], [-10, 33], [10, 37], [32, 31], [43, 12], [51, 12], [41, -4], [40, -15], [34, -26], [20, -35], [14, -24], [12, -5], [8, 4], [-8, 5], [-17, 14]],
  [[42, 45], [42, 66], [70, 73], [110, 77], [140, 72], [170, 69], [180, 65], [160, 58], [140, 54], [135, 43], [122, 40], [122, 30], [110, 20], [108, 10], [101, 2], [98, 15], [92, 22], [80, 8], [73, 20], [60, 25], [50, 30], [36, 35]],
  [[35, 30], [48, 30], [57, 24], [53, 15], [43, 12], [35, 28]],
  [[114, -22], [122, -18], [130, -12], [137, -12], [142, -11], [146, -19], [153, -27], [150, -37], [140, -38], [132, -32], [115, -34]],
  [[130, 31], [141, 36], [142, 45], [140, 41]], [[95, 5], [105, -6], [120, -8], [140, -4], [120, 2]],
];
function inPoly(x, y, P) { let c = false; for (let i = 0, j = P.length - 1; i < P.length; j = i++) { const [xi, yi] = P[i], [xj, yj] = P[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; }
const MAPW = 820, MAPH = 400;
const LANDPTS = [];
const MAPIMG = (function () {
  const c = mk(MAPW, MAPH), x = c.getContext('2d');
  for (let lat = 78; lat > -58; lat -= 3) for (let lon = -177; lon < 180; lon += 3) {
    if (!LAND.some(P => inPoly(lon, lat, P))) continue;
    const px = (lon + 180) / 360 * MAPW, py = (80 - lat) / 140 * MAPH;
    LANDPTS.push([px, py]); x.fillStyle = 'rgba(28,26,23,0.55)'; x.beginPath(); x.arc(px, py, 2.6, 0, 7); x.fill();
  }
  return c;
})();
const MAPPINS = (function () { const r = rng(33); return Array.from({ length: 186 }, () => ({ p: LANDPTS[Math.floor(r() * LANDPTS.length)], ts: .4 + r() * 2.8 })); })();

// ---------------------------------------------------------------- estaciones (centro en el mundo + inicio de su tiempo local)
const ST = [
  { x: 0, y: 0, t0: B[0], pin: [8, -193] },
  { x: 1150, y: 300, t0: B[1], pin: [-205, -453] },
  { x: 2300, y: 0, t0: B[2], pin: [-6, -423] },
  { x: 2300, y: 1300, t0: B[2] + 5.6, pin: [0, 17] },
  { x: 1150, y: 1650, t0: B[3], pin: [-207, -428] },
  { x: 0, y: 1450, t0: B[4], pin: [-5, -468] },
  { x: 0, y: 2800, t0: B[5], pin: [-220, -360], own: true },
  { x: 1150, y: 3050, t0: B[6], pin: [4, -428] },
];

// 1 · el premio --------------------------------------------------------------
const SIG = [[-60, 150], [-20, 105], [10, 160], [40, 110], [55, 150], [90, 120], [120, 160], [150, 115], [200, 150], [260, 132], [330, 140]];
function st1(ctx, t) {
  tag(ctx, -470, -470, 'EVIDENCIA 01 — EL PREMIO', pr(t, .3, .5));
  paper(ctx, 0, 0, 920, 430, -0.04, pr(t, 0, .6), c => {
    c.save(); c.beginPath(); c.rect(-460, -215, 920, 430); c.clip();
    c.strokeStyle = 'rgba(130,95,60,.10)'; c.lineWidth = 1.4;
    for (let k = 0; k < 20; k++) { c.beginPath(); for (let x = -460; x <= 460; x += 8) { const y = -215 + k * 23 + 7 * Math.sin(x / 38 + k * .9); x === -460 ? c.moveTo(x, y) : c.lineTo(x, y); } c.stroke(); }
    c.fillStyle = C.red; c.fillRect(-460, -215, 16, 430); c.restore();
    text(c, 'NETFLIX PRIZE', -405, -138, { f: font(800, 36), c: INK, ls: 5 });
    text(c, 'Nº 000001', 415, -140, { f: font(500, 22, MONO), c: SOFT, al: 'right' });
    text(c, 'FECHA  21 · 09 · 2009', 415, -104, { f: font(500, 22, MONO), c: SOFT, al: 'right' });
    text(c, 'PÁGUESE A', -405, -48, { f: font(500, 20, MONO), c: SOFT, ls: 2 });
    text(c, "BellKor's Pragmatic Chaos", -405, 2, { f: font(600, 40), c: INK });
    c.fillStyle = SOFT; c.fillRect(-405, 16, 520, 2);
    rrect(c, 150, -84, 265, 74, 6); c.lineWidth = 3; c.strokeStyle = INK; c.stroke();
    text(c, '$1.000.000', 282, -34, { f: font(700, 38, MONO), c: INK, al: 'center' });
    text(c, 'Un millón de dólares ——————', -405, 96, { f: 'italic 400 32px Georgia, serif', c: INK });
    const sp = eio(pr(t, .7, 1.1));
    c.beginPath(); c.moveTo(SIG[0][0] + 170, SIG[0][1] - 10);
    for (let i = 1; i < SIG.length; i++) { const [a, b] = SIG[i - 1], [cc, d] = SIG[i]; c.quadraticCurveTo(a + 170, b - 10, (a + cc) / 2 + 170, (b + d) / 2 - 10); }
    c.setLineDash([900, 900]); c.lineDashOffset = 900 * (1 - sp); c.lineWidth = 3.2; c.strokeStyle = '#20305a'; c.lineCap = 'round'; c.stroke(); c.setLineDash([]);
    c.fillStyle = SOFT; c.fillRect(130, 168, 285, 2);
    text(c, 'FIRMA', 130, 194, { f: font(500, 18, MONO), c: SOFT, ls: 2 });
    stamp(c, 20, 10, 'NUNCA SE USÓ', -0.18, pr(t, 2.75, .9), 84);
  });
}

// 2 · el concurso --------------------------------------------------------------
const POSTERS = [{ x: 140, n: 'Película A', v: 4 }, { x: 250, n: 'Película B', v: 2 }, { x: 360, n: 'Película C', v: 5 }];
const MX = { cols: 20, rows: 11, cell: 30, ox: -300, oy: 10 };   // relativo a la estación
const FLY = (function () {
  const r = rng(21), cells = []; for (let i = 0; i < MX.cols * MX.rows; i++) cells.push(i);
  for (let i = cells.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1));[cells[i], cells[j]] = [cells[j], cells[i]]; }
  return cells.slice(0, 70).map(cl => { const P = POSTERS[Math.floor(r() * 3)]; return { cx: MX.ox + (cl % MX.cols) * MX.cell + 15, cy: MX.oy + Math.floor(cl / MX.cols) * MX.cell + 15, sx: P.x - 20 + r() * 40, sy: -240, ts: 5.6 + r() * 1.6, v: 1 + Math.floor(r() * 5) }; });
})();
const FINE = (function () {
  const c = mk(300, 300), x = c.getContext('2d'), r = rng(5), n = 6;
  x.fillStyle = PAPER2; x.fillRect(0, 0, 300, 300);
  x.fillStyle = 'rgba(28,26,23,0.10)'; for (let i = 0; i < 300; i += n) for (let j = 0; j < 300; j += n) x.fillRect(i + 1, j + 1, n - 2, n - 2);
  x.fillStyle = C.red; for (let k = 0; k < 30; k++) x.fillRect(Math.floor(r() * 50) * n + 1, Math.floor(r() * 50) * n + 1, n - 2, n - 2);
  return c;
})();
function st2(ctx, t) {
  tag(ctx, -470, -520, 'EVIDENCIA 02 — EL CONCURSO', pr(t, 0, .5));
  paper(ctx, -200, -330, 540, 290, -0.03, pr(t, .2, .6), c => {
    text(c, 'NETFLIX PRIZE · OCTUBRE 2006', -240, -105, { f: font(700, 22, MONO), c: '#fff', ls: 2 });
    para(c, '1.000.000 $ para quien mejore un 10 % las recomendaciones de Netflix.', -240, -30, 480, 40, { f: font(700, 32), c: INK });
    text(c, 'Métrica: RMSE frente a Cinematch', -240, 100, { f: font(400, 20, MONO), c: SOFT });
    marker(c, [[-240, 52], [-60, 50]], pr(t, 2.0, .5), C.red, 6);
  }, { band: C.red, bandH: 52 });
  // monitor con usuarios valorando
  const ma = pr(t, 2.4, .5);
  if (ma > 0) {
    ctx.save(); ctx.globalAlpha *= clamp(ma * 2); ctx.translate(0, 20 * (1 - eo(ma)));
    ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 14;
    rrect(ctx, 70, -440, 360, 250, 14); ctx.fillStyle = '#26282d'; ctx.fill(); ctx.shadowColor = 'transparent';
    rrect(ctx, 84, -426, 332, 200, 6); ctx.fillStyle = '#0e0f12'; ctx.fill();
    ctx.fillStyle = '#26282d'; ctx.fillRect(235, -190, 30, 26); ctx.fillRect(200, -166, 100, 8);
    text(ctx, 'usuarios valorando', 250, -406, { f: font(400, 15, MONO), c: C.mut, al: 'center' });
    POSTERS.forEach((P, i) => {
      const g = ctx.createLinearGradient(0, -390, 0, -290); g.addColorStop(0, ['#5a2a2c', '#2b3a52', '#3d4a2c'][i]); g.addColorStop(1, '#111');
      ctx.fillStyle = g; ctx.fillRect(P.x - 42, -390, 84, 112);
      text(ctx, P.n, P.x, -296, { f: font(600, 12), c: '#ddd', al: 'center' });
      for (let k = 0; k < 5; k++) { const on = k < P.v && t > 3.0 + i * .5 + k * .12; text(ctx, '★', P.x - 34 + k * 17, -256, { f: font(400, 17), c: on ? '#f5c451' : '#444', al: 'center', bl: 'middle' }); }
    });
    ctx.restore();
  }
  // hoja de la matriz
  paper(ctx, 0, 190, 720, 560, 0.01, pr(t, 4.6, .6), c => {
    text(c, 'MATRIZ DE VALORACIONES', -330, -235, { f: font(700, 22, MONO), c: INK, ls: 2 });
    text(c, 'una fila por usuario · una columna por película', -330, -205, { f: font(400, 18, MONO), c: SOFT });
    c.strokeStyle = 'rgba(28,26,23,0.16)'; c.lineWidth = 1;
    for (let i = 0; i < MX.cols; i++) for (let j = 0; j < MX.rows; j++) c.strokeRect(MX.ox + i * MX.cell + 2.5, MX.oy - 190 + j * MX.cell + 2.5, MX.cell - 5, MX.cell - 5);
    const cA = pr(t, 5.8, .4) * (1 - pr(t, 8.0, .3));
    if (cA > 0) {
      text(c, fmt(100480507 * eo(pr(t, 5.8, 1.6))), -330, 232, { f: font(800, 46), c: INK, a: cA });
      text(c, 'valoraciones reales', 30, 230, { f: font(400, 20, MONO), c: SOFT, a: cA });
    }
    const vA = pr(t, 8.0, .4);
    if (vA > 0) {
      text(c, '98,8 %', -330, 232, { f: font(800, 46), c: C.red, a: vA });
      text(c, 'de las celdas, vacías', -150, 230, { f: font(400, 20, MONO), c: SOFT, a: vA });
    }
  }, { pin: false, tape: true });
  // valoraciones volando a la matriz
  for (const s of FLY) {
    const p = pr(t, s.ts, 1.0); if (p <= 0) continue;
    const cy = s.cy + 190 - 190;
    if (p < 1) { const q = eio(p); text(ctx, '★', lerp(s.sx, s.cx, q), lerp(s.sy, cy, q) - Math.sin(q * Math.PI) * 120, { f: font(400, 30 - 10 * q), c: '#f5c451', al: 'center', bl: 'middle' }); }
    else {
      ctx.fillStyle = `rgba(229,56,59,${0.3 + 0.14 * s.v})`; ctx.fillRect(s.cx - 12, cy - 12, 24, 24);
      text(ctx, String(s.v), s.cx, cy + 1, { f: font(700, 14, MONO), c: '#fff', al: 'center', bl: 'middle' });
    }
  }
  // lupa: a escala real casi todo está vacío
  const la = pr(t, 8.0, .5);
  if (la > 0) {
    const lx = 200, ly = 120, R = 150 * eo(la);
    ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 30;
    ctx.beginPath(); ctx.arc(lx, ly, R, 0, 7); ctx.fillStyle = PAPER2; ctx.fill(); ctx.shadowColor = 'transparent'; ctx.clip();
    ctx.drawImage(FINE, lx - 150, ly - 150); ctx.restore();
    ctx.save(); ctx.strokeStyle = '#2a2c31'; ctx.lineWidth = 14; ctx.beginPath(); ctx.arc(lx, ly, R, 0, 7); ctx.stroke();
    ctx.lineCap = 'round'; ctx.lineWidth = 22; ctx.beginPath(); ctx.moveTo(lx + R * .72, ly + R * .72); ctx.lineTo(lx + R * 1.2, ly + R * 1.2); ctx.stroke(); ctx.restore();
  }
}

// 3 · la carrera --------------------------------------------------------------
function st3(ctx, t) {
  tag(ctx, -470, -520, 'EVIDENCIA 03 — LA CARRERA', pr(t, 0, .5));
  paper(ctx, 0, -210, 900, 470, 0.015, pr(t, .1, .6), c => {
    text(c, 'PARTICIPANTES POR PAÍS', -420, -192, { f: font(700, 20, MONO), c: INK, ls: 2 });
    c.drawImage(MAPIMG, -MAPW / 2, -MAPH / 2 + 25);
    for (const m of MAPPINS) {
      const k = pr(t, m.ts, .5); if (k <= 0) continue;
      const x = m.p[0] - MAPW / 2, y = m.p[1] - MAPH / 2 + 25;
      c.fillStyle = C.red; c.beginPath(); c.arc(x, y, 4.5, 0, 7); c.fill();
      if (k < 1) { c.strokeStyle = `rgba(229,56,59,${1 - k})`; c.lineWidth = 2; c.beginPath(); c.arc(x, y, 4 + 18 * eo(k), 0, 7); c.stroke(); }
    }
  });
  const cnt = eo(pr(t, .4, 3.0));
  paper(ctx, -250, 95, 330, 130, -0.04, pr(t, .5, .5), c => {
    text(c, fmt(40000 * cnt) + (cnt > .99 ? '+' : ''), 0, 8, { f: font(800, 52), c: INK, al: 'center' });
    text(c, 'EQUIPOS', 0, 44, { f: font(600, 18, MONO), c: SOFT, al: 'center', ls: 3 });
  }, { pin: false, tape: true, col: '#f3e7a6' });
  paper(ctx, 250, 95, 330, 130, 0.035, pr(t, .7, .5), c => {
    text(c, String(MAPPINS.filter(m => t >= m.ts).length), 0, 8, { f: font(800, 52), c: C.red, al: 'center' });
    text(c, 'PAÍSES', 0, 44, { f: font(600, 18, MONO), c: SOFT, al: 'center', ls: 3 });
  }, { pin: false, tape: true, col: '#f3e7a6' });
  [['math', 'Matemáticos', -310, 3.3], ['student', 'Estudiantes', 0, 3.9], ['garage', 'Gente en su garaje', 310, 4.5]].forEach(([k, n, x, a], i) => {
    paper(ctx, x, 345, 270, 270, [-0.05, 0.02, 0.06][i], pr(t, a, .5), c => {
      c.fillStyle = '#d9d0bb'; c.fillRect(-115, -112, 230, 170);
      icon(c, k, 0, -26, 1.1);
      text(c, n, 0, 98, { f: font(600, 24), c: INK, al: 'center' });
    });
  });
}

// 4 · tres años hasta el 10 % ---------------------------------------------------
function st4(ctx, t) {
  tag(ctx, -470, -470, 'EVIDENCIA 04 — TRES AÑOS', pr(t, -.4, .5));
  const K = [[.2, .8, 0, 8.43, '2007'], [1.0, .8, 8.43, 9.44, '2008'], [1.8, .8, 9.44, 10.06, '2009']];
  K.forEach(([a, , , v1, y], i) => {
    paper(ctx, -300 + i * 300, -280, 240, 250, [-0.04, 0.02, -0.02][i], pr(t, a - .3, .5), c => {
      text(c, 'AÑO', 0, -95, { f: font(700, 20, MONO), c: '#fff', al: 'center', ls: 4 });
      text(c, y, 0, 10, { f: font(800, 78), c: INK, al: 'center' });
      text(c, v1.toFixed(2).replace('.', ',') + ' %', 0, 78, { f: font(700, 30, MONO), c: i === 2 ? C.red : SOFT, al: 'center' });
    }, { band: C.red, bandH: 50, tape: true, pin: false });
  });
  paper(ctx, 0, 160, 920, 330, 0.01, pr(t, -.2, .5), c => {
    const X0 = -400, X1 = 400, sx = v => X0 + (X1 - X0) * v / 11, Y = -20;
    text(c, 'MEJORA SOBRE CINEMATCH', X0, -100, { f: font(700, 20, MONO), c: INK, ls: 2 });
    text(c, 'META 10 %', X1, -100, { f: font(700, 20, MONO), c: C.red, al: 'right', ls: 2 });
    rrect(c, X0, Y, X1 - X0, 22, 11); c.fillStyle = 'rgba(28,26,23,0.12)'; c.fill();
    c.setLineDash([6, 6]); c.strokeStyle = C.red; c.lineWidth = 2; c.beginPath(); c.moveTo(sx(10), Y - 36); c.lineTo(sx(10), Y + 58); c.stroke(); c.setLineDash([]);
    let v = 0; for (const [a, d, v0, v1] of K) if (t >= a) v = lerp(v0, v1, eio(pr(t, a, d)));
    rrect(c, X0, Y, Math.max(22, sx(v) - X0), 22, 11); c.fillStyle = v >= 10 ? C.red : INK; c.fill();
    text(c, v.toFixed(2).replace('.', ',') + ' %', 0, 110, { f: font(800, 76), c: v >= 10 ? C.red : INK, al: 'center' });
  });
  stamp(ctx, 250, 260, '¡META!', -0.12, pr(t, 2.7, .9), 54);
}

// 5 · el empate por 20 minutos ---------------------------------------------------
function roll(t, a, d, target, seed) {
  if (pr(t, a, d) >= 1) return target;
  const r = rng(seed + Math.floor(t * 30)); return '0,' + String(8000 + Math.floor(r() * 1999)).slice(0, 4);
}
function st5(ctx, t) {
  tag(ctx, -470, -520, 'EVIDENCIA 05 — EL FINAL', pr(t, 0, .5));
  const win = pr(t, 5.6, .5);
  [["BellKor's Pragmatic Chaos", '18:18:28', -220, -0.03, .2], ['The Ensemble', '18:38:22', 220, 0.03, .45]].forEach(([n, hh, x, rot, a], i) => {
    paper(ctx, x, -170, 380, 560, rot, pr(t, a, .5), c => {
      text(c, 'ENVÍO FINAL', 0, -205, { f: font(700, 22, MONO), c: INK, al: 'center', ls: 4 });
      c.setLineDash([5, 6]); c.strokeStyle = 'rgba(28,26,23,.4)'; c.lineWidth = 2;
      for (const y of [-182, 40, 160]) { c.beginPath(); c.moveTo(-160, y); c.lineTo(160, y); c.stroke(); }
      c.setLineDash([]);
      para(c, n, 0, -140, 320, 34, { f: font(700, 30), c: INK, al: 'center' });
      text(c, 'RMSE en test', 0, -40, { f: font(400, 18, MONO), c: SOFT, al: 'center' });
      text(c, roll(t, .6, 1.4, '0,8567', i * 99), 0, 14, { f: font(800, 54, MONO), c: INK, al: 'center' });
      text(c, '26/07/2009', 0, 80, { f: font(400, 20, MONO), c: SOFT, al: 'center' });
      text(c, hh, 0, 132, { f: font(800, 44, MONO), c: i === 0 ? C.red : INK, al: 'center', a: pr(t, 3.2, .4) });
      for (let k = 0; k < 34; k++) { const w = [2, 4, 1, 3][(k * 7 + i) % 4]; c.fillStyle = INK; c.fillRect(-150 + k * 9, 185, w, 50); }
      if (i === 1 && win > 0) { c.fillStyle = `rgba(20,20,22,${.45 * win})`; c.fillRect(-190, -280, 380, 560); }
      if (i === 0) stamp(c, 0, 205, 'GANADOR', -0.08, pr(t, 5.6, .9), 46);
    });
  });
  stamp(ctx, 0, 150, '= EMPATE', -0.04, pr(t, 2.2, .9) * (1 - .6 * win), 40);
  // reloj: 20 minutos de diferencia
  const ca = pr(t, 3.0, .5);
  if (ca > 0) {
    const cx = -110, cy = 370, R = 130, m = lerp(18.47, 38.37, eio(pr(t, 3.4, 1.8)));
    paper(ctx, cx, cy, 2 * R + 20, 2 * R + 20, 0, ca, c => {
      c.fillStyle = PAPER; c.beginPath(); c.arc(0, 0, R, 0, 7); c.fill();
      c.strokeStyle = INK; c.lineWidth = 4; c.stroke();
      for (let i = 0; i < 60; i++) { const a = i / 60 * 6.283, l = i % 5 ? 8 : 18; c.lineWidth = i % 5 ? 2 : 4; c.beginPath(); c.moveTo(Math.sin(a) * (R - 6), -Math.cos(a) * (R - 6)); c.lineTo(Math.sin(a) * (R - 6 - l), -Math.cos(a) * (R - 6 - l)); c.stroke(); }
      const a0 = 18.47 / 60 * 6.283 - Math.PI / 2, a1 = m / 60 * 6.283 - Math.PI / 2;
      c.fillStyle = 'rgba(229,56,59,.35)'; c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, R - 26, a0, a1); c.closePath(); c.fill();
      const hand = (a, l, w) => { c.lineWidth = w; c.lineCap = 'round'; c.beginPath(); c.moveTo(0, 0); c.lineTo(Math.cos(a) * l, Math.sin(a) * l); c.stroke(); };
      c.strokeStyle = INK; hand((6 + m / 60) / 12 * 6.283 - Math.PI / 2, R * .5, 7); hand(a1, R * .8, 4);
      c.fillStyle = C.red; c.beginPath(); c.arc(0, 0, 7, 0, 7); c.fill();
    }, { col: 'rgba(0,0,0,0)', pin: false, dark: true });
    const b = pr(t, 5.0, .4);
    text(ctx, '20 min', 130, 365, { f: font(800, 84), c: C.red, a: b });
    text(ctx, 'de diferencia', 134, 415, { f: font(400, 24, MONO), c: C.mut, a: b });
  }
}

// 6 · la solución ganadora era inmantenible ---------------------------------------
const LBL = ['SVD', 'SVD++', 'timeSVD++', 'kNN', 'RBM', 'NNMF', 'PMF', 'GBDT', 'item-kNN', 'user-kNN', 'asym-SVD', 'NN', 'blend', 'LR', 'BPR', 'PCA', 'kNN-time', 'RBM-cond', 'GLM', 'mix'];
const NODES = (function () {
  const r = rng(41);
  return Array.from({ length: 112 }, (_, i) => ({ l: LBL[Math.floor(r() * LBL.length)] + (r() < .5 ? '·' + Math.floor(1 + r() * 9) : ''), x: -400 + r() * 800, y: -440 + r() * 380, ts: 1.8 + i * .027 + r() * .15 }));
})();
function st6(ctx, t) {
  tag(ctx, -470, -520, 'EVIDENCIA 06 — LA SOLUCIÓN GANADORA', pr(t, 0, .5));
  paper(ctx, 0, -190, 920, 600, -0.01, pr(t, .1, .6), c => {
    c.strokeStyle = 'rgba(255,255,255,0.06)'; c.lineWidth = 1;
    for (let x = -460; x <= 460; x += 40) { c.beginPath(); c.moveTo(x, -300); c.lineTo(x, 300); c.stroke(); }
    for (let y = -300; y <= 300; y += 40) { c.beginPath(); c.moveTo(-460, y); c.lineTo(460, y); c.stroke(); }
    text(c, 'ESQUEMA · SOLUCIÓN GANADORA', -430, -262, { f: font(700, 20, MONO), c: '#cfe0ff', ls: 2 });
    const oy = 230;
    c.lineWidth = 1;
    for (const n of NODES) { const p = pr(t, n.ts, .3); if (p <= 0) continue; c.strokeStyle = `rgba(207,224,255,${.18 * p})`; c.beginPath(); c.moveTo(n.x, n.y + 190); c.quadraticCurveTo(n.x, oy - 40, 0, oy); c.stroke(); }
    c.font = font(500, 15, MONO);
    for (const n of NODES) {
      const p = pr(t, n.ts, .3); if (p <= 0) continue;
      const w = c.measureText(n.l).width + 16;
      c.save(); c.globalAlpha *= p; rrect(c, n.x - w / 2, n.y + 190 - 13, w, 26, 6); c.fillStyle = '#16294a'; c.fill(); c.strokeStyle = 'rgba(207,224,255,.45)'; c.stroke();
      text(c, n.l, n.x, n.y + 191, { f: font(500, 15, MONO), c: '#e6eeff', al: 'center', bl: 'middle' }); c.restore();
    }
    c.fillStyle = C.red; c.beginPath(); c.arc(0, oy, 34, 0, 7); c.fill();
    text(c, 'ŷ', 0, oy + 2, { f: font(700, 34), al: 'center', bl: 'middle' });
    marker(c, [[-380, -220], [380, 250]], pr(t, 8.3, .45), C.red, 14);
    marker(c, [[380, -220], [-380, 250]], pr(t, 8.7, .45), C.red, 14);
  }, { col: '#0f2342', dark: true });
  const cnt = NODES.filter(n => t >= n.ts).length;
  paper(ctx, 330, -470, 240, 120, 0.06, pr(t, 1.8, .4), c => {
    text(c, cnt + (cnt >= 100 ? '+' : ''), 0, 6, { f: font(800, 50), c: INK, al: 'center' });
    text(c, 'MODELOS MEZCLADOS', 0, 40, { f: font(600, 15, MONO), c: SOFT, al: 'center', ls: 2 });
  }, { tape: true, pin: false, col: '#f3e7a6' });
  paper(ctx, -250, 300, 400, 300, -0.03, pr(t, 5.0, .5), c => {
    c.fillStyle = '#d9d0bb'; c.fillRect(-170, -120, 340, 180);
    icon(c, 'engineer', 0, -20, 1.4);
    text(c, 'Ingeniería de Netflix', 0, 110, { f: font(600, 24), c: INK, al: 'center' });
  });
  paper(ctx, 230, 300, 420, 300, 0.03, pr(t, 5.5, .5), c => {
    text(c, 'Coste de llevarlo', -180, -92, { f: font(600, 22, MONO), c: INK });
    text(c, 'a producción', -180, -64, { f: font(600, 22, MONO), c: INK });
    rrect(c, -180, -46, 360 * eo(pr(t, 5.9, 1.0)), 28, 6); c.fillStyle = C.red; c.fill();
    text(c, 'Mejora extra', -180, 30, { f: font(600, 22, MONO), c: INK, a: pr(t, 6.6, .3) });
    rrect(c, -180, 46, 30 * eo(pr(t, 6.8, .5)), 28, 6); c.fillStyle = INK; c.fill();
    text(c, 'esquema, no a escala', 180, 120, { f: font(400, 16, MONO), c: SOFT, al: 'right' });
  });
}

// 7 · el negocio cambia --------------------------------------------------------------
function st7(ctx, t) {
  tag(ctx, -470, -520, 'EVIDENCIA 07 — EL NEGOCIO CAMBIA', pr(t, 0, .5));
  paper(ctx, -220, -230, 440, 290, -0.06, pr(t, .1, .6), c => {
    c.save(); c.translate(40, -150); c.globalCompositeOperation = 'destination-over';
    const cg = c.createConicGradient(t * .8, 0, 0); ['#d8dbe2', '#9fb4d8', '#e9d3e8', '#c8e6d6', '#f1e3b8', '#d8dbe2'].forEach((cc, i) => cg.addColorStop(i / 5, cc));
    c.fillStyle = cg; c.beginPath(); c.arc(0, 0, 120, 0, 7); c.fill(); c.restore();
    c.strokeStyle = 'rgba(0,0,0,0.25)'; c.lineWidth = 3; c.beginPath(); c.moveTo(-210, -135); c.lineTo(0, 20); c.lineTo(210, -135); c.stroke();
    text(c, 'DVD POR CORREO', 0, 100, { f: font(700, 22, MONO), c: 'rgba(255,255,255,0.85)', al: 'center', ls: 4 });
  }, { col: C.red, dark: true, pin: false, tape: true });
  tag(ctx, -400, -40, 'ANTES', pr(t, .6, .4));
  marker(ctx, [[-30, -260], [60, -300], [150, -270], [190, -200]], pr(t, 2.6, .6), '#f2efe8', 6);
  marker(ctx, [[165, -225], [190, -200], [210, -232]], pr(t, 3.1, .2), '#f2efe8', 6);
  const tv = pr(t, 3.0, .5);
  if (tv > 0) {
    ctx.save(); ctx.globalAlpha *= clamp(tv * 2); ctx.translate(230, -60 + 20 * (1 - eo(tv)));
    ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 40; ctx.shadowOffsetY = 18;
    rrect(ctx, -220, -130, 440, 260, 16); ctx.fillStyle = '#16181d'; ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.strokeStyle = 'rgba(255,255,255,0.15)'; ctx.lineWidth = 2; ctx.stroke();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(0, -16, 50, 0, 7); ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.moveTo(-14, -40); ctx.lineTo(26, -16); ctx.lineTo(-14, 8); ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fillRect(-190, 92, 380, 6);
    const pp = .4 * pr(t, 3.4, 4.6); ctx.fillStyle = C.red; ctx.fillRect(-190, 92, 380 * pp, 6); ctx.beginPath(); ctx.arc(-190 + 380 * pp, 95, 9, 0, 7); ctx.fill();
    ctx.restore();
  }
  tag(ctx, 110, 130, 'DESPUÉS · STREAMING', pr(t, 3.4, .4));
  text(ctx, 'LO QUE HABÍA QUE PREDECIR', 0, 245, { f: font(600, 22, MONO), c: C.mut, al: 'center', ls: 3, a: pr(t, 4.5, .4) });
  paper(ctx, 0, 320, 560, 90, -0.01, pr(t, 4.6, .4), c => {
    text(c, '¿Qué nota le pondrás?  ★★★★☆', 0, 10, { f: font(700, 30), c: INK, al: 'center', bl: 'middle' });
    marker(c, [[-250, 8], [250, 0]], pr(t, 5.5, .4), C.red, 7);
  }, { pin: false, tape: true });
  paper(ctx, 0, 450, 560, 90, 0.015, pr(t, 5.9, .4), c => {
    text(c, '¿Qué vas a ver ahora?  ▶', 0, 10, { f: font(800, 30), c: '#fff', al: 'center', bl: 'middle' });
  }, { pin: false, tape: true, col: C.red, dark: true });
}

// 8 · lo que sí se quedaron ----------------------------------------------------------
const FX = { n: 14, c: 34, k: 4 };
const OBS = (function () { const r = rng(61), s = new Set(); for (let i = 0; i < 26; i++) s.add(Math.floor(r() * FX.n * FX.n)); return s; })();
const VAL = (function () { const r = rng(62); return Array.from({ length: FX.n * FX.n }, () => r()); })();
const UV = (function () { const r = rng(63); return Array.from({ length: FX.n * FX.k * 2 }, () => r()); })();
function st8(ctx, t) {
  tag(ctx, -470, -520, 'EVIDENCIA 08 — LO QUE SÍ USARON', pr(t, 0, .5));
  paper(ctx, 0, -20, 900, 860, 0.01, pr(t, .1, .6), c => {
    const { n, c: cs, k } = FX, Rx = -170, Ry = -230, Ux = Rx - k * cs - 30, Vy = Ry - k * cs - 30;
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const id = i * n + j, x = Rx + j * cs, y = Ry + i * cs;
      c.strokeStyle = 'rgba(28,26,23,0.15)'; c.lineWidth = 1; c.strokeRect(x + 2.5, y + 2.5, cs - 5, cs - 5);
      if (OBS.has(id)) { c.fillStyle = C.red; c.fillRect(x + 2, y + 2, cs - 4, cs - 4); }
      else { const f = pr(t, 4.0 + (i + j) / (2 * n) * 3.2, .4); if (f > 0) { c.fillStyle = `rgba(229,56,59,${(.12 + .45 * VAL[id]) * f})`; c.fillRect(x + 2, y + 2, cs - 4, cs - 4); } }
    }
    for (let i = 0; i < n; i++) for (let q = 0; q < k; q++) {
      c.globalAlpha = pr(t, 1.0 + i * .03, .3); c.fillStyle = `rgba(28,26,23,${.1 + .6 * UV[i * k + q]})`; c.fillRect(Ux + q * cs + 2, Ry + i * cs + 2, cs - 4, cs - 4);
      c.globalAlpha = pr(t, 1.3 + i * .03, .3); c.fillStyle = `rgba(28,26,23,${.1 + .6 * UV[n * k + i * k + q]})`; c.fillRect(Rx + i * cs + 2, Vy + q * cs + 2, cs - 4, cs - 4);
    }
    c.globalAlpha = 1;
    if (t > 4.0 && t < 7.6) {
      const s = Math.floor((t - 4.0) / .22), r = rng(70 + s), i = Math.floor(r() * n), j = Math.floor(r() * n);
      c.strokeStyle = INK; c.lineWidth = 3;
      c.strokeRect(Ux, Ry + i * cs, k * cs, cs); c.strokeRect(Rx + j * cs, Vy, cs, k * cs); c.strokeRect(Rx + j * cs, Ry + i * cs, cs, cs);
    }
    const ua = pr(t, 1.0, .5);
    text(c, 'R', Rx + n * cs + 14, Ry + 30, { f: font(800, 36), c: INK });
    text(c, 'U', Ux, Ry + n * cs + 40, { f: font(800, 36), c: INK, a: ua });
    text(c, 'Vᵀ', Rx + n * cs + 14, Vy + 40, { f: font(800, 36), c: INK, a: ua });
    text(c, 'usuarios', Ux - 4, Ry + n * cs + 70, { f: font(400, 17, MONO), c: SOFT, a: ua });
    text(c, 'películas', Rx + n * cs, Vy - 12, { f: font(400, 17, MONO), c: SOFT, al: 'right', a: ua });
    maskLine(c, 'R ≈ U · Vᵀ', 0, 330, 66, pr(t, 3.6, .6), { f: font(800, 66), c: INK, al: 'center' });
    text(c, 'FACTORIZACIÓN DE MATRICES', 0, 380, { f: font(700, 22, MONO), c: C.red, al: 'center', ls: 3, a: pr(t, 4.0, .5) });
  });
  paper(ctx, 300, 430, 330, 150, 0.05, pr(t, 6.2, .5), c => {
    para(c, 'Rellena las celdas vacías: así recomiendan muchos sistemas hoy.', -140, -24, 290, 30, { f: font(600, 22), c: INK });
  }, { tape: true, pin: false, col: '#f3e7a6' });
}

const STATIONS = [st1, st2, st3, st4, st5, st6, st7, st8];

// ---------------------------------------------------------------- cámara
const TRAVEL = 0.8;
const CAMK = (function () {
  const k = [[0, 0, 0, 1.22], [1.4, 0, 0, 1.1]];
  for (let i = 1; i < ST.length; i++) {
    const a = ST[i].t0 - 0.3, prev = ST[i - 1];
    k.push([a, prev.x, prev.y, 1.13]); k.push([a + TRAVEL, ST[i].x, ST[i].y, 1.1]);
  }
  const zo = B[7] - 0.3;
  k.push([zo, ST[7].x, ST[7].y, 1.13]);
  k.push([zo + 2.4, 1150, 1495, 0.30]);
  k.push([B[7] + BEATS[7], 1150, 1495, 0.29]);
  return k;
})();
function camAt(t) {
  if (t <= CAMK[0][0]) return CAMK[0].slice(1);
  for (let i = 0; i < CAMK.length - 1; i++) {
    const [a, x0, y0, z0] = CAMK[i], [b, x1, y1, z1] = CAMK[i + 1];
    if (t <= b) { const p = eio(clamp((t - a) / (b - a))); return [lerp(x0, x1, p), lerp(y0, y1, p), lerp(z0, z1, p)]; }
  }
  return CAMK[CAMK.length - 1].slice(1);
}
function moving(t) { const [x0, y0] = camAt(t - 0.03), [x1, y1] = camAt(t); return Math.hypot(x1 - x0, y1 - y0); }

// ---------------------------------------------------------------- hilo rojo entre evidencias
function thread(ctx, t) {
  ctx.save(); ctx.strokeStyle = 'rgba(214,40,46,0.9)'; ctx.lineWidth = 3.5; ctx.lineCap = 'round';
  ctx.shadowColor = 'rgba(0,0,0,.5)'; ctx.shadowBlur = 6; ctx.shadowOffsetY = 5;
  for (let i = 1; i < ST.length; i++) {
    const p = eio(pr(t, ST[i].t0 - 0.3, TRAVEL + .2)); if (p <= 0) continue;
    const a = [ST[i - 1].x + ST[i - 1].pin[0], ST[i - 1].y + ST[i - 1].pin[1]], b = [ST[i].x + ST[i].pin[0], ST[i].y + ST[i].pin[1]];
    const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 160];
    ctx.beginPath(); ctx.moveTo(...a);
    const N = 40; for (let s = 1; s <= N * p; s++) { const u = s / N; ctx.lineTo((1 - u) ** 2 * a[0] + 2 * u * (1 - u) * m[0] + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * u * (1 - u) * m[1] + u * u * b[1]); }
    ctx.stroke();
  }
  ctx.restore();
}

// ---------------------------------------------------------------- mundo
function world(ctx, t) {
  if (!PAPER_PAT) { PAPER_PAT = ctx.createPattern(PAPER_TEX, 'repeat'); BOARD_PAT = ctx.createPattern(BOARD_TEX, 'repeat'); }
  const [cx, cy, z] = camAt(t);
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#121214'; ctx.fillRect(0, 0, W, H);
  ctx.setTransform(z, 0, 0, z, 540 - cx * z, 800 - cy * z);
  const vx0 = cx - 540 / z, vy0 = cy - 800 / z, vw = W / z, vh = H / z;
  ctx.save(); ctx.globalAlpha = .5; ctx.fillStyle = BOARD_PAT; ctx.fillRect(vx0, vy0, vw, vh); ctx.restore();
  thread(ctx, t);
  ST.forEach((s, i) => {
    const lt = t - s.t0; if (lt < -0.35) return;
    if (s.x + 620 < vx0 || s.x - 620 > vx0 + vw || s.y + 640 < vy0 || s.y - 640 > vy0 + vh) return;
    ctx.save(); ctx.translate(s.x, s.y); STATIONS[i](ctx, lt); ctx.restore();
  });
  for (let i = 0; i < ST.length; i++) if (ST[i].own && t >= ST[i].t0 - .3) pin(ctx, ST[i].x + ST[i].pin[0], ST[i].y + ST[i].pin[1]);
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  // luz de flexo sobre la evidencia actual
  const g = ctx.createRadialGradient(540, 780, 200, 540, 780, 1100);
  g.addColorStop(0, 'rgba(255,240,215,0.06)'); g.addColorStop(1, 'rgba(0,0,0,0.45)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  // la lección
  const lt = t - B[7], la = pr(lt, 2.4, .6);
  if (la > 0) {
    ctx.fillStyle = `rgba(9,9,11,${.86 * la})`; ctx.fillRect(0, 0, W, H);
    text(ctx, 'LA LECCIÓN', 90, 470, { f: font(600, 26, MONO), c: C.red, ls: 5, a: la });
    const L = [['El mejor modelo', 600, 2.7], ['no es el que gana', 700, 2.85], ['la clasificación.', 800, 3.0],
               ['Es el que puedes', 980, 4.0], ['mantener en', 1080, 4.15], ['producción.', 1180, 4.3]];
    L.forEach(([s, y, a], i) => maskLine(ctx, s, 90, y, 88, pr(lt, a, .6), { f: font(800, 88), c: i === 5 ? C.red : (i < 3 ? C.mut : C.ink) }));
    const fa = pr(lt, 5.4, .5);
    ctx.globalAlpha = fa; ctx.fillStyle = 'rgba(255,255,255,0.2)'; ctx.fillRect(90, 1330, 900 * eo(fa), 2); ctx.globalAlpha = 1;
    text(ctx, '@r2d2.coder', 90, 1420, { f: font(700, 48), a: pr(lt, 5.6, .5) });
    text(ctx, 'Sígueme para más historias de datos', 90, 1470, { f: font(400, 26, MONO), c: C.mut, a: pr(lt, 5.8, .5) });
    text(ctx, 'Fuente: Netflix Tech Blog (2012) · Netflix Prize 2006–2009', 540, 1780, { f: font(400, 20, MONO), c: C.dim, al: 'center', a: pr(lt, 6.0, .5) });
  }
}

const STORY = {
  title: 'EL NETFLIX PRIZE',
  scenes: BEATS.map(d => ({ dur: d, draw: () => { } })),
  world,
  blurSamples: t => moving(t) > 25 ? 5 : 1,
  narr: [
    { scene: 0, a: .2, b: 2.6, text: 'Netflix pagó un millón de dólares por un algoritmo.' },
    { scene: 0, a: 2.7, b: 4.2, text: 'Y nunca lo usó.' },
    { scene: 1, a: .2, b: 5.4, text: 'En 2006 lanzaron un concurso: quien mejorara un 10% su sistema de recomendaciones se llevaba el millón.' },
    { scene: 1, a: 5.6, b: 8.6, text: 'Soltaron 100 millones de valoraciones reales de usuarios.' },
    { scene: 2, a: .2, b: 3.2, text: 'Se apuntaron más de 40.000 equipos de 186 países.' },
    { scene: 2, a: 3.3, b: 5.4, text: 'Matemáticos, estudiantes, gente en su garaje.' },
    { scene: 2, a: 5.6, b: 9.0, text: 'Tardaron tres años en llegar a ese 10%.' },
    { scene: 3, a: .2, b: 3.0, text: 'En 2009, dos equipos empataron en la puntuación.' },
    { scene: 3, a: 3.2, b: 7.2, text: 'Ganó el que envió su solución 20 minutos antes.' },
    { scene: 4, a: .2, b: 1.7, text: '¿Y por qué no lo usaron?' },
    { scene: 4, a: 1.8, b: 4.9, text: 'Porque la solución ganadora mezclaba más de cien modelos.' },
    { scene: 4, a: 5.0, b: 9.5, text: 'Era tan compleja que ponerla en producción costaba más de lo que mejoraba.' },
    { scene: 5, a: .2, b: 4.4, text: 'Además, Netflix ya estaba dejando de enviar DVDs para pasarse al streaming,' },
    { scene: 5, a: 4.5, b: 7.8, text: 'y lo que tenían que predecir ya no era lo mismo.' },
    { scene: 6, a: .2, b: 3.4, text: 'Eso sí, de las primeras rondas se quedaron con dos ideas,' },
    { scene: 6, a: 3.5, b: 6.0, text: 'y una de ellas, la factorización de matrices,' },
    { scene: 6, a: 6.1, b: 9.0, text: 'sigue siendo la base de muchos recomendadores actuales.' },
  ],
  events: [
    { scene: 0, at: 2.85, type: 'thud' },
    { scene: 1, at: 3.0, type: 'ticks', dur: 2.2, rate: 9 },
    { scene: 1, at: 5.6, type: 'ticks', dur: 2.6, rate: 26 },
    { scene: 1, at: 8.0, type: 'swell', dur: 0.8 },
    { scene: 2, at: 0.4, type: 'ticks', dur: 2.8, rate: 26 },
    { scene: 2, at: 6.0, type: 'ticks', dur: 2.0, rate: 14 },
    { scene: 2, at: 8.35, type: 'thud' },
    { scene: 3, at: 0.6, type: 'ticks', dur: 1.4, rate: 30 },
    { scene: 3, at: 2.25, type: 'thud' },
    { scene: 3, at: 3.4, type: 'ticks', dur: 1.8, rate: 12 },
    { scene: 3, at: 5.65, type: 'thud' },
    { scene: 4, at: 1.8, type: 'ticks', dur: 3.2, rate: 24 },
    { scene: 4, at: 8.3, type: 'swell', dur: 0.6 },
    { scene: 5, at: 2.6, type: 'swell', dur: 0.8 },
    { scene: 6, at: 3.6, type: 'ding' },
    { scene: 6, at: 4.0, type: 'ticks', dur: 3.6, rate: 18 },
    { scene: 7, at: 2.6, type: 'swell', dur: 1.0 },
  ],
};
setup();
renderFrame(0);
