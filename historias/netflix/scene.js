// Historia 01 · El Netflix Prize. Tiempos locales en segundos dentro de cada escena.

// ---------------------------------------------------------------- 1 · gancho: el cheque descartado
const STAMP = (function () {
  const c = mk(780, 220), x = c.getContext('2d');
  x.strokeStyle = C.red; x.lineWidth = 12; rrect(x, 10, 10, 760, 200, 14); x.stroke();
  x.lineWidth = 4; rrect(x, 28, 28, 724, 164, 8); x.stroke();
  x.fillStyle = C.red; x.font = font(900, 112); x.textAlign = 'center'; x.textBaseline = 'middle';
  x.letterSpacing = '6px'; x.fillText('DESCARTADO', 390, 116);
  // textura de tinta gastada
  const r = rng(3); x.globalCompositeOperation = 'destination-out';
  for (let i = 0; i < 2600; i++) { x.globalAlpha = r() * .8; x.beginPath(); x.arc(r() * 780, r() * 220, r() * 2.6, 0, 7); x.fill(); }
  for (let i = 0; i < 14; i++) { x.globalAlpha = .35; x.fillRect(0, r() * 220, 780, 1 + r() * 2); }
  return c;
})();
const DUST = (function () { const r = rng(11); return Array.from({ length: 46 }, () => ({ a: r() * 6.283, v: 260 + r() * 520, s: 2 + r() * 5 })); })();
const SIG = [[-60, 150], [-20, 105], [10, 160], [40, 110], [55, 150], [90, 120], [120, 160], [150, 115], [200, 150], [260, 132], [330, 140]];

function s1(ctx, t, T) {
  const ts = 2.75;
  // sacudida al caer el sello
  const sk = t > ts + .14 ? 22 * Math.pow(1 - pr(t, ts + .14, .5), 2) : 0;
  ctx.save(); ctx.translate(sk * Math.sin(t * 97), sk * Math.cos(t * 83));
  bg(ctx, 540, 860, 760, `rgba(229,56,59,${0.10 + 0.12 * pr(t, ts, .3)})`);
  const p = eo(pr(t, 0.0, 0.8));
  ctx.save(); ctx.translate(540, 860); ctx.rotate(-0.05);
  const s = lerp(1.2, 1, p) * (1 + 0.015 * t); ctx.scale(s, s); ctx.globalAlpha = p;
  ctx.shadowColor = 'rgba(0,0,0,.7)'; ctx.shadowBlur = 70; ctx.shadowOffsetY = 34;
  rrect(ctx, -460, -215, 920, 430, 16); ctx.fillStyle = C.paper; ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.save(); rrect(ctx, -460, -215, 920, 430, 16); ctx.clip();
  ctx.strokeStyle = 'rgba(130,95,60,.10)'; ctx.lineWidth = 1.4;
  for (let k = 0; k < 20; k++) {
    ctx.beginPath();
    for (let x = -460; x <= 460; x += 8) { const y = -215 + k * 23 + 7 * Math.sin(x / 38 + k * .9); x === -460 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); }
    ctx.stroke();
  }
  ctx.fillStyle = C.red; ctx.fillRect(-460, -215, 16, 430);
  ctx.restore();
  const ink = '#1c1a17', soft = '#76695a';
  text(ctx, 'NETFLIX PRIZE', -405, -138, { f: font(800, 36), c: ink, ls: 5 });
  text(ctx, 'Nº 000001', 415, -140, { f: font(500, 22, MONO), c: soft, al: 'right' });
  text(ctx, 'FECHA  21 · 09 · 2009', 415, -104, { f: font(500, 22, MONO), c: soft, al: 'right' });
  text(ctx, 'PÁGUESE A', -405, -48, { f: font(500, 20, MONO), c: soft, ls: 2 });
  text(ctx, "BellKor's Pragmatic Chaos", -405, 2, { f: font(600, 40), c: ink });
  ctx.fillStyle = soft; ctx.fillRect(-405, 16, 520, 2);
  rrect(ctx, 150, -84, 265, 74, 6); ctx.lineWidth = 3; ctx.strokeStyle = ink; ctx.stroke();
  text(ctx, '$1.000.000', 282, -34, { f: font(700, 38, MONO), c: ink, al: 'center' });
  text(ctx, 'Un millón de dólares ——————', -405, 96, { f: 'italic 400 32px Georgia, serif', c: ink });
  // firma que se dibuja
  const sp = eio(pr(t, 0.7, 1.1));
  ctx.beginPath(); ctx.moveTo(SIG[0][0] + 170, SIG[0][1] - 10);
  for (let i = 1; i < SIG.length; i++) { const [a, b] = SIG[i - 1], [c, d] = SIG[i]; ctx.quadraticCurveTo(a + 170, b - 10, (a + c) / 2 + 170, (b + d) / 2 - 10); }
  ctx.setLineDash([900, 900]); ctx.lineDashOffset = 900 * (1 - sp);
  ctx.lineWidth = 3.2; ctx.strokeStyle = '#20305a'; ctx.lineCap = 'round'; ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = soft; ctx.fillRect(130, 168, 285, 2);
  text(ctx, 'FIRMA', 130, 194, { f: font(500, 18, MONO), c: soft, ls: 2 });
  ctx.restore();
  // sello
  if (t > ts) {
    const q = pr(t, ts, 0.15), sc = lerp(2.8, 1, q * q);
    ctx.save(); ctx.translate(560, 880); ctx.rotate(-0.2); ctx.scale(sc, sc);
    ctx.globalAlpha = clamp(q * 1.6) * .94; ctx.globalCompositeOperation = 'multiply';
    ctx.drawImage(STAMP, -390, -110); ctx.restore();
    ctx.globalCompositeOperation = 'source-over';
    const dp = pr(t, ts + .14, .7);
    if (dp > 0 && dp < 1) for (const d of DUST) {
      ctx.globalAlpha = (1 - dp) * .7; ctx.fillStyle = '#d9cfbe';
      ctx.beginPath(); ctx.arc(560 + Math.cos(d.a) * (380 + d.v * eo(dp) * .5), 880 + Math.sin(d.a) * (110 + d.v * eo(dp) * .5), d.s, 0, 7); ctx.fill();
    }
    ctx.globalAlpha = 1;
  }
  ctx.restore();
}

