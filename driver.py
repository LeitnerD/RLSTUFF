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
  SB="../../traffic/sumo-1.1.0/bin/sumo-gui"
else:
  SB="../../traffic/sumo-1.1.0/bin/sumo"
SumoCmd=[SB, "--tripinfo-output", "tripInfo.xml","-c", "my_config.sumocfg"]

import traci
import traci.constants as tc

state_sizeV=500
state_sizeH=500
action_size=2
gamma=.7
lr=.1
epsilon=.1

os.system("../../traffic/sumo-1.1.0/bin/netconvert --node-files my_node.nod.xml --edge-files my_edge.edg.xml -t my_type.type.xml -o net2.net.xml")
traci.start(SumoCmd) 
stepSize=1#[traci.simulation.getDeltaT()]
Q=np.zeros((state_sizeV, state_sizeH, action_size))
import random

traci.simulationStep()
stateV=0
stateH=0
action=0
steps=1000000
paction=0
for j in range(steps):
	paction=action
	if (random.uniform(0,1)<epsilon):
		if (random.uniform(0,1)>.5):
			action=1
		else:
			action=0	
	else:
		if(Q[stateV,stateH,0]<Q[stateV,stateH,1]):
			action=1
		else:
			action=0
	if(action==1 and paction==action):
		traci.trafficlight.setProgram("n3", "HpassG")
	elif(action==1 and paction!=action):
		traci.trafficlight.setProgram("n3", "HpassY")
		traci.simulationStep()
		traci.simulationStep()
		traci.simulationStep()
		traci.trafficlight.setProgram("n3", "HpassG")
	elif(action==0 and paction==action):
		traci.trafficlight.setProgram("n3", "VpassG")
	elif(action==0 and paction!=action):
		traci.trafficlight.setProgram("n3", "VpassY")
		traci.simulationStep()
		traci.simulationStep()
		traci.simulationStep()
		traci.trafficlight.setProgram("n3", "VpassG")
	traci.simulationStep()
	epsilon=epsilon-.001
	num0=max(traci.edge.getLastStepVehicleNumber("1to3"),traci.edge.getLastStepVehicleNumber("2to3"))
	#if(num0>9):
	#	num0=9
	#print(num1)
	num1=max(traci.edge.getLastStepVehicleNumber("4to3"),traci.edge.getLastStepVehicleNumber("5to3"))
	#if(num1>9):
	#	num1=9
	#print(num2)
	new_stateV=num1
	new_stateH=num0
	#print(new_state)
	#if(new_state>99):
	#	new_state=99
	if (action==0):
		#reward=-traci.edge.getWaitingTime("1to3")-traci.edge.getWaitingTime("2to3")
		reward=num0-max(traci.edge.getWaitingTime("1to3"),traci.edge.getWaitingTime("2to3"))#-(traci.edge.getLastStepVehicleNumber("1to3")+traci.edge.getLastStepVehicleNumber("2to3"))
		#traci.edge.getLastStepMeanSpeed("1to3")+traci.edge.getLastStepMeanSpeed("2to3")
	else:
		#reward=-traci.edge.getWaitingTime("4to3")-traci.edge.getWaitingTime("5to3")
		reward=num1-max(traci.edge.getWaitingTime("4to3"),traci.edge.getWaitingTime("5to3"))#-(traci.edge.getLastStepVehicleNumber("4to3")+traci.edge.getLastStepVehicleNumber("5to3"))
	if(j>100):
		print(str(traci.edge.getWaitingTime("1to3"))+" "+str(traci.edge.getWaitingTime("2to3"))+" "+str(traci.edge.getWaitingTime("4to3"))+" "+str(traci.edge.getWaitingTime("5to3")))
	#print(Q)
	Q[stateV, stateH, action] = Q[stateV, stateH, action] + lr * (reward + gamma * np.max(Q[new_stateV, new_stateH, :]) - Q[stateV,stateH, action])
	stateV=new_stateV
	stateH=new_stateH