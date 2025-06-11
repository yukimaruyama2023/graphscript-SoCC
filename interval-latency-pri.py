#!/usr/bin/python3

from bar_graph_util import *

# 測定データ関係のパラメータ
interval_list = [1000, 100, 10]
dir = "Latency-vs-Interval-numa-conf-pri"

# 入力受け取り
indicator = int(input("Enter 0 or 1 which specify kernel or user: ").strip())
priority_monitoring = int(
    input("Use priority monitoring? (0: no, 1: yes): ").strip())

# 生データでレイテンシが何列目にあるか
latency_column = 2

# グラフ関連のパラメータ
graph_time_unit = "us"
use_log_scale = True

# ファイルの読み込み
if indicator == 0:
    # kernel モードは今まで通り 2系列
    filenames = {
        "Netdata": [
            f"{dir}/netdata-kernel-interval-1000ms.csv",
            f"{dir}/netdata-kernel-interval-100ms.csv",
            f"{dir}/netdata-kernel-interval-10ms.csv"
        ],
        "XDP": [
            f"{dir}/xdp-kernel-interval-1000ms.csv",
            f"{dir}/xdp-kernel-interval-100ms.csv",
            f"{dir}/xdp-kernel-interval-10ms.csv"
        ]
    }

elif indicator == 1:
    if priority_monitoring:
        filenames = {
            "Netdata": [
                f"{dir}/netdata-user-interval-1000ms.csv",
                f"{dir}/netdata-user-interval-100ms.csv",
                f"{dir}/netdata-user-interval-10ms.csv"
            ],
            "Priority Netdata": [
                f"{dir}/netdata-user-interval-1000ms-fifo.csv",
                f"{dir}/netdata-user-interval-100ms-fifo.csv",
                f"{dir}/netdata-user-interval-10ms-fifo.csv"
            ],
            "XDP": [
                f"{dir}/xdp-user-interval-1000ms.csv",
                f"{dir}/xdp-user-interval-100ms.csv",
                f"{dir}/xdp-user-interval-10ms.csv"
            ]
        }
    else:
        filenames = {
            "Netdata": [
                f"{dir}/netdata-user-interval-1000ms.csv",
                f"{dir}/netdata-user-interval-100ms.csv",
                f"{dir}/netdata-user-interval-10ms.csv"
            ],
            "XDP": [
                f"{dir}/xdp-user-interval-1000ms.csv",
                f"{dir}/xdp-user-interval-100ms.csv",
                f"{dir}/xdp-user-interval-10ms.csv"
            ]
        }
else:
    raise ValueError("Invalid indicator (must be 0 or 1)")

# メトリクス選択
print("Select metric to visualize:")
print("average  : 0")
print("90%ile   : 1")
print("99%ile   : 2")
print("99.9%ile : 3")
print("max      : 4")
metric = int(input("Enter: "))

# 各手法に対して、該当するメトリクスを抽出
label_list = []
series_list = []

for label, file_list in filenames.items():
    raw_data = load_data(file_list, latency_column)

    if metric == 0:
        data = calc_average(raw_data)
    elif metric == 1:
        data = calc_90_percentile(raw_data)
    elif metric == 2:
        data = calc_99_percentile(raw_data)
    elif metric == 3:
        data = calc_999_percentile(raw_data)
    elif metric == 4:
        data = calc_max_latency(raw_data)
    else:
        raise ValueError("Invalid metric")

    label_list.append(label)
    series_list.append(data)
    print(f"{label}: {[f'{x:.3f}' for x in data]}")

# 棒グラフ描画
show_bar_graph_multi(series_list, interval_list, label_list,
                     xlabel="Sample Interval (ms)",
                     unit=graph_time_unit,
                     log_scale=use_log_scale)
