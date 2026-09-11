#!/usr/bin/env python3
"""Matchmaking simulation  --  CLI entry point.

Generates players with random skill, runs matches (random matchmaking
by default), updates Elo, and reports the final skill vs elo distribution.

Override points:
  * matchmaking.py : pick_match()   - how teams are formed
  * elo.py         : update_elo()   - how ratings are updated
  * match.py       : play_match()   - how a winner is decided
"""
from __future__ import annotations

import argparse
import sys

from simulation import Simulation
from report import text_report, plot_report


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Matchmaking simulation with Elo ratings.",
    )
    p.add_argument("--players", type=int, default=1000,
                   help="Number of players to generate (default 1000).")
    p.add_argument("--matches", type=int, default=50000,
                   help="Number of matches to simulate (default 50000).")
    p.add_argument("--team-size", type=int, default=5,
                   help="Players per team (default 5).")
    p.add_argument("--initial-elo", type=float, default=1000.0,
                   help="Starting Elo for every player (default 1000).")
    p.add_argument("--kfactor", type=float, default=32.0,
                   help="Elo K-factor (default 32).")
    p.add_argument("--seed", type=int, default=None,
                   help="Random seed for reproducibility.")
    p.add_argument("--save-plots", type=str, default=None,
                   help="Path to save the plot figure (e.g. result.png).")
    p.add_argument("--no-show", action="store_true",
                   help="Do not display the plot interactively.")
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Print progress during simulation.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_argparser().parse_args(argv)

    if args.players < args.team_size * 2:
        print(f"Error: need at least {args.team_size * 2} players, "
              f"got {args.players}.", file=sys.stderr)
        return 1

    sim = Simulation(
        num_players=args.players,
        num_matches=args.matches,
        team_size=args.team_size,
        initial_elo=args.initial_elo,
        kfactor=args.kfactor,
        seed=args.seed,
    )

    print(f"Running simulation: {args.players} players, "
          f"{args.matches} matches, team size {args.team_size}.")
    sim.run(verbose=args.verbose)

    print()
    print(text_report(sim.players))

    plot_report(
        sim.players,
        save_path=args.save_plots,
        show=not args.no_show,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())