import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


sample = int(input("Enter 5 or 10 to specify # of sample: "))
if sample == 5:
    data_xdp_interval_1s = [24400, 24660, 28662, 24818, 26036]
    data_netdata_interval_1s = [28631, 24951, 25376, 24697, 29917]
    data_xdp_interval_0_1s = [25259, 26579, 22387, 24017, 30099]
    data_netdata_interval_0_1s = [25535, 25385, 25198, 24992, 22915]
    data_xdp_interval_0_01s = [21676, 29923, 22025, 27475, 27661]
    data_netdata_interval_0_01s = [22255, 21340, 20989, 22454, 22156]
elif sample == 10:
    data_xdp_interval_1s = [24400, 24660, 28662, 24818,
                            26036, 25113, 26220, 26827, 26342, 32449]
    data_netdata_interval_1s = [28631, 24951, 25376,
                                24697, 29917, 26708, 26561, 20467, 24863, 25310]
    data_xdp_interval_0_1s = [25259, 26579, 22387,
                              24017, 30099, 26901, 25966, 27148, 24771, 26356]
    data_netdata_interval_0_1s = [25535, 25385, 25198,
                                  24992, 22915, 27744, 26420, 24042, 25437, 28212]
    data_xdp_interval_0_01s = [21676, 29923, 22025,
                               27475, 27661, 25568, 25510, 24739, 26531, 24942]
    data_netdata_interval_0_01s = [
        22255, 21340, 20989, 22454, 22156, 23796, 29294, 24731, 31316, 28629]
else:
    print("Enter 5 or 10")
    exit(1)

data_dict = {
    'X-Monitor (1000ms)': data_xdp_interval_1s,
    'Netdata (1000ms)': data_netdata_interval_1s,
    'X-Monitor (100ms)': data_xdp_interval_0_1s,
    'Netdata (100ms)': data_netdata_interval_0_1s,
    'X-Monitor (10ms)': data_xdp_interval_0_01s,
    'Netdata (10ms)': data_netdata_interval_0_01s
}
df = pd.DataFrame(data_dict)

print("data_xdp_interval_1s mean and SD is ", np.mean(
    data_xdp_interval_1s), np.std(data_xdp_interval_1s))
print("data_netdata_interval_1s mean and SD is ", np.mean(
    data_netdata_interval_1s), np.std(data_netdata_interval_1s))

print("data_xdp_interval_0.1s mean and SD is ", np.mean(
    data_xdp_interval_0_1s), np.std(data_xdp_interval_0_1s))
print("data_netdata_interval_0.1s mean and SD is ", np.mean(
    data_netdata_interval_0_1s), np.std(data_netdata_interval_0_1s))

print("data_xdp_interval_0.01s mean and SD is ", np.mean(
    data_xdp_interval_0_01s), np.std(data_xdp_interval_0_01s))
print("data_netdata_interval_0.01s mean and SD is ", np.mean(
    data_netdata_interval_0_01s), np.std(data_netdata_interval_0_01s))

# ボックスプロットの作成
plt.figure(figsize=(10, 6))  # グラフのサイズを設定
df.boxplot(patch_artist=True)  # DataFrameからボックスプロットを生成

# x軸ラベルのカスタマイズ
plt.xticks(
    ticks=range(1, len(data_dict) + 1),
    labels=["X-Monitor", "Netdata", "X-Monitor",
            "Netdata", "X-Monitor", "Netdata"],
    rotation=0,  # ラベルを水平に
    ha="center"  # ラベルを中央揃え
)

# 下部に追加ラベルを配置
for i, interval in enumerate(["1000ms", "100ms", "10ms"]):
    plt.text(
        x=(i * 2) + 1.5,  # X位置をグループの中央に
        y=plt.gca().get_ylim()[0] - 500,  # Y位置を調整（ラベルを下に配置）
        s=interval,
        ha="center",
        fontsize=10,
        color="black"
    )

plt.ylabel("Throughput (ops/sec)")
plt.tight_layout()
plt.show()