// ---------------------------------------------------------------- 2 · el concurso: lluvia de valoraciones → matriz
const G2 = { cols: 26, rows: 24, cell: 32, x0: 124, y0: 400 };
const STARS = (function () {
  const r = rng(21), cells = [];
  for (let i = 0; i < G2.cols * G2.rows; i++) cells.push(i);
  for (let i = cells.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1));[cells[i], cells[j]] = [cells[j], cells[i]]; }
  return cells.slice(0, 96).map((c, i) => ({
    cx: G2.x0 + (c % G2.cols) * G2.cell + G2.cell / 2, cy: G2.y0 + Math.floor(c / G2.cols) * G2.cell + G2.cell / 2,
    sx: r() * W, sy: -60 - r() * 500, ts: 0.3 + r() * 3.4, d: 1.0 + r() * .5, v: 1 + Math.floor(r() * 5),
  }));
})();
const FINE = (function () {
  // la misma matriz a escala real de dispersión: 1,2 % de celdas con valoración
  const c = mk(832, 768), x = c.getContext('2d'), r = rng(5), n = 8;
  x.fillStyle = 'rgba(255,255,255,0.05)';
  for (let i = 0; i < 832; i += n) for (let j = 0; j < 768; j += n) x.fillRect(i + 1, j + 1, n - 2, n - 2);
  x.fillStyle = C.red;
  for (let k = 0; k < Math.round(104 * 96 * 0.0118); k++) x.fillRect(Math.floor(r() * 104) * n + 1, Math.floor(r() * 96) * n + 1, n - 2, n - 2);
  return c;
})();
function s2(ctx, t, T) {
  bg(ctx, 540, 780, 700, 'rgba(229,56,59,0.07)');
  text(ctx, 'OCT 2006 · EL CONCURSO', 70, 280, { f: font(600, 24, MONO), c: C.red, ls: 3, a: pr(t, .2, .5) });
  maskLine(ctx, 'Baja el error un 10 % → 1 M$', 70, 340, 40, pr(t, 1.4, .6), { f: font(700, 40) });
  const gA = pr(t, .2, .8) * (1 - pr(t, 7.4, .6)), fA = pr(t, 7.5, .7);
  const { cols, rows, cell, x0, y0 } = G2;
  ctx.globalAlpha = gA; ctx.strokeStyle = 'rgba(255,255,255,0.08)'; ctx.lineWidth = 1;
  for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) ctx.strokeRect(x0 + i * cell + 2.5, y0 + j * cell + 2.5, cell - 5, cell - 5);
  text(ctx, 'películas →', x0, y0 - 16, { f: font(400, 22, MONO), c: C.mut });
  ctx.save(); ctx.translate(x0 - 16, y0); ctx.rotate(Math.PI / 2); text(ctx, 'usuarios →', 0, 0, { f: font(400, 22, MONO), c: C.mut }); ctx.restore();
  ctx.globalAlpha = 1;
  for (const s of STARS) {
    const p = pr(t, s.ts, s.d);
    if (p <= 0) continue;
    if (p < 1) {
      const q = eio(p), x = lerp(s.sx, s.cx, q), y = lerp(s.sy, s.cy, q);
      text(ctx, '★', x, y, { f: font(400, 34 - 8 * q), c: '#f5c451', al: 'center', bl: 'middle', a: .9 });
    } else {
      const k = pr(t, s.ts + s.d, .35);
      ctx.globalAlpha = gA;
      ctx.fillStyle = `rgba(229,56,59,${0.25 + 0.15 * s.v})`; ctx.fillRect(s.cx - 13, s.cy - 13, 26, 26);
      text(ctx, String(s.v), s.cx, s.cy + 1, { f: font(700, 15, MONO), c: '#fff', al: 'center', bl: 'middle', a: .85 });
      if (k < 1) { ctx.strokeStyle = `rgba(245,196,81,${1 - k})`; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(s.cx, s.cy, 10 + 26 * eo(k), 0, 7); ctx.stroke(); }
      ctx.globalAlpha = 1;
    }
  }
  if (fA > 0) { ctx.globalAlpha = fA; ctx.drawImage(FINE, x0, y0); ctx.globalAlpha = 1; }
  // contadores
  const cA = pr(t, 5.6, .4) * (1 - pr(t, 7.4, .4));
  if (cA > 0) {
    text(ctx, fmt(100480507 * eo(pr(t, 5.6, 1.6))), 540, 1262, { f: font(800, 76), c: C.ink, al: 'center', a: cA });
    text(ctx, 'valoraciones reales · 480.189 usuarios · 17.770 pelis', 540, 1312, { f: font(400, 24, MONO), c: C.mut, al: 'center', a: cA * pr(t, 6.2, .5) });
  }
  if (fA > 0) {
    text(ctx, '98,8 %', 540, 1262, { f: font(800, 76), c: C.red, al: 'center', a: pr(t, 7.8, .4) });
    text(ctx, 'de la matriz usuario × película está vacía', 540, 1312, { f: font(400, 24, MONO), c: C.mut, al: 'center', a: pr(t, 8.1, .5) });
  }
}

