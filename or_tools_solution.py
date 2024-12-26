import sys
import time
from ortools.sat.python import cp_model
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class NQueenSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, queens: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__queens = queens
        self.__solution_count = 0
        self.__start_time = time.time()

    @property
    def solution_count(self) -> int:
        return self.__solution_count

    def on_solution_callback(self):
        current_time = time.time()
        print(
            f"Solution {self.__solution_count}, "
            f"time = {current_time - self.__start_time} s"
        )
        self.__solution_count += 1

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

def solve_n_queens(board_size: int, all_solutions: bool, print_information: bool = True) -> None:
    print(board_size, all_solutions)
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
    solver.parameters.enumerate_all_solutions = all_solutions

    solution_printer = NQueenSolutionPrinter(queens) if print_information else None

    start = time.time()
    solver.solve(model, solution_printer)
    total_time = time.time() - start

    # Statistics.
    if print_information:
        print("\nStatistics")
        print(f"  conflicts      : {solver.num_conflicts}")
        print(f"  branches       : {solver.num_branches}")
        print(f"  wall time      : {solver.wall_time} s")
        print(f"  solutions found: {solution_printer.solution_count}")
        print(f"  total time     : {total_time}")

    return total_time

def run_tests(max_board_size: int = 10, nr_tests_per_board_size: int = 5) -> list[list[float]]:
    # solver: callable[[int], float], 
    results = {}
    for board_size in range(1, max_board_size + 1):
        board_size_results = []
        for _ in range(nr_tests_per_board_size):
            # time_result = solver(board_size)
            time_result = solve_n_queens(board_size, all_solutions=True, print_information=False)
            board_size_results.append(time_result)
        results[f"size_{board_size}"] = board_size_results
    return pd.DataFrame(results)

def plot_times(times_taken: pd.DataFrame):
    sns.lineplot(times_taken)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the N Queens problem.")
    parser.add_argument("-n", "--board_size", type=int, default=8, help="Size of the chessboard (default: 8)")
    parser.add_argument("-a", "--all_solutions", action="store_true", help="Show all solutions (default: False)")
    parser.add_argument("-r", "--run_tests", action="store_true", help="Run all tests (default: False)")

    args = parser.parse_args()
    if args.run_tests:
        results = run_tests(15, 5)
        results.to_csv("results.csv", index=None)
        plot_times(results)
        treated_results = results.agg(["mean", "std"], axis=0)
        print(treated_results)

        # Transpose the DataFrame
        df_transposed = treated_results.transpose()

        # Reset index for Seaborn compatibility
        df_transposed.reset_index(inplace=True)
        df_transposed.columns = ['Size', 'Mean', 'Std']  # Rename columns for better plot readability

        # Melt the DataFrame to long format for Seaborn
        df_melted = df_transposed.melt(id_vars='Size', var_name='Metric', value_name='Value')

        # Plot using Seaborn
        sns.lineplot(data=df_melted, x='Size', y='Value', hue='Metric')
        plt.title('Mean and Std for Sizes')
        plt.show()
    else:
        solve_n_queens(args.board_size, args.all_solutions)
