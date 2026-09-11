"""Matchmaking strategy  --  OVERRIDE POINT #1.

Swap or edit ``pick_match`` to experiment with different matchmaking
strategies (e.g. Elo-balanced, skill-balanced, queue-based, ...).

Contract
--------
pick_match(players, history, rng, team_size=5) -> (team_a, team_b)

* ``players``  : list of all Player objects (read-only; do not mutate).
* ``history``  : list of past match records, each is a dict:
                 {"team_a": [...], "team_b": [...], "winners": [...], "losers": [...]}
                 (empty on the very first call).
* ``rng``      : a random.Random instance for deterministic behaviour.
* ``team_size``: number of players per team (default 5).

Return two lists of ``team_size`` Player objects each, with no overlap.
"""
from __future__ import annotations

import random
from typing import Sequence

from player import Player


def pick_match(
    players: Sequence[Player],
    history: list[dict],
    rng: random.Random | None = None,
    team_size: int = 5,
) -> tuple[list[Player], list[Player]]:
    """Default strategy: pick 2*team_size distinct players at random."""
    if rng is None:
        rng = random

    if len(players) < team_size * 2:
        raise ValueError(
            f"Need at least {team_size * 2} players, got {len(players)}"
        )

    chosen = rng.sample(list(players), team_size * 2)
    team_a = chosen[:team_size]
    team_b = chosen[team_size:]
    return team_a, team_b