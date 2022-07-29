import sys

INTMAX = sys.maxint()
numkeys = 0

try:
    experiment = sys.argv[1]
    numkeys = sys.argv[2]
except:
    print("Command: python createDB.py [experiment] [num keys]")




dbFile1= open("../db/dbOddsMin.txt",'w')
dbFile2= open("../db/dbOddsMax.txt",'w')


for i in range(numkeys):
    dbFile1.write(str(2*i+1)+"\n")
    dbFile2.write(str(INTMAX-2*i)+"\n")

dbFile1.close()
dbFile2.close()