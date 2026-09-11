"""Simulation orchestrator.

Wires together matchmaking -> match -> elo update, and keeps a history
of every match played for later analysis or for matchmaking strategies
that want to look at past results.
"""
from __future__ import annotations

import random
from typing import Callable

from player import Player
from match import play_match
from matchmaking import pick_match
from elo import update_elo


class Simulation:
    """Run a full matchmaking simulation.

    Parameters
    ----------
    num_players : int
        How many players to generate.
    num_matches : int
        Total matches to simulate.
    team_size   : int
        Players per team (default 5).
    initial_elo : float
        Starting Elo for every player.
    kfactor     : float
        Elo K-factor.
    seed        : int | None
        RNG seed for reproducibility.

    Override points
    ----------------
    ``matchmaking_fn`` and ``elo_fn`` can be replaced with custom callables
    that follow the same contract as the defaults in ``matchmaking.py``
    and ``elo.py``.
    """

    def __init__(
        self,
        num_players: int = 1000,
        num_matches: int = 50000,
        team_size: int = 5,
        initial_elo: float = 1000.0,
        kfactor: float = 32.0,
        seed: int | None = None,
        matchmaking_fn: Callable = pick_match,
        elo_fn: Callable = update_elo,
        match_fn: Callable = play_match,
    ) -> None:
        self.team_size = team_size
        self.kfactor = kfactor
        self.matchmaking_fn = matchmaking_fn
        self.elo_fn = elo_fn
        self.match_fn = match_fn
        self.rng = random.Random(seed)

        # Generate players with uniform random skill 0-100.
        self.players: list[Player] = [
            Player(id=i, skill=self.rng.uniform(0, 100), elo=initial_elo)
            for i in range(num_players)
        ]
        self.history: list[dict] = []
        self.num_matches = num_matches

    # ------------------------------------------------------------------ #
    def run(self, verbose: bool = False) -> None:
        """Run the full simulation."""
        log_every = max(1, self.num_matches // 20)
        for i in range(self.num_matches):
            team_a, team_b = self.matchmaking_fn(
                self.players, self.history, self.rng, self.team_size
            )
            winners, losers = self.match_fn(team_a, team_b, self.rng)
            self.elo_fn(winners, losers, self.kfactor)

            self.history.append(
                {
                    "team_a": [p.id for p in team_a],
                    "team_b": [p.id for p in team_b],
                    "winners": [p.id for p in winners],
                    "losers": [p.id for p in losers],
                }
            )

            if verbose and (i + 1) % log_every == 0:
                print(f"  match {i + 1}/{self.num_matches}")

    # ------------------------------------------------------------------ #
    def summary(self) -> dict:
        """Return a summary dict of the final state."""
        elos = [p.elo for p in self.players]
        skills = [p.skill for p in self.players]
        games = [p.games_played for p in self.players]
        return {
            "num_players": len(self.players),
            "num_matches": len(self.history),
            "elo_min": min(elos),
            "elo_max": max(elos),
            "elo_mean": sum(elos) / len(elos),
            "skill_min": min(skills),
            "skill_max": max(skills),
            "skill_mean": sum(skills) / len(skills),
            "games_min": min(games),
            "games_max": max(games),
            "games_mean": sum(games) / len(games),
        }