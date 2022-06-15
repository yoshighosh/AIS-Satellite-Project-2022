# final_linear_fit.py

import sys, os, os.path, glob, extractcols, linear_fit_all

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
	S = OS
	M = len(S)
	while ((M > 0) and (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):
		S = S[0:M-1]
		M = M-1
	return S

def extract_file_cols(dirname):
	xfilenames = glob.glob(dirname + '/track*.csv')
	filelist = []
	for xfilename in xfilenames:
		extractcols.extractcols(xfilename, ",", [1,2])

def linear_fit():
	xfilenames = glob.glob('firstTwoCols/cols*.csv')
	filelist = []
	for xfilename in xfilenames:
		linear_fit_all.linear_fit_all(xfilename, ",")

if __name__=="__main__":
	#extract_file_cols(r"data\tracks")
	linear_fit()