#!/usr/bin/env python

# Read DAKOTA parameters file (aprepro or standard format) and call a
# Python module rosenbrock for analysis.  Uses same rosenbrock.py as
# linked case for consistency.

# DAKOTA will execute this script as
#   rosenbrock_bb.py params.in results.out
# so sys.argv[1] will be the parameters file and
#    sys.argv[2] will be the results file to return to DAKOTA

# necessary python modules
import sys
import re
import os
import time
import numpy as np
# ----------------------------
# Parse DAKOTA parameters file
# ----------------------------

# setup regular expressions for parameter/label matching
e = '-?(?:\\d+\\.?\\d*|\\.\\d+)[eEdD](?:\\+|-)?\\d+' # exponential notation
f = '-?\\d+\\.\\d*|-?\\.\\d+'                        # floating point
i = '-?\\d+'                                         # integer
value = e+'|'+f+'|'+i                                # numeric field
tag = '\\w+(?::\\w+)*'                               # text tag field

# regular expression for aprepro parameters format
aprepro_regex = re.compile('^\s*\{\s*(' + tag + ')\s*=\s*(' + value +')\s*\}$')
# regular expression for standard parameters format
standard_regex = re.compile('^\s*(' + value +')\s+(' + tag + ')$')

# open DAKOTA parameters file for reading
paramsfile = open(sys.argv[1], 'r')

# extract the parameters from the file and store in a dictionary
paramsdict = {}
for line in paramsfile:
    m = aprepro_regex.match(line)
    if m:
        paramsdict[m.group(1)] = m.group(2)
    else:
        m = standard_regex.match(line)
        if m:
            paramsdict[m.group(2)] = m.group(1)

paramsfile.close()



# execute the rosenbrock analysis as a separate Python module
print("Running calculation...")
t0=time.time()

from subEPlus import calcTemp,calcEnergy,readData,getTag

x_values_temp,x_values_PMV,x_values_energy=readData()
y_values_temp=calcTemp(x_values_temp)
on_off_schedule=np.zeros(36)
indexOf1st1=np.argwhere(y_values_temp[30:66]>29)
on_off_schedule[indexOf1st1[0,0]:36]=1

x_values_PMV[:,5]=y_values_temp

tagValueDict=paramsdict

x_values_energy[30:36,]=tagValueDict['ClTemp1100']
x_values_energy[36:42,]=tagValueDict['ClTemp1130']
x_values_energy[42:48,]=tagValueDict['ClTemp1200']
x_values_energy[48:54,]=tagValueDict['ClTemp1230']
x_values_energy[54:66,]=tagValueDict['ClTemp1330']
x_values_energy[30:66,7]=on_off_schedule
#'ClTemp1100' 'ClTemp1130'  'ClTemp1200' 'ClTemp1230' 'ClTemp1330'
energy_cost,sumPMV=calcEnergy(x_values_energy,x_values_PMV)
print("calculation complete.",'\tTime Cost',time.time()-t0)


# ----------------------------
# Return the results to DAKOTA
# ----------------------------

# write the results.out file for return to DAKOTA
# this example only has a single function, so make some assumptions;
# not processing DVV
outfile = open('results.out.tmp', 'w')

# write functions
outfile.write(str(energy_cost)+'\n')
outfile.write(str(sumPMV))
outfile.close()

# move the temporary results file to the one DAKOTA expects
import shutil
shutil.move('results.out.tmp', sys.argv[2])
#os.system('mv results.out.tmp ' + sys.argv[2])