// ---------------------------------------------------------------- 3 · la carrera: el mundo compitiendo + barra de progreso
const BOX = [[25, 60, -125, -70], [-35, 5, -75, -40], [36, 60, -10, 30], [-30, 30, -10, 40], [10, 55, 60, 140], [-35, -15, 115, 150], [20, 40, 35, 60]];
const DOTS = (function () {
  const r = rng(31);
  return Array.from({ length: 186 }, (_, i) => {
    const b = BOX[Math.floor(r() * BOX.length)];
    return { lat: lerp(b[0], b[1], r()), lon: lerp(b[2], b[3], r()), ts: 0.4 + r() * 3.4 };
  });
})();
function proj(lat, lon, lon0, lat0, R) {
  const f = lat * Math.PI / 180, l = (lon - lon0) * Math.PI / 180, f0 = lat0 * Math.PI / 180;
  return {
    x: R * Math.cos(f) * Math.sin(l),
    y: -R * (Math.cos(f0) * Math.sin(f) - Math.sin(f0) * Math.cos(f) * Math.cos(l)),
    z: Math.sin(f0) * Math.sin(f) + Math.cos(f0) * Math.cos(f) * Math.cos(l),
  };
}
function s3(ctx, t, T) {
  bg(ctx, 540, 640, 620, 'rgba(229,56,59,0.10)');
  const gx = 540, gy = 640, R = 300, lon0 = -40 + t * 11, lat0 = 22;
  const ga = pr(t, 0, .6);
  ctx.globalAlpha = ga;
  const sg = ctx.createRadialGradient(gx - 90, gy - 110, 20, gx, gy, R);
  sg.addColorStop(0, '#1b1d24'); sg.addColorStop(1, '#0c0d10');
  ctx.fillStyle = sg; ctx.beginPath(); ctx.arc(gx, gy, R, 0, 7); ctx.fill();
  ctx.strokeStyle = 'rgba(255,255,255,0.22)'; ctx.lineWidth = 1.5; ctx.stroke();
  const line = (pts) => {
    ctx.beginPath(); let on = false;
    for (const p of pts) { if (p.z > 0) { on ? ctx.lineTo(gx + p.x, gy + p.y) : ctx.moveTo(gx + p.x, gy + p.y); on = true; } else on = false; }
    ctx.stroke();
  };
  ctx.strokeStyle = 'rgba(255,255,255,0.09)'; ctx.lineWidth = 1;
  for (let lon = -180; lon < 180; lon += 20) { const pts = []; for (let lat = -90; lat <= 90; lat += 4) pts.push(proj(lat, lon, lon0, lat0, R)); line(pts); }
  for (let lat = -60; lat <= 60; lat += 20) { const pts = []; for (let lon = -180; lon <= 180; lon += 4) pts.push(proj(lat, lon, lon0, lat0, R)); line(pts); }
  let lit = 0;
  for (const d of DOTS) {
    if (t < d.ts) continue; lit++;
    const p = proj(d.lat, d.lon, lon0, lat0, R);
    if (p.z <= 0) continue;
    const k = pr(t, d.ts, .7), sh = .35 + .65 * p.z;
    ctx.fillStyle = C.red; ctx.globalAlpha = ga * sh;
    ctx.beginPath(); ctx.arc(gx + p.x, gy + p.y, 4.5, 0, 7); ctx.fill();
    if (k < 1) { ctx.strokeStyle = `rgba(229,56,59,${(1 - k) * sh})`; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(gx + p.x, gy + p.y, 4 + 22 * eo(k), 0, 7); ctx.stroke(); }
  }
  ctx.globalAlpha = 1;
  // estadísticas
  const sa = pr(t, .4, .5) * (1 - pr(t, 5.2, .4));
  if (sa > 0) {
    const c = eo(pr(t, .4, 3.4));
    text(ctx, fmt(40000 * c) + (c > .99 ? '+' : ''), 300, 1090, { f: font(800, 72), al: 'center', a: sa });
    text(ctx, 'EQUIPOS', 300, 1136, { f: font(500, 22, MONO), c: C.mut, al: 'center', ls: 3, a: sa });
    text(ctx, String(lit), 780, 1090, { f: font(800, 72), c: C.red, al: 'center', a: sa });
    text(ctx, 'PAÍSES', 780, 1136, { f: font(500, 22, MONO), c: C.mut, al: 'center', ls: 3, a: sa });
  }
  // barra de progreso hacia el 10 %
  const pa = pr(t, 5.5, .5);
  if (pa > 0) {
    const X0 = 100, X1 = 980, sx = v => X0 + (X1 - X0) * v / 11, Y = 1060;
    ctx.globalAlpha = pa;
    text(ctx, 'MEJORA SOBRE CINEMATCH', X0, 1000, { f: font(500, 22, MONO), c: C.mut, ls: 2 });
    text(ctx, 'META 10 %', X1, 1000, { f: font(600, 22, MONO), c: C.red, al: 'right', ls: 2 });
    rrect(ctx, X0, Y, X1 - X0, 16, 8); ctx.fillStyle = 'rgba(255,255,255,0.10)'; ctx.fill();
    ctx.setLineDash([6, 6]); ctx.strokeStyle = C.red; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(sx(10), 1030); ctx.lineTo(sx(10), 1100); ctx.stroke(); ctx.setLineDash([]);
    const K = [[5.9, .9, 0, 8.43, '2007', 1], [6.9, .8, 8.43, 9.44, '2008', -1], [7.9, .8, 9.44, 10.06, '2009', 1]];
    let v = 0;
    for (const [a, d, v0, v1] of K) if (t >= a) v = lerp(v0, v1, eio(pr(t, a, d)));
    const hit = v >= 10;
    rrect(ctx, X0, Y, Math.max(16, sx(v) - X0), 16, 8); ctx.fillStyle = hit ? C.red : C.ink; ctx.fill();
    if (hit) { ctx.shadowColor = C.red; ctx.shadowBlur = 30; ctx.fill(); ctx.shadowBlur = 0; ctx.shadowColor = 'transparent'; }
    for (const [a, d, , v1, y, up] of K) {
      const la = pr(t, a + d, .3); if (la <= 0) continue;
      ctx.globalAlpha = pa * la; ctx.fillStyle = C.ink; ctx.fillRect(sx(v1) - 1, Y - 6, 2, 28);
      text(ctx, y, sx(v1), up > 0 ? 1124 : 1046, { f: font(500, 20, MONO), c: C.mut, al: 'center' });
      ctx.globalAlpha = pa;
    }
    text(ctx, v.toFixed(2).replace('.', ',') + ' %', 540, 1235, { f: font(800, 84), c: hit ? C.red : C.ink, al: 'center' });
    ctx.globalAlpha = 1;
  }
}

