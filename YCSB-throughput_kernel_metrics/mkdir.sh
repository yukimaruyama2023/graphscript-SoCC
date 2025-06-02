#!/bin/bash

# 親ディレクトリ
base_dir="YCSB-throughput"

# ディレクトリ名のリスト（相対パス）
dirs=(
  data_netdata_interval_0_01s
  data_netdata_interval_1s
  data_xdp_interval_0_01s
  data_xdp_interval_1s
  data_netdata_interval_0_1s
  data_no_monitoring
  data_xdp_interval_0_1s
)

# 各ディレクトリを作成
for dir in "${dirs[@]}"; do
  mkdir -p "$base_dir/$dir"
done
