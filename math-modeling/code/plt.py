import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi


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
print(weights)

developed = data[data["PWRAM"] > 0.8]
developing = data[data["PWRAM"] <= 0.8]

# 绘制合并的雷达图
def plot_combined_radar(developed_data, developing_data):
    categories = ["HDI", "GGI", "GII", "EPI", "PWRAM"]
    
    developed_avg = developed_data[categories].mean()
    developing_avg = developing_data[categories].mean()
    
    # 雷达图的角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    developed_avg = developed_avg.tolist()
    developing_avg = developing_avg.tolist()
    
    # 添加起点，使得图形是闭合的
    developed_avg += developed_avg[:1]
    developing_avg += developing_avg[:1]
    angles += angles[:1]
    
    # 创建一个雷达图
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    # 绘制发达国家的雷达图
    ax.plot(angles, developed_avg, linewidth=2, linestyle='solid', label='Developed Country', color='blue', marker='o')
    
    # 绘制发展中国家的雷达图
    ax.plot(angles, developing_avg, linewidth=2, linestyle='solid', label='Developing Country', color='red', marker='o')
    
    # 设置刻度标签
    ax.set_yticklabels([0.2, 0.4, 0.6, 0.8, 1.0], fontsize=12)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=16)
    
    # 设置标题
    # 显示图例
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.2), fontsize=12)
    
    plt.tight_layout()
    
    plt.show()

# 绘制合并后的雷达图
plot_combined_radar(developed, developing)