// ---------------------------------------------------------------- 4 · el empate: 20 minutos
function roll(t, a, d, target, seed) {
  const p = pr(t, a, d); if (p >= 1) return target;
  const r = rng(seed + Math.floor(t * 30)); return '0,' + String(8000 + Math.floor(r() * 1999)).slice(0, 4);
}
function s4(ctx, t, T) {
  bg(ctx, 540, 700, 700, 'rgba(229,56,59,0.07)');
  text(ctx, 'CLASIFICACIÓN FINAL · JULIO 2009', 70, 300, { f: font(600, 24, MONO), c: C.red, ls: 3, a: pr(t, .1, .4) });
  const win = pr(t, 5.6, .4);
  const rows = [
    { n: "BellKor's Pragmatic Chaos", y: 360, a: .2, hh: '18:18:28' },
    { n: 'The Ensemble', y: 540, a: .45, hh: '18:38:22' },
  ];
  rows.forEach((r, i) => {
    const p = eo(pr(t, r.a, .5)), dim = i === 1 ? 1 - .65 * win : 1;
    ctx.save(); ctx.translate((1 - p) * 120, 0); ctx.globalAlpha = p * dim;
    rrect(ctx, 70, r.y, 940, 150, 16); ctx.fillStyle = '#121418'; ctx.fill();
    ctx.strokeStyle = i === 0 && win > 0 ? `rgba(229,56,59,${win})` : 'rgba(255,255,255,0.10)'; ctx.lineWidth = 2; ctx.stroke();
    text(ctx, r.n, 110, r.y + 66, { f: font(700, 40) });
    text(ctx, 'RMSE en test · enviado ' + r.hh, 110, r.y + 112, { f: font(400, 22, MONO), c: C.mut });
    text(ctx, roll(t, .6, 1.4, '0,8567', i * 99), 970, r.y + 72, { f: font(700, 50, MONO), al: 'right' });
    text(ctx, '10,06 %', 970, r.y + 114, { f: font(500, 24, MONO), c: C.mut, al: 'right', a: pr(t, 2, .3) });
    ctx.restore();
  });
  // insignia de empate
  const e = pr(t, 2.2, .25);
  if (e > 0) {
    const s = lerp(1.6, 1, eo(e)) ;
    ctx.save(); ctx.translate(540, 525); ctx.scale(s, s); ctx.globalAlpha = e * (1 - .7 * win);
    rrect(ctx, -110, -26, 220, 52, 26); ctx.fillStyle = C.red; ctx.fill();
    text(ctx, '= EMPATE', 0, 2, { f: font(800, 26), al: 'center', bl: 'middle', ls: 2 });
    ctx.restore();
  }
  // ganador
  if (win > 0) {
    ctx.save(); ctx.globalAlpha = win;
    rrect(ctx, 820, 330, 180, 46, 23); ctx.fillStyle = C.red; ctx.fill();
    text(ctx, 'GANADOR', 910, 354, { f: font(800, 22), al: 'center', bl: 'middle', ls: 3 });
    ctx.restore();
  }
  // línea temporal
  const la = pr(t, 3.0, .4);
  if (la > 0) {
    const X0 = 110, X1 = 970, m0 = 10 * 60, m1 = 45 * 60, sx = s => X0 + (X1 - X0) * (s - m0) / (m1 - m0), Y = 1010;
    const head = lerp(m0, m1, eio(pr(t, 3.1, 1.8)));
    ctx.globalAlpha = la;
    text(ctx, '26 DE JULIO DE 2009', X0, 880, { f: font(500, 22, MONO), c: C.mut, ls: 2 });
    ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fillRect(X0, Y, X1 - X0, 2);
    ctx.fillStyle = C.ink; ctx.fillRect(X0, Y, sx(head) - X0, 2);
    for (let m = 10; m <= 45; m += 5) {
      ctx.fillStyle = 'rgba(255,255,255,0.3)'; ctx.fillRect(sx(m * 60) - 1, Y + 8, 2, 10);
      text(ctx, '18:' + String(m).padStart(2, '0'), sx(m * 60), Y + 46, { f: font(400, 18, MONO), c: C.dim, al: 'center' });
    }
    const marks = [[18 * 60 + 28, 'BellKor', C.red], [38 * 60 + 22, 'Ensemble', C.ink]];
    for (const [s, n, col] of marks) {
      if (head < s) continue;
      const k = pr(head, s, 90);
      ctx.fillStyle = col; ctx.beginPath(); ctx.arc(sx(s), Y + 1, 9 * eo(k), 0, 7); ctx.fill();
      text(ctx, n, sx(s), Y - 26, { f: font(700, 26), c: col, al: 'center', a: k });
    }
    const b = pr(t, 4.9, .5);
    if (b > 0) {
      const a = sx(18 * 60 + 28), c = sx(38 * 60 + 22), y = Y + 84;
      ctx.globalAlpha = la * b; ctx.strokeStyle = C.red; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(a, y - 14); ctx.lineTo(a, y); ctx.lineTo(lerp(a, c, eo(b)), y); ctx.stroke();
      if (b >= 1) { ctx.beginPath(); ctx.moveTo(c, y); ctx.lineTo(c, y - 14); ctx.stroke(); }
      text(ctx, '20 min', (a + c) / 2, y + 74, { f: font(800, 64), c: C.red, al: 'center' });
    }
    ctx.globalAlpha = 1;
  }
}

