"""
Benchmark: Plain Minimax vs Minimax + Alpha-Beta Pruning
------------------------------------------------------------
Runs both algorithms on the same set of mid-game board positions at
increasing depths and reports:
  - Nodes explored
  - Time taken
  - Speedup / pruning efficiency

This produces the empirical results you'd want in a report to show WHY
alpha-beta pruning matters, not just that it exists.

Run with: python3 benchmark.py
(Note: plain minimax gets very slow past depth 6 - that's expected and
 is itself part of the point being demonstrated.)
"""

import time
import math
import random
import csv

from game import Connect4, PLAYER, AI
from ai import minimax_plain, minimax_ab, NodeCounter


def make_midgame_position(num_random_moves=6, seed=None):
    """Create a semi-random mid-game board so benchmarks aren't trivial (empty board)
    or already terminal."""
    rng = random.Random(seed)
    game = Connect4()
    turn = PLAYER
    moves_made = 0
    while moves_made < num_random_moves and not game.is_terminal():
        col = rng.choice(game.valid_moves())
        game.drop_piece(col, turn)
        turn = AI if turn == PLAYER else PLAYER
        moves_made += 1
    return game


def benchmark_depth(depth, num_positions=3, seed_base=0):
    results = []
    for i in range(num_positions):
        game = make_midgame_position(num_random_moves=6, seed=seed_base + i)

        # Plain minimax
        counter_plain = NodeCounter()
        t0 = time.perf_counter()
        minimax_plain(game.copy(), depth, True, counter_plain)
        t_plain = time.perf_counter() - t0

        # Alpha-beta minimax
        counter_ab = NodeCounter()
        t0 = time.perf_counter()
        minimax_ab(game.copy(), depth, -math.inf, math.inf, True, counter_ab)
        t_ab = time.perf_counter() - t0

        results.append({
            "depth": depth,
            "position": i,
            "plain_nodes": counter_plain.count,
            "plain_time_s": round(t_plain, 4),
            "ab_nodes": counter_ab.count,
            "ab_time_s": round(t_ab, 4),
            "node_reduction_pct": round(
                100 * (1 - counter_ab.count / counter_plain.count), 2
            ) if counter_plain.count else 0,
            "speedup_x": round(t_plain / t_ab, 2) if t_ab > 0 else float('inf'),
        })
    return results


def main():
    # NOTE: plain minimax at depth > 6 can take a long time on a 7-wide board.
    # Start conservative; raise MAX_DEPTH once you've seen timing at lower depths.
    DEPTHS = [1, 2, 3, 4, 5]
    all_results = []

    print(f"{'Depth':<7}{'Plain Nodes':<14}{'AB Nodes':<12}{'Reduction %':<14}{'Plain t(s)':<12}{'AB t(s)':<10}{'Speedup':<8}")
    print("-" * 80)

    for depth in DEPTHS:
        results = benchmark_depth(depth, num_positions=3)
        for r in results:
            all_results.append(r)
        # Average across positions for a clean printed summary
        avg_plain_nodes = sum(r["plain_nodes"] for r in results) / len(results)
        avg_ab_nodes = sum(r["ab_nodes"] for r in results) / len(results)
        avg_plain_t = sum(r["plain_time_s"] for r in results) / len(results)
        avg_ab_t = sum(r["ab_time_s"] for r in results) / len(results)
        avg_reduction = 100 * (1 - avg_ab_nodes / avg_plain_nodes) if avg_plain_nodes else 0
        avg_speedup = avg_plain_t / avg_ab_t if avg_ab_t > 0 else float('inf')

        print(f"{depth:<7}{avg_plain_nodes:<14.0f}{avg_ab_nodes:<12.0f}{avg_reduction:<14.2f}{avg_plain_t:<12.4f}{avg_ab_t:<10.4f}{avg_speedup:<8.2f}")

    # Save raw results to CSV for use in charts/report
    with open("benchmark_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
        writer.writeheader()
        writer.writerows(all_results)

    print("\nRaw results written to benchmark_results.csv")
    print("Tip: plot 'depth' vs 'plain_nodes'/'ab_nodes' (log scale) for your report.")


if __name__ == "__main__":
    main()
