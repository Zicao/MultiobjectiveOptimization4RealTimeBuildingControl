#run optimization
import csv
import numpy as np 
import pandas as pd
import os
import re
from sklearn import svm
import time
from dateutil.parser import parse
from sklearn.externals import joblib


def getHM(time_string):
    return [parse(time_string).hour,parse(time_string).minute]

def checkDateTimes(dateTimes):
    #print(dateTimes[0])
    if re.search('24:00:00',dateTimes[0]):
        dateTimes[0]=re.sub('24:00:00','00:00:00',dateTimes[0])
    return dateTimes[0]

#get input parameters. Some parameters, such as site environmental statues, are constant. And some other parameters are generated by
#by SVM model, i.e. the output of step k are the input of step of K+1.


#write output
#write PMV and EnergyCost
#
def getTag(params_file):
	'''
	'''
	tagValueDict={}
	with open(params_file) as paramsfile:
		for line in paramsfile:
			if re.search('\{\s*(\w+)\s*=\s*(-?(\d+\\.?\d*|\.\d+)[eEdD](\+|-)?\d+)\s*\}',line,re.I):
				tag=re.search('\{\s*(\w+)\s*=\s*(-?(\d+\\.?\d*|\.\d+)[eEdD](\+|-)?\d+)\s*\}',line,re.I).group(1)
				value=re.search('\{\s*(\w+)\s*=\s*(-?(\d+\\.?\d*|\.\d+)[eEdD](\+|-)?\d+)\s*\}',line,re.I).group(2)
				tagValueDict[tag]=value
			elif re.search('\{\s*(\w+)\s*=\s*(\d+\\.?\d*)\s*\}',line,re.I):
				tag=re.search('\{\s*(\w+)\s*=\s*(\d+\\.?\d*)\s*\}',line,re.I).group(1)
				value=re.search('\{\s*(\w+)\s*=\s*(\d+\\.?\d*)\s*\}',line,re.I).group(2)
				tagValueDict[tag]=value
			elif re.search('\{\s*([^\s]+)\s*=\s*(\d+\\.?\d*)\s*\}',line,re.I):
				tag=re.search('\{\s*([^\s]+)\s*=\s*(\d+\\.?\d*)\s*\}',line,re.I).group(1)
				value=re.search('\{\s*([^\s]+)\s*=\s*(\d+\\.?\d*)\s*\}',line,re.I).group(2)
				tagValueDict[tag]=value
	return tagValueDict

def calcTemp(testX_temp):
	clf_temp=joblib.load('BigTempWithDecisionTree.m')
	predicted_temp=clf_temp.predict(testX_temp)
	return predicted_temp

def calcEnergy(testX_energy,testX_PMV):
	clf_energy = joblib.load("BigEnergyWithDecisionTree.m")
	predicted_energy=clf_energy.predict(testX_energy)
	elec_price=[0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,#89\
            1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,#1011\
            1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,2.92,2.92,2.92,2.92,2.92,2.92,#1213\
            2.92,2.92,2.92,2.92,2.92,2.92,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,0.8595,#14,15\
            1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782,1.3782]#16,17
	TOU=np.array(elec_price)
	#print(predicted_energy)
	energy_cost=predicted_energy.dot(TOU.T)/12000
	PMV=calcPMV(testX_PMV)
	sumPMV=2800*np.absolute(PMV).sum()
	return energy_cost,sumPMV


def calcPMV(testX_PMV):
	clf_PMV = joblib.load('BigPMVWithDecisionTree.m')
	predicted_PMV = clf_PMV.predict(testX_PMV)
	return predicted_PMV

def readData():
	x_values=np.load('x_value_big.npy')
	if x_values is not None:
		x_values_temp=x_values[:,[0,1,2,3,4,6,7]]
		x_values_PMV=x_values[:,:6]
		x_values_energy=x_values
		return x_values_temp,x_values_PMV,x_values_energy
	else:
		print('error with x_values')

if __name__ == '__main__':
	x_values_temp,x_values_PMV,x_values_energy=readData()
	y_values_temp=calcTemp(x_values_temp)
	on_off_schedule=np.zeros(36)
	indexOf1st1=np.argwhere(y_values_temp[30:66]>29)
	on_off_schedule[indexOf1st1[0,0]:36]=1
	x_values_PMV[:,5]=y_values_temp

	tagValueDict=getTag('params.in')

	x_values_energy[30:36,]=tagValueDict['ClTemp1100']
	x_values_energy[36:42,]=tagValueDict['ClTemp1130']
	x_values_energy[42:48,]=tagValueDict['ClTemp1200']
	x_values_energy[48:54,]=tagValueDict['ClTemp1230']
	x_values_energy[54:66,]=tagValueDict['ClTemp1330']
	x_values_energy[30:66,7]=on_off_schedule
	energy_cost,sumPMV=calcEnergy(x_values_energy,x_values_PMV)
	print(energy_cost,sumPMV)