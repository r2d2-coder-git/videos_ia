// Fotogramas de estilo: el mismo momento ("Soltaron 100 millones de valoraciones") en 4 direcciones visuales.
// t en [0,1) → A notebook · [1,2) → B suizo · [2,3) → C partículas · [3,4) → D informe

// ---------------------------------------------------------------- A · Notebook (terminal / Jupyter)
function styleA(ctx) {
  const BG = '#0d1117', PAN = '#161b22', LN = '#30363d', TX = '#e6edf3', MU = '#7d8590', KW = '#ff7b72', STR = '#a5d6ff', FN = '#d2a8ff', NUM = '#79c0ff', GRN = '#3fb950';
  ctx.fillStyle = BG; ctx.fillRect(0, 0, W, H);
  // barra de ventana
  ctx.fillStyle = PAN; ctx.fillRect(0, 90, W, 80);
  ['#ff5f57', '#febc2e', '#28c840'].forEach((c, i) => { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(60 + i * 34, 130, 10, 0, 7); ctx.fill(); });
  rrect(ctx, 190, 104, 420, 66, [10, 10, 0, 0]); ctx.fillStyle = BG; ctx.fill();
  text(ctx, 'netflix_prize.ipynb', 220, 145, { f: font(500, 24, MONO), c: TX });
  text(ctx, 'Historias de datos · 02/08', 1020, 145, { f: font(400, 20, MONO), c: MU, al: 'right' });
  const cell = (y, n, lines, h, run) => {
    text(ctx, `[${n}]:`, 40, y + 46, { f: font(500, 22, MONO), c: run ? GRN : MU });
    rrect(ctx, 110, y, 930, h, 10); ctx.fillStyle = PAN; ctx.fill(); ctx.strokeStyle = run ? GRN : LN; ctx.lineWidth = 2; ctx.stroke();
    lines.forEach((l, i) => { let x = 134; for (const [s, c] of l) { text(ctx, s, x, y + 46 + i * 40, { f: font(500, 26, MONO), c }); ctx.font = font(500, 26, MONO); x += ctx.measureText(s).width; } });
  };
  // celda anterior, ya ejecutada (continuidad: el notebook hace scroll hacia arriba)
  ctx.globalAlpha = .45;
  cell(210, 2, [[['# Oct 2006 · 1.000.000 $ por mejorar un 10 %', MU]], [['premio', TX], [' = ', KW], ['1_000_000', NUM]]], 100);
  ctx.globalAlpha = 1;
  cell(350, 3, [[['# Netflix publica los datos del concurso', MU]], [['ratings', TX], [' = ', KW], ['pd', TX], ['.', TX], ['read_csv', FN], ['(', TX], ['"netflix_prize.csv"', STR], [')', TX]], [['ratings', TX], ['.', TX], ['shape', TX]]], 150, true);
  text(ctx, 'Out[3]:', 24, 560, { f: font(500, 22, MONO), c: KW });
  text(ctx, '(100.480.507, 3)', 134, 572, { f: font(800, 64, MONO), c: TX });
  text(ctx, 'filas = valoraciones reales de usuarios', 134, 620, { f: font(400, 22, MONO), c: MU });
  // tabla de muestra
  const rows = [['usuario', 'película', 'nota'], ['1488844', 'Dinosaur Planet', '3'], ['822109', 'Isle of Man TT', '5'], ['885013', 'Character', '4'], ['30878', 'Paula Abdul', '4']];
  rows.forEach((r, i) => {
    const y = 690 + i * 48;
    if (i === 0) { ctx.fillStyle = '#1f2630'; ctx.fillRect(134, y - 34, 880, 48); }
    else { ctx.fillStyle = LN; ctx.fillRect(134, y + 14, 880, 1); }
    text(ctx, r[0], 154, y, { f: font(i ? 400 : 700, 24, MONO), c: i ? TX : MU });
    text(ctx, r[1], 420, y, { f: font(i ? 400 : 700, 24, MONO), c: i ? TX : MU });
    text(ctx, r[2], 990, y, { f: font(i ? 600 : 700, 24, MONO), c: i ? NUM : MU, al: 'right' });
  });
  // aviso estilo terminal
  rrect(ctx, 134, 960, 880, 110, 10); ctx.fillStyle = 'rgba(210,153,34,0.12)'; ctx.fill(); ctx.strokeStyle = '#d29922'; ctx.lineWidth = 2; ctx.stroke();
  text(ctx, 'WARNING', 160, 1004, { f: font(700, 22, MONO), c: '#d29922', ls: 2 });
  text(ctx, 'matriz usuario × película: 98,8 % vacía', 160, 1046, { f: font(500, 26, MONO), c: TX });
  // barra de pasos
  const steps = ['premio', 'datos', 'carrera', 'empate', 'giro', 'negocio', 'svd', 'lección'];
  steps.forEach((s, i) => { text(ctx, (i === 1 ? '▸ ' : '  ') + s, 134 + (i % 4) * 220, 1150 + Math.floor(i / 4) * 40, { f: font(i === 1 ? 700 : 400, 22, MONO), c: i < 1 ? GRN : i === 1 ? TX : MU }); });
  text(ctx, 'Continuidad: el notebook avanza celda a celda y hace scroll', 540, 1830, { f: font(400, 20, MONO), c: MU, al: 'center' });
}

