# Matchmaking Simulation

A lightweight simulation framework for experimenting with matchmaking
strategies and rating systems in a 5v5 team game.

Players are assigned a hidden **skill** value (0–100, fixed for the
simulation). They play matches; the winner of each match is decided
probabilistically based on the summed skill of each team. After every
match, a visible **Elo** rating is updated for all participants. At the
end you can inspect how well the visible Elo tracks the hidden skill —
and how much your matchmaking strategy is responsible for that.

The two core pieces of logic — **how teams are formed** and **how ratings
are updated** — are isolated as single functions so you can swap them out
without touching the rest of the code.

## Quick start

```bash
# optional: create a venv
python -m venv .venv && source .venv/bin/activate

# install matplotlib (only dependency)
pip install -r requirements.txt

# run with defaults: 1000 players, 50000 matches, 5v5
python main.py --seed 42 --no-show --save-plots result.png

# or interactively (opens a window)
python main.py --seed 42
```

Example output:

```
Running simulation: 1000 players, 50000 matches, team size 5.

===== Simulation Report =====
Players          : 1000
Skill  range     : 0.0 - 100.0  (mean 51.3)
Elo   range      : 544.4 - 1427.0  (mean 1000.0)
Games range      : 429 - 581  (mean 500.0)
Pearson(skill,elo): 0.6851
=============================
Saved plot to result.png
```

## CLI flags

| Flag | Default | Description |
|---|---|---|
| `--players` | `1000` | Number of players generated |
| `--matches` | `50000` | Number of matches simulated |
| `--team-size` | `5` | Players per team |
| `--initial-elo` | `1000.0` | Starting Elo for every player |
| `--kfactor` | `32.0` | Elo K-factor |
| `--seed` | `None` | RNG seed for reproducibility |
| `--save-plots` | `None` | Path to save the figure (e.g. `result.png`) |
| `--no-show` | off | Suppress interactive plot window |
| `-v` / `--verbose` | off | Print progress during the run |

## Project layout

```
matchmaking-simulation/
├── main.py            # CLI entry point
├── simulation.py      # Orchestrator (Simulation class)
├── player.py          # Player dataclass (id, skill, elo, games_played)
├── match.py           # Match resolution — override point
├── matchmaking.py     # Team formation  — override point #1
├── elo.py             # Rating update  — override point #2
├── report.py          # Text summary + matplotlib plots
└── requirements.txt   # matplotlib
```

## How a match works

1. **Matchmaking** picks two disjoint teams of `team_size` players from
   the pool.
2. Each team's total skill is summed. The probability that team A wins
   is `sum_skill_a / (sum_skill_a + sum_skill_b)`. A coin is flipped
   with that probability to decide the winner.
3. **Elo update** adjusts every participant's rating. The default uses
   each team's average Elo, a logistic expected-score formula, and a
   K-factor applied to the actual result (win = 1, loss = 0).
4. Each player's `games_played` counter is incremented, and the result
   is recorded in `history` for future matchmaking decisions.

## Override points

### Matchmaking (`matchmaking.py`)

```python
def pick_match(players, history, rng, team_size=5) -> (team_a, team_b):
    ...
```

- `players` — all `Player` objects (read-only, do not mutate).
- `history` — list of past match dicts:
  `{"team_a": [ids], "team_b": [ids], "winners": [ids], "losers": [ids]}`
  (empty on the first call).
- `rng` — a `random.Random` instance for deterministic behaviour.

Return two lists of `team_size` players each, with no overlap.

### Elo (`elo.py`)

```python
def update_elo(winners, losers, kfactor=32.0) -> None:
    ...
```

Mutate `player.elo` and increment `player.games_played` in place. The
default is zero-sum (winners gain exactly what losers lose).

### Match resolution (`match.py`)

```python
def play_match(team_a, team_b, rng) -> (winners, losers):
    ...
```

Returns `(winners, losers)` as lists of `Player` objects.

### Using custom functions

You can pass custom callables directly to the `Simulation` constructor
without editing the default modules:

```python
from simulation import Simulation

sim = Simulation(
    num_players=1000,
    num_matches=50000,
    seed=42,
    matchmaking_fn=my_matchmaking,
    elo_fn=my_elo_update,
)
sim.run()
```

## Rough outline of results

Below are the behaviours observed with the **default** settings (random
matchmaking, standard team-average Elo, K=32). All runs use a fixed
seed for reproducibility.

### Default (random matchmaking)

| Setting | Value |
|---|---|
| Players | 1000 |
| Matches | 50000 |
| Team size | 5 |
| Seed | 42 |

| Metric | Value |
|---|---|
| Skill range | 0.0 – 100.0 (mean 51.3) |
| Elo range | 544.4 – 1427.0 (mean 1000.0) |
| Games played | 429 – 581 (mean 500.0) |
| **Pearson(skill, elo)** | **0.6851** |

The Elo distribution is roughly bell-shaped around 1000 and wider than
the skill distribution, because Elo is a noisy estimator driven by
stochastic match outcomes. The scatter of skill vs Elo shows a clear
positive trend — higher-skill players tend to land at higher Elo — but
with substantial spread, especially among players who happened to play
fewer matches or got unlucky teammates.

The `games_played` counter matters: with random matchmaking the spread
is modest (429–581), but if you constrain matchmaking (e.g. a queue that
prioritises waiting time) some players may play far more or fewer games
than others, which skews their Elo reliability. The scatter plot sizes
points by games played so this is visible at a glance.

### Larger run

| Setting | Value |
|---|---|
| Players | 2000 |
| Matches | 100000 |
| Seed | 7 |

| Metric | Value |
|---|---|
| Elo range | 479.4 – 1489.0 (mean 1000.0) |
| Games played | 429 – 579 (mean 500.0) |
| **Pearson(skill, elo)** | **0.6669** |

Scaling up the player count and match count gives a similar correlation
(~0.67), confirming the default settings reach a stable regime rather
than improving indefinitely with more matches.

### Equal skill (control)

When every player is assigned the same skill (50.0), the Pearson
correlation between skill and Elo is ~0.000 by construction, and Elo
values undergo a random walk around the starting 1000. This confirms
the Elo system does not invent a skill signal where none exists.

### Bimodal skill

With two groups (skill 100 vs skill 0), the high-skill group converges
to a mean Elo of ~1203 while the low-skill group drops to ~797, a clean
separation that shows the rating system tracks skill at the extremes.

### Custom matchmaking experiment

Swapping in a **skill-balanced** matchmaking function (sorts players by
skill and pairs the strongest with the weakest) drops the Pearson
correlation from ~0.69 to ~0.30. This is expected: balanced teams put
strong and weak players on the same side, so weak players get "carried"
and their Elo no longer reflects their individual skill as cleanly. This
demonstrates that the override points produce meaningfully different
simulation outcomes.