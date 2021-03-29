from typing import List
import matplotlib.pyplot as plt
from operator import add
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


pdiags = get_diag(dotplot)
rdiags = get_skew_diag(dotplot)

plt.style.use("classic")

fig, axs = plt.subplots(3, figsize=(6, 9))
title = sys.argv[1].split("\\")[-1]
fig.suptitle(f"HITS HISTOGRAM: {title}", fontweight="bold")
axs[0].set_title("Hits for main diagonals [↘]")
axs[0].plot(pdiags, linewidth=1, color="r")
axs[1].set_title("Hits for skew diagonals [↙]")
axs[1].plot(rdiags, linewidth=1, color="g")
axs[2].set_title("Sum")
axs[2].plot(
    list(map(add, pdiags, rdiags)),
    linewidth=1,
    color="k",
)

max_y = max(axs[0].get_ylim()[1], axs[1].get_ylim()[1], axs[2].get_ylim()[1])

for ax in axs:
    ax.set(xlabel="Diagonal number", ylabel="Number of hits", ylim=[-10, max_y])
    ax.label_outer()
    ax.grid(True)

plt.savefig(sys.argv[1] + "_hist.png", dpi=300, bbox_inches="tight")
