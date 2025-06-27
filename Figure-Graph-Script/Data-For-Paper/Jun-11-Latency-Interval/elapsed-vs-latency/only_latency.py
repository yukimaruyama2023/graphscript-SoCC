import numpy as np
import matplotlib.pyplot as plt
import sys

micron_unicode = '\u03BC'
METRIC_NAME = "system"
METRICS_UNIT = "ms"

max = int(input("input max value of vertical axis: "))

# データの読み込み
data = np.loadtxt(sys.argv[1], delimiter=",", skiprows=0, usecols=(1, 2))
data = np.transpose(data)

TIMESEC_COL = 0
LATENCY_COL = 1

plt.rcParams["font.size"] = 23

fig, ax1 = plt.subplots(figsize=(9.5, 8))

# パーセンタイルの計算
latency = data[LATENCY_COL]
percentiles = np.percentile(latency, [50, 90, 99])
print(f"50th percentile latency: {percentiles[0]} us")
print(f"90th percentile latency: {percentiles[1]} us")
print(f"99th percentile latency: {percentiles[2]} us")

# 経過時間と遅延時間の準備
elapsed = data[TIMESEC_COL] - data[TIMESEC_COL][0]
latency = data[LATENCY_COL] / 1000  # msに変換

# グラフの描画
# ax1.plot(elapsed, latency, label="Monitoring Latency",
#          color="orange", marker="^")
ax1.plot(elapsed, latency, label="Monitoring Latency",
         color="orange", marker="^")

# 軸ラベルと範囲の設定
ax1.set_xlabel("Elapsed Time [s]")
ax1.set_ylabel("Latency [ms]")
ax1.set_ylim(0, max)

ax1.set_xlim(-0.5, 10.5)
ax1.set_xticks(np.arange(0, 11, 1))

# グリッドのカスタマイズ（横線だけ表示）
ax1.grid(axis='y')  # y軸方向のグリッドを表示

plt.subplots_adjust(right=0.98)

# 凡例の設定
handler, label = ax1.get_legend_handles_labels()
ax1.legend(handler, label, loc="upper right", fontsize="small")
ax1.legend(handler, label, loc="upper center",
           bbox_to_anchor=(0.5, 1.15), fontsize=25, ncol=1)

for spine in ax1.spines.values():
    spine.set_linewidth(1.5)
# グラフの表示
plt.show()
