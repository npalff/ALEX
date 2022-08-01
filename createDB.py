import sys
import math

INTMAX = 2147483647
numkeys = 0

try:
    experiment = sys.argv[1]
    numkeys = sys.argv[2]
except:
    print("Command: python createDB.py [experiment] [num keys]")

numkeys=int(numkeys)

dbFile1= open("../db/createdDB.txt",'w')
#dbFile1= open("createdDB.txt",'w')

if experiment=="minMax":
    for i in range(int(math.ceil(numkeys/2))):
        dbFile1.write(str(2*i+1)+"\n")
    for i in range(int(math.ceil(numkeys/2))):
        dbFile1.write(str(INTMAX-2*i)+"\n")


elif experiment=="density":
    for i in range(int(math.ceil(numkeys/2))):
        dbFile1.write(str(2*i+1)+"\n")
    for i in range(int(math.ceil(numkeys/2))):
        dbFile1.write(str(2*i)+"\n")

elif experiment=="primeNumbers":
    arrayAux =[]
    primeCounterAux = 0
    i=1
    while(primeCounterAux != numkeys):
        if i>1:
            for j in range(2,i):
                print("i:" + str(i))
                print("j:" + str(j)+"\n")
                if(i%j == 0):
                    break
    
            else:
                primeCounterAux +=1
                arrayAux.append(i)
                dbFile1.write(str(i)+"\n")
        i+=1

else:
    "No experiment with this name"



dbFile1.close()
