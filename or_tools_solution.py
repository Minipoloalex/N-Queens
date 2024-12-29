import sys
import time
from ortools.sat.python import cp_model
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils import run_tests


class NQueenSolutionHandler(cp_model.CpSolverSolutionCallback):
    """Print possible solutions for the N-Queens problem"""

    def __init__(self, queens: list[cp_model.IntVar], find_all_solutions: bool, print_information: bool):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__queens = queens
        self.find_all_solutions = find_all_solutions
        self.print_information = print_information
        self.__solution_count = 0
        self.__start_time = time.time()

    @property
    def solution_count(self) -> int:
        return self.__solution_count

    def on_solution_callback(self):
        self.__solution_count += 1
        if self.print_information:  # Print solution and information
            current_time = time.time()
            print(
                f"Solution {self.__solution_count}, "
                f"time = {current_time - self.__start_time} s"
            )

            all_queens = range(len(self.__queens))
            for i in all_queens:
                for j in all_queens:
                    if self.value(self.__queens[j]) == i:
                        # There is a queen in column j, row i.
                        print("Q", end=" ")
                    else:
                        print("_", end=" ")
                print()
            print()

        if not self.find_all_solutions:
            # Make sure it stops trying to find solutions after finding one
            self.stop_search()

def solve_n_queens(board_size: int, all_solutions: bool, print_solutions: bool, print_information: bool = True) -> float:
    # Creates the solver
    model = cp_model.CpModel()

    # Creates the variables
    # There are `board_size` number of variables, one for a queen in each column
    # of the board. The value of each variable is the row that the queen is in
    queens = [model.new_int_var(0, board_size - 1, f"x_{i}") for i in range(board_size)]

    # Creates the constraints
    # All rows must be different
    model.add_all_different(queens)

    # No two queens can be on the same diagonal
    model.add_all_different(queens[i] + i for i in range(board_size))
    model.add_all_different(queens[i] - i for i in range(board_size))

    # Solve the model
    solver = cp_model.CpSolver()
    # By itself, this does not enforce that the solver will stop after finding one solution
    solver.parameters.enumerate_all_solutions = all_solutions

    solution_handler = NQueenSolutionHandler(queens, all_solutions, print_solutions)

    start = time.time()
    solver.solve(model, solution_handler)
    total_time = time.time() - start

    # Statistics
    if print_information:
        print("\nStatistics")
        print(f"  conflicts      : {solver.num_conflicts}")
        print(f"  branches       : {solver.num_branches}")
        print(f"  wall time      : {solver.wall_time} s")
        print(f"  solutions found: {solution_handler.solution_count}")
        print(f"  total time     : {total_time}")
    else:
        print(f"Solutions found: {solution_handler.solution_count}")
    return total_time


def run_timing_tests(max_board_size: int, nr_tests_per_board_size: int, find_all_solutions: bool) -> pd.DataFrame:
    def solve(board_size: int) -> float:
        return solve_n_queens(board_size, all_solutions=find_all_solutions, print_solutions=False, print_information=False)

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

        results.to_csv(f"results_or_tools_{args.run_tests}.csv", index=None)

    else:
        solve_n_queens(args.board_size, args.all_solutions, args.print_solutions, print_information=True)
