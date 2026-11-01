// aviones-wald · Historias de datos · estilo A (Notebook).
// Un notebook oscuro que avanza celda a celda; cada beat es una celda con su salida. El mismo avión
// (cenital, con sus agujeros) atraviesa toda la historia: se acribilla, se blinda mal, se vuelve fantasma,
// se blinda bien y acaba dibujado en el informe de Wald. Su cara entra como «telón» desde arriba.
(async () => {
  const T = await cargarVoz('voz.tiempos.json');
  const E = T.en;
  const B = await (await fetch('beats.json')).json();
  // lib.js declara `let CARA` (no llega a window) y capture.py solo hace seek si window.CARA: lo exponemos aquí
  const _cara = await cargarCara('cara.mp4'); if (_cara) window.CARA = _cara;

  const beats = B.beats.map(b => ({ ...b, t0: E(b.ancla) }));
  beats[0].t0 = 0;
  beats.forEach((b, i) => { b.t1 = i + 1 < beats.length ? beats[i + 1].t0 : T.duracion + 0.8; b.d = b.t1 - b.t0; });
  const BN = n => beats[n - 1];
  const rel = (n, s) => E(s, BN(n).t0) - BN(n).t0;          // sub-ancla, en segundos desde el inicio del beat n

  // ---------------------------------------------------------------- paleta (estilo A · Notebook)
  const N = {
    BG: '#0d1117', PAN: '#161b22', PAN2: '#1c2128', LN: '#30363d', TX: '#e6edf3', MU: '#7d8590', KW: '#ff7b72',
    STR: '#a5d6ff', FN: '#d2a8ff', NUM: '#79c0ff', GRN: '#3fb950', OR: '#ff911e', RED: '#f85149',
    PL: '#aeb7c2', PLS: '#e6edf3', PAPER: '#ece6d6', INK: '#2b2620',
  };
  const TYPE = '"American Typewriter", "Courier New", monospace';
  const TMP = mk(W, H);
  const ramp = (t, a, d) => eio(pr(t, a, d));
  const L2 = (A, Bp, p) => ({ x: lerp(A.x, Bp.x, p), y: lerp(A.y, Bp.y, p), s: lerp(A.s, Bp.s, p) });
  function wrap(ctx, s, f, maxW) {
    ctx.save(); ctx.font = f; const out = []; let l = '';
    for (const w of s.split(' ')) { const tt = l ? l + ' ' + w : w; if (ctx.measureText(tt).width > maxW && l) { out.push(l); l = w; } else l = tt; }
    if (l) out.push(l); ctx.restore(); return out;
  }
  const hex = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16));
  const mix = (a, b, p) => { const A = hex(a), Bc = hex(b); return `rgb(${A.map((v, i) => Math.round(lerp(v, Bc[i], p))).join(',')})`; };
  const tw = (ctx, s, f) => { ctx.save(); ctx.font = f; const w = ctx.measureText(s).width; ctx.restore(); return w; };

  // ---------------------------------------------------------------- el avión (cenital, morro arriba). Unidad = media envergadura
  const sym = pts => [...pts, ...pts.slice(1, -1).reverse().map(([x, y]) => [-x, y])];
  const le = ax => -0.18 + (ax - 0.08) * 0.125, te = ax => 0.16 - (ax - 0.08) * 0.125;
  const FUS = sym([[0, -0.64], [0.04, -0.61], [0.07, -0.53], [0.085, -0.38], [0.09, -0.1], [0.08, 0.3], [0.055, 0.62], [0.028, 0.8], [0, 0.82]]);
  const WING = [[0.07, le(0.07)], [0.97, le(0.97)], [1.0, -0.035], [0.99, 0.03], [0.96, te(0.96)], [0.07, te(0.07)]];
  const TAIL = [[0.03, 0.58], [0.33, 0.665], [0.355, 0.70], [0.34, 0.745], [0.03, 0.765]];
  const ENG = [-0.55, -0.28, 0.28, 0.55].map(x => ({ x, y: le(Math.abs(x)) - 0.02 }));
  const poly = (pts, m = 1) => { const p = new Path2D(); pts.forEach(([x, y], i) => i ? p.lineTo(x * m, y) : p.moveTo(x * m, y)); p.closePath(); return p; };
  const NAC = ENG.map(e => { const p = new Path2D(); p.roundRect(e.x - 0.042, e.y - 0.13, 0.084, 0.25, 0.04); return p; });
  const P_WING = [poly(WING), poly(WING, -1), poly(TAIL), poly(TAIL, -1)], P_FUS = poly(FUS);
  const PARTS = [...P_WING, P_FUS, ...NAC];

  // agujeros (patrón ilustrativo, nunca en los motores) y su orden de llegada
  const HOLES = (() => {
    const r = rng(43), out = []; let tries = 0;
    const nearEng = (x, y) => ENG.some(e => Math.abs(x - e.x) < 0.078 && y > e.y - 0.17 && y < e.y + 0.15);
    const add = (zone, n, gen) => {
      let c = 0;
      while (c < n && tries++ < 20000) {
        const [x, y] = gen();
        if (nearEng(x, y) || out.some(o => Math.hypot(o.x - x, o.y - y) < 0.04)) continue;
        out.push({ x, y, zone }); c++;
      }
    };
    add('fus', 24, () => [(r() - .5) * 0.1, -0.46 + r() * 1.1]);
    add('ala', 40, () => { const s = r() < .5 ? -1 : 1, ax = 0.13 + r() * 0.8; return [s * ax, lerp(le(ax) + 0.03, te(ax) - 0.03, r())]; });
    add('fus', 6, () => { const s = r() < .5 ? -1 : 1; return [s * (0.08 + r() * 0.22), 0.67 + r() * 0.05]; });
    for (let i = out.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [out[i], out[j]] = [out[j], out[i]]; }
    return out;
  })();
  const ENG_HOLES = ENG.flatMap((e, i) => [[-0.015, -0.06], [0.012, 0.0], [-0.008, 0.06]].map(([dx, dy]) => ({ x: e.x + dx, y: e.y + dy })));

  // placas de blindaje: la solución «obvia» (fuselaje y alas) y su destino en los motores
  const PL_OBV = [
    { x: 0, y: -0.24, w: 0.17, h: 0.44 }, { x: 0, y: 0.36, w: 0.15, h: 0.5 },
    { x: 0.415, y: -0.01, w: 0.13, h: 0.2 }, { x: -0.415, y: -0.01, w: 0.13, h: 0.2 },
    { x: 0.77, y: -0.012, w: 0.27, h: 0.12 }, { x: -0.77, y: -0.012, w: 0.27, h: 0.12 },
  ];
  const engPlate = e => ({ x: e.x, y: e.y - 0.005, w: 0.115, h: 0.29 });
  const PL_GOOD = [engPlate(ENG[2]), engPlate(ENG[1]), null, null, engPlate(ENG[3]), engPlate(ENG[0])];

  function decorate(ctx, s, o) {
    if (o.heat) {
      ctx.save(); ctx.globalAlpha *= o.heat;
      ctx.fillStyle = 'rgba(255,145,30,0.16)'; P_WING.forEach(p => ctx.fill(p));
      ctx.fillStyle = 'rgba(255,145,30,0.30)'; ctx.fill(P_FUS);
      ctx.restore();
    }
    if (o.glow) {
      ctx.save(); ctx.globalAlpha *= o.glow;
      for (const e of ENG) {
        const g = ctx.createRadialGradient(e.x, e.y, 0, e.x, e.y, 0.2);
        g.addColorStop(0, 'rgba(255,145,30,0.55)'); g.addColorStop(1, 'rgba(255,145,30,0)');
        ctx.fillStyle = g; ctx.fillRect(e.x - 0.2, e.y - 0.2, 0.4, 0.4);
      }
      ctx.fillStyle = N.OR; NAC.forEach(p => ctx.fill(p));
      ctx.restore();
    }
    const rr = Math.max(0.013, 2.6 / s);
    if (o.dots) {
      const n = Math.min(HOLES.length, o.dots);
      ctx.fillStyle = o.dotC || N.RED;
      for (let k = 0; k < n; k++) {
        const h = HOLES[k]; let x = h.x, y = h.y;
        if (o.rain != null) {
          const p = pr(o.rain, o.rainA + k * o.rainStep, 0.32);
          if (p <= 0) continue;
          const fx = o.rainFrom.x + (((k * 37) % 11) - 5) * 0.012, fy = o.rainFrom.y;
          x = lerp(fx, h.x, p); y = lerp(fy, h.y, p * p);
        }
        ctx.beginPath(); ctx.arc(x, y, rr, 0, 7); ctx.fill();
      }
    }
    if (o.engHoles) {
      ctx.save(); ctx.globalAlpha *= o.engHoles; ctx.fillStyle = N.RED;
      for (const h of ENG_HOLES) { ctx.beginPath(); ctx.arc(h.x, h.y, rr * 1.15, 0, 7); ctx.fill(); }
      ctx.restore();
    }
    if (o.plates) for (const P of o.plates) {
      if (!P || P.a <= 0) continue;
      ctx.save(); ctx.globalAlpha *= P.a ?? 1; ctx.translate(P.x, P.y); if (P.r) ctx.rotate(P.r); const k = P.k ?? 1; ctx.scale(k, k);
      ctx.beginPath(); ctx.roundRect(-P.w / 2, -P.h / 2, P.w, P.h, 0.018);
      ctx.fillStyle = P.c || '#59626d'; ctx.fill(); ctx.lineWidth = 2 / s; ctx.strokeStyle = '#9aa4ae'; ctx.stroke();
      ctx.fillStyle = '#d0d7de'; const bo = Math.max(0.009, 2 / s), m = 0.022;
      for (const [bx, by] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) { ctx.beginPath(); ctx.arc(bx * (P.w / 2 - m), by * (P.h / 2 - m), bo, 0, 7); ctx.fill(); }
      ctx.restore();
    }
  }
  function plane(ctx, cx, cy, s, o = {}) {
    const a = o.a ?? 1;
    if (a <= 0.003 || s <= 0) return;
    if (a < 0.997 || o.ghost) {
      const tc = TMP.getContext('2d'); tc.setTransform(1, 0, 0, 1, 0, 0); tc.clearRect(0, 0, W, H); tc.globalAlpha = 1;
      tc.setTransform(ctx.getTransform());
      if (o.ghost) {
        tc.save(); tc.translate(cx, cy); if (o.rot) tc.rotate(o.rot); tc.scale(s, s);
        tc.setLineDash([9 / s, 7 / s]); tc.lineWidth = 4 / s; tc.strokeStyle = o.stroke || '#8b949e'; PARTS.forEach(p => tc.stroke(p));
        tc.setLineDash([]); tc.globalCompositeOperation = 'destination-out'; PARTS.forEach(p => tc.fill(p));
        tc.globalCompositeOperation = 'source-over'; tc.fillStyle = 'rgba(174,183,194,0.06)'; PARTS.forEach(p => tc.fill(p));
        decorate(tc, s, o); tc.restore();
      } else plane(tc, cx, cy, s, { ...o, a: 1 });
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha *= a; ctx.drawImage(TMP, 0, 0); ctx.restore();
      if (o.zeros) zeros(ctx, cx, cy, s, o.zeros * a, o.zeroLit);
      return;
    }
    ctx.save(); ctx.translate(cx, cy); if (o.rot) ctx.rotate(o.rot); ctx.scale(s, s); ctx.lineJoin = 'round';
    ctx.strokeStyle = o.stroke || N.PLS; ctx.lineWidth = (o.lw ?? 2) * 2 / s; PARTS.forEach(p => ctx.stroke(p));
    ctx.fillStyle = o.fill || N.PL; PARTS.forEach(p => ctx.fill(p));
    if (!o.flat) { ctx.strokeStyle = 'rgba(13,17,23,0.18)'; ctx.lineWidth = 1.2 / s; ctx.beginPath(); ctx.moveTo(0, -0.5); ctx.lineTo(0, 0.74); ctx.stroke(); }
    decorate(ctx, s, o);
    ctx.restore();
    if (o.zeros) zeros(ctx, cx, cy, s, o.zeros, o.zeroLit);
  }
  function zeros(ctx, cx, cy, s, a, lit = 0) {
    for (const e of ENG) {
      const x = cx + e.x * s, y = cy + (e.y - 0.27) * s, sz = clamp(s / 300, 0.6, 2.2);
      ctx.save(); ctx.globalAlpha *= a; ctx.translate(x, y); ctx.scale(sz, sz);
      if (lit) { ctx.shadowColor = 'rgba(255,255,255,0.9)'; ctx.shadowBlur = 24 * lit; }
      rrect(ctx, -24, -24, 48, 48, 9); ctx.fillStyle = lit ? '#f6f8fa' : N.PAN2; ctx.fill();
      ctx.shadowBlur = 0; ctx.lineWidth = 2; ctx.strokeStyle = lit ? '#fff' : N.LN; ctx.stroke();
      text(ctx, '0', 0, 2, { f: font(800, 32, MONO), c: lit ? N.BG : N.TX, al: 'center', bl: 'middle' });
      ctx.restore();
    }
  }

  // ---------------------------------------------------------------- piezas del notebook
  function tokens(line) {
    const out = [], re = /(#.*$)|("[^"]*")|(\b\d[\d_]*\b)|(\b(?:True|False|None|not|in|and|or|len)\b)|([A-Za-z_][\w]*)(?=\()|(==|=|~)/g;
    let last = 0, m;
    while ((m = re.exec(line))) {
      if (m.index > last) out.push([line.slice(last, m.index), N.TX]);
      out.push([m[0], m[1] ? N.MU : m[2] ? N.STR : m[3] ? N.NUM : m[4] ? N.KW : m[5] ? N.FN : N.KW]);
      last = m.index + m[0].length;
    }
    if (last < line.length) out.push([line.slice(last), N.TX]);
    return out;
  }
  const CF = font(500, 27, MONO);
  function cellBox(ctx, y, n, lines, lt, a) {
    if (a <= 0) return;
    const h = 34 + lines.length * 42, run = lt < 0.75;
    ctx.save(); ctx.globalAlpha *= a;
    text(ctx, run ? '[*]:' : `[${n}]:`, 30, y + 50, { f: font(500, 22, MONO), c: run ? N.GRN : N.MU });
    rrect(ctx, 100, y, 940, h, 10); ctx.fillStyle = N.PAN; ctx.fill();
    ctx.strokeStyle = lt < 1.3 ? N.GRN : N.LN; ctx.lineWidth = 2; ctx.stroke();
    const total = lines.reduce((s, l) => s + l.length, 0); let left = Math.floor(total * pr(lt, 0.05, 0.42));
    let cur = null;
    lines.forEach((l, i) => {
      let x = 126; const yy = y + 50 + i * 42;
      for (const [s, c] of tokens(l)) {
        if (left <= 0) break;
        const ss = s.slice(0, left); left -= ss.length;
        text(ctx, ss, x, yy, { f: CF, c }); x += tw(ctx, ss, CF);
        cur = [x, yy];
      }
    });
    if (lt < 0.55 && cur) { ctx.fillStyle = N.TX; ctx.fillRect(cur[0] + 2, cur[1] - 24, 13, 30); }
    ctx.restore();
  }
  function card(ctx, x, y, w, h, a, title) {
    if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a;
    ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 10;
    rrect(ctx, x, y, w, h, 14); ctx.fillStyle = 'rgba(13,17,23,0.94)'; ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.strokeStyle = N.LN; ctx.lineWidth = 2; ctx.stroke();
    if (title) text(ctx, title, x + 22, y + 38, { f: font(500, 20, MONO), c: N.MU });
    ctx.restore();
  }
  function errBox(ctx, x, y, w, kind, msg, a) {
    if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a;
    rrect(ctx, x, y, w, 104, 10); ctx.fillStyle = 'rgba(248,81,73,0.13)'; ctx.fill(); ctx.strokeStyle = N.RED; ctx.lineWidth = 2; ctx.stroke();
    text(ctx, kind, x + 24, y + 40, { f: font(700, 24, MONO), c: N.RED });
    text(ctx, msg, x + 24, y + 80, { f: font(500, 25, MONO), c: N.TX });
    ctx.restore();
  }
  function check(ctx, x, y, a, jit, label, t) {
    if (a <= 0) return;
    const dx = jit * Math.sin(t * 71) * 7, dr = jit * Math.sin(t * 53) * 0.06;
    ctx.save(); ctx.globalAlpha *= a; ctx.translate(x + dx, y); ctx.rotate(dr);
    rrect(ctx, -70, -46, 140, 92, 14); ctx.fillStyle = 'rgba(63,185,80,0.14)'; ctx.fill(); ctx.strokeStyle = N.GRN; ctx.lineWidth = 3; ctx.stroke();
    ctx.strokeStyle = N.GRN; ctx.lineWidth = 9; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(-28, 2); ctx.lineTo(-8, 22); ctx.lineTo(30, -22); ctx.stroke();
    if (label) text(ctx, label, 0, 82, { f: font(600, 22, MONO), c: N.GRN, al: 'center' });
    ctx.restore();
  }
  function chrome(ctx) {
    ctx.fillStyle = N.PAN; ctx.fillRect(0, 100, W, 84);
    ['#ff5f57', '#febc2e', '#28c840'].forEach((c, i) => { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(54 + i * 32, 142, 9, 0, 7); ctx.fill(); });
    rrect(ctx, 170, 112, 400, 72, [10, 10, 0, 0]); ctx.fillStyle = N.BG; ctx.fill();
    text(ctx, 'aviones_wald.ipynb', 196, 157, { f: font(500, 24, MONO), c: N.TX });
    text(ctx, 'Historias de datos', 1030, 155, { f: font(400, 20, MONO), c: N.MU, al: 'right' });
  }

  // ---------------------------------------------------------------- celdas de código (el notebook avanza)
  const CELLS = [];
  const cellAt = (n, lines, dt = 0) => CELLS.push({ t: BN(n).t0 + dt, lines });
  cellAt(2, ['# 1943 · Segunda Guerra Mundial', 'flota = bombarderos(año=1943)']);
  cellAt(3, ['perdidos = flota[flota.fecha == "1943-08-17"]', 'len(perdidos)']);
  cellAt(4, ['srg = grupo("Statistical Research Group")', 'srg.sede']);
  cellAt(5, ['srg.miembros["Abraham Wald"]']);
  cellAt(6, ['avion.blindar(zonas="todo")']);
  cellAt(7, ['# solo los aviones que volvieron', 'volvieron.agujeros.plot()']);
  cellAt(8, ['volvieron.agujeros["motores"]']);
  cellAt(9, ['avion.blindar(zonas=["fuselaje", "alas"])']);
  cellAt(11, ['no_volvieron = flota[~flota.volvio]']);
  cellAt(12, ['no_volvieron.agujeros']);
  cellAt(13, ['avion.blindar(zonas=["motores"])']);
  cellAt(14, ['wald.informe(1943)']);
  cellAt(15, ['vulnerabilidad = estimar(solo=volvieron)']);
  cellAt(17, ['clientes[clientes.activo]']);
  cellAt(18, ['startups[startups.exito]']);
  cellAt(18, ['modelos[modelos.en_produccion]'], rel(18, 'solo los modelos'));
  CELLS.forEach((c, i) => c.n = i + 1);
  function drawCells(ctx, t, lay) {
    let k = -1; CELLS.forEach((c, i) => { if (c.t <= t + 1e-6) k = i; });
    if (k < 0) return null;
    const cur = CELLS[k], prev = CELLS[k - 1], lt = t - cur.t, p = eio(pr(lt, 0, 0.35));
    const y0 = lerp(222, 678, lay);
    if (prev && p < 1) cellBox(ctx, y0 - 190 * p, prev.n, prev.lines, 9, 1 - p);
    cellBox(ctx, y0 + 190 * (1 - p), cur.n, cur.lines, lt, p);
    return cur;
  }

  // ---------------------------------------------------------------- posiciones compartidas
  const MAIN = z => ({ x: 540, y: z.y + 470, s: 300 });          // el avión protagonista en el escenario
  const CARD_PL = { x: 800, y: 455, s: 185 };                       // el avión en la tarjeta sobre su cara
  const formSlot = (k, z, lt) => {
    const r = Math.floor(k / 6), c = k % 6;
    return { x: 540 + (c - 2.5) * 140 + (r % 2 ? 35 : -35), y: z.y + 660 + (r - 4.5) * 62 + Math.abs(c - 2.5) * 20 - lt * 26 + Math.sin(lt * 1.3 + k) * 3 };
  };
  const HERO_K = 26;   // la plaza de la formación que ocupa el avión del gancho
  const gridSlot = (k, z) => ({ x: 540 + ((k % 10) - 4.5) * 94, y: z.y + 420 + Math.floor(k / 10) * 94 });
  const ANG = -0.5;
  const blockMap = (k, z) => {   // manzanas de Manhattan (coordenadas de mapa → pantalla)
    const i = k % 6, j = Math.floor(k / 6), mx = (i - 2.5) * 180, my = (j - 4.5) * 64;
    const ca = Math.cos(ANG), sa = Math.sin(ANG);
    return { x: 540 + mx * ca - my * sa, y: z.y + 500 + mx * sa + my * ca };
  };

  // calendario de taco
  function calendar(ctx, x, y, s, top, big, sub, tear) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    const w = 280, h = 230;
    const page = (a, b, c) => {
      rrect(ctx, -w / 2, 0, w, h, 12); ctx.fillStyle = '#f0f2f5'; ctx.fill();
      ctx.save(); ctx.beginPath(); ctx.roundRect(-w / 2, 0, w, 58, [12, 12, 0, 0]); ctx.fillStyle = '#da3633'; ctx.fill(); ctx.restore();
      text(ctx, a, 0, 40, { f: font(700, 26, MONO), c: '#fff', al: 'center', ls: 4 });
      text(ctx, b, 0, 158, { f: font(800, b.length > 4 ? 80 : 96, MONO), c: N.BG, al: 'center' });
      if (c) text(ctx, c, 0, 206, { f: font(600, 26, MONO), c: '#57606a', al: 'center', ls: 3 });
    };
    page(top[1], big[1], sub[1]);
    if (tear < 1) {
      ctx.save(); const q = eo(tear);
      ctx.translate(-w / 2, 0); ctx.rotate(-q * 0.9); ctx.translate(w / 2 - q * 60, q * q * 500);
      ctx.globalAlpha *= 1 - q; page(top[0], big[0], sub[0]); ctx.restore();
    }
    ctx.fillStyle = '#57606a'; for (let i = -2; i <= 2; i++) { ctx.beginPath(); ctx.arc(i * 50, 0, 7, 0, 7); ctx.fill(); }
    ctx.restore();
  }

  // ================================================================= DIBUJOS POR BEAT
  // DRAW[n](ctx, lt, z, capa, b): capa 'under' = bajo el telón de su cara; 'over' = encima.
  const DRAW = {};

  // 1 · Gancho (cara): tarjeta con el avión acribillado; sello «AL REVÉS»
  const tRev = rel(1, 'al revés');
  function stamp(ctx, x, y, q, a = 1) {
    if (q <= 0) return;
    ctx.save(); ctx.globalAlpha *= clamp(q * 4) * a; ctx.translate(x, y); ctx.rotate(-0.16); const k = lerp(1.9, 1, eo(q)); ctx.scale(k, k);
    rrect(ctx, -170, -52, 340, 104, 12); ctx.lineWidth = 7; ctx.strokeStyle = N.OR; ctx.stroke();
    ctx.fillStyle = 'rgba(255,145,30,0.12)'; ctx.fill();
    text(ctx, 'AL REVÉS', 0, 4, { f: font(900, 62), c: N.OR, al: 'center', bl: 'middle', ls: 3 });
    ctx.restore();
  }
  DRAW[1] = (ctx, lt, z, capa) => {
    if (capa !== 'over') return;
    const p = eo(pr(lt, 0.2, 0.5));
    card(ctx, 580, 220 + 30 * (1 - p), 440, 470, p, 'Out[ ]: impactos');
    plane(ctx, CARD_PL.x, CARD_PL.y + 30 * (1 - p), CARD_PL.s, { a: p, dots: 999 });
    stamp(ctx, 800, 560, pr(lt, tRev, 0.22));
  };

  // 2 · 1943: el avión del gancho se encoge y es uno de una formación; calendario 1943
  DRAW[2] = (ctx, lt, z, capa) => {
    const hp = ramp(lt, 0, 0.5), sp = ramp(lt, 0.45, 0.7);
    const slot = formSlot(HERO_K, z, lt);
    const hero = L2(L2(CARD_PL, { x: 540, y: z.y + 560, s: 185 }, hp), { ...slot, s: 30 }, sp);
    if (capa === 'over') {
      if (lt < 0.5) {
        plane(ctx, hero.x, hero.y, hero.s, { dots: 999 });
        stamp(ctx, lerp(800, 540, hp), lerp(560, z.y + 665, hp), 1, 1 - hp);
      }
      return;
    }
    ctx.save(); ctx.globalAlpha *= pr(lt, 0.25, 0.3); calendar(ctx, 540, z.y + 30 - 40 * (1 - eo(pr(lt, 0.25, 0.4))), 1, ['', 'AÑO'], ['', '1943'], ['', 'IIGM'], 1); ctx.restore();
    for (let k = 0; k < 60; k++) {
      if (k === HERO_K) continue;
      const P = formSlot(k, z, lt), d = Math.hypot(k % 6 - 2, Math.floor(k / 6) - 4);
      const a = pr(lt, 0.7 + d * 0.06, 0.3);
      if (a > 0) plane(ctx, P.x, P.y, 30 * eo(a), { flat: true });
    }
    if (lt >= 0.5) plane(ctx, hero.x, hero.y, hero.s, { dots: Math.round(999 * (1 - sp)), flat: hero.s < 60 });
  };

  // 3 · 17 ago 1943: la formación se ordena en cuadrícula; 60 se apagan; contador 0 → 60
  const T3 = { a: 0.7, step: 1.85 / 60 };
  const lost3 = lt => clamp(Math.floor((lt - T3.a) / T3.step) + 1, 0, 60);
  DRAW[3] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const cp = ramp(lt, 0, 0.5), gp = ramp(lt, 0.1, 0.7);
    calendar(ctx, lerp(540, 230, cp), z.y + 30, lerp(1, 0.9, cp), ['AÑO', 'AGOSTO'], ['1943', '17'], ['IIGM', '1943'], pr(lt, 0.15, 0.6));
    const n = lost3(lt);
    for (let k = 0; k < 60; k++) {
      const A = formSlot(k, z, BN(2).d), G = gridSlot(k, z);
      const x = lerp(A.x, G.x, gp), y = lerp(A.y, G.y, gp);
      const off = k < n ? pr(lt, T3.a + k * T3.step, 0.25) : 0;
      plane(ctx, x, y, 30, { fill: mix(N.PL, '#2a3039', off), stroke: mix(N.PLS, '#3b424c', off), flat: true });
    }
    const a = pr(lt, 0.4, 0.3);
    text(ctx, String(n), 760, z.y + 190, { f: font(800, 170, MONO), c: n ? N.RED : N.TX, al: 'center', a });
    text(ctx, 'no vuelven', 760, z.y + 245, { f: font(500, 30, MONO), c: N.TX, al: 'center', a });
    text(ctx, 'misión Schweinfurt-Regensburg', 540, z.y + 945, { f: font(400, 21, MONO), c: N.MU, al: 'center', a: pr(lt, 1.2, 0.4) });
  };

  // 4 · Columbia: la cuadrícula se aleja y es Manhattan; pin en Columbia; zoom a la placa del SRG
  const T4 = { pin: rel(4, 'Universidad de Columbia'), zoom: rel(4, 'un grupo de matemáticos') };
  function door(ctx, cx, cy, k, open, a = 1) {
    ctx.save(); ctx.globalAlpha *= a; ctx.translate(cx, cy); ctx.scale(k, k);
    rrect(ctx, -250, -330, 500, 660, 8); ctx.fillStyle = '#0a0d11'; ctx.fill();
    ctx.strokeStyle = '#3d444d'; ctx.lineWidth = 10; ctx.stroke();
    for (const sd of [-1, 1]) {
      ctx.save(); ctx.translate(sd * 125 + sd * open * 240, 0); ctx.globalAlpha *= 1 - open * 0.9;
      ctx.fillStyle = '#20262e'; ctx.fillRect(-120, -320, 240, 640);
      ctx.strokeStyle = '#2f363f'; ctx.lineWidth = 4; ctx.strokeRect(-90, -280, 180, 220); ctx.strokeRect(-90, -20, 180, 300);
      ctx.fillStyle = '#8a7a52'; ctx.beginPath(); ctx.arc(-sd * 95, 40, 9, 0, 7); ctx.fill();
      ctx.restore();
    }
    // placa
    ctx.save(); ctx.globalAlpha *= 1 - open;
    const g = ctx.createLinearGradient(0, -235, 0, -95); g.addColorStop(0, '#d9b65a'); g.addColorStop(1, '#9a7a2a');
    rrect(ctx, -205, -235, 410, 140, 8); ctx.fillStyle = g; ctx.fill(); ctx.strokeStyle = '#5b4714'; ctx.lineWidth = 3; ctx.stroke();
    text(ctx, 'STATISTICAL', 0, -192, { f: font(800, 30, SANS), c: '#3a2c08', al: 'center', ls: 5 });
    text(ctx, 'RESEARCH GROUP', 0, -152, { f: font(800, 30, SANS), c: '#3a2c08', al: 'center', ls: 5 });
    text(ctx, 'COLUMBIA UNIVERSITY · N.Y.', 0, -115, { f: font(600, 16, MONO), c: '#4a3a10', al: 'center', ls: 3 });
    ctx.restore();
    ctx.restore();
  }
  DRAW[4] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const mp = ramp(lt, 0, 0.8), pinP = pr(lt, T4.pin, 0.35);
    const zp = ramp(lt, T4.zoom - 0.1, 0.7), dp = ramp(lt, T4.zoom + 0.25, 0.45);
    const pin = blockMap(8, z);
    ctx.save();
    ctx.beginPath(); ctx.rect(40, z.y, 1000, 1390 - z.y); ctx.clip();
    ctx.globalAlpha = 1 - dp;
    ctx.translate(pin.x, pin.y); const zk = lerp(lerp(1, 0.82, mp), 7, zp * zp); ctx.scale(zk, zk); ctx.translate(-pin.x, -pin.y);
    // río y calles (aparecen alrededor)
    const ex = pr(lt, 0.3, 0.6);
    ctx.save(); ctx.translate(540, z.y + 500); ctx.rotate(ANG);
    ctx.globalAlpha *= ex;
    ctx.fillStyle = '#0f2236'; ctx.fillRect(-1700, -2200, 1700 - 560, 4400); ctx.fillRect(560, -2200, 1200, 4400);
    text(ctx, 'RÍO HUDSON', -640, -80, { f: font(600, 22, MONO), c: '#3a6ea5', ls: 8, al: 'center' });
    text(ctx, 'MANHATTAN', 0, 400, { f: font(700, 26, MONO), c: '#59626d', ls: 14, al: 'center' });
    ctx.fillStyle = '#1b222b';
    for (let i = 0; i <= 5; i++) for (let j = -16; j <= 24; j++) {
      if (j >= 0 && j <= 9) continue;
      if (j === 12 || j === 13) continue;
      ctx.fillRect((i - 2.5) * 180 - 75, (j - 4.5) * 64 - 22, 150, 44);
    }
    ctx.restore();
    for (let k = 0; k < 60; k++) {
      const G = gridSlot(k, z), M = blockMap(k, z), x = lerp(G.x, M.x, mp), y = lerp(G.y, M.y, mp);
      if (mp < 1) plane(ctx, x, y, 30 * (1 - mp), { fill: '#2a3039', stroke: '#3b424c', flat: true });
      ctx.save(); ctx.translate(x, y); ctx.rotate(ANG); ctx.globalAlpha *= mp;
      ctx.fillStyle = k === 8 && pinP > 0 ? '#3a2a24' : '#1f2630'; ctx.fillRect(-75 * mp, -22 * mp, 150 * mp, 44 * mp);
      ctx.restore();
    }
    // pin
    if (pinP > 0) {
      const py = pin.y - 40 * (1 - eo(pinP)) * 3;
      ctx.save(); ctx.globalAlpha *= clamp(pinP * 3);
      ctx.fillStyle = N.KW; ctx.beginPath(); ctx.arc(pin.x, py - 46, 22, Math.PI, 0); ctx.lineTo(pin.x, py); ctx.closePath(); ctx.fill();
      ctx.fillStyle = N.BG; ctx.beginPath(); ctx.arc(pin.x, py - 46, 8, 0, 7); ctx.fill();
      ctx.restore();
      const la = pr(lt, T4.pin + 0.3, 0.3) * (1 - pr(lt, T4.zoom - 0.15, 0.2));
      ctx.save(); ctx.globalAlpha *= la;
      rrect(ctx, pin.x + 34, pin.y - 112, 360, 84, 10); ctx.fillStyle = 'rgba(22,27,34,0.95)'; ctx.fill(); ctx.strokeStyle = N.LN; ctx.lineWidth = 2; ctx.stroke();
      text(ctx, 'Columbia University', pin.x + 54, pin.y - 76, { f: font(600, 24, MONO), c: N.TX });
      text(ctx, 'Nueva York', pin.x + 54, pin.y - 44, { f: font(400, 20, MONO), c: N.MU });
      ctx.restore();
    }
    ctx.restore();
    if (dp > 0) door(ctx, 540, z.y + 470, lerp(1.25, 1, eo(dp)), 0, dp);
  };

  // 5 · Wald (híbrido): se abre la puerta y sale su ficha; ruta Viena → Nueva York, 1938
  const T5 = { huido: rel(5, 'que había huido') };
  DRAW[5] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const op = ramp(lt, 0.15, 0.5);
    const dk = lerp(1, 0.78, ramp(lt, 0, 0.45));
    if (op < 1) door(ctx, 540, lerp(410 + 470, z.y + 270, ramp(lt, 0, 0.45)), dk, op, 1);
    const cp = ramp(lt, 0.35, 0.45);
    ficha(ctx, 540, z.y + 275 + 40 * (1 - cp), 1, cp, lt, pr(lt, T5.huido, 0.9));
  };
  function ficha(ctx, cx, cy, k, a, lt, route, fold = 0) {
    if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a; ctx.translate(cx, cy); ctx.scale(k, k * (1 - fold));
    const w = 820, h = 500;
    ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 12;
    ctx.fillStyle = N.PAPER; ctx.fillRect(-w / 2, -h / 2, w, h); ctx.shadowColor = 'transparent';
    ctx.fillStyle = '#d64545'; ctx.fillRect(-w / 2, -h / 2 + 92, w, 3);
    ctx.strokeStyle = 'rgba(80,110,160,0.25)'; ctx.lineWidth = 1.5;
    for (let i = 0; i < 8; i++) { ctx.beginPath(); ctx.moveTo(-w / 2, -h / 2 + 140 + i * 46); ctx.lineTo(w / 2, -h / 2 + 140 + i * 46); ctx.stroke(); }
    const ty = (s, x, y, sz, wt = 400, start = 0) => {
      const n = Math.floor(s.length * pr(lt, start, s.length * 0.022));
      text(ctx, s.slice(0, n), x, y, { f: font(wt, sz, TYPE), c: N.INK });
    };
    ty('ABRAHAM WALD · 1902', -w / 2 + 40, -h / 2 + 70, 42, 700, 0.35);
    ty('Matemático. Huye de la Austria nazi', -w / 2 + 40, -h / 2 + 150, 26, 400, 0.8);
    ty('tras la anexión (1938).', -w / 2 + 40, -h / 2 + 196, 26, 400, 1.3);
    // mini mapa de ruta
    const ny = { x: -w / 2 + 120, y: h / 2 - 110 }, vi = { x: w / 2 - 120, y: h / 2 - 110 };
    ctx.globalAlpha *= clamp(route * 4 + (route > 0 ? 0.2 : 0));
    if (route > 0) {
      for (const [P, l] of [[ny, 'NUEVA YORK'], [vi, 'VIENA']]) {
        ctx.fillStyle = N.INK; ctx.beginPath(); ctx.arc(P.x, P.y, 9, 0, 7); ctx.fill();
        text(ctx, l, P.x, P.y + 44, { f: font(700, 22, TYPE), c: N.INK, al: 'center', ls: 2 });
      }
      ctx.strokeStyle = '#d64545'; ctx.lineWidth = 4; ctx.setLineDash([12, 9]);
      const q = eo(route); ctx.beginPath();
      for (let i = 0; i <= 40 * q; i++) { const u = i / 40, x = lerp(vi.x, ny.x, u), y = vi.y - Math.sin(u * Math.PI) * 120; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
      ctx.stroke(); ctx.setLineDash([]);
      if (q > 0.98) { ctx.fillStyle = '#d64545'; ctx.beginPath(); ctx.moveTo(ny.x - 4, ny.y - 14); ctx.lineTo(ny.x + 22, ny.y - 30); ctx.lineTo(ny.x + 18, ny.y - 2); ctx.fill(); }
      text(ctx, '1938', 0, vi.y - 136, { f: font(700, 28, TYPE), c: '#d64545', al: 'center', a: clamp(route * 2 - 0.5) });
    }
    ctx.restore();
  }

  // 6 · El problema: la ficha es una báscula (acero vs avión); blindarlo entero falla; «¿?»
  const T6 = { forrar: rel(6, 'No puedes forrar'), donde: rel(6, 'Dónde lo pones') };
  const COVER = [ // todas las placas para «forrar el avión entero»
    ...PL_OBV, ...ENG.map(engPlate), { x: 0.19, y: 0.7, w: 0.3, h: 0.1 }, { x: -0.19, y: 0.7, w: 0.3, h: 0.1 }, { x: 0, y: -0.53, w: 0.13, h: 0.18 },
  ];
  DRAW[6] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const fold = ramp(lt, 0, 0.3);
    if (fold < 1) ficha(ctx, 540, z.y + 275 - (850 - 410) * 0 , 1, 1, 99, 1, fold);
    const sa = pr(lt, 0.2, 0.3) * (1 - ramp(lt, T6.forrar - 0.15, 0.35));
    const tilt = -0.2 * ramp(lt, 0.5, 0.9);
    const piv = { x: 540, y: z.y + 230 }, L = 330;
    const endL = { x: piv.x - L * Math.cos(tilt), y: piv.y - L * Math.sin(tilt) }, endR = { x: piv.x + L * Math.cos(tilt), y: piv.y + L * Math.sin(tilt) };
    const panR = { x: endR.x, y: endR.y + 260 };
    if (sa > 0) {
      ctx.save(); ctx.globalAlpha *= sa;
      // poste y viga
      ctx.fillStyle = N.LN; ctx.fillRect(piv.x - 8, piv.y, 16, 520); ctx.fillRect(piv.x - 110, piv.y + 520, 220, 14);
      ctx.strokeStyle = N.MU; ctx.lineWidth = 10; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(endL.x, endL.y); ctx.lineTo(endR.x, endR.y); ctx.stroke();
      ctx.fillStyle = N.TX; ctx.beginPath(); ctx.arc(piv.x, piv.y, 13, 0, 7); ctx.fill();
      for (const e of [endL, endR]) {
        ctx.strokeStyle = N.LN; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(e.x, e.y); ctx.lineTo(e.x - 120, e.y + 250); ctx.moveTo(e.x, e.y); ctx.lineTo(e.x + 120, e.y + 250); ctx.stroke();
        ctx.strokeStyle = N.MU; ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(e.x - 140, e.y + 260); ctx.lineTo(e.x + 140, e.y + 260); ctx.stroke();
      }
      // placa de acero
      const pl = { x: endL.x, y: endL.y + 222 };
      rrect(ctx, pl.x - 110, pl.y - 30, 220, 64, 8); ctx.fillStyle = '#59626d'; ctx.fill(); ctx.strokeStyle = '#9aa4ae'; ctx.lineWidth = 2; ctx.stroke();
      text(ctx, 'ACERO', pl.x, pl.y + 2, { f: font(800, 28, MONO), c: '#e6edf3', al: 'center', bl: 'middle', ls: 6 });
      // combustible
      const fuel = 1 - 0.55 * ramp(lt, 0.5, 0.9);
      text(ctx, 'combustible', 140, z.y + 820, { f: font(500, 24, MONO), c: N.MU });
      rrect(ctx, 330, z.y + 798, 600, 30, 6); ctx.fillStyle = N.PAN2; ctx.fill(); ctx.strokeStyle = N.LN; ctx.stroke();
      rrect(ctx, 330, z.y + 798, 600 * fuel, 30, 6); ctx.fillStyle = fuel < 0.6 ? N.KW : N.GRN; ctx.fill();
      text(ctx, '+ peso  →  − alcance, − maniobra', 540, z.y + 880, { f: font(400, 22, MONO), c: N.MU, al: 'center' });
      ctx.restore();
    }
    // el avión: del platillo al centro; placas que lo cubren todo, crujido, saltan
    const M = MAIN(z), mv = ramp(lt, T6.forrar - 0.1, 0.5);
    const P = L2({ x: panR.x, y: panR.y - 70, s: 110 }, M, mv);
    const cov = T6.forrar + 0.35, boom = T6.forrar + 1.15;
    const plates = COVER.map((c, i) => {
      const pin = pr(lt, cov + i * 0.045, 0.25), out = pr(lt, boom, 0.6);
      if (pin <= 0) return null;
      const ang = Math.atan2(c.y + 0.01, c.x + 0.001), fly = eo(out) * 1.4;
      return { ...c, x: c.x + Math.cos(ang) * fly + (1 - eo(pin)) * c.x * 0.6, y: c.y + Math.sin(ang) * fly - (1 - eo(pin)) * 0.5, a: clamp(pin * 3) * (1 - out), r: fly * (i % 2 ? 1 : -1) * 0.8 };
    });
    const shake = pr(lt, boom - 0.4, 0.4) * (1 - pr(lt, boom, 0.1));
    const fade = pr(lt, 0.2, 0.3);
    plane(ctx, P.x + Math.sin(lt * 90) * 8 * shake, P.y + Math.cos(lt * 77) * 5 * shake, P.s, { plates, a: fade });
    errBox(ctx, 120, z.y + 860, 840, 'ValueError', 'demasiado peso: no despega', pr(lt, boom - 0.05, 0.2) * (1 - pr(lt, T6.donde + 0.4, 0.3)));
    const qa = eo(pr(lt, T6.donde, 0.35));
    text(ctx, '¿?', 540, M.y - 230 + 30 * (1 - qa), { f: font(800, 150), c: N.OR, al: 'center', a: qa });
  };

  // 7 · Los datos: el «¿?» se deshace en puntos rojos que caen sobre el avión; recuento por zona
  const R7 = { rainA: 0.25, rainStep: 2.2 / HOLES.length, rainFrom: { x: 0, y: -0.85 } };
  function tallies(ctx, z, counts, a, hiMot = 0, lt = 0) {
    const y0 = z.y + 815, rows = [['fuselaje', counts.fus], ['alas', counts.ala], ['motores', counts.mot]];
    ctx.save(); ctx.globalAlpha *= a;
    rows.forEach(([l, n], i) => {
      const y = y0 + i * 50, hi = i === 2 ? hiMot : 0;
      text(ctx, l, 290, y + 10, { f: font(500, 26, MONO), c: hi ? '#fff' : N.MU, al: 'right' });
      for (let k = 0; k < n; k++) { ctx.fillStyle = N.RED; ctx.fillRect(312 + k * 15, y - 12, 11, 26); }
      if (i === 2) {
        if (hi) { ctx.save(); ctx.shadowColor = '#fff'; ctx.shadowBlur = 18 * hi; }
        text(ctx, '≈ 0', 320, y + 11, { f: font(800, 30, MONO), c: hi ? '#fff' : N.MU });
        if (hi) ctx.restore();
      }
    });
    text(ctx, 'patrón ilustrativo', 1000, y0 + 150, { f: font(400, 18, MONO), c: N.MU, al: 'right' });
    ctx.restore();
  }
  const countAt = n => { const c = { fus: 0, ala: 0, mot: 0 }; for (let k = 0; k < n; k++) c[HOLES[k].zone]++; return c; };
  const landed = lt => clamp(Math.floor((lt - R7.rainA - 0.32) / R7.rainStep) + 1, 0, HOLES.length);
  DRAW[7] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const M = MAIN(z);
    plane(ctx, M.x, M.y, M.s, { dots: 999, rain: lt, ...R7 });
    const qa = 1 - pr(lt, 0.05, 0.35);
    text(ctx, '¿?', 540, M.y - 230, { f: font(800, 150 * (1 + 0.3 * (1 - qa))), c: N.OR, al: 'center', a: qa });
    tallies(ctx, z, countAt(landed(lt)), pr(lt, 0.2, 0.3));
  };
  // 8 · Motores limpios: un «0» encima de cada motor
  DRAW[8] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const M = MAIN(z), za = pr(lt, 0.1, 0.3), lit = pr(lt, 0.45, 0.3);
    plane(ctx, M.x, M.y, M.s, { dots: 999, zeros: za, zeroLit: lit });
    tallies(ctx, z, countAt(HOLES.length), 1, lit, lt);
  };
  // 9 · Lo obvio: placas atornilladas sobre los agujeros; un tic verde… que tiembla
  const T9 = { ref: rel(9, 'refuerza donde') };
  const platesObv = (lt, a0 = 0.1) => PL_OBV.map((p, i) => { const q = pr(lt, a0 + i * 0.16, 0.3); return { ...p, a: clamp(q * 3), k: lerp(1.5, 1, eo(q)), y: p.y - 0.25 * (1 - eo(q)) }; });
  DRAW[9] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const M = MAIN(z);
    plane(ctx, M.x, M.y, M.s, { dots: 999, zeros: 1 - pr(lt, 0, 0.3), zeroLit: 1, plates: platesObv(lt, T9.ref - 0.35) });
    tallies(ctx, z, countAt(HOLES.length), 1 - pr(lt, 0, 0.35));
    const ca = pr(lt, T9.ref + 0.8, 0.25);
    check(ctx, 900, z.y + 110, ca, clamp((lt - T9.ref - 1.2) / 0.8) * 1.0, '¿seguro?', lt);
  };

  // 10 · Giro (cara): el avión blindado, en una esquina, se vuelve fantasma
  const T10 = { q: rel(10, 'y los aviones que no volvieron') };
  DRAW[10] = (ctx, lt, z, capa) => {
    if (capa !== 'over') return;
    const mv = ramp(lt, 0, 0.5), M = MAIN({ y: 410 });
    const P = L2(M, CARD_PL, mv);
    card(ctx, 580, 220, 440, 470, mv, 'Out[ ]: avion');
    const g = ramp(lt, T10.q, 0.8);
    const o = { dots: 999, plates: PL_OBV.map(p => ({ ...p, a: 1 })) };
    if (g > 0) plane(ctx, P.x, P.y, P.s, { ...o, ghost: true, a: 0.25 + 0.75 * g, stroke: '#c9d1d9' });
    plane(ctx, P.x, P.y, P.s, { ...o, a: 1 - g * 0.85 });
  };

  // 11 · Los que no volvieron: zoom a un motor limpio; aparecen fantasmas con el motor perforado
  const GHOSTS = [{ x: 205, dy: 180 }, { x: 875, dy: 180 }, { x: 205, dy: 700 }, { x: 875, dy: 700 }];
  const platesOn = PL_OBV.map(p => ({ ...p, a: 1 }));
  DRAW[11] = (ctx, lt, z, capa) => {
    const M = MAIN(z), e = ENG[3];
    const zin = ramp(lt, 0.0, 0.8), zout = ramp(lt, 1.3, 0.7);
    const sZ = 820, Z = { x: 540 - e.x * sZ, y: z.y + 520 - e.y * sZ, s: sZ };
    const S = { x: 540, y: z.y + 450, s: 230 };
    const fromCard = L2(CARD_PL, M, ramp(lt, 0, 0.45));
    const P = L2(L2(fromCard, Z, zin), S, zout);
    if ((capa === 'over') === (lt < 0.42)) plane(ctx, P.x, P.y, P.s, { dots: 999, plates: platesOn, zeros: 1, zeroLit: zin * (1 - zout) });
    if (capa === 'over') return;
    GHOSTS.forEach((g, i) => {
      const a = pr(lt, 1.5 + i * 0.18, 0.4);
      plane(ctx, g.x, z.y + g.dy, 120, { ghost: true, a, engHoles: 1, dots: 999, dotC: 'rgba(248,81,73,0.35)' });
    });
  };
  // 12 · Derribados: los fantasmas caen con estela de humo; el superviviente se queda solo
  const T12 = { fall: [0.15, 0.55, 0.95, 1.35] };
  DRAW[12] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const S = { x: 540, y: z.y + 450, s: 230 }, M = MAIN(z);
    const P = L2(S, M, ramp(lt, BN(12).d - 0.6, 0.6));
    GHOSTS.forEach((g, i) => {
      const f = Math.max(0, lt - T12.fall[i]), y = z.y + g.dy + 260 * f * f + 30 * f, rot = f * (i % 2 ? 0.9 : -0.9);
      const x = g.x + f * (i % 2 ? 60 : -60);
      // humo
      ctx.save();
      for (let k = 0; k < 18; k++) {
        const ff = f - k * 0.05; if (ff <= 0) break;
        const sy = z.y + g.dy + 260 * ff * ff + 30 * ff, sx = g.x + ff * (i % 2 ? 60 : -60);
        ctx.fillStyle = `rgba(139,148,158,${0.16 * (1 - k / 18)})`; ctx.beginPath(); ctx.arc(sx + Math.sin(k * 2.1) * 6, sy - 30, 14 + k * 2.2, 0, 7); ctx.fill();
      }
      ctx.restore();
      if (y < 1600) plane(ctx, x, y, 120, { ghost: true, a: 1 - pr(f, 0.6, 0.6), engHoles: 1, dots: 999, dotC: 'rgba(248,81,73,0.35)', rot });
    });
    plane(ctx, P.x, P.y, P.s, { dots: 999, plates: platesOn });
    errBox(ctx, 120, z.y + 840, 840, 'KeyError', "'no_volvieron': no hay datos", pr(lt, 1.6, 0.25));
  };
  // 13 · La inversión: las placas pasan a los motores; los motores se iluminan; el tic deja de temblar
  const T13 = { tumba: rel(13, 'un balazo te tumba') };
  const platesMove = lt => PL_OBV.map((p, i) => {
    const q = ramp(lt, 0.15 + i * 0.1, 0.6), g = PL_GOOD[i];
    if (!g) return { ...p, a: 1 - q, y: p.y - q * 0.3 };
    return { x: lerp(p.x, g.x, q), y: lerp(p.y, g.y, q) - Math.sin(q * Math.PI) * 0.25, w: lerp(p.w, g.w, q), h: lerp(p.h, g.h, q), a: 1, r: Math.sin(q * Math.PI) * 0.6 };
  });
  DRAW[13] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const M = MAIN(z), gl = pr(lt, T13.tumba - 0.3, 0.5);
    plane(ctx, M.x, M.y, M.s, { dots: 999, plates: platesMove(lt), glow: gl, zeros: 1 - pr(lt, 0.0, 0.3), zeroLit: 1 });
    check(ctx, 900, z.y + 110, pr(lt, 1.1, 0.3), 0, 'ahora sí', lt);
  };

  // 14 · El informe (híbrido): el avión se aplana y es el dibujo de la portada del memorándum
  function memo(ctx, cx, cy, k, a, lt) {
    if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a; ctx.translate(cx, cy); ctx.scale(k, k);
    const w = 600, h = 520;
    ctx.shadowColor = 'rgba(0,0,0,0.55)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 12; ctx.fillStyle = N.PAPER; ctx.fillRect(-w / 2, -h / 2, w, h); ctx.shadowColor = 'transparent';
    text(ctx, 'STATISTICAL RESEARCH GROUP · COLUMBIA UNIVERSITY', 0, -h / 2 + 42, { f: font(400, 15, TYPE), c: N.INK, al: 'center', ls: 1 });
    ctx.fillStyle = N.INK; ctx.fillRect(-w / 2 + 40, -h / 2 + 58, w - 80, 2);
    const ls = wrap(ctx, 'A Method of Estimating Plane Vulnerability Based on Damage of Survivors', font(700, 27, TYPE), w - 90);
    ls.forEach((l, i) => text(ctx, l, 0, -h / 2 + 104 + i * 36, { f: font(700, 27, TYPE), c: N.INK, al: 'center' }));
    text(ctx, 'Abraham Wald', 0, h / 2 - 62, { f: font(400, 24, TYPE), c: N.INK, al: 'center' });
    text(ctx, '1943', 0, h / 2 - 28, { f: font(700, 24, TYPE), c: N.INK, al: 'center' });
    ctx.restore();
  }
  const MEMO = z => ({ x: 540, y: z.y + 275, k: 1 });
  const MEMO_PL = z => ({ x: 540, y: z.y + 330, s: 105 });
  DRAW[14] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const m = MEMO(z), ma = ramp(lt, 0.2, 0.45), fl = ramp(lt, 0.05, 0.7);
    memo(ctx, m.x, m.y + 30 * (1 - ma), lerp(1.06, 1, ma), ma, lt);
    const P = L2(MAIN({ y: 410 }), MEMO_PL(z), fl);
    const ink = pr(lt, 0.35, 0.4);
    const good = PL_GOOD.filter(Boolean).map(p => ({ ...p, a: 1 - ink }));
    plane(ctx, P.x, P.y, P.s, { glow: 1 - ink * 0.4, plates: good, dots: 999, a: 1 - ink * 0.999, flat: true });
    plane(ctx, P.x, P.y, P.s, { fill: N.PAPER, stroke: N.INK, lw: 1.5, flat: true, glow: 0.65 * ink, a: ink });
  };

  // 15 · El método (híbrido): el memo se abre: volvieron | no volvieron → una estimación con zonas
  const T15 = { merge: rel(15, 'usando solo los que sobreviven') };
  function page(ctx, x, y, w, h, a, title) {
    ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = N.PAPER; ctx.fillRect(x, y, w, h);
    text(ctx, title, x + w / 2, y + 42, { f: font(700, 22, TYPE), c: N.INK, al: 'center', ls: 2 }); ctx.restore();
  }
  DRAW[15] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const op = ramp(lt, 0, 0.5), mg = ramp(lt, T15.merge - 0.2, 0.7);
    const top = z.y + 15, h = 500;
    if (op < 1) memo(ctx, 540, z.y + 275, 1, 1 - op, 99);
    if (op < 1) plane(ctx, MEMO_PL(z).x, MEMO_PL(z).y, 105, { fill: N.PAPER, stroke: N.INK, lw: 1.5, flat: true, glow: 0.65, a: 1 - op });
    const sep = 1 - mg, la = op * sep;
    const lx = lerp(lerp(240, 60, op), 240, mg), rx = lerp(lerp(240, 560, op), 240, mg);
    page(ctx, lx, top, 460, h, la, 'VOLVIERON');
    page(ctx, rx, top, 460, h, la, 'NO VOLVIERON');
    if (la > 0) {
      plane(ctx, lx + 230, top + 270, 150, { fill: N.PAPER, stroke: N.INK, lw: 1.5, flat: true, dots: 999, a: la });
      [[-95, -75], [95, -75], [0, 105]].forEach(([dx, dy], i) => plane(ctx, rx + 230 + dx, top + 270 + dy, 82, { ghost: true, stroke: N.INK, engHoles: 1, a: la * pr(lt, 0.3 + i * 0.15, 0.3) }));
    }
    // flecha y estimación
    const ea = mg;
    if (ea > 0) {
      ctx.save(); ctx.globalAlpha *= ea;
      rrect(ctx, 150, top, 780, h, 4); ctx.fillStyle = '#161b22'; ctx.fill(); ctx.strokeStyle = N.LN; ctx.lineWidth = 2; ctx.stroke();
      text(ctx, '→ estimación', 180, top + 50, { f: font(700, 26, MONO), c: N.OR });
      ctx.restore();
      plane(ctx, 540, top + 275, 170, { heat: 1, glow: 1, a: ea, flat: true });
      ctx.save(); ctx.globalAlpha *= ea;
      const gx = 330, gy = top + h - 50, gwid = 420, gr = ctx.createLinearGradient(gx, 0, gx + gwid, 0);
      gr.addColorStop(0, '#aeb7c2'); gr.addColorStop(1, N.OR);
      ctx.fillStyle = gr; ctx.fillRect(gx, gy, gwid, 14);
      text(ctx, 'menos', gx - 14, gy + 13, { f: font(500, 20, MONO), c: N.MU, al: 'right' });
      text(ctx, 'más vulnerable', gx + gwid + 14, gy + 13, { f: font(500, 20, MONO), c: N.OR });
      ctx.restore();
    }
  };

  // 16 · El nombre (cara): rótulo «SESGO DE SUPERVIVENCIA» con el avión como icono
  function rotulo(ctx, a, y) {
    card(ctx, 70, y, 940, 220, a);
    plane(ctx, 170, y + 110, 70, { glow: 1, a, flat: true, plates: PL_GOOD.filter(Boolean).map(p => ({ ...p, a: 1 })) });
    text(ctx, 'SESGO DE', 270, y + 98, { f: font(800, 54), c: N.TX, a });
    text(ctx, 'SUPERVIVENCIA', 270, y + 160, { f: font(900, 62), c: N.OR, a });
  }
  DRAW[16] = (ctx, lt, z, capa) => {
    if (capa !== 'over') return;
    const a = eo(pr(lt, 0.15, 0.4));
    rotulo(ctx, a, 220 + 40 * (1 - a));
  };

  // 17 · En tu trabajo (híbrido): tabla de clientes; las bajas son filas fantasma en naranja
  const T17 = { rows: rel(17, 'cuando analizas'), ghosts: rel(17, 'que siguen') };
  const CLI = [['C-1042', 'Pro', '26', 'activo'], ['C-1187', 'Básico', '3', 'baja'], ['C-1203', 'Pro', '14', 'activo'], ['C-1311', 'Básico', '2', 'baja'], ['C-1376', 'Pro', '19', 'activo'], ['C-1420', 'Básico', '1', 'baja']];
  function blink(lt, a0) { return lt < a0 ? 0 : 0.55 + 0.45 * Math.cos((lt - a0) * 7); }
  function table(ctx, x, y, w, head, rows, cols, ghost, lt, a0, g0, a = 1) {
    ctx.save(); ctx.globalAlpha *= a;
    ctx.fillStyle = '#1f2630'; ctx.fillRect(x, y, w, 52);
    head.forEach((h, j) => text(ctx, h, x + cols[j], y + 35, { f: font(700, 24, MONO), c: N.MU, al: j === head.length - 1 ? 'right' : 'left' }));
    rows.forEach((r, i) => {
      const yy = y + 52 + i * 64, ra = pr(lt, a0 + i * 0.1, 0.25), gh = ghost(r);
      if (ra <= 0) return;
      ctx.save(); ctx.globalAlpha *= ra;
      if (gh) {
        const ga = pr(lt, g0, 0.3);
        ctx.globalAlpha *= 1 - 0.65 * ga;
        if (ga > 0) {
          ctx.save(); ctx.globalAlpha = a * ra * ga * blink(lt, g0);
          ctx.setLineDash([10, 7]); ctx.strokeStyle = N.OR; ctx.lineWidth = 3; rrect(ctx, x + 4, yy + 6, w - 8, 54, 8); ctx.stroke();
          ctx.fillStyle = 'rgba(255,145,30,0.10)'; ctx.fill(); ctx.restore();
        }
      }
      r.forEach((c, j) => text(ctx, c, x + cols[j], yy + 42, { f: font(500, 26, MONO), c: gh ? N.MU : (j === r.length - 1 ? N.GRN : N.TX), al: j === r.length - 1 ? 'right' : 'left' }));
      if (!gh) { ctx.fillStyle = N.LN; ctx.fillRect(x, yy + 63, w, 1); }
      ctx.restore();
    });
    ctx.restore();
  }
  DRAW[17] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    table(ctx, 90, z.y + 30, 900, ['cliente', 'plan', 'meses', 'estado'], CLI, [24, 260, 470, 876], r => r[3] === 'baja', lt, Math.min(T17.rows, 0.4), T17.ghosts);
    text(ctx, 'tu análisis solo ve las filas activas', 540, z.y + 500, { f: font(400, 22, MONO), c: N.MU, al: 'center', a: pr(lt, T17.ghosts + 0.3, 0.3) });
  };
  // 18 · Más ejemplos (híbrido): pared de startups (las cerradas, fantasma) y modelos descartados
  const T18 = { mod: rel(18, 'solo los modelos') };
  const STARTUPS = ['Lumo', 'Ferra', 'Datix', 'Ondo', 'Kubo', 'Veta', 'Mirat', 'Tesk', 'Zuna', 'Pliq', 'Rovo', 'Albo'];
  const VIVAS = new Set([2, 7, 9]);
  const MODELS = [['regresion_v1', 'descartado'], ['random_forest_v2', 'descartado'], ['xgboost_v3', 'producción'], ['red_neuronal_v1', 'descartado'], ['xgboost_v4', 'producción']];
  DRAW[18] = (ctx, lt, z, capa) => {
    if (capa !== 'under') return;
    const out = ramp(lt, 0, 0.4);
    if (out < 1) table(ctx, 90 - 1000 * out, z.y + 30, 900, ['cliente', 'plan', 'meses', 'estado'], CLI, [24, 260, 470, 876], r => r[3] === 'baja', 99, 0, 0);
    const mo = ramp(lt, T18.mod - 0.15, 0.4);
    // startups
    const sx = 1000 * (1 - ramp(lt, 0.05, 0.45)) - 1000 * mo;
    STARTUPS.forEach((nm, i) => {
      const c = i % 4, r = Math.floor(i / 4), x = 90 + c * 228 + sx, y = z.y + 30 + r * 150, viva = VIVAS.has(i);
      const g = viva ? 0 : pr(lt, 0.7, 0.3);
      ctx.save(); ctx.globalAlpha *= pr(lt, 0.1 + i * 0.03, 0.2) * (viva ? 1 : 1 - 0.65 * g);
      rrect(ctx, x, y, 210, 132, 12); ctx.fillStyle = viva ? '#1f2630' : N.PAN; ctx.fill();
      ctx.strokeStyle = viva ? N.MU : N.LN; ctx.lineWidth = 2; ctx.stroke();
      ctx.fillStyle = viva ? N.TX : N.MU; ctx.beginPath(); ctx.arc(x + 105, y + 50, 24, 0, 7); ctx.fill();
      text(ctx, nm[0], x + 105, y + 51, { f: font(800, 26), c: N.BG, al: 'center', bl: 'middle' });
      text(ctx, nm, x + 105, y + 108, { f: font(600, 24, MONO), c: viva ? N.TX : N.MU, al: 'center' });
      ctx.restore();
      if (!viva && g > 0) {
        ctx.save(); ctx.globalAlpha *= g * blink(lt, 0.7); ctx.setLineDash([10, 7]); ctx.strokeStyle = N.OR; ctx.lineWidth = 3;
        rrect(ctx, x, y, 210, 132, 12); ctx.stroke(); ctx.restore();
      }
    });
    text(ctx, 'las que cerraron no salen en la foto', 540 + sx, z.y + 500, { f: font(400, 22, MONO), c: N.MU, al: 'center', a: pr(lt, 0.9, 0.3) });
    // modelos
    if (mo > 0) {
      const mx = 1000 * (1 - mo), ml = lt - T18.mod;
      MODELS.forEach(([nm, st], i) => {
        const y = z.y + 40 + i * 78, prod = st === 'producción', g = prod ? 0 : pr(ml, 0.5, 0.3);
        ctx.save(); ctx.globalAlpha *= pr(ml, i * 0.08, 0.2);
        ctx.globalAlpha *= 1 - 0.6 * g;
        text(ctx, nm, 110 + mx, y + 40, { f: font(500, 28, MONO), c: prod ? N.TX : N.MU });
        text(ctx, prod ? '✓ ' + st : st, 970 + mx, y + 40, { f: font(600, 24, MONO), c: prod ? N.GRN : N.MU, al: 'right' });
        if (!prod && g > 0) { ctx.fillStyle = N.MU; ctx.fillRect(105 + mx, y + 31, tw(ctx, nm, font(500, 28, MONO)) * g + 10, 3); }
        ctx.restore();
        if (!prod && g > 0) {
          ctx.save(); ctx.globalAlpha *= g * blink(ml, 0.5); ctx.setLineDash([10, 7]); ctx.strokeStyle = N.OR; ctx.lineWidth = 3;
          rrect(ctx, 90 + mx, y + 2, 900, 62, 8); ctx.stroke(); ctx.restore();
        }
        if (prod) { ctx.fillStyle = N.LN; ctx.fillRect(90 + mx, y + 66, 900, 1); }
      });
    }
  };

  // 19 · Criterio (cara): una tabla con huecos discontinuos y «¿QUIÉN FALTA?»
  const T19 = { q: rel(19, 'pregúntate quién falta') };
  DRAW[19] = (ctx, lt, z, capa) => {
    if (capa !== 'over') return;
    const a = eo(pr(lt, 0.1, 0.4)), x = 580, y = 250 + 30 * (1 - a), w = 420;
    card(ctx, x - 20, y - 30, w + 40, 500, a, 'Out[ ]: tus_datos');
    const rows = [['0.82', '37'], null, ['0.65', '12'], null, ['0.77', '25']];
    const CX = [20, 170, w - 20];
    ctx.save(); ctx.globalAlpha *= a;
    ctx.fillStyle = '#1f2630'; ctx.fillRect(x, y + 20, w, 48);
    ['id', 'x', 'n'].forEach((h, j) => text(ctx, h, x + CX[j], y + 53, { f: font(700, 24, MONO), c: N.MU, al: j === 2 ? 'right' : 'left' }));
    rows.forEach((r, i) => {
      const yy = y + 72 + i * 62;
      if (r) {
        [String(i + 1), ...r].forEach((c, j) => text(ctx, c, x + CX[j], yy + 40, { f: font(500, 26, MONO), c: N.TX, al: j === 2 ? 'right' : 'left' }));
        ctx.fillStyle = N.LN; ctx.fillRect(x, yy + 60, w, 1);
      } else {
        ctx.save(); ctx.globalAlpha *= pr(lt, 0.5, 0.3) * blink(lt, 0.8); ctx.setLineDash([10, 7]); ctx.strokeStyle = N.OR; ctx.lineWidth = 3;
        rrect(ctx, x + 4, yy + 6, w - 8, 52, 8); ctx.stroke(); ctx.restore();
        text(ctx, '?', x + w / 2, yy + 42, { f: font(800, 30, MONO), c: N.OR, al: 'center', a: pr(lt, 0.5, 0.3) });
      }
    });
    const qa = eo(pr(lt, T19.q - 0.1, 0.35));
    text(ctx, '¿QUIÉN FALTA?', x + w / 2, y + 430 + 20 * (1 - qa), { f: font(900, 46), c: N.OR, al: 'center', a: qa, ls: 1 });
    ctx.restore();
  };
  // 20 · CTA (cara): el avión, ya blindado en los motores, cruza; @r2d2.coder y fuentes
  DRAW[20] = (ctx, lt, z, capa) => {
    if (capa !== 'over') return;
    const x = lerp(-220, 1300, pr(lt, 0, 2.5));
    plane(ctx, x, 430, 170, { rot: Math.PI / 2, glow: 1, plates: PL_GOOD.filter(Boolean).map(p => ({ ...p, a: 1 })), flat: true });
    const a = eo(pr(lt, 0.3, 0.4));
    ctx.save(); ctx.globalAlpha *= a;
    rrect(ctx, 290, 1215, 500, 96, 48); ctx.fillStyle = 'rgba(13,17,23,0.88)'; ctx.fill(); ctx.strokeStyle = N.OR; ctx.lineWidth = 3; ctx.stroke();
    text(ctx, '@r2d2.coder', 540, 1264, { f: font(800, 50, MONO), c: N.TX, al: 'center', bl: 'middle' });
    rrect(ctx, 60, 1625, 960, 104, 12); ctx.fillStyle = 'rgba(13,17,23,0.82)'; ctx.fill();
    text(ctx, 'Fuentes: A. Wald (1943), Statistical Research Group,', 84, 1667, { f: font(400, 20, MONO), c: N.MU });
    text(ctx, 'Columbia · Mangel y Samaniego, JASA (1984)', 84, 1701, { f: font(400, 20, MONO), c: N.MU });
    ctx.restore();
  };

  // ================================================================= composición
  const tgt = i => {
    const b = beats[i];
    if (b.plano === 'anim') return { lay: 0, cur: 0 };
    if (b.plano === 'hibrido') return { lay: 1, cur: 640 };
    return { lay: i > 0 ? tgt(i - 1).lay : 0, cur: H };
  };
  const HANDOFF = new Set([2, 11]);   // beats que recogen el objeto de la tarjeta anterior (no se funde)
  function beatAt(t) { const i = beats.findIndex(b => t >= b.t0 && t < b.t1); return i < 0 ? beats.length - 1 : i; }
  function world(ctx, t) {
    const i = beatAt(t), b = beats[i], lt = t - b.t0;
    const A = i > 0 ? tgt(i - 1) : tgt(0), Bt = tgt(i), p = eio(pr(lt, 0, 0.42));
    const lay = lerp(A.lay, Bt.lay, p), cur = lerp(A.cur, Bt.cur, p);
    const z = { x: 60, y: lerp(410, 850, lay), w: 960 }; z.h = 1390 - z.y;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.fillStyle = N.BG; ctx.fillRect(0, 0, W, H);
    if (cur < H - 1) {
      chrome(ctx);
      const cell = drawCells(ctx, t, lay);
      if (b.plano === 'cara') {
        let k = i - 1; while (k >= 0 && beats[k].plano === 'cara') k--;
        ctx.save(); ctx.beginPath(); ctx.rect(0, z.y - 24, W, 1395 - z.y + 24); ctx.clip();
        if (k >= 0) DRAW[beats[k].n]?.(ctx, beats[k].d - 0.001, z, 'under', beats[k]);
        ctx.restore();
      } else {
        ctx.save(); ctx.beginPath(); ctx.rect(0, z.y - 24, W, 1395 - z.y + 24); ctx.clip();
        DRAW[b.n]?.(ctx, lt, z, 'under', b);
        ctx.restore();
        if (cell) text(ctx, `Out[${cell.n}]:`, 30, z.y - 4, { f: font(500, 22, MONO), c: N.KW, a: pr(t - cell.t, 0.5, 0.2) });
      }
    }
    if (cur > 1) {
      const q = clamp((cur - 640) / 1280);
      drawCara(ctx, 0, 0, W, cur, { zoom: lerp(1.15, 1, q), dy: lerp(120, 0, q) });
      if (cur < H - 1) { ctx.fillStyle = N.LN; ctx.fillRect(0, cur - 2, W, 3); }
    }
    // la tarjeta del beat «cara» anterior se va (salvo cuando el siguiente recoge su objeto)
    if (i > 0 && beats[i - 1].plano === 'cara' && !HANDOFF.has(b.n) && lt < 0.35) {
      ctx.save(); ctx.globalAlpha = 1 - lt / 0.35; DRAW[beats[i - 1].n]?.(ctx, beats[i - 1].d, z, 'over', beats[i - 1]); ctx.restore();
    }
    DRAW[b.n]?.(ctx, lt, z, 'over', b);
  }

  // ================================================================= sonido
  const at = (n, s = 0) => BN(n).t0 + s;
  const events = [
    { t: at(1, tRev), type: 'thud' },
    { t: at(2, 0.3), type: 'ding' },
    { t: at(3, T3.a), type: 'ticks', dur: 1.85, rate: 32 },
    { t: at(4, T4.pin), type: 'thud' },
    { t: at(6, T6.forrar + 1.15), type: 'thud' },
    { t: at(7, R7.rainA + 0.3), type: 'ticks', dur: 2.2, rate: 30 },
    { t: at(8, 0.45), type: 'ding' },
    { t: at(9, T9.ref + 0.8), type: 'ding' },
    { t: at(10), type: 'swell', dur: 1.2 },
    ...T12.fall.map(f => ({ t: at(12, f), type: 'fall', dur: 1.0 })),
    { t: at(13, T13.tumba - 0.3), type: 'ding' },
    { t: at(14, 0.3), type: 'thud' },
    { t: at(16, 0.15), type: 'thud' },
    { t: at(19, T19.q - 0.1), type: 'ding' },
  ];

  window.STORY = {
    title: B.titulo, hud: false, grain: 0.08, vignette: false,
    scenes: beats.map(b => ({ dur: b.d, draw: () => { } })),
    world, voz: T, events,
  };
  setup();
  renderFrame(0);
})();
