#!/usr/bin/python3

from bar_graph_util import *

# 測定データ関係のパラメータ
# インターバルのリスト
interval_list = [1000, 100, 10]

indicator = int(input("Enter 0 or 1 which specify kernel or user: "))
# 従来手法のデータのファイル名
#
# dir = "Latency-vs-Interval-numa-conf"

# kernel metrics を取得の時 go.d.plugin を切ってある
dir = "Jun-11-Latency-interval"
if indicator == 0:
    filename_conventional = [
        f"{dir}/netdata-kernel-Interval-1000ms.csv",
        f"{dir}/netdata-kernel-Interval-100ms.csv",
        f"{dir}/netdata-kernel-Interval-10ms.csv"
    ]
    # 提案手法のデータのファイル名
    filename_proposal = [
        f"{dir}/xdp-kernel-Interval-1000ms.csv",
        f"{dir}/xdp-kernel-Interval-100ms.csv",
        f"{dir}/xdp-kernel-Interval-10ms.csv"
    ]
elif indicator == 1:
    filename_conventional = [
        f"{dir}/netdata-user-Interval-1000ms.csv",
        f"{dir}/netdata-user-Interval-100ms.csv",
        f"{dir}/netdata-user-Interval-10ms.csv"
    ]
    # 提案手法のデータのファイル名
    filename_proposal = [
        f"{dir}/xdp-user-Interval-1000ms.csv",
        f"{dir}/xdp-user-Interval-100ms.csv",
        f"{dir}/xdp-user-Interval-10ms.csv"
    ]
else:
    print("The number you entered is not moderate.")


# 生データでレイテンシが何列目にあるか
latency_column = 2

# グラフ関連のパラメータ
# グラフで表示する時間の単位 (ns, us, ms, s)
graph_time_unit = "us"
# log-scaleで表示するか
use_log_scale = True

if __name__ == "__main__":
    raw_latency_conventional = load_data(filename_conventional, latency_column)
    raw_latency_proposal = load_data(filename_proposal, latency_column)

    average_latency_conventional = calc_average(raw_latency_conventional)
    average_latency_proposal = calc_average(raw_latency_proposal)
    latency_90_conventional = calc_90_percentile(
        raw_latency_conventional)  # 追加
    latency_90_proposal = calc_90_percentile(raw_latency_proposal)
    latency_99_conventional = calc_99_percentile(raw_latency_conventional)
    latency_99_proposal = calc_99_percentile(raw_latency_proposal)
    latency_999_conventional = calc_999_percentile(raw_latency_conventional)
    latency_999_proposal = calc_999_percentile(raw_latency_proposal)
    latency_max_conventional = calc_max_latency(raw_latency_conventional)
    latency_max_proposal = calc_max_latency(raw_latency_proposal)

    print("average  : 0")
    print("90%ile   : 1")
    print("99%ile   : 2")
    print("99.9%ile : 3")
    print("max      : 4")
    input = int(input("Enter: "))

    if input == 0:
        conventional = average_latency_conventional
        proposal = average_latency_proposal
    elif input == 1:
        conventional = latency_90_conventional
        proposal = latency_90_proposal
    elif input == 2:
        conventional = latency_99_conventional
        proposal = latency_99_proposal
    elif input == 3:
        conventional = latency_999_conventional
        proposal = latency_999_proposal
    elif input == 4:
        conventional = latency_max_conventional
        proposal = latency_max_proposal
    else:
        raise ValueError("Invalid input")

    print([f"{x:.3f}" for x in conventional])
    print([f"{x:.3f}" for x in proposal])

    # 10ms のデータのみ取り出す（インデックス 2）
    latency_conventional_10ms = raw_latency_conventional[2]
    latency_proposal_10ms = raw_latency_proposal[2]

    print(f"[10ms Only] Netdata min: {min(latency_conventional_10ms) / 1000:.3f} ms, "
          f"max: {max(latency_conventional_10ms) / 1000:.3f} ms")
    print(f"[10ms Only] XDP     min: {min(latency_proposal_10ms) / 1000:.3f} ms, "
          f"max: {max(latency_proposal_10ms) / 1000:.3f} ms")
    show_bar_graph(conventional, proposal,
                   interval_list, "Sample Interval (ms)", graph_time_unit, log_scale=use_log_scale)
