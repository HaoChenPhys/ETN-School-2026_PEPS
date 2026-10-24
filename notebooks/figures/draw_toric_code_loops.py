"""Draw the periodic-lattice illustrations used in the toric-code solution notebook."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle


FIGURES = Path(__file__).resolve().parent
PDF = FIGURES / "toric_code_loops.pdf"
N = 5
BLUE = "#176B9B"
TEAL = "#15806F"
AMBER = "#B77700"
INK = "#243444"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "pdf.fonttype": 42, "text.color": INK,
    "axes.titlecolor": INK, "figure.facecolor": "white",
})


def horizontal(y):
    return {(x, y, "r") for x in range(N)}


def vertical(x):
    return {(x, y, "u") for y in range(N)}


def edge(ax, x, y, direction, **style):
    """Split a wrapping edge at the identified boundary."""
    if direction == "r":
        segments = [([x, x + 1], [y, y])] if x < N - 1 else [
            ([x, N - 0.5], [y, y]), ([-0.5, 0], [y, y])]
    else:
        segments = [([x, x], [y, y + 1])] if y < N - 1 else [
            ([x, x], [y, N - 0.5]), ([x, x], [-0.5, 0])]
    for xs, ys in segments:
        ax.plot(xs, ys, **style)


def lattice(ax):
    ax.add_patch(Rectangle((-0.5, -0.5), N, N, facecolor="#F8FAFC",
                           edgecolor="#9AA9B5", linewidth=1, zorder=0))
    for x in range(N):
        for y in range(N):
            for direction in ("r", "u"):
                edge(ax, x, y, direction, color="#D8E0E6", linewidth=0.8, zorder=1)
    xs, ys = zip(*[(x, y) for x in range(N) for y in range(N)])
    ax.scatter(xs, ys, s=8, color="#A8B4BF", zorder=2)
    # Matching arrows identify opposite boundaries of the fundamental square.
    for y in (-0.5, N - 0.5):
        ax.annotate("", xy=(1.0, y), xytext=(0.0, y),
                    arrowprops={"arrowstyle": "->", "color": INK, "lw": 1.1})
    for x in (-0.5, N - 0.5):
        ax.annotate("", xy=(x, 1.0), xytext=(x, 0.0),
                    arrowprops={"arrowstyle": "->", "color": INK, "lw": 1.1})
    ax.set(xlim=(-0.75, N + 0.25), ylim=(-0.75, N + 0.15), aspect="equal")
    ax.axis("off")


def occupied(ax, edges, color=BLUE):
    for x, y, direction in sorted(edges):
        edge(ax, x, y, direction, color=color, linewidth=3.6,
             solid_capstyle="round", zorder=4)


def check_closed(edges):
    degree = {(x, y): 0 for x in range(N) for y in range(N)}
    for x, y, direction in edges:
        degree[x, y] += 1
        other = ((x + 1) % N, y) if direction == "r" else (x, (y + 1) % N)
        degree[other] += 1
    assert all(d % 2 == 0 for d in degree.values())


def dual_loops(ax):
    # These paths run through plaquette centers, perpendicular to occupied edges.
    ax.plot([2.5, 2.5], [-0.5, N - 0.5], "--", color=AMBER,
            linewidth=1.7, zorder=5)
    ax.plot([-0.5, N - 0.5], [2.5, 2.5], "--", color=AMBER,
            linewidth=1.7, zorder=5)
    ax.text(2.5, N - 0.18, r"$\gamma_a^*$", ha="center", va="bottom", color=AMBER)
    ax.text(N - 0.2, 2.5, r"$\gamma_b^*$", ha="left", va="center", color=AMBER)


def topology_page(pdf):
    fig, axes = plt.subplots(1, 2, figsize=(10, 7.1))
    fig.subplots_adjust(left=0.055, right=0.97, bottom=0.22, top=0.78, wspace=0.17)
    fig.suptitle("Closed loops on a torus", x=0.055, y=0.96, ha="left",
                 fontsize=21, fontweight="bold")
    fig.text(0.055, 0.895, "Identify opposite sides of the square, as indicated by matching arrows.",
             fontsize=12)
    local = {(1, 1, "r"), (1, 2, "r"), (1, 1, "u"), (2, 1, "u")}
    check_closed(local)
    for ax in axes:
        lattice(ax)
    occupied(axes[0], local)
    axes[0].set_title(r"Contractible loop $C_0$", pad=13, fontsize=14)
    axes[0].text(0.5, -0.075, "Can shrink by local plaquette flips.",
                 transform=axes[0].transAxes, ha="center", fontsize=11)
    occupied(axes[1], horizontal(1), BLUE)
    occupied(axes[1], vertical(3), TEAL)
    axes[1].text(1.3, 1.18, r"$C_x$", color=BLUE, fontsize=14)
    axes[1].text(3.12, 3.5, r"$C_y$", color=TEAL, fontsize=14)
    axes[1].set_title("Two noncontractible cycles", pad=13, fontsize=14)
    axes[1].text(0.5, -0.075, "Wrap around the two directions of the torus.",
                 transform=axes[1].transAxes, ha="center", fontsize=11)
    fig.text(0.055, 0.125, "A line reaching a seam continues at the matching point on the opposite side.",
             fontsize=11)
    fig.text(0.055, 0.075, "Every vertex has even occupancy. Four occupied edges at a vertex are allowed.",
             fontsize=11)
    fig.text(0.95, 0.035, "1 / 2", ha="right", fontsize=9, color="#657583")
    pdf.savefig(fig)
    fig.savefig(FIGURES / "toric_code_loops.png", dpi=160)
    plt.close(fig)


def sectors_page(pdf):
    fig, axes = plt.subplots(2, 2, figsize=(10, 10.7))
    fig.subplots_adjust(left=0.07, right=0.95, bottom=0.14, top=0.82,
                        wspace=0.18, hspace=0.27)
    fig.suptitle("Four winding-parity sectors", x=0.065, y=0.967, ha="left",
                 fontsize=21, fontweight="bold")
    fig.text(0.065, 0.915,
             r"$a=N(C\cap\gamma_a^*)\;\mathrm{mod}\;2,\qquad"
             r"b=N(C\cap\gamma_b^*)\;\mathrm{mod}\;2$", fontsize=15)
    fig.legend(handles=[Line2D([], [], color=BLUE, lw=3.6, label="Occupied edges"),
                        Line2D([], [], color=AMBER, lw=1.7, ls="--", label="Dual measuring loops")],
               loc="upper left", bbox_to_anchor=(0.055, 0.885), ncol=2, frameon=False)
    examples = [
        ((0, 0), horizontal(0) | horizontal(3)),
        ((1, 0), horizontal(1)),
        ((0, 1), vertical(3)),
        ((1, 1), horizontal(1) | vertical(3)),
    ]
    for ax, ((a, b), edges) in zip(axes.flat, examples):
        check_closed(edges)
        crossings_a = sum(direction == "r" and x == 2 for x, y, direction in edges)
        crossings_b = sum(direction == "u" and y == 2 for x, y, direction in edges)
        assert (crossings_a % 2, crossings_b % 2) == (a, b)
        lattice(ax)
        occupied(ax, edges)
        dual_loops(ax)
        ax.set_title(fr"$(a,b)=({a},{b})$", pad=13, fontsize=15)
        ax.text(0.5, -0.035, f"Crossings: ({crossings_a}, {crossings_b})",
                transform=ax.transAxes, ha="center", fontsize=10.5)
    fig.text(0.065, 0.09, "Each panel shows one configuration, not an entire ground state.", fontsize=11)
    fig.text(0.065, 0.057, "A sector ground state sums equally over all configurations with those parities.", fontsize=11)
    fig.text(0.95, 0.025, "2 / 2", ha="right", fontsize=9, color="#657583")
    pdf.savefig(fig)
    fig.savefig(FIGURES / "toric_code_sectors.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    PDF.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(PDF, metadata={"Title": "Toric-code loops and winding sectors",
                                "Subject": "Illustrations for the ETN School PEPS tutorial"}) as pdf:
        topology_page(pdf)
        sectors_page(pdf)
    print(PDF)
