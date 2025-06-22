import os
import re
import numpy as np
import matplotlib.pyplot as plt

# 対象ディレクトリ
log_dir = "./NUMA-LOG"

# 入力（kernel または user）
mode = input("Input: kernel or user: ").strip().lower()
if mode not in ["kernel", "user"]:
    raise ValueError("Inpurt user or kernel")

# 描画順序に対応するラベル
labels = ["No-Monitoring", "Netdata-1000ms", "Netdata-100ms", "Netdata-10ms",
          "X-Monitor-1000ms", "X-Monitor-100ms", "X-Monitor-10ms"]

# ファイル対応表
file_patterns = {
    "No-Monitoring": ["no-monitoring-2.txt"],
    "Netdata-1000ms": [f"netdata-{mode}-1000ms.txt"],
    "Netdata-100ms": [f"netdata-{mode}-100ms.txt"],
    "Netdata-10ms": [f"netdata-{mode}-10ms.txt"],
    "X-Monitor-1000ms": [f"xdp-{mode}-1000ms.txt"],
    "X-Monitor-100ms": [f"xdp-{mode}-100ms.txt"],
    "X-Monitor-10ms": [f"xdp-{mode}-10ms.txt"],
}

# Throughput抽出パターン
throughput_pattern = re.compile(
    r"\[OVERALL\], Throughput\(ops/sec\), ([\d.]+)")

# データ格納用
data = {label: [] for label in labels}

# スループット抽出
for label, files in file_patterns.items():
    for fname in files:
        path = os.path.join(log_dir, fname)
        if not os.path.exists(path):
            print(f"[SKIP] {path} は存在しません")
            continue
        with open(path, 'r') as f:
            for line in f:
                match = throughput_pattern.search(line)
                if match:
                    value = float(match.group(1))
                    data[label].append(value)
                    print(f"[OK] {fname}: {value}")
                    break
            else:
                print(f"[NG] {fname}: throughput 行が見つかりません")

# 平均と標準偏差を計算
means = []
stds = []
for label in labels:
    values = data[label]
    means.append(np.mean(values) / 1000 if values else 0)
    stds.append(np.std(values) / 1000 if len(values) > 1 else 0)

# プロット開始
plt.figure(figsize=(12, 6))
x = np.arange(len(labels))

# 色設定
# colors = [
#     "#999999",  # no-monitoring
#     "#e69f00", "#e69f00", "#e69f00",  # netdata
#     "#0072b2", "#0072b2", "#0072b2",  # x-monitor
# ]
colors = [
    "#999999",  # No-Monitoring
    "coral", "coral", "coral",  # Netdata
    "#1f77b4", "#1f77b4", "#1f77b4",  # X-Monitor
]

# 棒グラフ
plt.bar(x, means, color=colors, width=0.7)

# 下段ラベル（各バーの詳細）
sub_labels = ["", "1000ms", "100ms", "10ms", "1000ms", "100ms", "10ms"]
plt.xticks(x, sub_labels, fontsize=15)

# 上段ラベル（グループラベル）
group_labels = ["No-Monitoring", "Netdata", "Netdata",
                "Netdata", "X-Monitor", "X-Monitor", "X-Monitor"]
for i, label in enumerate(group_labels):
    # 中央に1回だけ表示
    if i in [0, 2, 5]:  # 中央バーを代表として使う
        group = group_labels[i]
        # 範囲の平均位置を計算（Netdata: i=2 → x=[1,2,3] → 中央=2）
        if group == "Netdata":
            xpos = np.mean(x[1:4])
        elif group == "X-Monitor":
            xpos = np.mean(x[4:7])
        elif group == "No-Monitoring":
            xpos = x[0]
        plt.text(xpos, -0.1 * max(means), group, ha='center', va='top',
                 fontsize=25, transform=plt.gca().transData)

# 軸などの設定
plt.ylabel("Throughput (K ops/sec)", fontsize=25)
plt.grid(axis='y')
plt.ylim(0, max(means) * 1.1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.tight_layout()
plt.show()
