import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


sample = int(input("Enter 5 or 10 to specify # of sample: "))
if sample == 5:
    data_xdp_interval_1s = [24400, 24660, 28662, 24818, 26036]
    data_xdp_interval_0_1s = [25259, 26579, 22387, 24017, 30099]
    data_xdp_interval_0_01s = [21676, 29923, 22025, 27475, 27661]
    data_netdata_interval_1s = [28631, 24951, 25376, 24697, 29917]
    data_netdata_interval_0_1s = [25535, 25385, 25198, 24992, 22915]
    data_netdata_interval_0_01s = [22255, 21340, 20989, 22454, 22156]
elif sample == 10:
    data_no_monitoring = [30229, 27950, 26808, 24353,
                          25149, 29315, 26850, 27024, 23159, 24641]
    data_xdp_interval_1s = [24400, 24660, 28662, 24818,
                            26036, 25113, 26220, 26827, 26342, 32449]
    data_xdp_interval_0_1s = [25259, 26579, 22387,
                              24017, 30099, 26901, 25966, 27148, 24771, 26356]
    data_xdp_interval_0_01s = [21676, 29923, 22025,
                               27475, 27661, 25568, 25510, 24739, 26531, 24942]
    data_netdata_interval_1s = [28631, 24951, 25376,
                                24697, 29917, 26708, 26561, 20467, 24863, 25310]
    data_netdata_interval_0_1s = [25535, 25385, 25198,
                                  24992, 22915, 27744, 26420, 24042, 25437, 28212]
    data_netdata_interval_0_01s = [
        22255, 21340, 20989, 22454, 22156, 23796, 29294, 24731, 31316, 28629]
else:
    print("Enter 5 or 10")
    exit(1)

data_no_monitoring = [x / 1000 for x in data_no_monitoring]
data_xdp_interval_1s = [x / 1000 for x in data_xdp_interval_1s]
data_xdp_interval_0_1s = [x / 1000 for x in data_xdp_interval_0_1s]
data_xdp_interval_0_01s = [x / 1000 for x in data_xdp_interval_0_01s]
data_netdata_interval_1s = [x / 1000 for x in data_netdata_interval_1s]
data_netdata_interval_0_1s = [x / 1000 for x in data_netdata_interval_0_1s]
data_netdata_interval_0_01s = [x / 1000 for x in data_netdata_interval_0_01s]

data_dict = {
    'w/o Monitoring': data_no_monitoring,
    'X-Monitor, Interval1s': data_xdp_interval_1s,
    'X-Monitor, Interval0.1s': data_xdp_interval_0_1s,
    'X-Monitor, Interval0.01s': data_xdp_interval_0_01s,
    'Netdata, Interval1s': data_netdata_interval_1s,
    'Netdata, Interval0.1s': data_netdata_interval_0_1s,
    'Netdata,Interval0.01s': data_netdata_interval_0_01s
}
df = pd.DataFrame(data_dict)

print("data_xdp_interval_1s mean and SD is ", np.mean(
    data_xdp_interval_1s), np.std(data_xdp_interval_1s))
print("data_xdp_interval_0.1s mean and SD is ", np.mean(
    data_xdp_interval_0_1s), np.std(data_xdp_interval_0_1s))
print("data_xdp_interval_0.01s mean and SD is ", np.mean(
    data_xdp_interval_0_01s), np.std(data_xdp_interval_0_01s))

print("data_netdata_interval_1s mean and SD is ", np.mean(
    data_netdata_interval_1s), np.std(data_netdata_interval_1s))
print("data_netdata_interval_0.1s mean and SD is ", np.mean(
    data_netdata_interval_0_1s), np.std(data_netdata_interval_0_1s))
print("data_netdata_interval_0.01s mean and SD is ", np.mean(
    data_netdata_interval_0_01s), np.std(data_netdata_interval_0_01s))

# # ボックスプロットの作成
# plt.figure(figsize=(10, 6))  # グラフのサイズを設定
# # df.boxplot(patch_artist=True)  # DataFrameからボックスプロットを生成
# boxplot = df.boxplot(patch_artist=False)
# # plt.title("Box Plot of Latency Data for Different Intervals")
# plt.ylabel("Throughput (ops/sec)")
# # plt.xlabel("Data Groups")
#
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()
# plt.show()

# return_type='dict'で要素を取得
boxplot = df.boxplot(patch_artist=True, return_type='dict', grid=False)
colors = ['aliceblue'] + ['royalblue'] * 3 + ['darkorange'] * 3
for box, color in zip(boxplot['boxes'], colors):
    box.set_facecolor(color)

# 中央値の線をカスタマイズ
for median in boxplot['medians']:
    median.set_color('black')  # 中央値の線の色を設定
    median.set_linewidth(2.0)  # 中央値の線の太さを設定

plt.grid(axis='y', linestyle='--', linewidth=0.7)  # 水平線のみグリッドを表示
# ラベルやレイアウトの調整
plt.ylabel("Throughput (Kops/sec)")
plt.xticks(rotation=45, ha='right')
# plt.legend(loc="upper right")  # 凡例を追加
plt.ylim(16, 36)
plt.tight_layout()
plt.show()
