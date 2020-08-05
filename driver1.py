#import os, sys
#if'SUMO_HOME' in os.environ:
#  tools=os.path.join(os.environ['SUMO_HOME'], 'tools')
#  sys.path.append(tools)
#else:
#  print("NOPE!!!")
#
#
#if(sys.argv[1]=="GUI"):
#  SB="~/localstorage/myLocal/traffic/sumo/bin/sumo-gui"
#else:
#  SB="~/localstorage/myLocal/traffic/sumo/bin/sumo"
#if(sys.argv[2]=="y"):
#  os.system("~/localstorage/myLocal/traffic/sumo/bin/netconvert --node-files my_node.nod.xml --edge-files my_edge.edg.xml -t my_type.type.xml -o net2.net.xml")
#  #config=sys.argv[3]
#  #os.system("~/localstorage/myLocal/traffic/sumo-1.1.0/bin/sumo --tripinfo-output tripInfo.xml -c "+config)
#import traci
#import traci.constants as tc
#SumoCmd=[SB, "--tripinfo-output", "tripInfo.xml","-c", "my_config.sumocfg"]
#traci.start(SumoCmd)
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
          #allTT[index].append(float(.65064*len(allQueues[max])+float(intercept[0])*1.89094+yelDur[0]+.65064*len(allQueues[index])))
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
          #X.append(float(allTT[index][index2]))
          #del allTT[index][index2]
          del allQueues[index][index2]
    tmp=tmp+1
import os, sys
import numpy as np
import csv
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
if'SUMO_HOME' in os.environ:
  tools=os.path.join(os.environ['SUMO_HOME'], 'tools')
  sys.path.append(tools)
else:
  print("NOPE!!!")

if(sys.argv[1]=="GUI"):
  SB="../../traffic/sumo-1.1.0/bin/sumo-gui"
else:
  SB="../../traffic/sumo-1.1.0/bin/sumo"
SumoCmd=[SB, "--tripinfo-output", "tripInfo.xml","-c", "my_config.sumocfg"]

import traci
import traci.constants as tc
#array of all entery loops
enteryLoops=["loop13_0","loop13_1","loop23_0","loop23_1","loop43_0","loop43_1","loop53_0","loop53_1"]
exitLoops=  ["loop32_0","loop32_1","loop31_0","loop31_1","loop35_0","loop35_1","loop34_0","loop34_1"]
#list of Queues for each road [1to3][2to3][4to3][5to3]
allQueues=[[],[],[],[]]

X=[]
Y=[]


wait=np.array([0.0,0.0,0.0,0.0])
nVeh=np.array([0,0,0,0])
edges=["1to3","2to3","4to3","5to3"]
state_size=10000
action_size=2
gamma=.2
lr=.5
bonus=0
ln=0
avWait=0
k=0
itt=int(sys.argv[4])
epsilon=.9-.002*itt
if(itt%50==0):
	line="./trafficGen2 100 2 1"
	os.system(line)
os.system("../../traffic/sumo-1.1.0/bin/netconvert --node-files my_node.nod.xml --edge-files my_edge.edg.xml -t my_type.type.xml -o net2.net.xml")
traci.start(SumoCmd) 
stepSize=1#[traci.simulation.getDeltaT()]
avOut=file("ave.txt",'w')
Q=np.zeros((state_size, action_size))
if itt==0:
	Q.fill(.5)
if(sys.argv[2]=="t"):
	with open(str(sys.argv[3])) as csvfile:
		qOut=csv.reader(csvfile,delimiter=',')
	#tmp=qOut.read()
	#print(tmp)
		for row in qOut:
		#t=l.split(",")
		#print(t)
			#print(row)
			Q[ln,0]=float(row[0])#float(t[0])
			Q[ln,1]=float(row[1])#float(t[1])
			
			#print(Q[ln])
			ln=ln+1
	#qOut.close()
#Q=qOut.read()
import random

