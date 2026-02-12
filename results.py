import os
import pandas as pd

folder = config_dic["results_folder"]

files = [f for f in os.listdir(folder) if f.endswith(".csv")]

dfs = []

for file in files:
    df = pd.read_csv(os.path.join(folder, file))
    df["round"] = file.replace(".csv", "")
    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)


df_pivot = df_all.pivot_table(
    index="technology",
    columns="round",
    values="TOTAL_INCOMES"
)
