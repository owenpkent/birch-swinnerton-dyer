"""manim scene: the chord-and-tangent group law on an elliptic curve.

Shows, on E: y^2 = x^3 - x + 1, two points P and Q, the line through them, the
third intersection point R, and its reflection over the x-axis giving P + Q.
This is the operation that makes E(Q) a group and that underlies the whole
notion of rank, hence BSD.

Render:
    manim -pql visualizations/group_law.py GroupLawScene
"""

from __future__ import annotations

import numpy as np

try:
    from manim import (
        Scene, Axes, Dot, Line, DashedLine, MathTex, Create, FadeIn,
        VGroup, BLUE, YELLOW, GREEN, RED, WHITE,
    )
except Exception as exc:  # manim optional at import time
    raise SystemExit(
        "manim is required to render this scene. Install with: pip install manim\n"
        f"(import failed: {exc})"
    )


# E: y^2 = x^3 - x + 1
def f(x: float) -> float:
    return x ** 3 - x + 1.0


def y_upper(x: float) -> float:
    v = f(x)
    return float(np.sqrt(v)) if v >= 0 else float("nan")


def curve_points(xmin: float, xmax: float, n: int = 400):
    xs = np.linspace(xmin, xmax, n)
    upper = [(x, y_upper(x)) for x in xs if f(x) >= 0]
    return upper


def third_intersection(px, py, qx, qy):
    """Third intersection of the secant/tangent line with the cubic.

    For y = m x + b, substituting into y^2 = x^3 - x + 1 gives a cubic in x whose
    roots sum to m^2. So x_R = m^2 - px - qx, and y_R = m x_R + b. The group sum
    P + Q is the reflection (x_R, -y_R).
    """
    if abs(px - qx) < 1e-9 and abs(py - qy) < 1e-9:
        # tangent: slope from implicit differentiation 2y y' = 3x^2 - 1
        m = (3 * px * px - 1) / (2 * py)
    else:
        m = (qy - py) / (qx - px)
    b = py - m * px
    xr = m * m - px - qx
    yr = m * xr + b
    return xr, yr, m, b


class GroupLawScene(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=6,
            tips=False,
        )

        upper = curve_points(-1.4, 2.6)
        lower = [(x, -y) for (x, y) in upper]
        curve_upper = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.012, color=BLUE) for (x, y) in upper
        ])
        curve_lower = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.012, color=BLUE) for (x, y) in lower
        ])

        title = MathTex(r"y^2 = x^3 - x + 1").to_edge(2 * np.array([0, 1, 0]))

        self.play(Create(axes), FadeIn(title))
        self.play(FadeIn(curve_upper), FadeIn(curve_lower))

        # two rational points on the curve
        px, py = -1.0, y_upper(-1.0)   # (-1, 1)
        qx, qy = 0.0, y_upper(0.0)     # (0, 1)
        P = Dot(axes.c2p(px, py), color=YELLOW)
        Q = Dot(axes.c2p(qx, qy), color=YELLOW)
        P_lbl = MathTex("P").next_to(P, np.array([-1, 1, 0]) * 0.4)
        Q_lbl = MathTex("Q").next_to(Q, np.array([1, 1, 0]) * 0.4)
        self.play(FadeIn(P), FadeIn(Q), FadeIn(P_lbl), FadeIn(Q_lbl))

        xr, yr, m, b = third_intersection(px, py, qx, qy)

        # secant line P--Q extended to the third intersection R
        x0, x1 = -1.6, max(2.4, xr + 0.3)
        line = Line(
            axes.c2p(x0, m * x0 + b),
            axes.c2p(x1, m * x1 + b),
            color=GREEN,
        )
        self.play(Create(line))

        R = Dot(axes.c2p(xr, yr), color=RED)
        R_lbl = MathTex("R").next_to(R, np.array([1, -1, 0]) * 0.4)
        self.play(FadeIn(R), FadeIn(R_lbl))

        # reflection over the x-axis gives P + Q
        drop = DashedLine(axes.c2p(xr, yr), axes.c2p(xr, -yr), color=WHITE)
        S = Dot(axes.c2p(xr, -yr), color=YELLOW)
        S_lbl = MathTex("P+Q").next_to(S, np.array([1, 1, 0]) * 0.4)
        self.play(Create(drop))
        self.play(FadeIn(S), FadeIn(S_lbl))

        caption = MathTex(
            r"\text{the third intersection, reflected, is } P+Q"
        ).scale(0.7).to_edge(np.array([0, -1, 0]))
        self.play(FadeIn(caption))
        self.wait(2)
