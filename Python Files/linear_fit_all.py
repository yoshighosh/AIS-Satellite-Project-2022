# linear_fit_all.py
# runs the given data through extractcols.py and linear_fit_general.py, and outputs the important values to an output file
# Author: Aroshi Ghosh, Lahari Y, 6/2022

import sys, os, os.path, glob, extractcols, linear_fit_general

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S

def linear_fit_all(inFile, delim):
	xypairs = []
	with open(inFile, 'r') as f:
		for line in f:
			pline = (endclean(line)).split(delim)
			xypairs.append(list([float(pline[0]),float(pline[1])]))
	linear_fit(xypairs, inFile)

def linear_fit(xypairs, inFile):
	file = "output/" + inFile[13:len(inFile)-4] + ".txt"	
	total = len(xypairs)
	half = total // 2
	# checking to see if the first half is crazy before splitting it in half
	equation = linear_fit_general.linear_fit_general(xypairs[:half])
	M = float(equation[0])
	B = float(equation[1])
	error = float(equation[2])
	SD = float(equation[3])
	if (error < 0.00003):
		with open(file, 'a') as f:
			f.write(str(M) + "*X + "+ str(B) + " with mean error " + str(error) + ", and standard deviation " + str(SD))
			f.write("\n")
	else:
		linear_fit(xypairs[:half], inFile)
	# checking to see if the second half is crazy before splitting it in half
	equation = linear_fit_general.linear_fit_general(xypairs[half:])
	M = equation[0]
	B = equation[1]
	error = equation[2]
	SD = equation[3]
	if (error < 0.3):
		with open(file, 'a') as f:
			f.write(str(M) + "*X + "+ str(B) + " with mean error " + str(error) + ", and standard deviation " + str(SD))
			f.write("\n")
	else:
		linear_fit(xypairs[half:], inFile)

def get_num_lines(inFile):
	num_lines = 0
	#path = "output\\" + inFile[7:len(inFile)-4] + ".txt"
	fileObj = open(inFile, 'r')
	file = fileObj.read().splitlines() # array
	if (len(file) == 2 and file[0] == file[1]):
			num_lines += 1
	else: 
		for row in file:
			num_lines += 1
	return num_lines
	
if __name__ == "__main__":
	inFile = sys.argv[1]
	delim = sys.argv[2]
	xypairs = []
	with open(inFile, 'r') as f:
		for line in f:
			pline = (endclean(line)).split(delim)
			xypairs.append(list([float(pline[0]),float(pline[1])]))
	linear_fit(xypairs, inFile)
	#print(get_num_lines(inFile))
