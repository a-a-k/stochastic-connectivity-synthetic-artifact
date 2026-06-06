from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def write_sensitivity_heatmap(heatmap: dict[str, object], out: str | Path, dpi: int = 220) -> Path:
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    theta_values = np.asarray(heatmap["theta_values"], dtype=float)
    rho_values = np.asarray(heatmap["rho_values"], dtype=float)
    gain = np.asarray(heatmap["gain"], dtype=float)
    service_live_improved = np.asarray(heatmap["service_live_improved"], dtype=float)

    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    image = ax.imshow(
        gain,
        origin="lower",
        aspect="auto",
        extent=[theta_values.min(), theta_values.max(), rho_values.min(), rho_values.max()],
        cmap="viridis",
    )
    contour_x = theta_values
    contour_y = service_live_improved
    mask = (contour_y >= rho_values.min()) & (contour_y <= rho_values.max())
    if mask.any():
        ax.plot(contour_x[mask], contour_y[mask], color="white", linewidth=1.8, label="rho = live(R=3)")
    ax.set_xlabel("node replica live probability theta")
    ax.set_ylabel("edge live probability rho")
    ax.set_title("Node-vs-edge sensitivity: gain from R=1 to R=3")
    ax.legend(loc="lower right", fontsize=8, framealpha=0.85)
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("availability gain")
    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)
    return out_path
