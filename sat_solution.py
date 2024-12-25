import argparse
from pysat.solvers import Glucose42
import numpy as np
import time
import pandas as pd

class QueensSolver:
    n: int
    board: list[list[int]]

    def __init__(self, n: int) -> None:
        self.n = n
        self.__init_variables()

    def __init_variables(self) -> None:
        # Q[i][j] will denote there is a queen on square (i, j)
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]

        var_id = 1
        for r in range(self.n):
            for c in range(self.n):
                self.board[r][c] = var_id
                var_id += 1

    def squares_in_row(self, r: int) -> set:
        return {self.board[r][c] for c in range(self.n)}

    def squares_in_col(self, c: int) -> set:
        return {self.board[r][c] for r in range(self.n)}

    def add_if_in_range(self, s: set, r: int, c: int) -> None:
        if r in range(self.n) and c in range(self.n):
            s.add(self.board[r][c])

    def squares_in_diagonals(self, r: int, c: int) -> set:
        ans = set()
        for i in range(self.n):
            self.add_if_in_range(ans, r + i, c + i)
            self.add_if_in_range(ans, r + i, c - i)
            self.add_if_in_range(ans, r - i, c + i)
            self.add_if_in_range(ans, r - i, c - i)
        return ans

    def squares_attacked(self, r: int, c: int) -> set:
        ans = self.squares_in_row(r)
        ans.update(self.squares_in_col(c))
        ans.update(self.squares_in_diagonals(r, c))
        ans.remove(self.board[r][c])
        return ans

    def print_solution(self, model: list[int]) -> None:
        model_2d = np.reshape(model, (self.n, self.n))
        for row in model_2d:
            print(''.join('Q' if val > 0 else '.' for val in row))

    def solve(self):
        solver = Glucose42()
        for i in range(self.n):
            solver.add_clause(self.squares_in_row(i))
            solver.add_clause(self.squares_in_col(i))
        for r in range(self.n):
            for c in range(self.n):
                for variable in self.squares_attacked(r, c):
                    solver.add_clause([-self.board[r][c], -variable])   # self.board[r][c] -> -variable
        start = time.time()
        has_solution = solver.solve()
        total_time = time.time() - start

        if has_solution:
            model = solver.get_model()
            print(model)
            self.print_solution(model)

        return total_time

def run_tests(max_board_size: int, number_of_times: int) -> pd.DataFrame:
    pass
    # results = {}
    # for board_size in range(1, max_board_size + 1):
    #     for _ in range(number_of_times):
    #         queens_solver = QueensSolver(board_size)
    #         time_taken = queens_solver.solve()
    #         results[board_size] = time_taken
    # return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the N Queens problem.")
    parser.add_argument("-n", "--board_size", type=int, default=8, help="Size of the chessboard (default: 8)")
    parser.add_argument("-r", "--run_tests", action="store_true", help="Run all tests (default: False). If set ignores other parameters")

    args = parser.parse_args()
    if args.run_tests:
        results = run_tests(max_board_size = 15, number_of_times = 5)
    else:
        queens_solver = QueensSolver(args.board_size)
        queens_solver.solve()
