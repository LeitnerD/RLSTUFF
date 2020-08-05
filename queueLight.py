import os, sys
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
if'SUMO_HOME' in os.environ:
  tools=os.path.join(os.environ['SUMO_HOME'], 'tools')
  sys.path.append(tools)
else:
  print("NOPE!!!")

if(sys.argv[1]=="GUI"):
  SB="../traffic/sumo-1.1.0/bin/sumo-gui"
else:
  SB="../../traffic/sumo-1.1.0/bin/sumo"
SumoCmd=[SB, "--tripinfo-output", "tripInfo.xml","-c", "my_config.sumocfg"]

def findMax(index):
  max=0
  if(index==0 or index==1):
    for i in range(2,4):
      if(len(allQueues[i])>max):
        max=i
  else:
    for i in range(2):
      if(len(allQueues[i])>max):
        max=i
  return max
def checkEntryLoops():
  tmp=0
  for loop in enteryLoops:
    if (traci.inductionloop.getLastStepVehicleNumber(loop) > 0):
      temp= traci.inductionloop.getVehicleData(loop)
      for veh in temp:
        index=int(tmp/2)
        if veh[0] not in allQueues[index]:
          allQueues[index].append(veh[0])
          #allTT[index].append(float(queueTime[len(allQueues[index])+1]))
          max=0
          if(index==0 or index==1):
            for i in range(2,4):
              if(len(allQueues[i])>max):
                max=i
          else:
             for i in range(2):
              if(len(allQueues[i])>max):
                max=i
          allTT[index].append(float(.65064*len(allQueues[max])+float(intercept[0])*1.89094+yelDur[0]+.65064*len(allQueues[index])))
          #allTT[index].append(float((200-len(allQueues[index]))/15+.65064*len(allQueues[max])+int(mul)*1.89094+yelDur[0]+.65064*len(allQueues[index])))

          #print(allTT)
    tmp=tmp+1

def checkExitLoops():
  tmp=0
  for loop in exitLoops:
    if (traci.inductionloop.getLastStepVehicleNumber(loop) > 0):
      temp= traci.inductionloop.getVehicleData(loop)
      for veh in temp:
        #index=int(tmp/2)
        route=traci.vehicle.getRouteID(veh[0])
        if (route=="route0" or route=="route4" ):
          index=0
        elif(route=="route2" or route=="route6" ):
          index=1
        elif(route=="route1" or route=="route5"  ):
          index=2
        elif(route=="route3" or route=="route7"  ):
          index=3
        if veh[0] in allQueues[index]:
          index2=allQueues[index].index(veh[0])
          Y.append(float(traci.vehicle.getAccumulatedWaitingTime(veh[0])))
          X.append(float(allTT[index][index2]))
          del allTT[index][index2]
          del allQueues[index][index2]
    tmp=tmp+1

def  upDateLights():
  if(lightDirection[0]=="V"):
    for car in allQueues[0]:
      index2=allQueues[0].index(car)
      max=findMax(0)
      #allTT[0][index2]=float(.65064*len(allQueues[max])+float(intercept[0])*1.89094+yelDur[0]+.65064*len(allQueues[0]))
      if (traci.vehicle.getWaitingTime(car) > (allTT[0][index2] - (.65064*index2/2+yelDur[0]))and currentPhase[0]>minTime[0]):
      #if (traci.vehicle.getWaitingTime(car) > (allTT[0][index2])):
        changeLightsVtoH()
        currentPhase[0]=0.0
        break
  if(lightDirection[0]=="V"):
    for car in allQueues[1]:
      index2=allQueues[1].index(car)
      max=findMax(1)
      #allTT[1][index2]=float(.65064*len(allQueues[max])+float(intercept[0])*1.89094+yelDur[0]+.65064*len(allQueues[1]))
      if (traci.vehicle.getWaitingTime(car) > (allTT[1][index2] - (.65064*index2/2+yelDur[0]))and currentPhase[0]>minTime[0]):
      #if (traci.vehicle.getWaitingTime(car) > (allTT[1][index2])):
        changeLightsVtoH()
        currentPhase[0]=0.0
        break
  if(lightDirection[0]=="H"):
    for car in allQueues[2]:      
      index2=allQueues[2].index(car)
      max=findMax(2)
      #if (traci.vehicle.getWaitingTime(car) > (allTT[2][index2])):
      #allTT[2][index2]=float(.65064*len(allQueues[max])+float(intercept[0])*1.89094+yelDur[0]+.65064*len(allQueues[2]))
      if (traci.vehicle.getWaitingTime(car) > (allTT[2][index2] - (.65064*index2/2+yelDur[0]))and currentPhase[0]>minTime[0]):
        changeLightsHtoV()
        currentPhase[0]=0.0
        break
  if(lightDirection[0]=="H"):
    for car in allQueues[3]:
      index2=allQueues[3].index(car)
      max=findMax(3)
      #if (traci.vehicle.getWaitingTime(car) > (allTT[3][index2])):
      #allTT[3][index2]=float(.65064*len(allQueues[max])+float(intercept[0])*1.89094+yelDur[0]+.65064*len(allQueues[3]))
      if (traci.vehicle.getWaitingTime(car) > (allTT[3][index2] - (.65064*index2/2+yelDur[0]))and currentPhase[0]>minTime[0]):
        changeLightsHtoV()
        currentPhase[0]=0.0
        break

