import sys
import math
from random import seed
from random import randint
from random import random

INTMAX = 2147483647
numkeys = 0

try:
    experiment = sys.argv[1]
    numkeys = sys.argv[2]
except:
    print("Command: python createDB.py [experiment] [num keys]")

numkeys=int(numkeys)

#dbFile1= open("../db/createdDB.txt",'w')
#dbFile1= open("createdDB.txt",'w')

if experiment=="minMax":
    dbFile1= open("minMax.txt",'w')
    for i in range(int(math.ceil(numkeys/2))):
        dbFile1.write(str(2*i+1)+"\n")
    for i in range(int(math.ceil(numkeys/2))):
        dbFile1.write(str(INTMAX-2*i)+"\n")


elif experiment=="density":
    dbFile1= open("density.txt",'w')
    for i in range(int(math.ceil(numkeys/2))):
        dbFile1.write(str(2*i+1)+"\n")
    for i in range(int(math.ceil(numkeys/2))):
        dbFile1.write(str(2*i)+"\n")

elif experiment=="primeNumbers":
    dbFile1= open("primeNumbers.txt",'w')
    arrayAux =[]
    primeCounterAux = 0
    i=1
    while(primeCounterAux != numkeys):
        if i>1:
            for j in range(2,i):
                #print("i:" + str(i))
                #print("j:" + str(j)+"\n")
                if(i%j == 0):
                    break
    
            else:
                primeCounterAux +=1
                arrayAux.append(i)
                dbFile1.write(str(i)+"\n")
        i+=1

elif experiment=="repeat":
    counter1=0
    counter2=0
    keysCounter=0
    
    try:
        number_primeNumbers = sys.argv[3]
    except:
        print("Missing number of prime numbers to repeat")
    
    db_fileName = "repeat_"+number_primeNumbers+".txt"
    dbFile1= open(db_fileName,'w')
    primeArray = []
    primeCounterAux = 0
    i=1
    while(primeCounterAux != int(number_primeNumbers)):
        if i>1:
            for j in range(2,i):
                if(i%j == 0):
                    break
        
            else:
                primeCounterAux +=1
                primeArray.append(i)
        i+=1
        
    while(keysCounter != numkeys):
        dbFile1.write(str(primeArray[keysCounter%int(number_primeNumbers)])+"\n")
        keysCounter+=1
elif experiment=="random":
    db_fileName = "random"+".txt"
    dbFile1= open(db_fileName,'w')
    for i in range(numkeys):
        seed()
        dbFile1.write(str(randint(0, INTMAX))+"\n")


else:
    "No experiment with this name"



dbFile1.close()
