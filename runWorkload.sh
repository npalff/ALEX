#!/bin/sh 



gdown 1Q89-v4FJLEwIKL3YY3oCeOEs0VUuv5bD


./build/benchmark --keys_file=ycsb-200M.bin.data --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0 --lookup_distribution=zipf --print_batch_stats >> ycsb_0.csv
./build/benchmark --keys_file=ycsb-200M.bin.data --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0.05 --lookup_distribution=zipf --print_batch_stats >> ycsb_5.csv
./build/benchmark --keys_file=ycsb-200M.bin.data --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0.33 --lookup_distribution=zipf --print_batch_stats >> ycsb_33.csv
./build/benchmark --keys_file=ycsb-200M.bin.data --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0.5 --lookup_distribution=zipf --print_batch_stats >> ycsb_50.csv
./build/benchmark --keys_file=ycsb-200M.bin.data --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0.66 --lookup_distribution=zipf --print_batch_stats >> ycsb_66.csv
./build/benchmark --keys_file=ycsb-200M.bin.data --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=1 --lookup_distribution=zipf --print_batch_stats >> ycsb_100.csv


echo 'Finished workload for ycsb-200M.bin.data'
