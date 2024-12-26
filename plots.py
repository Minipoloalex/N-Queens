import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

result_files = {
    # "Backtracking inefficient": "results_inefficient_backtracking",
    "Backtracking efficient": "results_backtracking_all-solutions.csv",
    "Backtracking bitwise": "results_bitwise_all-solutions.csv",
    # "OR-Tools": "results_or_tools.csv",
    # "SAT Solver": "results_sat.csv",
}

dfs = []
file_label_column = "Approach"
for file_label, file in result_files.items():
    df = pd.read_csv(file)
    df = df.agg(["mean", "std"], axis=0)
    df = df.transpose().reset_index()
    df.columns = ["Size", "Mean", "Std"]
    df[file_label_column] = file_label
    dfs.append(df)

df = pd.concat(dfs)
df["Size"] = df["Size"].str[5:]
sns.lineplot(x='Size', y='Mean', hue='Approach', data=df, marker='o')
plt.xlabel("Board Size (n x n)")
plt.ylabel("Average Time Taken (s)")
plt.show()