// ---------------------------------------------------------------- 5 · el giro: +100 modelos inmantenibles
const LBL = ['SVD', 'SVD++', 'timeSVD++', 'kNN', 'RBM', 'NNMF', 'PMF', 'GBDT', 'item-kNN', 'user-kNN', 'asym-SVD', 'NN', 'blend', 'LR', 'BPR', 'PCA', 'kNN-time', 'RBM-cond', 'GLM', 'mix'];
const NODES = (function () {
  const r = rng(41), out = [];
  for (let i = 0; i < 112; i++) {
    const l = LBL[Math.floor(r() * LBL.length)] + (r() < .5 ? '·' + Math.floor(1 + r() * 9) : '');
    out.push({ l, x: 90 + r() * 900, y: 400 + r() * 540, ts: .3 + i * .036 + r() * .2, vy: 400 + r() * 900, rot: (r() - .5) * 2, cx: (r() - .5) * 2 });
  }
  return out;
})();
function s5(ctx, t, T) {
  bg(ctx, 540, 1040, 600, `rgba(229,56,59,${0.08 + 0.06 * pr(t, 1.8, 3)})`);
  const ox = 540, oy = 1040, col = 8.4, dimm = 1 - .55 * pr(t, 5.4, .5);
  const fall = t > col ? t - col : 0;
  // conexiones
  ctx.lineWidth = 1;
  for (const n of NODES) {
    const p = pr(t, n.ts, .3); if (p <= 0) continue;
    ctx.strokeStyle = `rgba(229,56,59,${.16 * p * dimm * (1 - pr(t, col, .3))})`;
    ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.quadraticCurveTo(n.x, oy - 40, ox, oy); ctx.stroke();
  }
  ctx.font = font(500, 17, MONO);
  for (const n of NODES) {
    const p = pr(t, n.ts, .3); if (p <= 0) continue;
    const w = ctx.measureText(n.l).width + 20;
    const x = n.x + n.cx * 80 * fall, y = n.y + n.vy * fall * fall;
    if (y > H + 60) continue;
    ctx.save(); ctx.translate(x, y); ctx.rotate(n.rot * fall * 1.5); ctx.scale(lerp(.6, 1, eo(p)), lerp(.6, 1, eo(p)));
    ctx.globalAlpha = p * dimm;
    rrect(ctx, -w / 2, -16, w, 32, 8); ctx.fillStyle = '#15171c'; ctx.fill(); ctx.strokeStyle = 'rgba(255,255,255,0.14)'; ctx.stroke();
    text(ctx, n.l, 0, 1, { f: font(500, 17, MONO), c: '#c9ccd2', al: 'center', bl: 'middle' });
    ctx.restore();
  }
  // nodo de salida
  const op = eo(pr(t, .2, .5));
  ctx.save(); ctx.globalAlpha = op;
  ctx.shadowColor = C.red; ctx.shadowBlur = 40 + 20 * Math.sin(t * 3);
  ctx.fillStyle = C.red; ctx.beginPath(); ctx.arc(ox, oy, 46, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
  text(ctx, 'ŷ', ox, oy + 2, { f: font(700, 46), al: 'center', bl: 'middle' });
  text(ctx, 'predicción final', ox, oy + 84, { f: font(400, 22, MONO), c: C.mut, al: 'center' });
  ctx.restore();
  // contador de modelos
  const cnt = NODES.filter(n => t >= n.ts).length;
  text(ctx, cnt + (cnt >= 100 ? '+' : ''), 70, 290, { f: font(800, 64), c: C.ink, a: pr(t, .3, .3) * (1 - pr(t, col, .4)) });
  text(ctx, 'MODELOS MEZCLADOS', 70, 330, { f: font(500, 22, MONO), c: C.mut, ls: 3, a: pr(t, .3, .3) * (1 - pr(t, col, .4)) });
  // coste vs mejora
  const ba = pr(t, 5.6, .4);
  if (ba > 0) {
    ctx.globalAlpha = ba;
    text(ctx, 'Coste de llevarlo a producción', 100, 1200, { f: font(500, 24, MONO), c: C.ink });
    rrect(ctx, 100, 1218, 880 * eo(pr(t, 5.8, 1.1)), 26, 6); ctx.fillStyle = C.red; ctx.fill();
    text(ctx, 'Mejora extra que aportaba', 100, 1296, { f: font(500, 24, MONO), c: C.ink, a: pr(t, 6.6, .3) });
    rrect(ctx, 100, 1314, 70 * eo(pr(t, 6.8, .6)), 26, 6); ctx.fillStyle = C.ink; ctx.fill();
    text(ctx, 'esquema, no a escala', 980, 1380, { f: font(400, 18, MONO), c: C.dim, al: 'right' });
    ctx.globalAlpha = 1;
  }
}

// ---------------------------------------------------------------- 6 · DVD → streaming
function s6(ctx, t, T) {
  bg(ctx, 540, 720, 640, 'rgba(229,56,59,0.10)');
  const m = eio(pr(t, 2.6, 1.4));
  const ew = lerp(640, 680, m), eh = lerp(420, 382, m), er = lerp(14, 22, m);
  const rgb = [lerp(229, 21, m), lerp(56, 23, m), lerp(59, 28, m)].map(Math.round);
  const cy = 740, ap = eo(pr(t, 0, .6));
  ctx.globalAlpha = ap;
  // disco asomando
  const dy = lerp(cy - 210, cy, m), ds = lerp(1, .25, m);
  ctx.save(); ctx.translate(540, dy); ctx.scale(ds, ds); ctx.globalAlpha = ap * (1 - m);
  const cg = ctx.createConicGradient(t * .8, 0, 0);
  ['#d8dbe2', '#9fb4d8', '#e9d3e8', '#c8e6d6', '#f1e3b8', '#d8dbe2'].forEach((c, i) => cg.addColorStop(i / 5, c));
  ctx.fillStyle = cg; ctx.beginPath(); ctx.arc(0, 0, 170, 0, 7); ctx.fill();
  ctx.fillStyle = '#2a2c31'; ctx.beginPath(); ctx.arc(0, 0, 26, 0, 7); ctx.fill();
  ctx.restore();
  // sobre → botón
  ctx.save(); ctx.globalAlpha = ap;
  ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 50; ctx.shadowOffsetY = 24;
  rrect(ctx, 540 - ew / 2, cy - eh / 2, ew, eh, er); ctx.fillStyle = `rgb(${rgb})`; ctx.fill();
  ctx.shadowColor = 'transparent';
  // pantalla de streaming: marco, barra de reproducción roja
  if (m > 0) {
    ctx.globalAlpha = ap * m; ctx.strokeStyle = 'rgba(255,255,255,0.18)'; ctx.lineWidth = 2; ctx.stroke();
    const bx = 540 - ew / 2 + 36, bw = ew - 72, by = cy + eh / 2 - 40;
    ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fillRect(bx, by, bw, 6);
    const pp = .35 * pr(t, 3.4, 4.6); ctx.fillStyle = C.red; ctx.fillRect(bx, by, bw * pp, 6);
    ctx.beginPath(); ctx.arc(bx + bw * pp, by + 3, 10, 0, 7); ctx.fill();
  }
  ctx.globalAlpha = ap * (1 - m); ctx.strokeStyle = 'rgba(0,0,0,0.25)'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(540 - ew / 2 + 10, cy - eh / 2 + 10); ctx.lineTo(540, cy + 30); ctx.lineTo(540 + ew / 2 - 10, cy - eh / 2 + 10); ctx.stroke();
  text(ctx, 'DEVOLVER ANTES DEL ENVÍO', 540, cy + eh / 2 - 40, { f: font(600, 20, MONO), c: 'rgba(0,0,0,0.45)', al: 'center', ls: 3 });
  ctx.globalAlpha = ap * m;
  const s = 1 * eo(m);
  ctx.translate(540, cy - 14); ctx.scale(s, s);
  ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(0, 0, 70, 0, 7); ctx.stroke();
  ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.moveTo(-20, -32); ctx.lineTo(34, 0); ctx.lineTo(-20, 32); ctx.closePath();
  ctx.lineJoin = 'round'; ctx.lineWidth = 8; ctx.stroke(); ctx.fill();
  ctx.restore();
  ctx.globalAlpha = 1;
  text(ctx, 'ANTES · DVD POR CORREO', 540, 400, { f: font(600, 26, MONO), c: C.mut, al: 'center', ls: 3, a: ap * (1 - pr(t, 2.6, .5)) });
  text(ctx, 'DESPUÉS · STREAMING', 540, 400, { f: font(600, 26, MONO), c: C.red, al: 'center', ls: 3, a: pr(t, 3.4, .5) });
  // qué había que predecir
  const qa = pr(t, 4.6, .5);
  if (qa > 0) {
    const chip = (s, x, y, a, hl) => {
      ctx.save(); ctx.globalAlpha = a; ctx.font = font(600, 28);
      const w = ctx.measureText(s).width + 48;
      rrect(ctx, x - w / 2, y - 34, w, 68, 34); ctx.fillStyle = hl ? C.red : '#15171c'; ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,0.14)'; ctx.lineWidth = 2; ctx.stroke();
      text(ctx, s, x, y + 2, { f: font(600, 28), al: 'center', bl: 'middle' }); ctx.restore();
    };
    text(ctx, 'LO QUE HABÍA QUE PREDECIR', 540, 1080, { f: font(500, 22, MONO), c: C.mut, al: 'center', ls: 3, a: qa });
    chip('¿Qué nota le pondrás? ★', 540, 1150, qa * (1 - .6 * pr(t, 5.6, .4)), false);
    const b = pr(t, 5.6, .5);
    if (b > 0) {
      text(ctx, '↓', 540, 1232, { f: font(600, 36), c: C.mut, al: 'center', a: b });
      chip('¿Qué vas a ver ahora? ▶', 540, 1300, b, true);
    }
  }
}

