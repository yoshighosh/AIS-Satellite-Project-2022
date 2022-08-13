# create_metadata.py
# Creates a metadata file of all the important features of ship tracks. The values of each column are listed in the text file metadata_table_values.txt. Each row represents a ship.
# Authors: Aroshi Ghosh, Lahari Y (6/2022)

import sys, os, os.path, glob, csv, math, linear_fit_all, logistic_function
from map_coords_to_latlong_bin_center import map_coords_to_latlong_bin_center
from collections import Counter

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
	S = OS
	M = len(S)
	while ((M > 0) and (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):
		S = S[0:M-1]
		M = M-1
	return S

def metadata(dirname1, dirname2):
	with open('metadata.csv', 'a', newline='') as file:
		writer = csv.writer(file)
		header = ['key', 'numeric type', 'string type', 'ID', 'time ratio', 'number of line segments', 'mean speed', 'standard deviation in speed', 'number of acceleration points', 'length', 'ratio of width to length', 'type of cargo', 'receiver class', 'number of neighbors', 'distance ratio']
		writer.writerow(header)
		path = dirname2 + '/cols_1_2_*.txt'
		xfilenames = glob.glob(path)
		row = 2
		for xfilename in xfilenames:
			print(row)
			key = xfilename[22:len(xfilename)-4]
			filename = dirname1 + '/track_' + key + '.csv'
			array = list(csv.reader(open(filename)))
			num_type = 0
			if (array[len(array)-1][3] != ''):
				num_type = array[len(array)-1][3]
			type = get_type(num_type)
			ID = ""
			if ("track_IMO" in xfilename):
				ID = "IMO"
			elif("track_CALL" in xfilename):
				ID = "call sign"
			else:
				ID = "MMSI"
			time_ratio = getTimeRatio(filename)
			num_lines = linear_fit_all.get_num_lines(xfilename)
			num_lines = logistic(num_lines, 4, 0.01)
			speed = getSpeed(key) # returns a list
			avg_speed = speed[0] # in nautical miles per hour
			avg_speed = logistic(avg_speed, 8, 0.1)
			sd_speed = speed[1] # standard deviation in speed
			sd_speed = logistic(sd_speed, 5, 0.03)
			acceleration = getAcceleration(filename)
			acceleration = logistic(acceleration, 2, 0.1)
			info = getInfo(key) # returns list
			length = float(info[0])
			log_length = logistic(length, 22, 0.1)
			width = float(info[1])
			ratio = 0
			if (length > 0):
				ratio = round(width/length, 4)
			cargo_type = info[2]
			receiver_class = info[3]
			num_neighbors = getNumNeighbors(filename)
			num_neighbors = logistic(num_neighbors, 5.368, 1)
			dist_ratio = getDistRatio(filename)
			data = [key, num_type, type, ID, time_ratio, num_lines, avg_speed, sd_speed, acceleration, log_length, ratio, cargo_type, receiver_class, num_neighbors, dist_ratio]
			writer = csv.writer(file)
			writer.writerow(data)
			row += 1
	
def get_type(item):
	item = int(item)
	if item in range(1,21) or item in range(23,30) or item in range(33, 35) or item in range(38, 52) or item in range(53, 60) or item in range(90, 1001) or item in range(1005, 1012) or item == 1018 or item == 1022:
		return "Other"
	elif item in range(21, 23) or item in range (31, 33) or item == 53 or item == 1023 or item == 1025:
		return "Tug Tow"
	elif item == 30 or item in range(1001, 1003):
		return "Fishing"
	elif item == 35 or item == 1021:
		return "Military"
	elif item in range(36, 38) or item == 1019:
		return "Pleasure Craft/Sailing"
	elif item in range(60, 70) or item in range(1012, 1016):
		return "Passenger"
	elif item in range(70, 80) or item in range(1003, 1005) or item == 1016:
		return "Cargo"
	elif item in range(80, 90) or item == 1017 or item == 1024:
		return "Tanker"
	else:
		return "Unknown"

def logistic(x, center, slope):
	val = logistic_function.logistic_function(x, center, slope)
	return round(val, 4)

def getTimeRatio(filename):
	array = list(csv.reader(open(filename)))
	moving_time = 0
	for r in range(len(array)-1):
		time_diff = float(array[r+1][0])-float(array[r][0])
		if (time_diff <= 10800): # don't include time gaps of 3 hours (10,800 seconds)
			moving_time += time_diff
	week_time = 604800 # 604,800 seconds in a week
	return round(moving_time/week_time, 4)

def getSpeed(key):
	with open('stated_speeds_per_ship.txt', 'r', encoding='utf-8') as f:
		for line in f:
			line = endclean(line)
			pline = line.split(',')
			if (pline[0] == key):
				avg_speed = 0
				sd_speed = 0
				if (len(pline[1]) > 0):
					avg_speed = pline[1]
				if (len(pline[2]) > 0):
					sd_speed = pline[2]
				list = [avg_speed, sd_speed]
				return list
		return [0,0]

def getAcceleration(filename):
	count = 0
	array = list(csv.reader(open('track_delimitation_times.csv')))
	with open(filename, 'r') as f:
		for line in f:
			line = endclean(line)
			pline = line.split(',')
			lat = round(float(pline[1]), 2)
			long = round(float(pline[2]), 2)
			for row in array:
				if row[1] == "accelnorm":
					if lat == round(float(row[4]), 2) and long == round(float(row[5]), 2):
						count += 1
	return count # max 1098

def getInfo(key): # returns all the info from all_metadata.csv
	length = 0
	width = 0
	cargo_type = 0
	array = list(csv.reader(open('all_metadata.csv')))
	info = []
	for row in array:
		if (row[0] == key):
			if (len(row[2]) > 0):
				length = row[2]
			if (len(row[3]) > 0):
				width = row[3]
			if (len(row[4]) > 0):
				cargo_type = row[4]
			rec_class = row[5]
			info = [length, width, cargo_type, rec_class]
			return info

def getNumNeighbors(filename):
	count = 0
	total = 0
	array = list(csv.reader(open('geohist_1.0_by_position.csv')))
	with open(filename, 'r') as f:
		for line in f:
			line = endclean(line)
			pline = line.split(',')
			lat = map_coords_to_latlong_bin_center(float(pline[1]), 1.0)
			long = map_coords_to_latlong_bin_center(float(pline[2]), 1.0)
			num = 0
			for row in array:
				if (num != 0):
					if float(row[0]) == lat:
						if round(float(row[1]), 1) == long:
							count += 1
							total += float(row[2])
				num += 1
	average = 0
	if (count > 0):
		average = total/count
	log_average = math.log(1+average, 10)
	return round(log_average, 4)

def getDistRatio(filename):
	array = list(csv.reader(open(filename)))
	tot_dist = 0
	for r in range(len(array)-1):
		lat1 = float(array[r][1])
		lat2 = float(array[r+1][1])
		long1 = float(array[r][2])
		long2 = float(array[r+1][2])
		tot_dist += track_speed.calc_distance(lat1, lat2, long1, long2)
	displacement = 0
	lat1 = float(array[0][1])
	lat2 = float(array[len(array)-1][1])
	long1 = float(array[0][2])
	long2 = float(array[len(array)-1][2])
	displacement = track_speed.calc_distance(lat1, lat2, long1, long2)
	ratio = 0
	if (tot_dist > 0):
		ratio = displacement/tot_dist
	#print displacement, tot_dist, round(ratio, 4)
	return round(ratio, 4)

if __name__ == "__main__":
	dirname1 = sys.argv[1] # directory of track files
	dirname2 = sys.argv[2] # directory of linear fit output files
	metadata(dirname1, dirname2)
	#filename = sys.argv[1]
	#print(getDistRatio(filename))
	