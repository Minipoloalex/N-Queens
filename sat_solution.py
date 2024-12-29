import argparse
from pysat.solvers import Glucose42
import numpy as np
import time
import pandas as pd
from utils import run_tests

class QueensSolver:
    n: int
    board: list[list[int]]

    def __init__(self, n: int, find_all_solutions: bool, print_solutions: bool) -> None:
        self.n = n
        self.find_all_solutions = find_all_solutions
        self.print_solutions = print_solutions
        self.solution_count = 0
        self.__init_variables()

    def __init_variables(self) -> None:
        # Q[i][j] will denote there is a queen on square (i, j)

        # Setup the variable ids
        self.board = [[r * self.n + c + 1 for c in range(self.n)] for r in range(self.n)]

        # For example, for n = 4:
        # board = [
        #     [1, 2, 3, 4],
        #     [5, 6, 7, 8],
        #     [9, 10, 11, 12],
        #     [13, 14, 15, 16]
        # ]

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

    def handle_solution(self, model: list[int]) -> None:
        self.solution_count += 1
        if self.print_solutions:
            self.print_solution(model)

    def print_solution(self, model: list[int]) -> None:
        model_2d = np.reshape(model, (self.n, self.n))
        print(f"Solution {self.solution_count}")
        for row in model_2d:
            print(''.join('Q' if val > 0 else '.' for val in row))
        print()

    def solve(self):
        solver = Glucose42()
        for i in range(self.n):
            solver.add_clause(self.squares_in_row(i))   # a row must have a queen
            solver.add_clause(self.squares_in_col(i))   # a column must have a queen

        for r in range(self.n):
            for c in range(self.n):
                for variable in self.squares_attacked(r, c):
                    # A queen at (r, c) makes it so all 
                    # attacked variables must be false
                    # self.board[r][c] -> -variable
                    solver.add_clause([-self.board[r][c], -variable])

        if self.find_all_solutions: # Find all valid solutions
            start = time.time()
            for model in solver.enum_models():
                self.handle_solution(model)
            total_time = time.time() - start
        else:
            start = time.time()
            has_solution = solver.solve()   # Find just one solution
            if has_solution:
                model = solver.get_model()
                self.handle_solution(model)

            total_time = time.time() - start

        print(f"Found {self.solution_count} solution(s) for a board size of {self.n}")
        return total_time


def run_timing_tests(max_board_size: int, nr_tests_per_board_size: int, find_all_solutions: bool) -> pd.DataFrame:
    def solve(board_size: int) -> float:
        return QueensSolver(board_size).solve()
    return run_tests(solve, max_board_size, nr_tests_per_board_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the N Queens problem.")
    parser.add_argument("--board_size", type=int, default=8, help="Size of the chessboard (default: 8)")
    parser.add_argument("--all_solutions", action="store_true", help="Find all solutions (default: False)")
    parser.add_argument("--print_solutions", action="store_true", help="Show solutions found (default: False)")
    parser.add_argument("--run_tests", choices=["false", "all_solutions", "one_solution"], default="false", help="Run all tests (default: False)")

    MAX_BOARD_SIZE = 15
    NR_TESTS_PER_BOARD_SIZE = 5
    args = parser.parse_args()

    if args.run_tests != "false":
        if args.run_tests == "all_solutions":
            results = run_timing_tests(MAX_BOARD_SIZE, NR_TESTS_PER_BOARD_SIZE, find_all_solutions=True)
        elif args.run_tests == "one_solution":
            results = run_timing_tests(MAX_BOARD_SIZE, NR_TESTS_PER_BOARD_SIZE, find_all_solutions=False)

        results.to_csv(f"results_sat_{args.run_tests}.csv", index=None)

    else:
        queens_solver = QueensSolver(args.board_size, args.all_solutions, args.print_solutions)
        queens_solver.solve()
