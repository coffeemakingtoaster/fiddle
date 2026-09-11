"""Reporting / plotting for a finished simulation.

Produces a multi-panel matplotlib figure:
  1. Scatter of skill vs elo (alpha/size scaled by games_played).
  2. Histogram of skill distribution.
  3. Histogram of elo distribution.
  4. Histogram of games_played distribution.

Also prints a textual summary including Pearson correlation between
skill and elo.
"""
from __future__ import annotations

import math
from typing import Sequence

from player import Player


def _pearson(xs: Sequence[float], ys: Sequence[float]) -> float:
    n = len(xs)
    if n == 0:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return sxy / (sx * sy)


def text_report(players: Sequence[Player]) -> str:
    skills = [p.skill for p in players]
    elos = [p.elo for p in players]
    games = [p.games_played for p in players]
    corr = _pearson(skills, elos)
    lines = [
        "===== Simulation Report =====",
        f"Players          : {len(players)}",
        f"Skill  range     : {min(skills):.1f} - {max(skills):.1f}"
        f"  (mean {sum(skills)/len(skills):.1f})",
        f"Elo   range      : {min(elos):.1f} - {max(elos):.1f}"
        f"  (mean {sum(elos)/len(elos):.1f})",
        f"Games range      : {min(games)} - {max(games)}"
        f"  (mean {sum(games)/len(games):.1f})",
        f"Pearson(skill,elo): {corr:.4f}",
        "=============================",
    ]
    return "\n".join(lines)


def plot_report(
    players: Sequence[Player],
    save_path: str | None = None,
    show: bool = True,
) -> None:
    """Render and optionally save/show the multi-panel figure."""
    import matplotlib.pyplot as plt

    skills = [p.skill for p in players]
    elos = [p.elo for p in players]
    games = [p.games_played for p in players]
    corr = _pearson(skills, elos)

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle("Matchmaking Simulation Results", fontsize=14)

    # --- Panel 1: skill vs elo scatter -------------------------------- #
    ax = axes[0, 0]
    max_games = max(games) if games else 1
    # size grows with games played; alpha keeps it readable
    sizes = [20 + 80 * (g / max_games) for g in games]
    ax.scatter(skills, elos, s=sizes, alpha=0.4, edgecolors="none")
    ax.set_xlabel("Skill")
    ax.set_ylabel("Elo")
    ax.set_title(f"Skill vs Elo  (Pearson r = {corr:.3f})")

    # --- Panel 2: skill histogram ------------------------------------- #
    ax = axes[0, 1]
    ax.hist(skills, bins=30, edgecolor="black", alpha=0.7)
    ax.set_xlabel("Skill")
    ax.set_ylabel("Count")
    ax.set_title("Skill Distribution")

    # --- Panel 3: elo histogram --------------------------------------- #
    ax = axes[1, 0]
    ax.hist(elos, bins=30, edgecolor="black", alpha=0.7, color="orange")
    ax.set_xlabel("Elo")
    ax.set_ylabel("Count")
    ax.set_title("Elo Distribution")

    # --- Panel 4: games played histogram ------------------------------ #
    ax = axes[1, 1]
    ax.hist(games, bins=30, edgecolor="black", alpha=0.7, color="green")
    ax.set_xlabel("Games Played")
    ax.set_ylabel("Count")
    ax.set_title("Games Played Distribution")

    plt.tight_layout(rect=(0, 0, 1, 0.96))

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved plot to {save_path}")
    if show:
        plt.show()
    plt.close(fig)