from sys import argv
import csv
import re
import os
def avePmv(resultsfile,outputfile):
	sum_pmv=0.0
	iteration_num=0
	day=0
	hour=0
	valid_iteration_num=0
	with open(resultsfile,"r") as results_file:
		results_file_csv=csv.reader(results_file)
		headers = next(results_file_csv)
		#Row = namedtuple('Row', headings)
		for row in results_file_csv:
			iteration_num +=1
			day=int(iteration_num/1440)
			hour=int(iteration_num/60)-day*24

			if (hour>=8 and hour<=17 and day>=0 and day<=4):
				sum_pmv += float(row[12])
				valid_iteration_num +=1
	average_pmv=sum_pmv/valid_iteration_num
	with open(outputfile,"w") as input_file:
		input_file.write(str(average_pmv)+"\n")

def squaredPmv(resultsfile,workTable,outputfile,Wpmv):
	sum_pmv=0.0
	iteration_num=0
	day=0
	hour=0
	valid_iteration_num=0
	timestep=5
	#WpmvList=[]
	with open(resultsfile,"r") as results_file:
		results_file_csv=csv.reader(results_file)
		for row in results_file_csv:
			iteration_num +=1
			day=int(iteration_num*timestep/1440)
			hour=int(iteration_num*timestep/60)-day*24
			if (hour>=8 and hour<=16 and day>=0 and day<=4):
				pmv=float(row[13])
				sum_pmv +=abs(pmv)
				valid_iteration_num +=1

	energy_cost=writeEnergyCost(workTable,outputfile)
	print('energy',energy_cost)
	print('sum_pmv',sum_pmv)
	try:
		Wpmv=3.82
	except:
		Wpmv=5.5
	#print('Wpmv',Wpmv)
	pmvSum=Wpmv*sum_pmv
	#print('pmvSum',pmvSum)
	with open(outputfile,"a+") as input_file:
		input_file.write(str(energy_cost)+"\n")
		input_file.write(str(pmvSum))

def writeEnergyCost(workTable,outputfile):
	energy_cost=0
	with open(workTable,"r") as work_Table:
		for line in work_Table:
			matchedenergy=re.findall(r'EnergyCharges\s\(.{1}\),((\d+\.\d*),){6}(\d+\.\d*).+',line,re.I) 
			if matchedenergy:
				energy_cost=matchedenergy[0][2]
	return energy_cost

def Wpmv_cal(objectivefile):
	pmv_column=[]
	energycost_column=[]
	Wpmv_column=[]
	Wpmv=5.1
	i=-1
	with open(objectivefile) as objective_file:
		objective_file_csv=csv.reader(objective_file)
		#headers=next(objective_file_csv)
		for row in objective_file_csv:
			i+=1
			if i>1 and i<=10:
				pmv_column.append(row[0])
				energycost_column.append(row[1])
				Wpmv_column.append(row[2])
				Wpmv=float(row[1])/float(row[0])
			elif i==1:
				pmv_column.append(row[0])
				energycost_column.append(row[1])
				Wpmv=float(row[1])/float(row[0])
			elif i>=11:
				Wpmv_column.sort()
				Wpmv=float(Wpmv_column[0])
	return Wpmv
'''Wpmv=5.0
squaredPmv(argv[1],argv[2],argv[3],Wpmv)'''
if __name__ == '__main__':
	Wpmv=5.0
	squaredPmv('work.csv','workTable.csv','results.out',Wpmv)#work.csv workTable.csv results.out
 