// ---------------------------------------------------------------- 7 · lo que sí se quedaron: factorización de matrices
const FX = { n: 18, c: 34, k: 5, x0: 360, y0: 500, ux: 160, vy: 316 };
const OBS = (function () { const r = rng(61), s = new Set(); for (let i = 0; i < 40; i++) s.add(Math.floor(r() * FX.n * FX.n)); return s; })();
const VAL = (function () { const r = rng(62); return Array.from({ length: FX.n * FX.n }, () => r()); })();
const UV = (function () { const r = rng(63); return Array.from({ length: FX.n * FX.k * 2 }, () => r()); })();
function s7(ctx, t, T) {
  bg(ctx, 600, 800, 700, 'rgba(229,56,59,0.08)');
  const { n, c, k, x0, y0, ux, vy } = FX;
  const ra = pr(t, .1, .5);
  // R
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    const id = i * n + j, x = x0 + j * c, y = y0 + i * c;
    ctx.globalAlpha = ra;
    ctx.fillStyle = 'rgba(255,255,255,0.05)'; ctx.fillRect(x + 2, y + 2, c - 4, c - 4);
    if (OBS.has(id)) { ctx.fillStyle = C.red; ctx.fillRect(x + 2, y + 2, c - 4, c - 4); }
    else {
      const f = pr(t, 4.0 + (i + j) / (2 * n) * 3.2, .4);
      if (f > 0) { ctx.fillStyle = `rgba(229,56,59,${(.12 + .5 * VAL[id]) * f})`; ctx.fillRect(x + 2, y + 2, c - 4, c - 4); }
    }
  }
  // U (usuarios × gustos) y Vᵀ (gustos × películas)
  const ua = pr(t, 1.0, .6);
  for (let i = 0; i < n; i++) for (let q = 0; q < k; q++) {
    const f1 = pr(t, 1.0 + i * .03, .3), f2 = pr(t, 1.3 + i * .03, .3);
    ctx.globalAlpha = ua * f1; ctx.fillStyle = `rgba(242,241,238,${.12 + .6 * UV[i * k + q]})`;
    ctx.fillRect(ux + q * c + 2, y0 + i * c + 2, c - 4, c - 4);
    ctx.globalAlpha = ua * f2; ctx.fillStyle = `rgba(242,241,238,${.12 + .6 * UV[n * k + i * k + q]})`;
    ctx.fillRect(x0 + i * c + 2, vy + q * c + 2, c - 4, c - 4);
  }
  // cursor del producto fila × columna
  if (t > 4.0 && t < 7.6) {
    const s = Math.floor((t - 4.0) / .22), r = rng(70 + s), i = Math.floor(r() * n), j = Math.floor(r() * n);
    ctx.globalAlpha = .9; ctx.strokeStyle = '#fff'; ctx.lineWidth = 2;
    ctx.strokeRect(ux + 1, y0 + i * c + 1, k * c - 2, c - 2);
    ctx.strokeRect(x0 + j * c + 1, vy + 1, c - 2, k * c - 2);
    ctx.strokeRect(x0 + j * c + 1, y0 + i * c + 1, c - 2, c - 2);
  }
  ctx.globalAlpha = 1;
  text(ctx, 'R', x0 + n * c + 18, y0 + 34, { f: font(800, 40), a: ra });
  text(ctx, 'U', ux, y0 + n * c + 46, { f: font(800, 40), a: ua });
  text(ctx, 'Vᵀ', x0 + n * c + 18, vy + 50, { f: font(800, 40), a: ua });
  text(ctx, 'usuarios × gustos', ux, y0 + n * c + 80, { f: font(400, 20, MONO), c: C.mut, a: ua });
  text(ctx, 'gustos × películas', x0 + n * c - 6, vy - 16, { f: font(400, 20, MONO), c: C.mut, al: 'right', a: ua });
  maskLine(ctx, 'R ≈ U · Vᵀ', 540, 1225, 72, pr(t, 3.6, .6), { f: font(800, 72), al: 'center' });
  text(ctx, 'FACTORIZACIÓN DE MATRICES', 540, 1285, { f: font(600, 24, MONO), c: C.red, al: 'center', ls: 3, a: pr(t, 4.0, .5) });
  text(ctx, 'rellena las celdas vacías con predicciones', 540, 1325, { f: font(400, 22, MONO), c: C.mut, al: 'center', a: pr(t, 4.6, .5) });
}

