import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
# import scipy.stats as stat

plt.rcParams["font.size"] = 18

# plt.rcParams["font.size"] = 20
data_name = ""
# latency = np.loadtxt(data_name + "xdp_ycsb1.csv", delimiter=',', usecols=2)
# latency2 = np.loadtxt(data_name + "socket_ycsb1.csv",
#

max = int(input("input max value of x axis like 30: "))

latency = np.loadtxt(data_name + sys.argv[1], delimiter=',', usecols=2)
latency2 = np.loadtxt(data_name + sys.argv[2],
                      delimiter=',', usecols=2)
# latency = np.sort(latency / 1000000)
# latency2 = np.sort(latency2 / 1000000)
# latency = np.sort(latency)
# latency2 = np.sort(latency2)
latency = np.sort(latency / 1000)
latency2 = np.sort(latency2 / 1000)
cdf = np.cumsum(latency) / np.sum(latency)
p = 1. * np.arange(len(latency)) / (len(latency) - 1)
p2 = 1. * np.arange(len(latency2)) / (len(latency2) - 1)

# plt.plot(latency, p, marker="*", label="proposed")  # , linewidth=3.0)
# plt.plot(latency2, p2, marker="o", label="conventional")  # , linewidth=3.0)
# plt.tick_params(axis='both', which='major', labelsize=30)
# plt.tick_params(axis='both', which='minor', labelsize=30)

# fig, ax = plt.subplots(figsize=(6.4, 4.8))
fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(latency2, p2, marker="o", markersize=4,
        label="Netdata", color="#1f77b4")  # , linewidth=3.0)
ax.plot(latency, p, marker="*", markersize=4,
        label="X-Monitor", color="coral")  # , linewidth=3.0)
ax.tick_params(axis='both', which='major')
ax.tick_params(axis='both', which='minor')

# plt.hlines(0.999, -10, 7.254, "red", "dashed")  # , linewidth=3.0)
# plt.vlines(7.254, 0, 0.999, "red", "dashed")  # , linewidth=3.0)
# plt.vlines(0.1859, 0, 0.999, "red", "dashed")  # , linewidth=3.0)

# Adding horizontal dashed lines for 90% and 99% percentiles
# plt.hlines(0.9, -0.1, 12, colors='red', linestyles='dashed')
# plt.hlines(0.99, -0.1, 12, colors='red', linestyles='dashed')

# 90%ileと99%ileの横線を追加
ax.axhline(y=0.9, xmin=-1, xmax=12,
           color='black', linestyle='--', linewidth=1, dashes=(10, 5))
ax.axhline(y=0.99, xmin=-1, xmax=12,
           color='black', linestyle='--', linewidth=1, dashes=(10, 5))


ax.set_ylim((0.90, 1))
ax.set_xlim((-0.1, max))
# plt.xscale("log")
# plt.yticks([0.000, 0.500, 0.750, 1.000], ["0%", "50%", "75%", "100%"])
# plt.yticks([0.500, 0.700, 0.900, 1.000], ["50%", "70%", "90%", "100%"])
# plt.yticks([0.700, 0.800, 0.900, 1.000], ["70%", "80%", "90%", "100%"])
# ax.set_yticks([0.800,  0.900, 0.990, 1.000], [
#               str(min) + "%", "90%", "99%", "100%"])
ax.set_yticks([0.900, 0.990, 1.000], ["90%", "99%", "100%"])
# plt.yticks([0.900, 0.950, 0.975, 1.000], ["90.0%", "95%", "97.5%", "100%"])

# plt.xlabel("latency [ms]", fontsize=30)
# plt.ylabel("percentile", fontsize=30)
# plt.legend(fontsize=30, loc='lower right')

ax.set_xlabel("latency [ms]")
ax.set_ylabel("percentile")
# ax.legend(loc='lower right', labelspacing=0)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
# plt.hist(latency, normed=True, cumulative=True, label='CDF',histtype='step', alpha=0.8, color='k')

fig.tight_layout()
plt.show()
