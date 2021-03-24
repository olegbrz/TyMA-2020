from typing import List
import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) != 2:
    print("Usage: python hist <dotplot>")
    exit()

m = np.loadtxt(sys.argv[1], dtype="?", delimiter=" ")


def diag_hist(dotplot: np.array, skew: bool = False) -> List:
    """diag_hist computes the number of hits for each diagonal (primary or
       secondary) given a dotplot


    Args:
        dotplot (np.array): input dotplot.
        skew (bool, optional): switch between primary and secondary diagonals.
                               Defaults to False.

    Returns:
        List: counts of hits for every diagonal.
    """
    h, w = dotplot.shape
    d = h + w - 1
    histo = [0] * d
    if not skew:
        for k in range(0, d):
            i = max(k - w + 1, 0)
            j = max(w - k - 1, 0)
            while i < h and j < w:
                if dotplot[i, j]:
                    histo[k] += 1
                i += 1
                j += 1

    elif skew:
        for k in range(0, d):
            i = max(k - w + 1, 0)
            j = min(k, w - 1)
            while i < h and j >= 0:
                if dotplot[i, j]:
                    histo[k] += 1
                i += 1
                j -= 1

    return histo


fig, axs = plt.subplots(2, figsize=(10, 6))
fig.suptitle(f"HITS HISTOGRAM: {sys.argv[1]}")
axs[0].set_title("Hits for main diagonals [↘]")
axs[0].plot(diag_hist(m, False), linewidth=0.5, color="red")
axs[1].set_title("Hits for skew diagonals [↙]")
axs[1].plot(diag_hist(m, True), linewidth=0.5, color="blue")

max_y = max(axs[0].get_ylim()[1], axs[1].get_ylim()[1])

for ax in axs:
    ax.set(xlabel="Diagonal number", ylabel="Number of hits", ylim=[0, max_y])
    ax.label_outer()
plt.savefig(sys.argv[1] + "_hist.png", dpi=300, bbox_inches="tight")
plt.show()
print(sys.argv[1])
