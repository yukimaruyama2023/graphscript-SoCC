import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sample = int(input("Enter 5 or 10 to specify # of sample: "))

if sample == 5:
    data_xdp_interval_1s = [28307, 27677, 23760, 23785, 25132]
    data_xdp_interval_0_1s = [26750, 26553, 26006, 28571, 26963]
    data_xdp_interval_0_01s = [29626, 25835, 23809, 27855, 27783]
    data_netdata_interval_1s = [20690, 23076, 21341, 24454, 24716]
    data_netdata_interval_0_1s = [25347, 22229, 24144, 21112, 22097]
    data_netdata_interval_0_01s = [16966, 23754, 21173, 32664, 21686]
elif sample == 10:
    data_no_monitoring = [30229, 27950, 26808, 24353,
                          25149, 29315, 26850, 27024, 23159, 24641]
    data_xdp_interval_1s = [28307, 27677, 23760, 23785,
                            25132, 28326, 25327, 28904, 26554, 24627]
    data_xdp_interval_0_1s = [26750, 26553, 26006,
                              28571, 26963, 24237, 29174, 29769, 24600, 25687]
    data_xdp_interval_0_01s = [29626, 25835, 23809,
                               27855, 27783, 28048, 28742, 29749, 35066, 27514]
    data_netdata_interval_1s = [20690, 23076, 21341,
                                24454, 24716, 27293, 18274, 20709, 23910, 28024]
    data_netdata_interval_0_1s = [25347, 22229, 24144,
                                  21112, 22097, 24566, 23576, 26342, 27010, 28062]
    data_netdata_interval_0_01s = [
        16966, 23754, 21173, 32664, 21686, 25114, 26399, 17825, 18798, 29510]
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
    'a': data_no_monitoring,
    'b': data_xdp_interval_1s,
    'c': data_xdp_interval_0_1s,
    'd': data_xdp_interval_0_01s,
    'e': data_netdata_interval_1s,
    'f': data_netdata_interval_0_1s,
    'g': data_netdata_interval_0_01s
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

boxplot = df.boxplot(patch_artist=True, return_type='dict', grid=False)
colors = ['aliceblue'] + ['mediumturquoise'] * 3 + ['peachpuff'] * 3
colors = ['aliceblue'] + ['mediumturquoise'] * 3 + ['lightsalmon'] * 3
colors = ['aliceblue'] + ['peachpuff'] * 3 + ['mediumturquoise'] * 3
colors = ['aliceblue'] + ['peachpuff'] * 3 + ['paleturquoise'] * 3
colors = ['aliceblue'] + ['royalblue'] * 3 + ['darkorange'] * 3

# 箱ひげ図の色を変更
for box, color in zip(boxplot['boxes'], colors):
    box.set_facecolor(color)
# 中央値の線をカスタマイズ
for median in boxplot['medians']:
    median.set_color('black')  # 中央値の線の色を設定
    median.set_linewidth(2.0)  # 中央値の線の太さを設定

plt.text(1.5, -11, 'X-Monitor', ha='center', fontsize=12)
# Netdata（右三つ）のラベル
plt.text(5.5, -11, 'Netdata', ha='center', fontsize=12)

plt.grid(axis='y', linestyle='--', linewidth=0.7)  # 水平線のみグリッドを表示
# ラベルやレイアウトの調整
plt.ylabel("Throughput (Kops/sec)")
plt.xticks(ha='right')
# plt.legend(loc="upper right")  # 凡例を追加
plt.ylim(16, 36)
plt.tight_layout()
plt.show()