// ---------------------------------------------------------------- 8 · la lección
function s8(ctx, t, T) {
  bg(ctx, 200, 900, 900, 'rgba(229,56,59,0.07)');
  text(ctx, 'LA LECCIÓN', 90, 470, { f: font(600, 26, MONO), c: C.red, ls: 5, a: pr(t, .1, .4) });
  const L = [['El mejor modelo', 600, .3], ['no es el que gana', 700, .45], ['la clasificación.', 800, .6],
             ['Es el que puedes', 980, 2.2], ['mantener en', 1080, 2.35], ['producción.', 1180, 2.5]];
  L.forEach(([s, y, a], i) => maskLine(ctx, s, 90, y, 88, pr(t, a, .6), { f: font(800, 88), c: i === 5 ? C.red : (i < 3 ? C.mut : C.ink) }));
  const fa = pr(t, 4.6, .5);
  ctx.globalAlpha = fa; ctx.fillStyle = 'rgba(255,255,255,0.2)'; ctx.fillRect(90, 1330, 900 * eo(fa), 2); ctx.globalAlpha = 1;
  text(ctx, '@r2d2.coder', 90, 1420, { f: font(700, 48), a: pr(t, 4.8, .5) });
  text(ctx, 'Sígueme para más historias de datos', 90, 1470, { f: font(400, 26, MONO), c: C.mut, a: pr(t, 5.0, .5) });
  text(ctx, 'Fuente: Netflix Tech Blog (2012) · Netflix Prize 2006–2009', 540, 1780, { f: font(400, 20, MONO), c: C.dim, al: 'center', a: pr(t, 5.4, .5) });
}

