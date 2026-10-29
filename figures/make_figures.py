#!/usr/bin/env python3
"""生成三角函数专题笔记的函数图像。

用法：python3 figures/make_figures.py
输出：figures/*.png
"""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update(
    {
        "font.family": "Noto Sans CJK SC",
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False,
        "axes.edgecolor": "#4a4a4a",
        "axes.linewidth": 0.9,
        "axes.labelsize": 11,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "legend.frameon": False,
        "legend.fontsize": 9.5,
    }
)

PI = np.pi
COLOR = {
    "sin": "#1f6feb",
    "cos": "#d9480f",
    "tan": "#2f9e44",
    "cot": "#7048e8",
    "sec": "#0b7285",
    "csc": "#c2255c",
}
GRAY = "#8a8a8a"
DASH = (0, (4, 3))
DPI = 220

X_LIM = (-2 * PI, 2 * PI)
PI_TICKS = [-2 * PI, -1.5 * PI, -PI, -0.5 * PI, 0, 0.5 * PI, PI, 1.5 * PI, 2 * PI]


def pi_label(v: float) -> str:
    """把 k*pi/2 写成分数形式的刻度标签。"""
    if abs(v) < 1e-9:
        return r"$0$"
    k = int(round(v / (PI / 2)))
    num, den = k, 2
    if num % den == 0:
        num //= den
        den = 1
    sign = "-" if num < 0 else ""
    num = abs(num)
    if den == 1:
        body = r"\pi" if num == 1 else str(num) + r"\pi"
    else:
        top = r"\pi" if num == 1 else str(num) + r"\pi"
        body = r"\frac{" + top + "}{2}"
    return "$" + sign + body + "$"


def base_axes(ax, xlim, ylim, xticks, yticks, xlabels=None, grid=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels or [pi_label(v) for v in xticks])
    ax.set_yticks(yticks)
    ax.axhline(0, color="#333333", lw=0.9, zorder=1)
    ax.axvline(0, color="#333333", lw=0.9, zorder=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=3, color="#4a4a4a")
    if grid:
        ax.grid(True, color="#e2e6ea", lw=0.7, zorder=0)


def asymptotes(ax, xs, ylim):
    for x in xs:
        ax.plot([x, x], list(ylim), color=GRAY, lw=0.9, ls=DASH, zorder=2)


def plot_pieces(ax, f, xs, color, lw=2.6, n=6000):
    """按渐近线切段绘图，避免图像连成竖线。"""
    x = np.linspace(xs[0], xs[1], n)
    with np.errstate(divide="ignore", invalid="ignore"):
        y = f(x)
    y[(np.abs(y) > 200) | ~np.isfinite(y)] = np.nan
    ax.plot(x, y, color=color, lw=lw, zorder=5, solid_capstyle="round")


def curve_label(ax, text, xy, color, fontsize=12):
    ax.text(
        *xy,
        text,
        color=color,
        fontsize=fontsize,
        ha="center",
        va="center",
        zorder=10,
        bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.8),
    )


