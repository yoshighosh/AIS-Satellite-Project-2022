# combine_cols_AIS.py
# Author: Aroshi Ghosh, Lahari Y (7/2022)

import sys, os, os.path, glob, csv

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
	S = OS
	M = len(S)
	while ((M > 0) and (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):
		S = S[0:M-1]
		M = M-1
	return S

def get_cols(dirname, colnum, outfile):
	out = open(outfile, 'a', newline='')
	xfilenames = glob.glob(dirname + '/AIS*.csv')
	for xfilename in xfilenames:
		with open(xfilename, 'r', encoding='utf-8') as f:
			print("opened " + xfilename)
			line_num = 1
			for line in f:
				if (line_num != 1):
					line = endclean(line)
					pline = line.split(',')
					val = pline[colnum]
					print(val)
					out.write(val + '\n')
				line_num += 1
			print("finished " + xfilename)
	out.close()

def get_cols_mod(dirname, colnum, outfile):
	out = open(outfile, 'a', newline='')
	with open('data\AIS_2021_12_01.csv', 'r', encoding='utf-8') as f:
		print("opened AIS_2021_12_01.csv")
		line_num = 1
		for line in f:
			if (line_num != 1):
				line = endclean(line)
				pline = line.split(',')
				val = pline[colnum]
				print(val)
				out.write(val + '\n')
			line_num += 1
		print("finished AIS_2021_12_01.csv")
	with open('data\AIS_2021_12_02.csv', 'r', encoding='utf-8') as f:
		print("opened AIS_2021_12_02.csv")
		line_num = 1
		for line in f:
			if (line_num != 1):
				line = endclean(line)
				pline = line.split(',')
				val = pline[colnum]
				print(val)
				out.write(val + '\n')
			line_num += 1
		print("finished AIS_2021_12_02.csv")
	with open('data\AIS_2021_12_03.csv', 'r', encoding='utf-8') as f:
		print("opened AIS_2021_12_03.csv")
		line_num = 1
		for line in f:
			if (line_num != 1):
				line = endclean(line)
				pline = line.split(',')
				val = pline[colnum]
				print(val)
				out.write(val + '\n')
			line_num += 1
		print("finished AIS_2021_12_03.csv")
	with open('data\AIS_2021_12_04.csv', 'r', encoding='utf-8') as f:
		print("opened AIS_2021_12_04.csv")
		line_num = 1
		for line in f:
			if (line_num != 1):
				line = endclean(line)
				pline = line.split(',')
				val = pline[colnum]
				print(val)
				out.write(val + '\n')
			line_num += 1
		print("finished AIS_2021_12_04.csv")
	with open('data\AIS_2021_12_05.csv', 'r', encoding='utf-8') as f:
		print("opened AIS_2021_12_05.csv")
		line_num = 1
		for line in f:
			if (line_num != 1):
				line = endclean(line)
				pline = line.split(',')
				val = pline[colnum]
				print(val)
				out.write(val + '\n')
			line_num += 1
		print("finished AIS_2021_12_05.csv")
	with open('data\AIS_2021_12_06.csv', 'r', encoding='utf-8') as f:
		print("opened AIS_2021_12_06.csv")
		line_num = 1
		for line in f:
			if (line_num != 1):
				line = endclean(line)
				pline = line.split(',')
				val = pline[colnum]
				print(val)
				out.write(val + '\n')
			line_num += 1
		print("finished AIS_2021_12_06.csv")
	with open('data\AIS_2021_12_07.csv', 'r', encoding='utf-8') as f:
		print("opened AIS_2021_12_07.csv")
		line_num = 1
		for line in f:
			if (line_num != 1):
				line = endclean(line)
				pline = line.split(',')
				val = pline[colnum]
				print(val)
				out.write(val + '\n')
			line_num += 1
		print("finished AIS_2021_12_07.csv")
	out.close()

if __name__ == "__main__":
	dirname = sys.argv[1]
	colnum = sys.argv[2]
	outfile = sys.argv[3]
	#get_cols(dirname, int(colnum), outfile)
	get_cols_mod(dirname, int(colnum), outfile)