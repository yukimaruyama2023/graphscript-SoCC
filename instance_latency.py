#!/usr/bin/python3

from bar_graph_util import *

# 測定データ関係のパラメータ
# インスタンスの個数のリスト
instance_num_list = [1, 5, 10]

indicator = int(input("Enter 0 or 1 which specify kernel or user: "))
# 従来手法のデータのファイル名
if indicator == 0:
    filename_conventional = [
        "Latency-vs-Instances/netdata-kernel-interval0.01-instance1.csv",
        "Latency-vs-Instances/netdata-kernel-interval0.01-instance5.csv",
        "Latency-vs-Instances/netdata-kernel-interval0.01-instance10.csv"
    ]
# 提案手法のデータのファイル名
    filename_proposal = [
        "Latency-vs-Instances/xdp-kernel-interval0.01-instance1.csv",
        "Latency-vs-Instances/xdp-kernel-interval0.01-instance5.csv",
        "Latency-vs-Instances/xdp-kernel-interval0.01-instance10.csv"
    ]
elif indicator == 1:
    filename_conventional = [
        "Latency-vs-Instances/netdata-user-interval0.01-instance1.csv",
        "Latency-vs-Instances/netdata-user-interval0.01-instance5.csv",
        "Latency-vs-Instances/netdata-user-interval0.01-instance10.csv"
    ]
# 提案手法のデータのファイル名
    filename_proposal = [
        "Latency-vs-Instances/xdp-user-interval0.01-instance1.csv",
        "Latency-vs-Instances/xdp-user-interval0.01-instance5.csv",
        "Latency-vs-Instances/xdp-user-interval0.01-instance10.csv"
    ]
else:
    print("The number you entered is not moderate")


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
    latency_90_conventional = calc_90_percentile(raw_latency_conventional)
    latency_90_proposal = calc_90_percentile(raw_latency_proposal)
    latency_99_conventional = calc_99_percentile(raw_latency_conventional)
    latency_99_proposal = calc_99_percentile(raw_latency_proposal)
    latency_999_conventional = calc_999_percentile(raw_latency_conventional)
    latency_999_proposal = calc_999_percentile(raw_latency_proposal)

    print("50%ile   : 0")
    print("90%ile   : 1")
    print("99%ile   : 2")
    print("99.9%ile : 3")
    input = int(input("Enter: "))

    if input == 0:
        conventional = average_latency_conventional
        proposal = average_latency_proposal
        print(conventional)
        print(proposal)
    elif input == 1:
        conventional = latency_90_conventional
        proposal = latency_90_proposal
        print(conventional)
        print(proposal)
    elif input == 2:
        conventional = latency_99_conventional
        proposal = latency_99_proposal
        print(conventional)
        print(proposal)
    elif input == 3:
        conventional = latency_999_conventional
        proposal = latency_999_proposal
        print(conventional)
        print(proposal)
    else:
        print("Input moderate number")

    show_bar_graph(conventional, proposal,
                   instance_num_list, "Redis Instances", graph_time_unit, log_scale=use_log_scale)
