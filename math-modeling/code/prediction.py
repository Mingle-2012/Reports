import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt

# 从CSV文件中读取数据
# 请将 'plastic_production.csv' 替换为实际的文件路径
file_path = 'code/data/global-plastics-production.csv'
df = pd.read_csv(file_path)

# 确保列名正确，重命名为统一格式（如果有需要）
df.rename(columns={'Year': 'Year', 'Annual plastic production between 1950 and 2019': 'PlasticProduction'}, inplace=True)

# 检查数据
print(df.head())  # 打印前几行，确认数据是否正确读取

# 提取塑料生产数据
years = df['Year']
production = df['PlasticProduction']

# 创建二次指数平滑模型
model = ExponentialSmoothing(production, trend='add', seasonal=None, damped_trend=False)

# 拟合模型
model_fit = model.fit()

# 预测未来5年的数据
future_years = [df['Year'].iloc[-1] + i for i in range(1, 2)]  # 从最后一年开始预测
forecast = model_fit.forecast(len(future_years))  # 获取预测值

# 创建预测数据DataFrame
forecast_df = pd.DataFrame({'Year': future_years, 'Forecast': forecast})

# 合并历史数据和预测数据
full_df = pd.concat([df, forecast_df], ignore_index=True)

waste_ratio = 0.42

# 计算塑料废物量
df['PlasticWaste'] = df['PlasticProduction'] * waste_ratio

# 绘制实际值和预测值
plt.figure(figsize=(10, 6))
plt.plot(df['Year'], df['PlasticProduction'], label='Plastic Production', linewidth=3)
# plt.plot(forecast_df['Year'], forecast_df['Forecast'], label='Forecast', marker='x', linestyle='--', color='red', linewidth=3)
plt.plot(df['Year'], df['PlasticWaste'], label='Single-use Plastic Production', linewidth=2.5)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.title('Plastic Production', fontsize=20)
plt.xlabel('Year', fontsize=16)
plt.ylabel('Annual Plastic Production (Million Metric Tons)', fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.tight_layout()
plt.show()
