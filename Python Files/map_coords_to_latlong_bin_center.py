# map_coords_to_latlong_bin_center.py
# Maps a pair of latitude and longitude coordinates to the center of
# a roughly square bin whose sides are one degree of latitude times
# the granularity.
import sys, math

def map_coords_to_latlong_bin_center(latitude,longitude,granularity):
    centerlat = round(latitude/granularity)*granularity
    longgranularity = granularity / \
        math.sqrt(1-((latitude*latitude)/(90*90)))
    centerlong = round(longitude/longgranularity)*longgranularity
    return centerlat,centerlong

if __name__=="__main__":
    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])
    granularity = float(sys.argv[3])
    print(map_coords_to_latlong_bin_center(latitude,longitude,granularity))
