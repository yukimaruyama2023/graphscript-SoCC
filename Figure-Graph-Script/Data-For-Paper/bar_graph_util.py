import numpy as np
import matplotlib.pyplot as plt
from typing import List


"""
生データ(csv)をロードする

Parameters:
  filename_list: 生データのファイル名のリスト
  latency_column: レイテンシが何列目に書かれているか

Returns:
  List[np.ndarray]: レイテンシの配列のリスト
"""


def load_data(filename_list: List[str], latency_column: int) -> List[np.ndarray]:
    latency_data_list = []
    for filename in filename_list:
        data = np.loadtxt(filename, delimiter=",", usecols=latency_column)
        data = np.transpose(data)
        latency_data_list.append(data)
    return latency_data_list


"""
配列の値の平均を求める

Parameters:
  raw_latency_list: レイテンシの配列のリスト

Returns:
  List[float]: 平均値のリスト
"""


def calc_average(raw_latency_list: List[np.ndarray]) -> List[float]:
    average_list = []
    for raw_latency in raw_latency_list:
        average = np.average(raw_latency)
        average_list.append(average)
    return average_list


def calc_90_percentile(raw_latency_list: List[np.ndarray]) -> List[float]:
    percentile_90_list = []
    for raw_latency in raw_latency_list:
        percentile_90 = np.percentile(raw_latency, 90)
        percentile_90_list.append(percentile_90)
    return percentile_90_list


def calc_99_percentile(raw_latency_list: List[np.ndarray]) -> List[float]:
    percentile_99_list = []
    for raw_latency in raw_latency_list:
        percentile_99 = np.percentile(raw_latency, 99)
        percentile_99_list.append(percentile_99)
    return percentile_99_list


def calc_999_percentile(raw_latency_list: List[np.ndarray]) -> List[float]:
    percentile_999_list = []
    for raw_latency in raw_latency_list:
        percentile_999 = np.percentile(raw_latency, 99.9)
        percentile_999_list.append(percentile_999)
    return percentile_999_list


def calc_max_latency(raw_latency_list: List[np.ndarray]) -> List[float]:
    max_latency_list = []
    for raw_latency in raw_latency_list:
        max_latency = np.max(raw_latency)
        max_latency_list.append(max_latency)
    return max_latency_list


"""
棒グラフを表示する

Parameters:
  conventional: 従来手法の平均値の配列
  proposal: 提案手法の平均値の配列
  x_values: x軸のパラメータの値（e.g. Redisインスタンスの個数 [1, 5, 10]）
  x_label: x軸のラベル
  time_unit: レイテンシの単位
  log_scale: レイテンシを対数軸で表示するか
"""

plt.rcParams["font.size"] = 18

fig, ax = plt.subplots(figsize=(7, 6))  # デフォルトサイズを拡大
# fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.2)


def show_bar_graph(conventional, proposal, x_values, x_label, time_unit="us", log_scale=False):
    # グラフのサイズを設定
    fig, ax = plt.subplots(figsize=(7, 6))  # サイズを統一

    # x軸のインデックスを設定
    x_axis = list(range(len(x_values)))

    # 棒グラフを描画 (ax に直接描画)
    ax.bar(x_axis, conventional, align="edge", width=-
           0.2, label="Netdata", color="#1f77b4")
    ax.bar(x_axis, proposal, align="edge", width=0.2,
           label="X-Monitor", color="coral")

    # 軸ラベルと目盛りの設定
    ax.set_xticks(x_axis)
    ax.set_xticklabels(x_values)
    ax.set_xlabel(x_label, fontsize=16, labelpad=10)
    ax.set_ylabel(f"Latency ({time_unit})", fontsize=16, labelpad=10)
    ax.grid(axis='y')

    # 対数スケールの設定
    if log_scale:
        ax.set_yscale("log")

    # 凡例の設定
    # ax.legend(fontsize=14, loc="best")
    # ax.legend(loc='upper center', bbox_to_anchor(0.5, 1.15), ncol=3)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)

    # レイアウト調整
    fig.tight_layout()

    # グラフを表示
    plt.show()


def show_bar_graph_multi(data_series_list, x_labels, legends,
                         xlabel="", unit="", log_scale=False):
    x = np.arange(len(x_labels))
    total_width = 0.8
    num_series = len(data_series_list)
    bar_width = total_width / num_series

    # グラフのサイズを統一
    fig, ax = plt.subplots(figsize=(7, 6))

    for i, data in enumerate(data_series_list):
        offset = (i - num_series / 2) * bar_width + bar_width / 2
        ax.bar(x + offset, data, width=bar_width, label=legends[i])

    # 軸設定
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel(xlabel, fontsize=16, labelpad=10)
    ax.set_ylabel(f"Latency ({unit})", fontsize=16, labelpad=10)
    ax.grid(axis='y')

    # 対数スケール
    if log_scale:
        ax.set_yscale('log')

    ax.legend(loc='upper center', bbox_to_anchor=(
        0.5, 1.15), ncol=3, fontsize=13)

    fig.tight_layout()
    plt.show()

# def show_bar_graph_multi(data_series_list, x_labels, legends,
#                          xlabel="", unit="", log_scale=False):
#     x = np.arange(len(x_labels))  # x軸の位置（インターバル）
#
#     total_width = 0.8
#     num_series = len(data_series_list)
#     bar_width = total_width / num_series
#
#     fig, ax = plt.subplots()
#
#     for i, data in enumerate(data_series_list):
#         offset = (i - num_series / 2) * bar_width + bar_width / 2
#         ax.bar(x + offset, data, width=bar_width, label=legends[i])
#
#     ax.set_xticks(x)
#     ax.set_xticklabels(x_labels)
#     ax.set_xlabel(xlabel)
#     ax.set_ylabel(f"Latency ({unit})")
#     if log_scale:
#         ax.set_yscale('log')
#     ax.legend()
#     ax.grid(axis='y')
#     plt.tight_layout()
#     plt.show()
