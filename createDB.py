import sys

INTMAX = sys.maxint()
numkeys = 0

try:
    experiment = sys.argv[1]
    numkeys = sys.argv[2]
except:
    print("Command: python createDB.py [experiment] [num keys]")




dbFile1= open("../db/createdDB.txt",'w')

if experiment=="minMax":
    for i in range(numkeys):
        dbFile1.write(str(2*i+1)+"\n")
        dbFile2.write(str(INTMAX-2*i)+"\n")
elif experiment=="density":
    print("hello")
elif experiment=="primeNumbers":
    print("hello")
else:
    "No experiment with this name"




dbFile1.close()
