import sys
# sys.argv
numkeys = "20000000"
benchmarkFile=""
try:
    LI_system = sys.argv[1]
    benchmarkFile = sys.argv[2]
    experiment = sys.argv[3]
    itNumber = sys.argv[4]
    numkeys= sys.argv[5]
except:
    print("Command: python configWorkloads.py [LI system] [benchmark ID] [insert percentage] [Iterations number] [number of keys]")
GD_ID=""
keysFile=""
insertion_keys_file=""
keysType="binary"

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
elif benchmarkFile == "minMax":
    keysFile = "minMax.txt"
    keysType = "text"
elif benchmarkFile == "density":
    keysFile = "density.txt"
    keysType = "text"
elif benchmarkFile == "repeat_15":
    keysFile = "repeat_15.txt"
    keysType = "text"
elif benchmarkFile == "repeat_50":
    keysFile = "repeat_50.txt"
    keysType = "text"
elif benchmarkFile == "repeat_100":
    keysFile = "repeat_100.txt"
    keysType = "text"
elif benchmarkFile == "random":
    keysFile = "random.txt"
    keysType = "text"
elif benchmarkFile == "shipDates":
    keysFile = "shipDates.txt"
    keysType = "text"
elif benchmarkFile == "wiki":
    keysFile = "wiki"

else:
    print("Possible workloads:long, longlat, lognormal, ycsb, minMax, density, primeNumbers, repeat, random" )


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



### WORKLOAD 

try:
    workload_file = open("runWorkload.sh", 'w')
    workload_file.write("#!/bin/sh \n")
    workload_file.write("\n\n\n")
   # workload_file.write("gdown "+GD_ID+"\n")
   # workload_file.write("\n\n")
    ### Create DB
    #workload_file.write("python createDB.py "+benchmarkFile+" "+str(int(numkeys)*10)+"\necho \"DB Created\"")
    ########  ALEX  ########
    
    ### Warmup
    for i in range(4):
        workload_file.write("./build/"+ LI_system +" --keys_file=../db/"+keysFile+" --keys_file_type="+keysType+" --init_num_keys="+str(int(numkeys)/2)+" --total_num_keys="+numkeys+" --batch_size="+str(int(numkeys)/20)+" --insert_frac="+str(float(experiment)/100)+" --lookup_distribution=zipf --print_batch_stats\n")
        workload_file.write("\necho 'Finished Warmup "+str(i+1)+"'\n\n")
    ### Experiment
    
    for i in range(int(itNumber)):    
        workload_file.write("./build/"+ LI_system +" --keys_file=../db/"+keysFile+" --keys_file_type="+keysType+" --init_num_keys="+str(int(numkeys)/2)+" --total_num_keys="+numkeys+" --batch_size="+str(int(numkeys)/20)+" --insert_frac="+str(float(experiment)/100)+" --lookup_distribution=zipf --print_batch_stats >>"+LI_system+"_"+benchmarkFile+"_"+experiment+"_"+str(i+1)+".csv\n")
        workload_file.write("\necho 'Finished experiment "+str(i+1)+"'\n\n")


    workload_file.write("\n\n")
 
finally:
    workload_file.close()