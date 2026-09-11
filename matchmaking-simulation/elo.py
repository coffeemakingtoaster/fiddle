"""Elo / MMR calculation  --  OVERRIDE POINT #2.

Swap or edit ``update_elo`` to experiment with different rating systems
(e.g. individual Elo, Trueskill, MMR with confidence, ...).

Contract
--------
update_elo(winners, losers, kfactor=32) -> None

* ``winners`` : list of Player objects on the winning team.
* ``losers``  : list of Player objects on the losing team.
* ``kfactor`` : maximum rating change per match.

Mutates ``player.elo`` and increments ``player.games_played`` in place.
"""
from __future__ import annotations

import math
from typing import Sequence

from player import Player


def _expected_score(rating_a: float, rating_b: float) -> float:
    """Standard Elo expected score for player A vs player B."""
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))


def update_elo(
    winners: Sequence[Player],
    losers: Sequence[Player],
    kfactor: float = 32.0,
) -> None:
    """Default Elo: team-average rating, logistic expected score, K-factor.

    Each player's rating moves toward their expected result (win=1, loss=0).
    Both teams use their average rating as the effective team rating.
    """
    avg_win_elo = sum(p.elo for p in winners) / len(winners)
    avg_lose_elo = sum(p.elo for p in losers) / len(losers)

    exp_win = _expected_score(avg_win_elo, avg_lose_elo)
    exp_lose = 1.0 - exp_win

    # actual scores: winners got 1, losers got 0
    delta_win = kfactor * (1.0 - exp_win)
    delta_lose = kfactor * (0.0 - exp_lose)

    for p in winners:
        p.elo += delta_win
        p.games_played += 1
    for p in losers:
        p.elo += delta_lose
        p.games_played += 1