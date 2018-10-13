# receive params.in in.idf ros.idf
from sys import argv
import re

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
	#print(tagValueDict)
	return tagValueDict
def replaceDecTag(template_file, new_file, tagValueDict):
	newfile_str=''
	with open(template_file) as templatefile:
		for line in templatefile:
			if re.search('\{\s*(\w+)\s*\}',line):
				tag=re.search('\{\s*(\w+)\s*\}',line).group(1)
				try:
					value=tagValueDict[tag]
				except:
					value=None
				if value:
					line=re.sub('\{\s*(\w+)\s*\}',value,line)
					print(line)
			newfile_str=newfile_str+line
	with open(new_file,'w') as newfile:
		newfile.write(newfile_str)

if __name__ == '__main__':
	paramsfile, templatefile, newfile = argv[1],argv[2],argv[3]
	tagValueDict=getTag(paramsfile)
	replaceDecTag(templatefile,newfile, tagValueDict)