import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
def plotStuff(file,i,j):
  text=[]
  bin=[0]*8
  file=sys.argv[1]
  data=open(file,'r')
  #reads in every line of data and stores in text
  for l in data:
    text.append(l)
  #parse data into array
  newData=[]
  points=[]
  for l in text:
    if l.find("waitingTime")<> -1:
      line=l.split()
      newData.append(line)
  data.close()
  for l in newData:
    #print (l)
    points.append(l[13])
  nums=[]
  mean=0
  total=0
  for l in points:
    line=l.split("=")
    nums.append(line)
  waitTimes=[]
  for l in nums:
    nl=l[1].replace("\"","")
    waitTimes.append(float(nl))
    if(float(nl)<1):
      bin[0]=bin[0]+1
    if(float(nl)>0 and float(nl)<6):
      bin[1]=bin[1]+1
    if(float(nl)>5 and float(nl)<11):
      bin[2]=bin[2]+1
    if(float(nl)>10 and float(nl)<16):
      bin[3]=bin[3]+1
    if(float(nl)>15 and float(nl)<21):
      bin[4]=bin[4]+1
    if(float(nl)>20 and float(nl)<26):
      bin[5]=bin[5]+1
    if(float(nl)>25 and float(nl)<31):
      bin[6]=bin[6]+1
    if(float(nl)>30):
      bin[7]=bin[7]+1
    mean=mean+1
    total=total+float(nl)
  line=str(j)+","+str(names[i-1])+","+str(np.std(waitTimes))+","+str(np.average(waitTimes))+","+str(np.amax(waitTimes))+"\n"
  out.write(line)
  N=len(bin)
  x=range(N)
  for num in x:
    x[num]=x[num]-(i-2)*.2
  rect = ax.bar(x,bin,.2,label=names[i-1])
  #mean=total/mean
  for r in rect:
    xpos='center'
    h=r.get_height()
    ax.text(r.get_x()+r.get_width(),1.01*h,'{}'.format(h),ha='center',va='bottom')
    if(i==3):
      plt.xticks(x,("<1","1-5","6-10","11-15","16-20","21-25","26-30",">30"))
#names=["simple controller", "default controller", "delayed based", "actuated","Queue Time Y=3","Queue Time Y=4"]
#names=["yellow 0","yellow 1","yellow 2","yellow 3","yellow 4","yellow 5"]
#names=[".2 intercept"," .4 intercept",".6 intercept",".8 intercept", "1 intercept" ]
names=["100","80","60","40", "20" ]
if(sys.argv[2]=="y"):
  os.system("../traffic/sumo-1.1.0/bin/netconvert --node-files my_node.nod.xml --edge-files my_edge.edg.xml -t my_type.type.xml -o net2.net.xml")
  config=sys.argv[3]
  os.system("../traffic/sumo-1.1.0/bin/sumo --tripinfo-output tripInfo.xml -c "+config)
#os.system("./trafficGen 10000 1 0")
out=open("results.csv","w")
line=" ,,std dev,average,worst case\n"
out.write(line)
#for i in range(2,5):
 # config="my_config"+str(i)+".sumocfg"
 # os.system("../traffic/sumo-1.1.0/bin/sumo --tripinfo-output tripInfo.xml -c "+config)
  #plotStuff(sys.argv[1],i)
tt=[.5,.6,.7,.8,.9,1]
tl=[50,60,70,80,90]
for j in tt:
  fig, ax=plt.subplots()
  for i in range(1,6):
   # os.system("python queueLight.py no 120000 "+str(i-1))
    os.system("./trafficGen2 1000 "+str(j)+" "+str(tl[i-1]))
    os.system("python queueLight.py no 300000 3 .5 0")
    #config="my_config3.sumocfg"
    #os.system("../traffic/sumo-1.1.0/bin/sumo --tripinfo-output tripInfo.xml -c "+config)
    plotStuff(sys.argv[1],i,j)
  #os.system("python queueLight.py no 300000 3 1")
  #plotStuff(sys.argv[1],2)
  #os.system("python queueLight.py no 300000 3 2")
  #plotStuff(sys.argv[1],3)
  #plt.title("mean="+str(mean))
  
  ax.legend()
  plt.xlabel('Wait Time (s)')
  plt.ylabel('Number of Vehicles')
  plt.savefig("Graphs/waitPlot"+str(j)+".png")
  plt.clf()
