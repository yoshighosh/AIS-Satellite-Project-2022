# Change path variables to location of track files
# Returns a matrix which ships as the rows and columns to plot which pairs of ships have a coincidence


import matplotlib.pyplot as plt
import sys, os, os.path, glob, csv
from numpy import nan
from map_coords_to_latlong_bin_center import map_coords_to_latlong_bin_center
    


xfilenames = glob.glob('data/tracks/track*.csv')
   
def get_ship_keys():
    ships = {}
    id = -1
    for xfilename in xfilenames:
        ship = {"id" : [id, xfilename[18:len(xfilename)-4]], "day_1" : [], "day_2" : [], "day_3" : [], "day_4" : [], "day_5" : [], "day_6" : [], "day_7" : []}
        id += 1
        array = list(csv.reader(open(xfilename)))
        for row in array:
            try:
                print(row[1], row[2])
                lat, long = map_coords_to_latlong_bin_center(float(row[1]), float(row[2]), 1.0)
                bin_name = str(lat) + "_" + str(long)
                print(row[0])
                if int(row[0]) in range(1638316800, 1638403200):
                    day_list = ship["day_1"]
                elif int(row[0]) in range(1638403200, 1638489600):
                    day_list = ship["day_2"]
                elif int(row[0]) in range(1638489600, 1638576000):
                    day_list = ship["day_3"]
                elif int(row[0]) in range(1638576000, 1638662400):
                    day_list = ship["day_4"]
                elif int(row[0]) in range(1638662400, 1638748800):
                    day_list = ship["day_5"]
                elif int(row[0]) in range(1638748800, 1638835200):
                    day_list = ship["day_6"]
                elif int(row[0]) in range(1638835200, 1638921600):
                    day_list = ship["day_7"]
                print(day_list)
                if bin_name not in day_list:
                    day_list.append(bin_name)
            except:
                print("Empty Row")
        ships[id] = ship
        print(ship, id)
        path = 'data/tracks/bins/bins_' + xfilename[18:]
        with open(path, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(ship["day_1"])
            writer.writerow(ship["day_2"])
            writer.writerow(ship["day_3"])
            writer.writerow(ship["day_4"])
            writer.writerow(ship["day_5"])
            writer.writerow(ship["day_6"])
            writer.writerow(ship["day_7"])
        path = 'data/tracks/bins/ship_index'
        with open(path, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(ship["id"])
    return ships


def get_pair_counts(ships):
    pair_matrix = [[0 for col in range(len(ships))] for row in range(len(ships))]
    for id1 in range(0, len(ships)):
        for id2 in range(0, len(ships)):
            try:
                for bin in ships[id1]["day_1"]:
                    if bin in ships[id2]["day_1"]:
                        print(id1, id2)
                        pair_matrix[id1][id2] += 1
                        break
                for bin in ships[id1]["day_2"]:
                    if bin in ships[id2]["day_2"]:
                        print(id1, id2)
                        pair_matrix[id1][id2] += 1
                        break
                for bin in ships[id1]["day_3"]:
                    if bin in ships[id2]["day_4"]:
                        print(id1, id2)
                        pair_matrix[id1][id2] += 1
                        break
                for bin in ships[id1]["day_4"]:
                    if bin in ships[id2]["day_4"]:
                        print(id1, id2)
                        pair_matrix[id1][id2] += 1
                        break
                for bin in ships[id1]["day_5"]:
                    if bin in ships[id2]["day_5"]:
                        print(id1, id2)
                        pair_matrix[id1][id2] += 1
                        break
                for bin in ships[id1]["day_6"]:
                    if bin in ships[id2]["day_6"]:
                        print(id1, id2)
                        pair_matrix[id1][id2] += 1
                        break
                for bin in ships[id1]["day_7"]:
                    if bin in ships[id2]["day_7"]:
                        print(id1, id2)
                        pair_matrix[id1][id2] += 1
                        break
            except:
                print("index out of range")
    return pair_matrix
                

ships = get_ship_keys()
print(ships)
pairs = get_pair_counts(ships)
print(pairs)
path = 'data/tracks/pairs_large.csv'
with open(path, 'a') as file:
    writer = csv.writer(file)
    for row in pairs:
         writer.writerow(row)




