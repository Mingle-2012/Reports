import numpy as np
import pandas as pd

file_path = 'data/pwram.csv'
data = pd.read_csv(file_path)

for col in ["HDI", "GGI", "GII", "EPI"]:
    data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())

for col in ["HDI", "GGI", "GII", "EPI"]:
    data[f"p_{col}"] = data[col] / data[col].sum()

n = len(data)
k = -1 / np.log(n)

H = {}
for col in ["HDI", "GGI", "GII", "EPI"]:
    p = data[f"p_{col}"]
    H[col] = k * (p * np.log(p + 1e-10)).sum()

tmp = pd.DataFrame.from_dict(H, orient="index", columns=["H"])
tmp["d"] = 1 - tmp["H"]
tmp["w"] = tmp["d"] / tmp["d"].sum()

weights = tmp["w"].values
data["PWRAM"] = data[["HDI", "GGI", "GII", "EPI"]].values @ weights

dfs = data[["Country", "PWRAM"]].sort_values(by="PWRAM", ascending=False)
print(dfs)