import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

base_dir = "YCSB-throughput"

# サブディレクトリごとの名前と対応するラベル
group_labels = {
    "data_no_monitoring": "w/o Monitoring",
    "data_xdp_interval_1s": "X-Monitor, Interval1s",
    "data_xdp_interval_0_1s": "X-Monitor, Interval0.1s",
    "data_xdp_interval_0_01s": "X-Monitor, Interval0.01s",
    "data_netdata_interval_1s": "Netdata, Interval1s",
    "data_netdata_interval_0_1s": "Netdata, Interval0.1s",
    "data_netdata_interval_0_01s": "Netdata,Interval0.01s"
}

# 各サブディレクトリごとに Throughput を収集
throughput_data = {}

for group, label in group_labels.items():
    dir_path = os.path.join(base_dir, group)
    data = []

    if not os.path.isdir(dir_path):
        print(f"ディレクトリが存在しません: {dir_path}")
        continue

    for filename in sorted(os.listdir(dir_path)):
        file_path = os.path.join(dir_path, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, "r") as f:
            for line in f:
                if "Throughput(ops/sec)" in line:
                    match = re.search(
                        r"Throughput\(ops/sec\),\s*([0-9.]+)", line)
                    if match:
                        throughput = float(match.group(1)) / 1000  # Kops/sec
                        data.append(throughput)
                        break

    throughput_data[label] = data  # ラベルをキーに辞書へ格納

# DataFrame化
# df = pd.DataFrame(dict(throughput_data))  # カラム名にラベルが使われる
# DataFrame化：リスト長が異なっても OK（NaNで埋まる）
df = pd.DataFrame.from_dict(throughput_data, orient='index').transpose()

# 統計出力（X-MonitorとNetdata関連のみ）
for key in df.columns:
    if key.startswith("X-Monitor") or key.startswith("Netdata"):
        mean = np.mean(df[key])
        std = np.std(df[key])
        print(f"{key} mean and SD: {mean:.2f}, {std:.2f}")

# Boxplot作成
boxplot = df.boxplot(patch_artist=True, return_type='dict', grid=False)

# 色設定
colors = ['aliceblue'] + ['royalblue'] * 3 + ['darkorange'] * 3
for box, color in zip(boxplot['boxes'], colors):
    box.set_facecolor(color)

# 中央値線の装飾
for median in boxplot['medians']:
    median.set_color('black')
    median.set_linewidth(2.0)

# 軸・レイアウト
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.ylabel("Throughput (Kops/sec)")
plt.xticks(rotation=45, ha='right')
plt.ylim(2, 4)
plt.tight_layout()
plt.show()
