import matplotlib.pyplot as plt
import numpy as np
import sys

plt.rcParams["font.size"] = 18

max = int(input("input max value of x axis like 30: "))

# ファイル読み込みとソート（ミリ秒単位に変換）
latency1 = np.sort(np.loadtxt(sys.argv[1], delimiter=',', usecols=2) / 1000)
latency2 = np.sort(np.loadtxt(sys.argv[2], delimiter=',', usecols=2) / 1000)
latency3 = np.sort(np.loadtxt(sys.argv[3], delimiter=',', usecols=2) / 1000)

# CDF 計算
p1 = np.arange(len(latency1)) / (len(latency1) - 1)
p2 = np.arange(len(latency2)) / (len(latency2) - 1)
p3 = np.arange(len(latency3)) / (len(latency3) - 1)

# 描画
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(latency1, p1, marker="*", markersize=4, label="X-Monitor")
ax.plot(latency2, p2, marker="o", markersize=4, label="Netdata")
ax.plot(latency3, p3, marker="^", markersize=4, label="Netdata with priority")

# 水平線（90%, 99%）
ax.axhline(y=0.9, xmin=-1, xmax=12, color='black',
           linestyle='--', linewidth=1, dashes=(10, 5))
ax.axhline(y=0.99, xmin=-1, xmax=12, color='black',
           linestyle='--', linewidth=1, dashes=(10, 5))

# 軸範囲とラベル
ax.set_ylim((0.90, 1))
ax.set_xlim((-0.1, max))
ax.set_yticks([0.900, 0.990, 1.000], ["90%", "99%", "100%"])
ax.set_xlabel("latency [ms]")
ax.set_ylabel("percentile")
ax.legend(loc='lower right', labelspacing=0)

fig.tight_layout()
plt.show()
