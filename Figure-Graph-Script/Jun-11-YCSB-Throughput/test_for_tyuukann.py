import os
import re
import numpy as np
import matplotlib.pyplot as plt

# 対象ディレクトリ
log_dir = "./NUMA-LOG"

# 入力（kernel または user）
mode = input("Input: kernel or user: ").strip().lower()
if mode not in ["kernel", "user"]:
    raise ValueError("kernel または user を入力してください。")

# 対象ラベルと対応ファイルのみ（3つだけ）
labels = ["No-Monitoring", "Netdata-10ms", "X-Monitor-10ms"]
file_patterns = {
    "No-Monitoring": ["no-monitoring-2.txt"],
    "Netdata-10ms": [f"netdata-{mode}-10ms.txt"],
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
plt.figure(figsize=(8, 5))
x = np.arange(len(labels))

# 色（灰色, オレンジ, 青）
colors = ["#999999", "#E69F00", "#0072B2"]

# 棒グラフ描画
plt.bar(x, means, color=colors)
plt.xticks(x, labels, fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("Throughput (K ops/sec)", fontsize=16)
plt.tight_layout()
plt.show()