// ---------------------------------------------------------------- B · Suizo minimal
function styleB(ctx) {
  const BG = '#f3f1ec', K = '#111';
  ctx.fillStyle = BG; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = K; ctx.fillRect(60, 200, 960, 4);
  text(ctx, '02', 60, 420, { f: font(800, 230, '"Helvetica Neue", Helvetica, sans-serif'), c: C.red });
  text(ctx, 'El concurso', 420, 300, { f: font(700, 44, '"Helvetica Neue", Helvetica, sans-serif'), c: K });
  text(ctx, 'Netflix publica sus datos', 420, 350, { f: font(400, 34, '"Helvetica Neue", Helvetica, sans-serif'), c: '#666' });
  text(ctx, 'Oct 2006', 420, 400, { f: font(400, 34, '"Helvetica Neue", Helvetica, sans-serif'), c: '#666' });
  ctx.fillStyle = K; ctx.fillRect(60, 470, 960, 2);
  text(ctx, '100.480.507', 54, 640, { f: font(800, 168, '"Helvetica Neue", Helvetica, sans-serif'), c: K, ls: -6 });
  text(ctx, 'valoraciones reales de usuarios', 60, 700, { f: font(400, 36, '"Helvetica Neue", Helvetica, sans-serif'), c: K });
  // matriz minimal
  const r = rng(4), n = 26, m = 12, s = 36, x0 = 60, y0 = 770;
  for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) {
    const on = r() < 0.07;
    ctx.fillStyle = on ? C.red : 'rgba(17,17,17,0.08)'; ctx.fillRect(x0 + i * s + 3, y0 + j * s + 3, s - 6, s - 6);
  }
  ctx.fillStyle = K; ctx.fillRect(60, 1340, 960, 2);
  [['480.189', 'usuarios'], ['17.770', 'películas'], ['98,8 %', 'vacía']].forEach(([v, l], i) => {
    text(ctx, v, 60 + i * 330, 1300, { f: font(700, 48, '"Helvetica Neue", Helvetica, sans-serif'), c: i === 2 ? C.red : K });
  });
  [['usuarios'], ['películas'], ['vacía']].forEach(([l], i) => text(ctx, l, 60 + i * 330, 1385, { f: font(400, 28, '"Helvetica Neue", Helvetica, sans-serif'), c: '#666' }));
  text(ctx, 'Fuente: Netflix Prize dataset · n = 100.480.507', 60, 1830, { f: font(400, 22, '"Helvetica Neue", Helvetica, sans-serif'), c: '#888' });
  text(ctx, 'Continuidad: la retícula fija; números y bloques se deslizan sobre ella', 60, 1866, { f: font(400, 20, '"Helvetica Neue", Helvetica, sans-serif'), c: '#aaa' });
}

// ---------------------------------------------------------------- C · Partículas (cada punto es una valoración)
function styleC(ctx) {
  ctx.fillStyle = '#05060a'; ctx.fillRect(0, 0, W, H);
  const g = ctx.createRadialGradient(540, 760, 50, 540, 760, 800); g.addColorStop(0, 'rgba(60,80,140,0.22)'); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  const r = rng(12), n = 60, m = 52, s = 15, x0 = 540 - n * s / 2, y0 = 340;
  // corriente de partículas cayendo hacia la matriz (vienen de la escena anterior)
  for (let k = 0; k < 420; k++) {
    const x = 540 + (r() - .5) * 900 * Math.pow(r(), .5), y = 200 + r() * 140;
    ctx.fillStyle = `rgba(255,214,140,${.25 + r() * .6})`; ctx.beginPath(); ctx.arc(x, y, 1.2 + r() * 2.2, 0, 7); ctx.fill();
  }
  for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) {
    const x = x0 + i * s, y = y0 + j * s, on = r() < 0.03;
    if (on) {
      ctx.save(); ctx.shadowColor = C.red; ctx.shadowBlur = 14; ctx.fillStyle = '#ff5a5f'; ctx.beginPath(); ctx.arc(x, y, 4, 0, 7); ctx.fill(); ctx.restore();
    } else { ctx.fillStyle = 'rgba(140,160,210,0.14)'; ctx.beginPath(); ctx.arc(x, y, 1.6, 0, 7); ctx.fill(); }
  }
  text(ctx, 'cada punto = una valoración', 540, 1160, { f: font(400, 26, MONO), c: 'rgba(200,210,235,0.7)', al: 'center' });
  text(ctx, '100.480.507', 540, 1280, { f: font(200, 110), c: '#fff', al: 'center', ls: 2 });
  text(ctx, 'VALORACIONES · 98,8 % DE LA MATRIZ VACÍA', 540, 1335, { f: font(500, 22, MONO), c: '#ff5a5f', al: 'center', ls: 4 });
  text(ctx, 'HISTORIAS DE DATOS · 02', 540, 140, { f: font(500, 22, MONO), c: 'rgba(200,210,235,0.6)', al: 'center', ls: 6 });
  text(ctx, 'Continuidad: los mismos puntos se transforman en cada escena', 540, 1830, { f: font(400, 20, MONO), c: 'rgba(200,210,235,0.45)', al: 'center' });
}

