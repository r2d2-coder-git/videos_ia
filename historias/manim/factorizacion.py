"""Plano de prueba en Manim: cómo la factorización de matrices rellena las valoraciones que faltan.
Render: ../.venv-manim/bin/manim -qh --fps 30 -r 1080,1920 factorizacion.py Factorizacion"""
from manim import *
import random

config.pixel_width, config.pixel_height = 1080, 1920
config.frame_width, config.frame_height = 7.2, 12.8
config.background_color = "#0b0b0e"

RED = ManimColor("#e5383b")
INK = ManimColor("#f2f1ee")
MUT = ManimColor("#8b9099")
BLU = ManimColor("#5b8def")
SANS = "SF Pro Display"
MONO = "SF Mono"

random.seed(7)
NU, NP, K = 6, 7, 2
# gustos ocultos de usuarios (acción, drama) y perfil de películas
U = [[round(random.uniform(0, 1), 1) for _ in range(K)] for _ in range(NU)]
V = [[round(random.uniform(0, 1), 1) for _ in range(K)] for _ in range(NP)]
pred = [[1 + 4 * min(1, 1.6 * sum(U[i][k] * V[j][k] for k in range(K))) for j in range(NP)] for i in range(NU)]
known = {(i, j) for i in range(NU) for j in range(NP) if random.random() < 0.3}
known.add((0, 0))


def T(s, size=28, color=INK, font=SANS, weight=NORMAL):
    return Text(s, font=font, color=color, weight=weight).scale(size / 48)


def cell(val, filled, side=0.62):
    sq = Square(side, stroke_color=MUT, stroke_width=1.5, stroke_opacity=0.5)
    if filled:
        sq.set_fill(RED, opacity=0.25 + 0.14 * val).set_stroke(RED, 2, 0.9)
        lab = T(f"{round(val)}", 22, INK, MONO)
    else:
        lab = T("?", 22, MUT, MONO)
    return VGroup(sq, lab)


def grid(rows, cols, maker, side=0.62):
    g = VGroup(*[VGroup(*[maker(i, j) for j in range(cols)]).arrange(RIGHT, buff=0.06) for i in range(rows)]).arrange(DOWN, buff=0.06)
    return g


class Factorizacion(Scene):
    def construct(self):
        kicker = T("HISTORIAS DE DATOS · EL NETFLIX PRIZE", 18, MUT, MONO).to_edge(UP, buff=0.7)
        self.add(kicker)

        # 1 · la matriz con huecos
        R = grid(NU, NP, lambda i, j: cell(pred[i][j], (i, j) in known))
        R.move_to(UP * 1.2)
        rl = T("R · valoraciones", 30, INK, weight=BOLD).next_to(R, UP, buff=0.5)
        sub = T("filas = usuarios · columnas = películas", 20, MUT, MONO).next_to(R, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for row in R for c in row], lag_ratio=0.012), Write(rl), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.2))
        q = T("¿Qué nota pondría cada usuario en los «?»", 26, RED, weight=BOLD).next_to(sub, DOWN, buff=0.5)
        self.play(Write(q), run_time=1.0)
        self.wait(0.6)

        # 2 · R ≈ U · Vᵀ
        self.play(FadeOut(sub), FadeOut(q), FadeOut(rl), R.animate.scale(0.82).move_to(RIGHT * 0.95 + DOWN * 0.6), run_time=1.0)
        Ug = grid(NU, K, lambda i, k: VGroup(Square(0.5, stroke_width=0).set_fill(BLU, 0.15 + 0.75 * U[i][k]), T(f"{U[i][k]:.1f}", 16, INK, MONO)), 0.5)
        Ug.scale(0.82 / 0.82).next_to(R, LEFT, buff=0.45)
        Vg = VGroup(*[VGroup(*[VGroup(Square(0.5, stroke_width=0).set_fill(BLU, 0.15 + 0.75 * V[j][k]), T(f"{V[j][k]:.1f}", 16, INK, MONO)) for j in range(NP)]).arrange(RIGHT, buff=0.06) for k in range(K)]).arrange(DOWN, buff=0.06)
        Vg.match_width(R).next_to(R, UP, buff=0.45)
        Ul = T("U · gustos del usuario", 20, BLU, MONO).next_to(Ug, DOWN, buff=0.3).align_to(Ug, LEFT)
        Vl = T("Vᵀ · perfil de la película", 20, BLU, MONO).next_to(Vg, UP, buff=0.3).align_to(Vg, LEFT)
        ax = VGroup(T("acción", 16, MUT, MONO), T("drama", 16, MUT, MONO)).arrange(RIGHT, buff=0.25).next_to(Ug, UP, buff=0.15)
        self.play(LaggedStart(FadeIn(Ug, shift=RIGHT * 0.4), FadeIn(Vg, shift=DOWN * 0.4), lag_ratio=0.3), run_time=1.2)
        self.play(FadeIn(Ul), FadeIn(Vl), FadeIn(ax))
        eq = VGroup(T("R", 64, INK, weight=BOLD), T("≈", 64, INK), T("U", 64, BLU, weight=BOLD), T("·", 64, INK), T("Vᵀ", 64, BLU, weight=BOLD)).arrange(RIGHT, buff=0.3)
        eq.to_edge(DOWN, buff=2.6)
        self.play(Write(eq), run_time=1.0)
        self.wait(0.4)

        # 3 · una predicción: fila de U · columna de Vᵀ
        i, j = next((a, b) for a in range(NU) for b in range(NP) if (a, b) not in known and a >= 1)
        row = SurroundingRectangle(Ug[i], color=INK, buff=0.04)
        col = SurroundingRectangle(VGroup(*[Vg[k][j] for k in range(K)]), color=INK, buff=0.04)
        tgt = SurroundingRectangle(R[i][j], color=RED, buff=0.04, stroke_width=5)
        calc = T(f"{U[i][0]:.1f}×{V[j][0]:.1f} + {U[i][1]:.1f}×{V[j][1]:.1f}  →  {pred[i][j]:.1f} ★", 26, INK, MONO)
        calc.next_to(eq, DOWN, buff=0.6)
        self.play(Create(row), Create(col), run_time=0.7)
        self.play(TransformFromCopy(VGroup(row, col), tgt), FadeIn(calc, shift=UP * 0.2), run_time=1.0)
        filled = cell(pred[i][j], True).match_height(R[i][j]).move_to(R[i][j])
        self.play(Transform(R[i][j], filled), run_time=0.6)
        self.wait(0.5)

        # 4 · todos los huecos a la vez
        self.play(FadeOut(row), FadeOut(col), FadeOut(tgt), FadeOut(calc))
        anims = []
        for a in range(NU):
            for b in range(NP):
                if (a, b) in known or (a, b) == (i, j):
                    continue
                c = cell(pred[a][b], True).match_height(R[a][b]).move_to(R[a][b])
                c[0].set_fill(RED, opacity=0.12 + 0.1 * pred[a][b]).set_stroke(RED, 1.5, 0.5)
                anims.append(Transform(R[a][b], c))
        self.play(LaggedStart(*anims, lag_ratio=0.03), run_time=2.2)
        fin = T("Así recomienda: rellena los huecos", 25, INK, weight=BOLD).next_to(eq, DOWN, buff=0.6)
        fin2 = T("factorización de matrices", 24, RED, MONO).next_to(fin, DOWN, buff=0.25)
        self.play(FadeIn(fin, shift=UP * 0.2), FadeIn(fin2, shift=UP * 0.2))
        self.wait(1.5)
