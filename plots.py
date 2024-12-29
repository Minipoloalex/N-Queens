import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional
import os

def plot_files(files, title: Optional[str] = None):
    dfs = []
    file_label_column = "Approach"
    for file_label, file in files.items():
        df = pd.read_csv(os.path.join("results", file))
        df = df.agg(["mean", "std"], axis=0)
        df = df.transpose().reset_index()
        df.columns = ["Size", "Mean", "Std"]
        df[file_label_column] = file_label
        dfs.append(df)

    df = pd.concat(dfs)
    df["Size"] = df["Size"].str[5:].astype(int)
    sns.lineplot(x='Size', y='Mean', hue='Approach', data=df, marker='o')
    plt.title(title)
    plt.xlabel("Board Size (n x n)")
    plt.ylabel("Average Time Taken (s)")
    plt.show()

all_solutions_files = {
    "Backtracking Normal": "results_backtracking_all_solutions.csv",
    "Backtracking Bitwise": "results_bitwise_all_solutions.csv",
    "OR-Tools": "results_or_tools_all_solutions.csv",
    "Glucose 4.2 SAT Solver": "results_sat_all_solutions.csv",
}
one_solution_files = {
    "Backtracking Normal": "results_backtracking_one_solution.csv",
    "Backtracking Bitwise": "results_bitwise_one_solution.csv",
    "OR-Tools": "results_or_tools_one_solution.csv",
    "Glucose 4.2 SAT Solver": "results_sat_one_solution.csv",
}

plot_files(all_solutions_files, title="Time taken to find ALL solutions")
plot_files(one_solution_files, title="Time taken to find just ONE solution")
