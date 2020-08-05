import os, sys
tmp=file(sys.argv[1],'r')
num=0
count=0
for l in tmp:
	num=num+float(l)
	count=count+1
print(num/count)	
