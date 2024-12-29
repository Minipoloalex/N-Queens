import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional

def plot_files(files, title: Optional[str] = None):
    dfs = []
    file_label_column = "Approach"
    for file_label, file in files.items():
        df = pd.read_csv(file)
        df = df.agg(["mean", "std"], axis=0)
        df = df.transpose().reset_index()
        df.columns = ["Size", "Mean", "Std"]
        df[file_label_column] = file_label
        dfs.append(df)

    df = pd.concat(dfs)
    df["Size"] = df["Size"].str[5:]
    sns.lineplot(x='Size', y='Mean', hue='Approach', data=df, marker='o')
    plt.title(title)
    plt.xlabel("Board Size (n x n)")
    plt.ylabel("Average Time Taken (s)")
    plt.show()

all_solutions_files = {
    "Backtracking efficient": "results_backtracking_all_solutions.csv",
    "Backtracking bitwise": "results_bitwise_all_solutions.csv",
    # "OR-Tools": "results_or_tools_all_solutions.csv",
    # "SAT Solver": "results_sat_all_solutions.csv",
}
one_solution_files = {
    "OR-Tools": "results_or_tools_one_solution.csv",
    "SAT Solver": "results_sat_one_solution.csv",
    # "Backtracking efficient": "results_backtracking_one_solution.csv",
    "Backtracking bitwise": "results_bitwise_one_solution.csv",
}

plot_files(all_solutions_files, title="Time taken to find ALL solutions (s)")
plot_files(one_solution_files, title="Time taken to find just ONE solution (s)")
