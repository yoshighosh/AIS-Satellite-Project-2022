# linear_fit_all.py
# runs the given data through extractcols.py and linear_fit_general.py, and outputs the important values to an output file
# Author: Lahari Yallapragada, 6/2022

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
	ship_tracks = linear_fit_general.linear_fit_general(xypairs)
	M = ship_tracks[0]
	B = ship_tracks[1]
	error = ship_tracks[2]
	SD = ship_tracks[3]
	if (SD > 0.6):
		inFileMod = "output/" + inFile[13:len(inFile)-4]
		print(inFileMod)
		file = inFileMod + ".txt"
		if (error < 0.3):
			with open(file, 'a') as f:
				f.write(str(M) + "*X + "+ str(B) + " with mean error " + str(error) + ", and standard deviation " + str(SD))
		else:
			#open(file, 'w').close()
			total = len(xypairs)
			half = total // 2
			linear_fit(xypairs[:half], inFile)
			linear_fit(xypairs[half:], inFile)
	else:
		print("ship is not moving")
	

	
if __name__ == "__main__":
	inFile = sys.argv[1]
	delim = sys.argv[2]
	xypairs = []
	with open(inFile, 'r') as f:
		for line in f:
			pline = (endclean(line)).split(delim)
			xypairs.append(list([float(pline[0]),float(pline[1])]))
	linear_fit(xypairs, inFile)



#for xfile in xfilenames:
	#extractcols.extractcols(xfile,",",[1,2])
	#xfilenames = glob.glob(dirname + 'cols_1_2_track_*.csv')
	#with open("ship_tracks_vals.out", "w", encoding="utf-8") as f:
		#for xfile in xfilenames:
			#f.write(linear_fit_general.linear_fit_general(xfile, ","))
			#f.write("\n")
