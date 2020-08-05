import os, sys
line="python driver1.py GU f longTest/998W0Q.csv 0"
os.system(line)
for i in range(1,1000):
	f=file("name.txt",'r')
        name=f.readline()
        print("the file name is: "+name)
	line="python driver1.py gu t "+name+" "+str(i)
	os.system(line)
        f.close()
