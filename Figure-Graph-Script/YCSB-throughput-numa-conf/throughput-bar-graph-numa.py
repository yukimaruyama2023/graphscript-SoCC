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

# 描画順序に対応するラベル
labels = ["no-monitoring", "netdata-1000ms", "netdata-100ms", "netdata-10ms",
          "xdp-1000ms", "xdp-100ms", "xdp-10ms"]

# 対応するファイルリスト（no-monitoring は 2 のみ）
file_patterns = {
    "no-monitoring": ["no-monitoring-2.txt"],
    "netdata-1000ms": [f"netdata-{mode}-1000ms.txt"],
    "netdata-100ms": [f"netdata-{mode}-100ms.txt"],
    "netdata-10ms": [f"netdata-{mode}-10ms.txt"],
    "xdp-1000ms": [f"xdp-{mode}-1000ms.txt"],
    "xdp-100ms": [f"xdp-{mode}-100ms.txt"],
    "xdp-10ms": [f"xdp-{mode}-10ms.txt"],
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

# 棒グラフを描画
plt.figure(figsize=(12, 6))
x = np.arange(len(labels))
# 棒の色を指定
colors = [
    "purple",     # no-monitoring
    "orange",   # netdata
    "orange",
    "orange",
    "blue",    # xdp
    "blue",
    "blue"
]
plt.bar(x, means, color=colors)
plt.xticks(x, labels, rotation=45)
plt.ylabel("Throughput (ops/sec)")
plt.tight_layout()
plt.show()
