import sys
# sys.argv

benchmarkFile=""
try:
    benchmarkFile = sys.argv[1]
    LI_system = sys.argv[2]
except:
    print("Command: python configWorkloads.py [benchmark ID] [LI system]")
GD_ID=""
keysFile=""


if  benchmarkFile == "long":
    GD_ID="1zc90sD6Pze8UM_XYDmNjzPLqmKly8jKl"
    keysFile = "longitudes-200M.bin.data"
elif benchmarkFile == "longlat":
    GD_ID="1mH-y_PcLQ6p8kgAz9SB7ME4KeYAfRfmR"
    keysFile = "longlat-200M.bin.data"
elif benchmarkFile == "lognormal":
    GD_ID="1y-UBf8CuuFgAZkUg_2b_G8zh4iF_N-mq"
    keysFile = "lognormal-190M.bin.data"
elif benchmarkFile == "ycsb":
    GD_ID="1Q89-v4FJLEwIKL3YY3oCeOEs0VUuv5bD"
    keysFile = "ycsb-200M.bin.data"
else:
    print("Possible workloads:long, longlat, lognormal, ycsb" )


if LI_system == "lipp":
    filePath = "/ALEX/lipp_"
elif LI_system == "alex":
    filePath = "/ALEX/alex_"
elif LI_system == "pgm":
    filePath = "/ALEX/pgm_"
else:
    print("Possible systems:lipp, alex, pgm" )


'''
print("=========================")
print("GD_ID:   "+ GD_ID)
print("Keys File:   " + keysFile)
print("========================\n")
'''
try:
    workload_file = open("runWorkload.sh", 'w')
    workload_file.write("#!/bin/sh \n")
    workload_file.write("\n\n\n")
    workload_file.write("gdown "+GD_ID+"\n")
    workload_file.write("\n\n")
    
    ########  ALEX  ########
    
    workload_file.write("./build/"+ LI_system +" --keys_file="+keysFile+" --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0 --lookup_distribution=zipf --print_batch_stats >>"+LI_system+"_"+benchmarkFile+"_0.csv\n")
    workload_file.write("\necho 'Finished 0 percent insertion '\n\n")
    workload_file.write("./build/"+ LI_system +" --keys_file="+keysFile+" --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0.05 --lookup_distribution=zipf --print_batch_stats >>"+LI_system+"_"+benchmarkFile+"_5.csv\n")
    workload_file.write("\necho 'Finished 5 percent insertion '\n\n")
    workload_file.write("./build/"+ LI_system +" --keys_file="+keysFile+" --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0.33 --lookup_distribution=zipf --print_batch_stats >>"+LI_system+"_"+benchmarkFile+"_33.csv\n")
    workload_file.write("\necho 'Finished 33 percent insertion '\n\n")
    workload_file.write("./build/"+ LI_system +" --keys_file="+keysFile+" --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0.5 --lookup_distribution=zipf --print_batch_stats >>"+LI_system+"_"+benchmarkFile+"_50.csv\n")
    workload_file.write("\necho 'Finished 50 percent insertion '\n\n")
    workload_file.write("./build/"+ LI_system +" --keys_file="+keysFile+" --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=0.66 --lookup_distribution=zipf --print_batch_stats >>"+LI_system+"_"+benchmarkFile+"_66.csv\n")
    workload_file.write("\necho 'Finished 66 percent insertion '\n\n")
    workload_file.write("./build/"+ LI_system +" --keys_file="+keysFile+" --keys_file_type=binary --init_num_keys=10000000 --total_num_keys=20000000 --batch_size=1000000 --insert_frac=1 --lookup_distribution=zipf --print_batch_stats >>"+LI_system+"_"+benchmarkFile+"_100.csv\n")
    workload_file.write("\necho 'Finished 100 percent insertion '\n\n")
    workload_file.write("\n\n")
 
finally:
    workload_file.close()