// ---------------------------------------------------------------- D · Informe / dashboard
function styleD(ctx) {
  const BG = '#eef0f3', CARD = '#fff', K = '#1b1f24', MU = '#6a737d', BL = '#2f6fed';
  ctx.fillStyle = BG; ctx.fillRect(0, 0, W, H);
  const card = (x, y, w, h) => { ctx.save(); ctx.shadowColor = 'rgba(16,24,40,0.10)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 6; rrect(ctx, x, y, w, h, 18); ctx.fillStyle = CARD; ctx.fill(); ctx.restore(); };
  text(ctx, 'Caso 01 · Netflix Prize', 60, 160, { f: font(700, 40), c: K });
  text(ctx, 'Informe del caso · actualizado a oct 2006', 60, 205, { f: font(400, 24), c: MU });
  rrect(ctx, 820, 128, 200, 48, 24); ctx.fillStyle = 'rgba(229,56,59,0.1)'; ctx.fill();
  text(ctx, '● EN DIRECTO', 920, 160, { f: font(700, 20), c: C.red, al: 'center' });
  [['Valoraciones', '100,5 M', '+100 %'], ['Usuarios', '480.189', ''], ['Películas', '17.770', ''], ['Densidad', '1,2 %', '98,8 % vacía']].forEach(([l, v, d], i) => {
    const x = 60 + (i % 2) * 490, y = 250 + Math.floor(i / 2) * 190;
    card(x, y, 470, 170);
    text(ctx, l, x + 30, y + 50, { f: font(500, 24), c: MU });
    text(ctx, v, x + 30, y + 120, { f: font(800, 60), c: i === 3 ? C.red : K });
    if (d) text(ctx, d, x + 440, y + 50, { f: font(600, 20), c: i === 3 ? C.red : '#1a7f37', al: 'right' });
  });
  card(60, 640, 960, 560);
  text(ctx, 'Matriz usuario × película', 90, 695, { f: font(700, 28), c: K });
  text(ctx, 'cada celda: una nota de 1 a 5', 90, 732, { f: font(400, 22), c: MU });
  const r = rng(8), n = 30, m = 13, s = 30, x0 = 90, y0 = 770;
  for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) {
    const on = r() < 0.08, v = 1 + Math.floor(r() * 5);
    ctx.fillStyle = on ? `rgba(47,111,237,${.2 + .16 * v})` : '#f1f3f6'; rrect(ctx, x0 + i * s + 2, y0 + j * s + 2, s - 4, s - 4, 4); ctx.fill();
  }
  card(60, 1230, 960, 150);
  text(ctx, 'Línea temporal', 90, 1280, { f: font(700, 24), c: K });
  ctx.fillStyle = '#dfe3e8'; ctx.fillRect(90, 1325, 900, 6);
  ctx.fillStyle = BL; ctx.fillRect(90, 1325, 120, 6);
  ['2006', '2007', '2008', '2009'].forEach((y, i) => text(ctx, y, 90 + i * 300, 1365, { f: font(500, 20), c: i === 0 ? BL : MU }));
  ctx.fillStyle = BL; ctx.beginPath(); ctx.arc(210, 1328, 12, 0, 7); ctx.fill();
  text(ctx, 'Continuidad: el informe se actualiza; la línea temporal avanza', 540, 1830, { f: font(400, 20), c: MU, al: 'center' });
}

const STY = [styleA, styleB, styleC, styleD];
const STORY = {
  title: '', hud: false, vignette: false, grain: 0.08,
  scenes: STY.map(() => ({ dur: 1, draw: () => { } })),
  world: (ctx, t) => { ctx.setTransform(1, 0, 0, 1, 0, 0); STY[Math.min(3, Math.floor(t))](ctx); },
  narr: STY.map((_, i) => ({ scene: i, a: 0, b: 1, text: 'Soltaron 100 millones' })),
  events: [],
};
setup();
renderFrame(0.5);
