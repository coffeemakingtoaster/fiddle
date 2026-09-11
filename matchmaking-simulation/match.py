"""Match resolution.

This module decides who wins a single game.  Two teams face off; the
probability that team A wins is the fraction of total skill it holds.

Override / swap this module to experiment with different match models
(e.g. add variance, per-player contributions, draws, ...).
"""
from __future__ import annotations

import random
from typing import Sequence

from player import Player


def play_match(
    team_a: Sequence[Player],
    team_b: Sequence[Player],
    rng: random.Random | None = None,
) -> tuple[list[Player], list[Player]]:
    """Play one match and return (winners, losers).

    Win probability for team A = sum_skill_a / (sum_skill_a + sum_skill_b).
    A random draw decides the winner.
    """
    if rng is None:
        rng = random

    skill_a = sum(p.skill for p in team_a)
    skill_b = sum(p.skill for p in team_b)
    total = skill_a + skill_b
    if total == 0:
        p_a_win = 0.5
    else:
        p_a_win = skill_a / total

    if rng.random() < p_a_win:
        return list(team_a), list(team_b)
    return list(team_b), list(team_a)