import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 対象ディレクトリ
log_dir = "./NUMA-LOG"

# 入力（kernel または user）
mode = input("Input: kernel or user: ").strip().lower()
if mode not in ["kernel", "user"]:
    raise ValueError("kernel または user を入力してください。")

# スケジューリングポリシー（rr または fifo）
policy = input("Input scheduling policy (rr or fifo): ").strip().lower()
if policy not in ["rr", "fifo"]:
    raise ValueError("rr または fifo を入力してください。")

# ラベルとファイルマッピング
labels = [
    "No-Monitoring",
    "Netdata-1000ms", "Netdata-100ms", "Netdata-10ms",
    "Netdata-1000ms-priority", "Netdata-100ms-priority", "Netdata-10ms-priority",
    "X-Monitor-1000ms", "X-Monitor-100ms", "X-Monitor-10ms"
]

file_patterns = {
    "No-Monitoring": ["no-monitoring-2.txt"],
    "Netdata-1000ms": [f"netdata-{mode}-1000ms.txt"],
    "Netdata-100ms": [f"netdata-{mode}-100ms.txt"],
    "Netdata-10ms": [f"netdata-{mode}-10ms.txt"],
    "Netdata-1000ms-priority": [f"netdata-{mode}-1000ms-pri-{policy}.txt"],
    "Netdata-100ms-priority": [f"netdata-{mode}-100ms-pri-{policy}.txt"],
    "Netdata-10ms-priority": [f"netdata-{mode}-10ms-pri-{policy}.txt"],
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
    means.append(np.mean(values) if values else 0)
    stds.append(np.std(values) if len(values) > 1 else 0)

# 棒グラフ描画
plt.figure(figsize=(14, 6))
x = np.arange(len(labels))

# 色を指定
# colors = [
#     "purple",     # no-monitoring
#     "orange", "orange", "orange",        # netdata
#     "red", "red", "red",                 # netdata-priority
#     "blue", "blue", "blue"              # xdp
# ]
colors = [
    "#999999",        # no-monitoring
    "#E69F00", "#E69F00", "#E69F00",     # netdata
    "#D55E00", "#D55E00", "#D55E00",     # netdata-priority
    "#0072B2", "#0072B2", "#0072B2"      # xdp
]

plt.bar(x, means, color=colors)
plt.xticks(x, labels, rotation=45)
plt.grid(axis='y')
plt.ylabel("Throughput (ops/sec)")
plt.tight_layout()
plt.show()