def make_sin():
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    base_axes(ax, X_LIM, (-1.62, 1.62), PI_TICKS, [-1, 0, 1])
    for y in (1, -1):
        ax.axhline(y, color=GRAY, lw=0.8, ls=DASH, zorder=2)
    x = np.linspace(*X_LIM, 1200)
    ax.plot(x, np.sin(x), color=COLOR["sin"], lw=2.6, zorder=5)
    curve_label(ax, r"$y=\sin x$", (0.62 * PI, 1.34), COLOR["sin"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-sin.png", dpi=DPI)
    plt.close(fig)


def make_cos():
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    base_axes(ax, X_LIM, (-1.62, 1.62), PI_TICKS, [-1, 0, 1])
    for y in (1, -1):
        ax.axhline(y, color=GRAY, lw=0.8, ls=DASH, zorder=2)
    x = np.linspace(*X_LIM, 1200)
    ax.plot(x, np.cos(x), color=COLOR["cos"], lw=2.6, zorder=5)
    curve_label(ax, r"$y=\cos x$", (-0.86 * PI, 1.35), COLOR["cos"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-cos.png", dpi=DPI)
    plt.close(fig)


def make_tan():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ylim = (-4.3, 4.3)
    base_axes(ax, X_LIM, ylim, PI_TICKS, [-4, -2, 0, 2, 4])
    asymptotes(ax, [-1.5 * PI, -0.5 * PI, 0.5 * PI, 1.5 * PI], ylim)
    plot_pieces(ax, np.tan, X_LIM, COLOR["tan"])
    curve_label(ax, r"$y=\tan x$", (0.85 * PI, 3.2), COLOR["tan"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-tan.png", dpi=DPI)
    plt.close(fig)


def make_cot():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ylim = (-4.3, 4.3)
    base_axes(ax, X_LIM, ylim, PI_TICKS, [-4, -2, 0, 2, 4])
    asymptotes(ax, [-PI, 0, PI], ylim)
    plot_pieces(ax, lambda t: 1 / np.tan(t), X_LIM, COLOR["cot"])
    curve_label(ax, r"$y=\cot x$", (0.8 * PI, 3.2), COLOR["cot"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-cot.png", dpi=DPI)
    plt.close(fig)


def make_sec():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ylim = (-4.3, 4.3)
    base_axes(ax, X_LIM, ylim, PI_TICKS, [-3, -1, 1, 3])
    asymptotes(ax, [-1.5 * PI, -0.5 * PI, 0.5 * PI, 1.5 * PI], ylim)
    for y in (1, -1):
        ax.axhline(y, color=GRAY, lw=0.8, ls=(0, (2, 2)), zorder=2)
    plot_pieces(ax, lambda t: 1 / np.cos(t), X_LIM, COLOR["sec"])
    curve_label(ax, r"$y=\sec x$", (0.72 * PI, 3.4), COLOR["sec"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-sec.png", dpi=DPI)
    plt.close(fig)


def make_csc():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ylim = (-4.3, 4.3)
    base_axes(ax, X_LIM, ylim, PI_TICKS, [-3, -1, 1, 3])
    asymptotes(ax, [-PI, 0, PI], ylim)
    for y in (1, -1):
        ax.axhline(y, color=GRAY, lw=0.8, ls=(0, (2, 2)), zorder=2)
    plot_pieces(ax, lambda t: 1 / np.sin(t), X_LIM, COLOR["csc"])
    curve_label(ax, r"$y=\csc x$", (-0.72 * PI, 3.8), COLOR["csc"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-csc.png", dpi=DPI)
    plt.close(fig)


def make_overview():
    fig, axes = plt.subplots(2, 3, figsize=(10.2, 5.4))
    items = [
        ("sin", r"$y=\sin x$", np.sin, (-1.55, 1.55), [-1, 1], None, "sin"),
        ("cos", r"$y=\cos x$", np.cos, (-1.55, 1.55), [-1, 1], None, "cos"),
        ("tan", r"$y=\tan x$", np.tan, (-4.0, 4.0), [-2, 2], [-1.5 * PI, -0.5 * PI, 0.5 * PI, 1.5 * PI], "tan"),
        ("cot", r"$y=\cot x$", lambda t: 1 / np.tan(t), (-4.0, 4.0), [-2, 2], [-PI, 0, PI], "cot"),
        ("sec", r"$y=\sec x$", lambda t: 1 / np.cos(t), (-4.0, 4.0), [-2, 2], [-1.5 * PI, -0.5 * PI, 0.5 * PI, 1.5 * PI], "sec"),
        ("csc", r"$y=\csc x$", lambda t: 1 / np.sin(t), (-4.0, 4.0), [-2, 2], [-PI, 0, PI], "csc"),
    ]
    for ax, (_, title, f, ylim, yticks, asym, key) in zip(axes.flat, items):
        base_axes(ax, X_LIM, ylim, [-2 * PI, -PI, 0, PI, 2 * PI], yticks,
                  xlabels=[r"$-2\pi$", r"$-\pi$", r"$0$", r"$\pi$", r"$2\pi$"], grid=False)
        if asym:
            asymptotes(ax, asym, ylim)
        if key in ("sec", "csc"):
            for y in (1, -1):
                ax.axhline(y, color=GRAY, lw=0.7, ls=(0, (2, 2)), zorder=2)
        plot_pieces(ax, f, X_LIM, COLOR[key], lw=1.9, n=3000)
        ax.set_title(title, fontsize=12, color=COLOR[key], pad=4)
        ax.tick_params(labelsize=8.5)
    fig.tight_layout(pad=1.1, w_pad=1.4)
    fig.savefig("figures/fig-overview.png", dpi=200)
    plt.close(fig)


def make_unit_circle():
    a = np.deg2rad(50)
    ca, sa = np.cos(a), np.sin(a)
    ta = np.tan(a)
    cta = 1 / ta
    sec_a = 1 / ca
    csc_a = 1 / sa

    fig, ax = plt.subplots(figsize=(6.6, 6.45))
    ax.set_aspect("equal")
    ax.set_xlim(-1.16, 2.02)
    ax.set_ylim(-1.16, 1.95)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # 坐标轴（带箭头）
    ax.annotate("", xy=(1.99, 0), xytext=(-0.66, 0),
                arrowprops=dict(arrowstyle="-|>", color="#333333", lw=0.9,
                                mutation_scale=11, shrinkA=0, shrinkB=0), zorder=1)
    ax.annotate("", xy=(0, 1.9), xytext=(0, -0.56),
                arrowprops=dict(arrowstyle="-|>", color="#333333", lw=0.9,
                                mutation_scale=11, shrinkA=0, shrinkB=0), zorder=1)
    ax.text(1.97, -0.1, r"$x$", fontsize=12, ha="right", va="top")
    ax.text(-0.07, 1.9, r"$y$", fontsize=12, ha="right", va="top")

    # 单位圆与三条切线
    t = np.linspace(0, 2 * PI, 600)
    ax.plot(np.cos(t), np.sin(t), color="#222222", lw=1.5, zorder=3)
    ax.plot([1, 1], [-0.62, 1.44], color="#9a9a9a", lw=0.85, zorder=2)
    ax.plot([-0.62, 1.62], [1, 1], color="#9a9a9a", lw=0.85, zorder=2)
    d = np.array([-sa, ca])
    p0 = np.array([0, csc_a]) + 0.2 * d
    p1 = np.array([sec_a, 0]) - 0.2 * d
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="#9a9a9a", lw=0.85, zorder=2)

    # 终边（延长到正切线的交点 T）
    ax.plot([0, 1], [0, ta], color="#9a9a9a", lw=0.85, ls=DASH, zorder=2)

    # 角
    arc = np.linspace(0, a, 120)
    ax.plot(0.22 * np.cos(arc), 0.22 * np.sin(arc), color="#555555", lw=1.1, zorder=4)
    ax.text(0.255, 0.135, r"$\alpha$", fontsize=12, color="#333333")

    # 六条三角函数线
    ax.plot([ca, ca], [0, sa], color=COLOR["sin"], lw=4.0, zorder=6, solid_capstyle="round")
    ax.plot([0, ca], [0, 0], color=COLOR["cos"], lw=4.0, zorder=6, solid_capstyle="round")
    ax.plot([1, 1], [0, ta], color=COLOR["tan"], lw=4.0, zorder=6, solid_capstyle="round")
    ax.plot([0, cta], [1, 1], color=COLOR["cot"], lw=4.0, zorder=6, solid_capstyle="round")
    ax.plot([0, sec_a], [-0.05, -0.05], color=COLOR["sec"], lw=3.2, zorder=6, solid_capstyle="round")
    ax.plot([-0.05, -0.05], [0, csc_a], color=COLOR["csc"], lw=3.2, zorder=6, solid_capstyle="round")

    # 端点
    pts = {
        "O": (0, 0), "A": (1, 0), "B": (0, 1), "P": (ca, sa), "M": (ca, 0),
        "T": (1, ta), "S": (cta, 1), "Q": (sec_a, 0), "R": (0, csc_a),
    }
    for name, (x, y) in pts.items():
        ax.plot([x], [y], "o", ms=4.2, color="#222222", zorder=8)
    for name, xy in {
        "O": (-0.075, -0.075), "A": (1.075, 0.055), "B": (-0.1, 1.06),
        "P": (0.545, 0.815), "M": (0.6, 0.05), "T": (1.075, 1.27),
        "S": (0.8, 1.075), "Q": (sec_a + 0.02, -0.115), "R": (-0.1, csc_a + 0.02),
    }.items():
        ax.text(*xy, name, fontsize=11.5, color="#222222",
                ha="center", va="center", zorder=9)

    # 线段标注
    ax.text(ca + 0.08, sa * 0.42, r"$\sin\alpha$", color=COLOR["sin"], fontsize=12,
            rotation=90, ha="center", va="center", zorder=9,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
    ax.text(0.40, 0.085, r"$\cos\alpha$", color=COLOR["cos"], fontsize=12,
            ha="center", va="center", zorder=9,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
    ax.text(1.135, ta * 0.62, r"$\tan\alpha$", color=COLOR["tan"], fontsize=12,
            rotation=90, ha="center", va="center", zorder=9,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
    ax.text(0.40, 1.085, r"$\cot\alpha$", color=COLOR["cot"], fontsize=12,
            ha="center", va="center", zorder=9,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
    ax.text(1.17, -0.15, r"$\sec\alpha$", color=COLOR["sec"], fontsize=12,
            ha="center", va="center", zorder=9,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
    ax.text(-0.155, 0.75, r"$\csc\alpha$", color=COLOR["csc"], fontsize=12,
            rotation=90, ha="center", va="center", zorder=9,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))

    fig.tight_layout(pad=0.3)
    fig.savefig("figures/fig-unit-circle.png", dpi=200)
    plt.close(fig)


INV_COLOR = {
    "arcsin": "#0b7285",
    "arccos": "#7048e8",
    "arctan": "#2f9e44",
    "arccot": "#d9480f",
}


def _setup_inverse(ax, xlim, ylim, xticks, yticks, ylabels=None):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    if ylabels:
        ax.set_yticklabels(ylabels)
    ax.axhline(0, color="#333333", lw=0.9, zorder=1)
    ax.axvline(0, color="#333333", lw=0.9, zorder=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=3, color="#4a4a4a")
    ax.grid(True, color="#e2e6ea", lw=0.7, zorder=0)


def make_arcsin():
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    _setup_inverse(ax, (-1.22, 1.22), (-2.02, 2.02), [-1, 0, 1], [-PI / 2, 0, PI / 2],
                   [r"$-\frac{\pi}{2}$", r"$0$", r"$\frac{\pi}{2}$"])
    for y in (-PI / 2, PI / 2):
        ax.axhline(y, color=GRAY, lw=0.85, ls=DASH, zorder=2)
    x = np.linspace(-1, 1, 600)
    ax.plot(x, np.arcsin(x), color=INV_COLOR["arcsin"], lw=2.6, zorder=5)
    ax.plot([-1, 1], [-PI / 2, PI / 2], "o", ms=4.5, color=INV_COLOR["arcsin"], zorder=6)
    curve_label(ax, r"$y=\arcsin x$", (-0.60, 1.32), INV_COLOR["arcsin"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-arcsin.png", dpi=DPI)
    plt.close(fig)


def make_arccos():
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    _setup_inverse(ax, (-1.22, 1.22), (-0.75, 3.72), [-1, 0, 1], [0, PI / 2, PI],
                   [r"$0$", r"$\frac{\pi}{2}$", r"$\pi$"])
    ax.axhline(PI, color=GRAY, lw=0.85, ls=DASH, zorder=2)
    x = np.linspace(-1, 1, 600)
    ax.plot(x, np.arccos(x), color=INV_COLOR["arccos"], lw=2.6, zorder=5)
    ax.plot([1, -1], [0, PI], "o", ms=4.5, color=INV_COLOR["arccos"], zorder=6)
    curve_label(ax, r"$y=\arccos x$", (0.62, 2.92), INV_COLOR["arccos"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-arccos.png", dpi=DPI)
    plt.close(fig)


def make_arctan():
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    _setup_inverse(ax, (-5, 5), (-2.15, 2.15), [-4, -2, 0, 2, 4], [-PI / 2, 0, PI / 2],
                   [r"$-\frac{\pi}{2}$", r"$0$", r"$\frac{\pi}{2}$"])
    for y in (-PI / 2, PI / 2):
        ax.axhline(y, color=GRAY, lw=0.85, ls=DASH, zorder=2)
    x = np.linspace(-5, 5, 800)
    ax.plot(x, np.arctan(x), color=INV_COLOR["arctan"], lw=2.6, zorder=5)
    curve_label(ax, r"$y=\arctan x$", (-3.25, 1.32), INV_COLOR["arctan"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-arctan.png", dpi=DPI)
    plt.close(fig)


def make_arccot():
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    _setup_inverse(ax, (-5, 5), (-0.75, 3.85), [-4, -2, 0, 2, 4], [0, PI / 2, PI],
                   [r"$0$", r"$\frac{\pi}{2}$", r"$\pi$"])
    ax.axhline(PI, color=GRAY, lw=0.85, ls=DASH, zorder=2)
    x = np.linspace(-5, 5, 800)
    ax.plot(x, PI / 2 - np.arctan(x), color=INV_COLOR["arccot"], lw=2.6, zorder=5)
    curve_label(ax, r"$y=\operatorname{arccot} x$", (2.85, 2.72), INV_COLOR["arccot"])
    fig.tight_layout(pad=0.6)
    fig.savefig("figures/fig-arccot.png", dpi=DPI)
    plt.close(fig)


def make_inverse_symmetry():
    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    ax.set_aspect("equal")
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.8, 1.8)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.axhline(0, color="#333333", lw=0.9, zorder=1)
    ax.axvline(0, color="#333333", lw=0.9, zorder=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color="#e2e6ea", lw=0.7, zorder=0)
    ax.tick_params(length=3, color="#4a4a4a")

    lim = 1.75
    ax.plot([-lim, lim], [-lim, lim], color="#8a8a8a", lw=1.0, ls=DASH, zorder=2)
    ax.text(1.45, 1.52, r"$y=x$", color="#6a6a6a", fontsize=11.5, rotation=45,
            ha="center", va="center")

    xs = np.linspace(-PI / 2, PI / 2, 600)
    ax.plot(xs, np.sin(xs), color=COLOR["sin"], lw=2.4, zorder=5)
    xa = np.linspace(-1, 1, 600)
    ax.plot(xa, np.arcsin(xa), color=INV_COLOR["arcsin"], lw=2.4, zorder=5)

    x0 = 0.9
    y0 = np.sin(x0)
    ax.plot([x0, y0], [y0, x0], color="#6a6a6a", lw=1.0, ls=(0, (2, 2)), zorder=4)
    ax.plot([x0, y0], [y0, x0], ".", color="#444444", ms=6, zorder=6)

    curve_label(ax, r"$y=\sin x$", (1.15, -1.35), COLOR["sin"], fontsize=11.5)
    curve_label(ax, r"$y=\arcsin x$", (-1.42, 0.62), INV_COLOR["arcsin"], fontsize=11.5)

    fig.tight_layout(pad=0.4)
    fig.savefig("figures/fig-inverse-symmetry.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    make_sin()
    make_cos()
    make_tan()
    make_cot()
    make_sec()
    make_csc()
    make_arcsin()
    make_arccos()
    make_arctan()
    make_arccot()
    make_inverse_symmetry()
    make_overview()
    make_unit_circle()
    print("ok")