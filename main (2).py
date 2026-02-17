import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# Загрузка данных
# =========================
df = pd.read_csv("results.csv")

grouped = df.groupby("size")

mean_time = grouped["time_sec"].mean()
min_time = grouped["time_sec"].min()
max_time = grouped["time_sec"].max()

mean_swaps = grouped["swaps"].mean()
mean_passes = grouped["passes"].mean()

sizes = mean_time.index.values

# ==========================================================
# 1. Совмещённый график худшего времени и O(c * g(N))
# ==========================================================

# g(N) = N^2 для квадратичных алгоритмов
g = sizes ** 2

# Берём точки только при N > 1000
mask = sizes > 1000
g_large = g[mask]
worst_large = max_time.values[mask]

# Подбираем c так, чтобы O(c*g(N)) была немного выше худшего времени
c = np.max(worst_large / g_large) * 1.05

theoretical = c * g

plt.figure(figsize=(10,6))
plt.plot(sizes, max_time.values, marker='o', label="Худшее время")
plt.plot(sizes, theoretical, linestyle='--', label="O(c · N²)")

plt.xlabel("Размер массива N")
plt.ylabel("Время выполнения (сек)")
plt.title("Худшее время и теоретическая сложность O(N²)")
plt.legend()
plt.grid(True)
plt.savefig("graph_worst_vs_On2.png", dpi=300)
plt.show()

# ==========================================================
# 2. Среднее, лучшее и худшее время
# ==========================================================

plt.figure(figsize=(10,6))
plt.plot(sizes, mean_time.values, marker='o', label="Среднее время")
plt.plot(sizes, min_time.values, marker='o', label="Лучшее время")
plt.plot(sizes, max_time.values, marker='o', label="Худшее время")

plt.xlabel("Размер массива N")
plt.ylabel("Время выполнения (сек)")
plt.title("Среднее, лучшее и худшее время выполнения")
plt.legend()
plt.grid(True)
plt.savefig("graph_time_comparison.png", dpi=300)
plt.show()

# ==========================================================
# 3. Среднее количество обменов
# ==========================================================

plt.figure(figsize=(10,6))
plt.plot(sizes, mean_swaps.values, marker='o')

plt.xlabel("Размер массива N")
plt.ylabel("Среднее количество обменов")
plt.title("Среднее количество операций обмена")
plt.grid(True)
plt.savefig("graph_swaps.png", dpi=300)
plt.show()

# ==========================================================
# 4. Повторные обходы массива
# ==========================================================

plt.figure(figsize=(10,6))
plt.plot(sizes, mean_passes.values, marker='o')

plt.xlabel("Размер массива N")
plt.ylabel("Среднее количество повторных обходов")
plt.title("Повторные прохождения массива")
plt.grid(True)
plt.savefig("graph_passes.png", dpi=300)
plt.show()


