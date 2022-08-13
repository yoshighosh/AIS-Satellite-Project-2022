# get_geo_hist.py
# Creates a histogram of all locations in track data rounded to the
# nearest fraction of a degree of latitude, defined by the 2nd arg.
import sys, glob, math, map_coords_to_latlong_bin_center

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S   

def get_geo_hist(dirname,granularity):
    # Search the track files to for latitude-longitude pairs,
    # and map these to approximately square bins whose dimensions
    # are the granularity times a degree of latitude.
    geohist = {}
    filenames = glob.glob(dirname + '/tracks/track_*.csv')
    print(len(filenames),'track files found')
    for filename in filenames:
        k = filename.find('track_')
        xfilename = filename[k+6:len(filename)-4]
        print('Working on',xfilename)
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                pline = (endclean(line)).split(',')
                xlatitude = float(pline[1])
                xlongitude = float(pline[2])
                if (xlatitude > 55) or (xlatitude < 5) or \
                   (xlongitude > -45) or (xlongitude < -155):
                    continue
                latitude,longitude = map_coords_to_latlong_bin_center.map_coords_to_latlong_bin_center(xlatitude,xlongitude,granularity)
                key = str(latitude) + '|' + str(longitude)
                geohist[key] = geohist.get(key,0) + 1
    # Also look out counts of the "inflection points" found by
    # find_track_delimitation_times.py, and also put into lat-long bins.
    inflectionhist = {}
    with open(dirname+'/track_delimitation_times.csv','r',encoding='utf-8') as f:
        for line in f:
            pline = (endclean(line)).split(',')
            xlatitude = float(pline[4])
            xlongitude = float(pline[5])
            latitude,longitude = map_coords_to_latlong_bin_center.map_coords_to_latlong_bin_center(xlatitude,xlongitude,granularity)
            key = str(latitude) + '|' + str(longitude)
            inflectionhist[key] = inflectionhist.get(key,0) + 1
    print('Finished counting track delimitation times')
    geolist = []
    for key in geohist.keys():
        kb = key.find('|')
        latitude = float(key[0:kb])
        longitude = float(key[kb+1:len(key)])
        count = geohist[key]
        icount = inflectionhist.get(key,0)
        inflectionfrac = float(icount)/count
        geolist.append(list([latitude,longitude,count,inflectionfrac]))
    geolist = sorted(geolist)
    out = open(dirname + '/geohist_' + str(granularity) + '_by_position.csv', 'w')
    for geoitem in geolist:
        out.write(str(geoitem[0]) + ',' + str(geoitem[1]) + ',' + \
                  str(geoitem[2]) + ',' + str(round(geoitem[3],10)) + '\n')
    out.close()
    geolist = []
    for key in geohist.keys():
        kb = key.find('|')
        latitude = float(key[0:kb])
        longitude = float(key[kb+1:len(key)])
        count = geohist[key]
        icount = inflectionhist.get(key,0)
        inflectionfrac = float(icount)/count
        geolist.append(list([inflectionfrac,count,latitude,longitude]))
    geolist = sorted(geolist, reverse=True)
    out = open(dirname + '/geohist_' + str(granularity) + '_by_count.csv', 'w')
    for geoitem in geolist:
        out.write(str(geoitem[0]) + ',' + str(geoitem[1]) + ',' + \
                  str(geoitem[2]) + ',' + str(round(geoitem[3],5)) + '\n')
    out.close()
                
if __name__=="__main__":
    dirname = sys.argv[1]
    mult = float(sys.argv[2])
    get_geo_hist(dirname,mult)
