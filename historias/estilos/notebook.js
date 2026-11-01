// Estilo A · Notebook: piezas reutilizables (sacadas de aviones-wald). Cárgalo después de lib.js:
//   <script src="../estilos/notebook.js"></script>
// Uso: const NB = Notebook('mi_historia.ipynb');  NB.celdas.add(t, ['codigo', '...']);  NB.chrome(ctx); NB.celdas.draw(ctx, t, lay)
const NBC = {
  BG: '#0d1117', PAN: '#161b22', PAN2: '#1c2128', LN: '#30363d', TX: '#e6edf3', MU: '#7d8590', KW: '#ff7b72',
  STR: '#a5d6ff', FN: '#d2a8ff', NUM: '#79c0ff', GRN: '#3fb950', OR: '#ff911e', RED: '#f85149',
  PAPER: '#ece6d6', INK: '#2b2620',
};
// Acentos con significado (no decoración): rojo = datos/errores, naranja = la idea clave, verde = «ok» de Jupyter.

function Notebook(archivo) {
  const N = NBC, CF = font(500, 27, MONO);
  /** Resaltado mínimo de Python. */
  function tokens(line) {
    const out = [], re = /(#.*$)|("[^"]*"|'[^']*')|(\b\d[\d_.]*\b)|(\b(?:True|False|None|not|in|and|or|len|import|from|as|for|if|return|def)\b)|([A-Za-z_][\w]*)(?=\()|(==|=|~|\+|-|\*|\/)/g;
    let last = 0, m;
    while ((m = re.exec(line))) {
      if (m.index > last) out.push([line.slice(last, m.index), N.TX]);
      out.push([m[0], m[1] ? N.MU : m[2] ? N.STR : m[3] ? N.NUM : m[4] ? N.KW : m[5] ? N.FN : N.KW]);
      last = m.index + m[0].length;
    }
    if (last < line.length) out.push([line.slice(last), N.TX]);
    return out;
  }
  /** Celda de código que se escribe sola; [*] mientras «ejecuta», borde verde al acabar. lt = segundos desde que aparece. */
  function cellBox(ctx, y, n, lines, lt, a = 1) {
    if (a <= 0) return;
    const h = 34 + lines.length * 42, run = lt < 0.75;
    ctx.save(); ctx.globalAlpha *= a;
    text(ctx, run ? '[*]:' : `[${n}]:`, 30, y + 50, { f: font(500, 22, MONO), c: run ? N.GRN : N.MU });
    rrect(ctx, 100, y, 940, h, 10); ctx.fillStyle = N.PAN; ctx.fill();
    ctx.strokeStyle = lt < 1.3 ? N.GRN : N.LN; ctx.lineWidth = 2; ctx.stroke();
    const total = lines.reduce((s, l) => s + l.length, 0); let left = Math.floor(total * pr(lt, 0.05, 0.42)), cur = null;
    lines.forEach((l, i) => {
      let x = 126; const yy = y + 50 + i * 42;
      for (const [s, c] of tokens(l)) {
        if (left <= 0) break;
        const ss = s.slice(0, left); left -= ss.length;
        text(ctx, ss, x, yy, { f: CF, c }); x += tw(ctx, ss, CF); cur = [x, yy];
      }
    });
    if (lt < 0.55 && cur) { ctx.fillStyle = N.TX; ctx.fillRect(cur[0] + 2, cur[1] - 24, 13, 30); }
    ctx.restore();
  }
  /** Tarjeta flotante (para poner un objeto sobre su cara sin taparla). */
  function card(ctx, x, y, w, h, a = 1, title) {
    if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a;
    ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 10;
    rrect(ctx, x, y, w, h, 14); ctx.fillStyle = 'rgba(13,17,23,0.94)'; ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.strokeStyle = N.LN; ctx.lineWidth = 2; ctx.stroke();
    if (title) text(ctx, title, x + 22, y + 38, { f: font(500, 20, MONO), c: N.MU });
    ctx.restore();
  }
  /** Caja de error estilo traceback. */
  function errBox(ctx, x, y, w, kind, msg, a = 1) {
    if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a;
    rrect(ctx, x, y, w, 104, 10); ctx.fillStyle = 'rgba(248,81,73,0.13)'; ctx.fill(); ctx.strokeStyle = N.RED; ctx.lineWidth = 2; ctx.stroke();
    text(ctx, kind, x + 24, y + 40, { f: font(700, 24, MONO), c: N.RED });
    text(ctx, msg, x + 24, y + 80, { f: font(500, 25, MONO), c: N.TX });
    ctx.restore();
  }
  /** Tic verde; jit > 0 lo hace temblar (un «ok» del que no te fías). */
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
  /** Barra de ventana con la pestaña del notebook. */
  function chrome(ctx) {
    ctx.fillStyle = N.PAN; ctx.fillRect(0, 100, W, 84);
    ['#ff5f57', '#febc2e', '#28c840'].forEach((c, i) => { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(54 + i * 32, 142, 9, 0, 7); ctx.fill(); });
    rrect(ctx, 170, 112, 400, 72, [10, 10, 0, 0]); ctx.fillStyle = N.BG; ctx.fill();
    text(ctx, archivo, 196, 157, { f: font(500, 24, MONO), c: N.TX });
    text(ctx, 'Historias de datos', 1030, 155, { f: font(400, 20, MONO), c: N.MU, al: 'right' });
  }
  /** Pila de celdas: cada una aparece en su segundo y empuja a la anterior hacia arriba (continuidad de notebook).
   *  lay 0 = notebook arriba (anim), 1 = bajo la franja de su cara (hibrido). */
  const celdas = {
    lista: [],
    add(t, lines) { this.lista.push({ t, lines }); this.lista.sort((a, b) => a.t - b.t); this.lista.forEach((c, i) => c.n = i + 1); },
    draw(ctx, t, lay = 0) {
      let k = -1; this.lista.forEach((c, i) => { if (c.t <= t + 1e-6) k = i; });
      if (k < 0) return null;
      const cur = this.lista[k], prev = this.lista[k - 1], lt = t - cur.t, p = eio(pr(lt, 0, 0.35)), y0 = lerp(222, 678, lay);
      if (prev && p < 1) cellBox(ctx, y0 - 190 * p, prev.n, prev.lines, 9, 1 - p);
      cellBox(ctx, y0 + 190 * (1 - p), cur.n, cur.lines, lt, p);
      return cur;
    },
  };
  /** Etiqueta «Out[n]:» encima del escenario. */
  function out(ctx, cell, t, y) { if (cell) text(ctx, `Out[${cell.n}]:`, 30, y, { f: font(500, 22, MONO), c: N.KW, a: pr(t - cell.t, 0.5, 0.2) }); }
  return { N, tokens, cellBox, card, errBox, check, chrome, celdas, out };
}
