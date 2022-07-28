import sys

INTMAX = sys.maxint()

dbFile1= open("../db/dbOddsMin.txt",'w')
dbFile2= open("../db/dbOddsMax.txt",'w')


for i in range(20000):
    dbFile1.write(str(2*i+1)+"\n")
    dbFile2.write(str(INTMAX-2*i)+"\n")

dbFile1.close()
dbFile2.close()