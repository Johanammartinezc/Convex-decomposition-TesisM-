import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon

from postprocess_remove_hole_pieces import get_final_pieces_excluding_hole

def plot_solution_inst10():
    final_pieces, outer, inner, x, y = get_final_pieces_excluding_hole("inst10.txt")

    fig, ax = plt.subplots(figsize=(6,6))

    # outer
    O = list(outer) + [outer[0]]
    ox, oy = zip(*O)
    ax.plot(ox, oy)

    # inner
    I = list(inner) + [inner[0]]
    ix, iy = zip(*I)
    ax.plot(ix, iy)

    # piezas convexas finales
    for piece in final_pieces:
        poly_coords = [(x[i], y[i]) for i in piece]
        P = poly_coords + [poly_coords[0]]
        px, py = zip(*P)
        ax.plot(px, py)

    ax.set_aspect("equal", "box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.tight_layout()
    plt.savefig("inst10_optimal_solution.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    plot_solution_inst10()
