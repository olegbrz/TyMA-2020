from typing import List
import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) != 2:
    print("Usage: python hist <dotplot>")
    exit()

dotplot = np.loadtxt(sys.argv[1], dtype="?", delimiter=" ")


def get_diag(dotplot):
    height, width = dotplot.shape
    diagonals = height + width - 1
    counts = [0] * diagonals

    for d in range(0, diagonals):
        i = max(d - width + 1, 0)
        j = max(width - d - 1, 0)
        while i < height and j < width:
            if dotplot[i, j]:
                counts[d] += 1
            i += 1
            j += 1
    return counts


def get_skew_diag(dotplot):
    height, width = dotplot.shape
    diagonals = height + width - 1
    counts = [0] * diagonals

    for d in range(0, diagonals):
        i = max(d - width + 1, 0)
        j = min(d, width - 1)
        while i < height and j >= 0:
            if dotplot[i, j]:
                counts[d] += 1
            i += 1
            j -= 1
    return counts


fig, axs = plt.subplots(2, figsize=(10, 6))
fig.suptitle(f"HITS HISTOGRAM: {sys.argv[1]}")
axs[0].set_title("Hits for main diagonals [↘]")
axs[0].plot(get_diag(dotplot), linewidth=0.5, color="red")
axs[1].set_title("Hits for skew diagonals [↙]")
axs[1].plot(get_skew_diag(dotplot), linewidth=0.5, color="blue")

max_y = max(axs[0].get_ylim()[1], axs[1].get_ylim()[1])

for ax in axs:
    ax.set(xlabel="Diagonal number", ylabel="Number of hits", ylim=[0, max_y])
    ax.label_outer()

plt.savefig(sys.argv[1] + "_hist.png", dpi=300, bbox_inches="tight")
