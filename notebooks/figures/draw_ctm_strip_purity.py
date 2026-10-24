"""Show the physical-index connections in the two-copy purity contraction."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


BLUE, ORANGE, GRAY = "#2878a5", "#bc5a16", "0.3"


def arrow(ax, start, end, color=GRAY):
    ax.plot(*zip(start, end), color=color, lw=1.6, zorder=1)
    middle = [tuple((1-t)*a+t*b for a, b in zip(start, end)) for t in (.35, .65)]
    ax.add_patch(FancyArrowPatch(*middle, arrowstyle="-|>", mutation_scale=16,
                                color=color, lw=1.3, shrinkA=0, shrinkB=0))


fig, axes = plt.subplots(1, 2, figsize=(10, 5.2), constrained_layout=True)
for ax, columns in zip(axes, (False, True)):
    ax.set(xlim=(-2.1, 2.8), ylim=(-2.4, 2.4), aspect="equal")
    ax.axis("off")
    ax.set_title("Trace of the squared patch RDM" if not columns else
                 "Two-copy purity transfer tensor", fontsize=13, pad=12)
    for y, replica in ((1, 1), (-1, 2)):
        ax.add_patch(FancyBboxPatch((-.95, y-.30), 1.9, .60,
                                   boxstyle="round,pad=0.04", facecolor="#edf5fa",
                                   edgecolor=BLUE, lw=1.5, zorder=3))
        text = (fr"$\widetilde\rho_R^{{({replica})}}$" if not columns else
                f"column (copy {replica})")
        ax.text(0, y, text, ha="center", va="center", fontsize=12 if columns else 14, zorder=4)
        if columns:
            left, right = ("a", "b") if replica == 1 else ("c", "d")
            arrow(ax, (-2.05, y), (-.99, y))
            arrow(ax, (.99, y), (2.05, y))
            ax.text(-1.55, y+.12, f"${left}$", ha="center", fontsize=12)
            ax.text(1.55, y+.12, f"${right}$", ha="center", fontsize=12)

    # Both copies keep ket legs on top and bra legs on the bottom.
    # The inner line joins bra 1 to ket 2; the outer return joins bra 2 to ket 1.
    ax.plot([0, 0], [.66, -.66], color=BLUE, lw=1.8)
    ax.plot([0, 0, 2.35, 2.35, 0, 0],
            [-1.34, -1.95, -1.95, 1.95, 1.95, 1.34], color=ORANGE, lw=1.8)
    inner, outer = ("P,Q", "p,q") if columns else ("J", "I")
    ax.text(.12, 0, f'${inner}$', ha='left', va='center', fontsize=13, color=BLUE)
    ax.text(2.2, 0, f'${outer}$', ha='right', va='center', fontsize=13, color=ORANGE)
    for y,label in ((1.57,'ket'), (.46,'bra'), (-.46,'ket'), (-1.57,'bra')):
        ax.text(-.14, y, label, ha='right', va='center', fontsize=10)
    ax.text(.35, -2.25, 'Sum over all patch spins I and J' if not columns else
            'Fuse the left and right virtual pairs:\npurity_transfer[(a,c), (b,d)]',
            ha='center', va='center', fontsize=10)

fig.savefig(Path(__file__).with_name("ctm_purity_transfer.png"), dpi=200,
            bbox_inches="tight", pad_inches=.12)
plt.close(fig)