const STORY = {
  title: 'EL NETFLIX PRIZE',
  scenes: [
    { dur: 4.4, draw: s1 }, { dur: 10.5, draw: s2 }, { dur: 9.4, draw: s3 }, { dur: 7.6, draw: s4 },
    { dur: 9.8, draw: s5 }, { dur: 8.0, draw: s6 }, { dur: 9.2, draw: s7 }, { dur: 8.0, draw: s8 },
  ],
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
  // efectos de sonido sincronizados (los lee audio.py)
  events: [
    { scene: 0, at: 2.89, type: 'thud' },
    { scene: 1, at: 0.3, type: 'ticks', dur: 4.6, rate: 22 },
    { scene: 1, at: 5.6, type: 'ticks', dur: 1.6, rate: 30 },
    { scene: 1, at: 7.5, type: 'swell', dur: 1.2 },
    { scene: 2, at: 0.4, type: 'ticks', dur: 3.4, rate: 26 },
    { scene: 2, at: 8.5, type: 'ding' },
    { scene: 3, at: 0.6, type: 'ticks', dur: 1.4, rate: 30 },
    { scene: 3, at: 2.2, type: 'thud' },
    { scene: 3, at: 5.6, type: 'ding' },
    { scene: 4, at: 0.3, type: 'ticks', dur: 4.0, rate: 24 },
    { scene: 4, at: 8.4, type: 'fall', dur: 1.4 },
    { scene: 5, at: 2.6, type: 'swell', dur: 1.4 },
    { scene: 6, at: 3.6, type: 'ding' },
    { scene: 6, at: 4.0, type: 'ticks', dur: 3.6, rate: 18 },
    { scene: 7, at: 2.2, type: 'swell', dur: 1.0 },
  ],
};
setup();
renderFrame(0);
