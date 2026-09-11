from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Player:
    id: int
    skill: float
    elo: float = 1000.0
    games_played: int = 0

    def __repr__(self) -> str:
        return (
            f"Player(id={self.id}, skill={self.skill:.1f}, "
            f"elo={self.elo:.1f}, games={self.games_played})"
        )