traci.simulationStep()
state=0
action=0
steps=10000
paction=0
for j in range(steps):
	if j%30==0:
		paction=action
		if (random.uniform(0,1)<epsilon):
			if (random.uniform(0,1)>.5):
				action=1
			else:
				action=0	
		else:
			if(Q[state,0]<Q[state,1]):
				action=1
			else:
				action=0
		if(action==1 and paction==action):
			traci.trafficlight.setProgram("n3", "HpassG")
			bonus=bonus+1
		elif(action==1 and paction!=action):
			traci.trafficlight.setProgram("n3", "HpassY")
			for n in range(30):
				traci.simulationStep()
			traci.trafficlight.setProgram("n3", "HpassG")
			bonus=0
		elif(action==0 and paction==action):
			traci.trafficlight.setProgram("n3", "VpassG")
			bonus=bonus+1
		elif(action==0 and paction!=action):
			traci.trafficlight.setProgram("n3", "VpassY")
			for n in range(30):
				traci.simulationStep()
			traci.trafficlight.setProgram("n3", "VpassG")
			bonus=0
	for n in range(5):
		traci.simulationStep()
	epsilon=epsilon-.001
	checkEntryLoops()
	checkExitLoops()
		#print(allQueues[0])
	for lane in range(4):
		wait[lane]=traci.edge.getWaitingTime(str(edges[lane]))
		nVeh[lane]=traci.edge.getLastStepVehicleNumber(edges[lane])
	num0=max(nVeh[0],nVeh[1])
	num1=max(nVeh[2],nVeh[3])
	if(np.amin(nVeh)>0):
		#avWait=avWait+
		avOut.write(str(max(wait[0]/nVeh[0],wait[1]/nVeh[1],wait[2]/nVeh[2],wait[3]/nVeh[3]))+"\n")
		k=k+1

	#if(num0>9):
	#	num0=9
	#print(num1)
	#if(num1>9):
	#	num1=9
	#print(num2)
	new_state=num1*100+num0
	#print(new_state)
	#if(new_state>99):
	#	new_state=99
	if (action==0):# and num0>0 and num1>0):
		#reward=-traci.edge.getWaitingTime("1to3")-traci.edge.getWaitingTime("2to3")
		reward=-(wait[0]+wait[1]+wait[2]+wait[3])
		#reward=-(wait[0]/nVeh[0]+wait[1]/nVeh[1]+wait[2]/nVeh[2]+wait[3]/nVeh[3])

		#bonus*0-max(nVeh[0],nVeh[1])-max(nVeh[2],nVeh[3])#-(traci.edge.getLastStepVehicleNumber("1to3")+traci.edge.getLastStepVehicleNumber("2to3"))
		#traci.edge.getLastStepMeanSpeed("1to3")+traci.edge.getLastStepMeanSpeed("2to3")
	else: #num1>0 and num0>0:
		#reward=-traci.edge.getWaitingTime("4to3")-traci.edge.getWaitingTime("5to3")
		#reward=-max(wait[0]/nVeh[0],wait[1]/nVeh[1],wait[2]/nVeh[2],wait[3]/nVeh[3])
		#reward=-(wait[0]/nVeh[0]+wait[1]/nVeh[1]+wait[2]/nVeh[2]+wait[3]/nVeh[3])
		reward=-(wait[0]+wait[1]+wait[2]+wait[3])
		#reward=bonus*0-max(nVeh[2],nVeh[3])-max(nVeh[0],nVeh[1])#-(traci.edge.getLastStepVehicleNumber("4to3")+traci.edge.getLastStepVehicleNumber("5to3"))
	#else:
	#	reward=0
	if(max(nVeh)==0 and j>100):
		for m in range(30):
			traci.simulationStep()
		traci.close()
		break
	#if(j%1000==0):
	#	print("\n"+str(traci.edge.getWaitingTime("1to3"))+" "+str(traci.edge.getWaitingTime("2to3"))+" "+str(traci.edge.getWaitingTime("4to3"))+" "+str(traci.edge.getWaitingTime("5to3"))+"\n")
	#	if new_state==0:
	#		traci.close()
	#print(Q)
	if j%30==0:
		Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) - Q[state, action])
		state=new_state
name="longTest/"+str(itt)+"W"+str(avWait/k)+"Q.csv"
qOut=file(name,'w')
for l in range(state_size):
	dum=str(Q[l,0])+","+str(Q[l,1])+"\n"
	qOut.write(dum)
qOut.close()
qOut=file("name.txt", 'w')
qOut.write(name)
qOut.close()
qOut=file("steps.csv",'a')
qOut.write(str(j)+"\n")
#cmd="python driver1.py GU t "+name+ " "+str(itt+1)
#if itt<1000:
#	os.system(cmd)