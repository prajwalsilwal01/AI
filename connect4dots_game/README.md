# Connect Four — Minimax AI with Alpha-Beta Pruning

A playable Connect Four game where you compete against an AI opponent driven
by the **minimax algorithm** with **alpha-beta pruning**, plus a benchmark
suite that empirically compares plain minimax against the pruned version.

Built as a third-year engineering minor project to demonstrate a classic
adversarial search algorithm applied to a real, playable game — with data
to back up *why* the optimization matters, not just that it exists.

---

## Project structure

```
connect4-minimax/
├── game.py              # Board state, move validation, win/draw detection
├── ai.py                 # Minimax (plain + alpha-beta), heuristic evaluation
├── main.py               # Pygame GUI — play against the AI
├── benchmark.py           # Compares plain minimax vs alpha-beta (nodes, timing)
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Running the game

```bash
python3 main.py
```

- Click a column to drop your piece (red).
- The AI (yellow) responds automatically using alpha-beta minimax.
- Press `R` to restart after a game ends.
- Adjust difficulty by changing `SEARCH_DEPTH` in `main.py` (default 5).
  Higher = smarter but slower per move. 5–7 plays reasonably well on
  a normal laptop.

## Running the benchmark

```bash
python3 benchmark.py
```

This runs both plain minimax and alpha-beta minimax on the same set of
mid-game board positions at depths 1–5, and prints a table of:

- Nodes explored (plain vs. alpha-beta)
- Node reduction percentage
- Time taken
- Speedup factor

Results are also written to `benchmark_results.csv` so you can plot them
(e.g. nodes vs. depth on a log scale) for your report or presentation.

**Note:** plain minimax grows extremely fast with depth (branching factor
up to 7). Depths beyond 6–7 can take a long time — that slowdown is itself
part of what the benchmark demonstrates.

---

## How the algorithm works

### Minimax
Minimax explores the game tree by alternating between a **maximizing**
player (the AI) and a **minimizing** player (the opponent), assuming both
play optimally. At the bottom of the search (or at a terminal state), a
score is assigned; that score propagates back up the tree, with the
maximizer always picking the move that leads to the highest guaranteed
score, and the minimizer picking the lowest.

### Alpha-beta pruning
Alpha-beta pruning is an optimization on top of minimax: it keeps track of
the best score the maximizer can already guarantee (`alpha`) and the best
score the minimizer can already guarantee (`beta`). If, during search, a
branch is found that can't possibly beat what the other side already has
available elsewhere, that branch is skipped entirely. This doesn't change
the final decision — it's mathematically equivalent to plain minimax — it
just avoids wasted computation. In practice this cuts the number of
explored nodes by 70%+ even at shallow depths (see benchmark output).

### Heuristic evaluation
Since a full Connect Four game tree is too large to search to completion
within a reasonable time, the AI searches to a fixed depth and then scores
non-terminal positions using a heuristic (`score_position` in `ai.py`):

- Center column control is weighted positively (central pieces participate
  in more potential winning lines).
- Every possible 4-in-a-row "window" on the board is scored based on how
  many AI pieces, opponent pieces, and empty cells it contains — rewarding
  building toward a win and penalizing letting the opponent get 3-in-a-row
  with an open 4th cell.

### Move ordering
Columns are searched center-first (`_order_moves` in `ai.py`), since
central moves tend to be stronger in Connect Four. Searching likely-good
moves first improves how effectively alpha-beta pruning can cut branches.

---

## Possible extensions (if you want to push the project further)

- **Iterative deepening** with a time limit instead of a fixed depth, so
  the AI always uses the full time budget available.
- **Transposition table** (caching previously-seen board states) to avoid
  re-computing identical positions reached via different move orders.
- **Difficulty selector** in the GUI itself (easy/medium/hard mapped to
  search depth), rather than editing a constant in code.
- Swap the evaluation function or try a different game (e.g. Othello) to
  show the algorithm generalizes.
- Log AI decision time per move during real games (not just the benchmark
  script) to compare theoretical vs. practical performance.

## Report angle

If this is for a course deliverable, the benchmark data supports a solid
"algorithm analysis" section: plot node counts (log scale) and time vs.
search depth for both algorithms, and discuss why alpha-beta's worst-case
complexity is still O(b^d) but its practical/average-case performance
with good move ordering approaches O(b^(d/2)) — effectively doubling how
deep you can search in the same time budget.
