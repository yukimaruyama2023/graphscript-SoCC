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

# プロット
plt.figure(figsize=(14, 6))
x = np.arange(len(labels))

# 色指定
colors = [
    "#999999",              # no-monitoring
    "#E69F00", "#E69F00", "#E69F00",         # netdata
    "#D55E00", "#D55E00", "#D55E00",         # netdata-priority
    "#0072B2", "#0072B2", "#0072B2"          # xdp
]

plt.bar(x, means, color=colors)

# 下段ラベル（各バーの詳細）
sub_labels = [
    "",         # No-Monitoring
    "1000ms", "100ms", "10ms",                # Netdata
    "1000ms", "100ms", "10ms",                # Netdata-priority
    "1000ms", "100ms", "10ms"                 # X-Monitor
]
plt.xticks(x, sub_labels, fontsize=10)

# 上段グループラベル
group_labels = [
    "No-Monitoring",       # x=0
    "Netdata", "Netdata", "Netdata",                  # x=1~3
    "Netdata with priority", "Netdata-priority", "Netdata-priority",  # x=4~6
    "X-Monitor", "X-Monitor", "X-Monitor"             # x=7~9
]
group_positions = {
    "No-Monitoring": 0,
    "Netdata": np.mean(x[1:4]),
    "Netdata with priority": np.mean(x[4:7]),
    "X-Monitor": np.mean(x[7:10]),
}

for group, xpos in group_positions.items():
    plt.text(xpos, -0.05 * max(means), group, ha='center', va='top',
             fontsize=12, fontweight='bold', transform=plt.gca().transData)

# 軸などの設定
plt.ylabel("Throughput (ops/sec)")
plt.grid(axis='y')
plt.ylim(0, max(means) * 1.1)
plt.tight_layout()
plt.show()
