"""Draw a CTM column with physical ket legs above and bra legs below."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

GRAY, BLUE = "0.3", "#2878a5"


def bond(ax, start, end):
    ax.plot(*zip(start, end), color=GRAY, lw=1.5)
    points = [tuple((1-t)*a+t*b for a, b in zip(start, end)) for t in (.35, .65)]
    ax.add_patch(FancyArrowPatch(*points, arrowstyle="-|>", mutation_scale=15,
                                color=GRAY, lw=1.2, shrinkA=0, shrinkB=0))


def box(ax, x, y, text, width=.8, height=.36):
    ax.add_patch(FancyBboxPatch((x-width/2, y-height/2), width, height,
                               boxstyle="round,pad=0.025", edgecolor=BLUE,
                               facecolor="#edf5fa", lw=1.4, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=13, zorder=4)


fig, axes = plt.subplots(1, 2, figsize=(9, 4.8), constrained_layout=True)
for ax in axes:
    ax.set(xlim=(-2.1, 2.1), ylim=(-2.1, 2.1), aspect="equal")
    ax.axis("off")
ax = axes[0]
ax.set_title("Contract one column from top to bottom", fontsize=12)
for y, text in ((1.5, "$t$"), (.5, "$E_{\\mathrm{upper}}$"),
                (-.5, "$E_{\\mathrm{lower}}$"), (-1.5, "$b$")):
    box(ax, 0, y, text)
for y in (1.5, .5, -.5):
    bond(ax, (0, y-.21), (0, y-.79))
for y, left, right in ((1.5, "a", "c"), (.5, "l", "r"),
                        (-.5, "m", "s"), (-1.5, "b", "e")):
    if y == -1.5:
        bond(ax, (-.43, y), (-1.6, y))
        bond(ax, (1.6, y), (.43, y))
    else:
        bond(ax, (-1.6, y), (-.43, y))
        bond(ax, (.43, y), (1.6, y))
    ax.text(-1.45, y+.10, f"${left}$", ha="center", fontsize=12)
    ax.text(1.45, y+.10, f"${right}$", ha="center", fontsize=12)
for y, ket, bra in ((.5, "p", "P"), (-.5, "q", "Q")):
    ax.plot([-.23, -.80], [y+.21, y+.61], color=BLUE, lw=1.8)
    ax.plot([.23, .80], [y-.21, y-.61], color=BLUE, lw=1.8)
    ax.text(-.91, y+.61, f"${ket}$ (ket)", ha="right", va="center", fontsize=10, color=BLUE)
    ax.text(.91, y-.61, f"${bra}$ (bra)", ha="left", va="center", fontsize=10, color=BLUE)

ax = axes[1]
ax.set_title("Fuse the four virtual legs on each side", fontsize=12)
box(ax, 0, 0, "column", width=1.8, height=1.1)
bond(ax, (-1.85, 0), (-.93, 0))
bond(ax, (.93, 0), (1.85, 0))
ax.text(-1.4, .12, "$i$ (0)", ha="center", fontsize=11)
ax.text(1.4, .12, "$j$ (1)", ha="center", fontsize=11)
for x, ket, bra in ((-.45, "$p$ (2)", "$P$ (4)"), (.45, "$q$ (3)", "$Q$ (5)")):
    ax.plot([x, x], [.58, 1.28], color=BLUE, lw=1.8)
    ax.plot([x, x], [-.58, -1.28], color=BLUE, lw=1.8)
    ax.text(x, 1.42, ket, ha="center", fontsize=11, color=BLUE)
    ax.text(x, -1.5, bra, ha="center", fontsize=11, color=BLUE)
ax.text(0, 1.83, "ket", ha="center", fontsize=11, color=BLUE)
ax.text(0, -1.86, "bra", ha="center", fontsize=11, color=BLUE)
axes[0].text(0, -2.02, "Gray arrows: virtual signatures; blue legs: physical spins",
             ha="center", fontsize=9)
fig.savefig(Path(__file__).with_name("ctm_strip_column.png"), dpi=200,
            bbox_inches="tight", pad_inches=.12)
plt.close(fig)
