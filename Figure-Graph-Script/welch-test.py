# import numpy as np
# from scipy import stats
#
# input = int(input("Enter 0 for kernel 1 for user: "))
#
# if input == 0:
#     A = np.array([21676, 29923, 22025, 27475, 27661,
#                   25568, 25510, 24739, 26531, 24942])
#     B = np.array([22255, 21340, 20989, 22454, 22156,
#                   23796, 29294, 24731, 31316, 28629])
# elif input == 1:
#     A = np.array([29626, 25835, 23809, 27855, 27783,
#                  28048, 28742, 29749, 35066, 27514])
#     B = np.array([16966, 23754, 21173, 32664, 21686,
#                  25114, 26399, 17825, 18798, 29510])
# else:
#     print("enter moderate number")
#
# A_var = np.var(A, ddof=1)  # Aの不偏分散
# B_var = np.var(B, ddof=1)  # Bの不偏分散
# A_df = len(A) - 1  # Aの自由度
# B_df = len(B) - 1  # Bの自由度
# f = A_var / B_var  # F比の値
# one_sided_pval1 = stats.f.cdf(f, A_df, B_df)  # 片側検定のp値 1
# one_sided_pval2 = stats.f.sf(f, A_df, B_df)   # 片側検定のp値 2
# two_sided_pval = min(one_sided_pval1, one_sided_pval2) * 2  # 両側検定のp値
#
# print('F:       ', round(f, 3))
# print('p-value: ', round(two_sided_pval, 3))
#

import numpy as np
from scipy import stats

input_value = int(input("Enter 0 for kernel 1 for user: "))
interval = int(input("Enter 1, 2, 3 for 1s, 0.1s, 0.01s: "))

if input_value == 0:
    if interval == 1:
        A = np.array([24400, 24660, 28662, 24818, 26036,
                     25113, 26220, 26827, 26342, 32449])
        B = np.array([28631, 24951, 25376, 24697, 29917,
                     26708, 26561, 20467, 24863, 25310])
    elif interval == 2:
        A = np.array([25259, 26579, 22387, 24017, 30099,
                     26901, 25966, 27148, 24771, 26356])
        B = np.array([25535, 25385, 25198, 24992, 22915,
                     27744, 26420, 24042, 25437, 28212])
    elif interval == 3:
        A = np.array([21676, 29923, 22025, 27475, 27661,
                      25568, 25510, 24739, 26531, 24942])
        B = np.array([22255, 21340, 20989, 22454, 22156,
                      23796, 29294, 24731, 31316, 28629])
elif input_value == 1:
    if interval == 1:
        A = np.array([28307, 27677, 23760, 23785, 25132,
                     28326, 25327, 28904, 26554, 24627])
        B = np.array([20690, 23076, 21341, 24454, 24716,
                     27293, 18274, 20709, 23910, 28024])
    elif interval == 2:
        A = np.array([26750, 26553, 26006, 28571, 26963,
                     24237, 29174, 29769, 24600, 25687])
        B = np.array([25347, 22229, 24144, 21112, 22097,
                     24566, 23576, 26342, 27010, 28062])
    elif interval == 3:
        A = np.array([29626, 25835, 23809, 27855, 27783,
                      28048, 28742, 29749, 35066, 27514])
        B = np.array([16966, 23754, 21173, 32664, 21686,
                      25114, 26399, 17825, 18798, 29510])
else:
    print("Enter a valid number (0 or 1).")
    exit()

# Welchのt検定を実行
t_stat, p_value = stats.ttest_ind(A, B, equal_var=False, alternative='greater')

# 結果の表示
print("t-statistic:", round(t_stat, 3))
print("p-value:", round(p_value, 3))

# 結果の解釈
alpha = 0.05  # 有意水準
if p_value < alpha:
    print("Reject the null hypothesis: A's mean is statistically greater than B's mean.")
else:
    print("Fail to reject the null hypothesis: No evidence that A's mean is greater than B's mean.")
