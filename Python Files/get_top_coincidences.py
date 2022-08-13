import matplotlib.pyplot as plt
import sys, os, os.path, glob, csv
from numpy import nan
    



array = list(csv.reader(open('data/tracks/pairs_large.csv')))
ships = list(csv.reader(open('data/tracks/bins/ship_index.csv')))
print(array[1])
pairs = {}

zero = 0
one = 0
two = 0
three = 0
four = 0
five = 0
six = 0
seven = 0
total = 0

for id1 in range(len(array)):
    if id1%2 == 0:
        for id2 in range(int(len(array)/2)):
            #print(array[id1][id2])
            if id1 < id2:
                ship1 = ships[id1][1]
                ship2 = ships[id2*2][1]
                pair_name = ship1 + "_" + ship2
                print(pair_name)
                print(array[id1][id2])
                pairs[pair_name] = array[id1][id2]
                total += 1
                num = int(array[id1][id2])
                if num == 0:
                    zero += 1
                elif num == 1:
                    one += 1
                elif num == 2:
                    two += 1
                elif num == 3:
                    three += 1
                elif num == 4:
                    four += 1
                elif num == 5:
                    five += 1
                elif num == 6:
                    six += 1
                elif num == 7:
                    seven += 1

print("There were " + str(zero) + " pairs with no coincidences")
print("There were " + str(one) + " pairs with 1 coincidences")
print("There were " + str(two) + " pairs with 2 coincidences")
print("There were " + str(three) + " pairs with 3 coincidences")
print("There were " + str(four) + " pairs with 4 coincidences")
print("There were " + str(five) + " pairs with 5 coincidences")
print("There were " + str(six) + " pairs with 6 coincidences")
print("There were " + str(seven) + " pairs with 7 coincidences")
print("There were " + str(total) + " total unique pairs checked")

path = 'coincidences.csv'

    
with open(path, 'a') as file:
    writer = csv.writer(file)
    for pair in pairs:
        row = [pair, pairs[pair]]
        writer.writerow(row)
    