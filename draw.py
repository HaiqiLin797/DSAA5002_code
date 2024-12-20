import matplotlib.pyplot as plt

# 数据
x = list(range(12))
y = [63.7, None, 74.2, 71.7, 74.1, 74.2, 73.7, 74.7, 74.8, 74.8, 72.6, 72.4]

# 绘制图形
plt.figure(figsize=(10, 6))

# 绘制数据曲线，跳过 None 值
for i in range(1, len(y)):
    if y[i] is not None:
        plt.plot(i, y[i], 'bo-', label='Performance' if i == 2 else "")

# 绘制 baseline 的水平线
plt.axhline(y[0], color='r', linestyle='--', label='Baseline')

# 添加标签和标题
plt.title("Performance Comparison with Baseline")
plt.xlabel("Data Point Index")
plt.ylabel("Accuracy")
plt.legend()

# 显示图形
plt.show()