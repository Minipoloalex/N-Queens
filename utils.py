import pandas as pd
from typing import Callable


def run_tests(
    solve: Callable[[int], float],
    max_board_size: int = 10,
    nr_tests_per_board_size: int = 5,
) -> pd.DataFrame:
    results = {}
    for board_size in range(1, max_board_size + 1):
        board_size_results = []
        print(f"Starting to run tests for board size {board_size}")
        for _ in range(nr_tests_per_board_size):
            time_result = solve(board_size)
            board_size_results.append(time_result)
        results[f"size_{board_size}"] = board_size_results
    return pd.DataFrame(results)
