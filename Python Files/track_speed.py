# track_speed.py
# Creates a new file for each ship track with the time difference, distance traveled, and speed (in nautical miles per hour) in each row. Then it calculates the average speed for one ship. 
# Authors: Aroshi Ghosh, Lahari Y (6/2022)

import sys, os, os.path, glob, csv, math
import numpy as np

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
	S = OS
	M = len(S)
	while ((M > 0) and (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):
		S = S[0:M-1]
		M = M-1
	return S

def track_speed(dirname):
	xfilenames = glob.glob(dirname + '/track*.csv')
	for xfilename in xfilenames:
		array = list(csv.reader(open(xfilename)))
		path = 'track_avg_speed\speed_' + xfilename[12:]
		with open(path, 'a', newline='') as file:
			writer = csv.writer(file)
			if (len(array) <= 1):
				data = [0, 0, 0]
				writer.writerow(data)
			elif (len(array) >= 2 and len(array) <= 5):		
				time_diff = abs(float(array[len(array)-1][0])-float(array[0][0]))
				lat1 = float(array[0][1])
				lat2 = float(array[len(array)-1][1])
				long1 = float(array[0][2])
				long2 = float(array[len(array)-1][2])
				distance = calc_distance(lat1, lat2, long1, long2) # in nautical miles
				speed = (distance / time_diff) *3600 # in nautical miles per hour
				data = [time_diff, distance, speed] 
				print(data)
				writer.writerow(data)
			else: # if length of array is greater than 5
				for r in range(len(array)-5):		
					time_diff = abs(float(array[r+5][0])-float(array[r][0]))
					lat1 = float(array[r][1])
					lat2 = float(array[r+5][1])
					long1 = float(array[r][2])
					long2 = float(array[r+5][2])
					distance = calc_distance(lat1, lat2, long1, long2)
					speed = (distance / time_diff) *3600
					data = [time_diff, distance, speed]
					print(data)
					writer.writerow(data)
		
def calc_distance(lat1, lat2, long1, long2):
	latdiff = (lat2-lat1)*60 # converting to nautical miles
	longdiff = (long2-long1)*60
	correction_factor = math.sqrt(abs(1-((latdiff/90)**2)))
	longitude = correction_factor * longdiff
	distance = math.sqrt((latdiff**2) + (longitude**2)) # euclidean distance formula
	return distance # in nautical miles

def get_avg_speed(filename):
	array = list(csv.reader(open(filename)))
	num_rows = len(array)
	print(num_rows)
	total_speed = 0
	for r in range(num_rows):
		if (len(array[r]) != 0): 
			total_speed += float(array[r][2])
	avg_speed = total_speed / num_rows
	return round(avg_speed, 4) # in nautical miles per hour

def get_median_speed(filename):
	array = list(csv.reader(open(filename)))
	speed = []
	for r in range(len(array)):
		if (len(array[r]) > 0):
			speed.append(float(array[r][2]))
	median_speed = np.median(speed)
	return round(median_speed, 4)
	
if __name__ == "__main__":
	dirname = sys.argv[1]
	track_speed(dirname)
	#filename = sys.argv[1]
	#speed = get_median_speed(filename)
	#print(speed)