def changeLightsHtoV():
  if(str(traci.trafficlight.getProgram("n3"))=="HpassG"):
    traci.trafficlight.setProgram("n3", "VpassY")
    lightDirection[0]="Y"
    desiredDirection[0]="V"
  elif(str(traci.trafficlight.getProgram("n3"))=="VpassY" and changeTime[0] >= yelDur[0]):
    traci.trafficlight.setProgram("n3", "VpassG")
    desiredDirection[0]=""
    lightDirection[0]="V"


def changeLightsVtoH():
  if(str(traci.trafficlight.getProgram("n3"))=="VpassG"):
    traci.trafficlight.setProgram("n3", "HpassY")
    lightDirection[0]="Y"
    desiredDirection[0]="H"
  elif(str(traci.trafficlight.getProgram("n3"))=="HpassY" and changeTime[0] >=yelDur[0]):
    traci.trafficlight.setProgram("n3", "HpassG")
    desiredDirection[0]=""
    lightDirection[0]="H"
    currentPhase[0]=0.0


def finishCycle():
  if(changeTime[0]>=yelDur[0]):
    if(desiredDirection[0]=="V"):
      changeLightsHtoV()
      changeTime[0]=0.0
    elif(desiredDirection[0]=="H"):
      changeLightsVtoH()
      changeTime[0]=0.0
  else:
    changeTime[0]=changeTime[0]+stepSize[0]
    #print (str(changeTime[0]))



import traci
import traci.constants as tc
lightDirection=["V"]
desiredDirection=[""]
changeTime=[float(0.0)]
currentPhase=[float(0.0)]
steps=int(sys.argv[2])
yelDur=[float(sys.argv[3])]
intercept=[float(sys.argv[4])]
minTime=[float(sys.argv[5])]
endflag=0
#array of all entery loops
enteryLoops=["loop13_0","loop13_1","loop23_0","loop23_1","loop43_0","loop43_1","loop53_0","loop53_1"]
exitLoops=  ["loop32_0","loop32_1","loop31_0","loop31_1","loop35_0","loop35_1","loop34_0","loop34_1"]
#list of Queues for each road [1to3][2to3][4to3][5to3]
allQueues=[[],[],[],[]]
#list of Aprox travel time for each veh in Queue [1to3][2to3][4to3][5to3]
allTT=[[],[],[],[]]
X=[]
Y=[]


#start 
os.system("../../traffic/sumo-1.1.0/bin/netconvert --node-files my_node.nod.xml --edge-files my_edge.edg.xml -t my_type.type.xml -o net2.net.xml")
traci.start(SumoCmd) 
stepSize=[traci.simulation.getDeltaT()]
#queueTime=[0,2.955,3.014,3.868,4.027,4.91,5.153,6.02,6.333,7.17,7.562,8.353,8.827,9.559,10.113,10.783,11.414,12.025,12.727,13.285,14.048,14.557,15.376,15.839,16.711,17.134,18.05,18.439,19.394,19.753,20.742,21.078,22.094,22.414,23.448,23.756,24.804,25.102,26.161,26.452,27.52,27.805,28.879,29.161,30.239,30.52,31.601,31.881,32.964,33.244,34.328]
#out=open("waitTimes2.csv",'w')
#out.write("wait Time,Worse case,light color,my queue,other queue\n")
traci.trafficlight.setProgram("n3", "VpassG")
for step in range(steps):
  currentPhase[0]=currentPhase[0]+stepSize[0]
  traci.simulationStep()
  checkEntryLoops()
  checkExitLoops()
  if(lightDirection[0]!="Y"):
    upDateLights()
  else:
    finishCycle()
  if(len(allQueues[0])==0 and len(allQueues[1])==0 and len(allQueues[2])==0 and len(allQueues[3])==0):
    endflag=endflag+1
  else:
    endflag=0
  if(endflag==1000):
    break

traci.close()
plt.scatter(X,Y,color="red")
xx=[0,5,10,15,20]
yy=[0,5,10,15,20]
plt.plot(xx,yy)
plt.xlim(0,20)
plt.ylim(0,20)
plt.xlabel('Predicted Wait Time (s)')
plt.ylabel('Actual Wait Time (s)')
plt.savefig("Graphs/compare"+str(intercept[0])+".png")
print("\n")
