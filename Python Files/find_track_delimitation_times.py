# find_track_delimitation_times.py
# Finds places in each track where there is a time gap exceeds a threshold
# or a change in the velocity vector exceeds a threshold.
import sys, glob, math

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S 

def find_track_delimitation_times(dirname):
    sdmult = 20.0
    accelthresh = 0.0003
    timethreshes = {}
    with open(dirname + '/sampling_gaps_stats.csv', 'r', encoding='utf-8') as f:
        for line in f:
            pline = (endclean(line)).split(',')
            shipkey = pline[3]
            thresh = float(pline[1]) + sdmult*float(pline[2])
            timethreshes[shipkey] = thresh
    trackfiles = glob.glob(dirname + '/tracks/*')
    out = open(dirname + '/track_delimitation_times.csv', 'w')
    for trackfile in trackfiles:
        # print('Working on',trackfile)
        k = max(trackfile.rfind('/'),trackfile.rfind('\\'))
        shipkey = trackfile[k+7:len(trackfile)-4]
        timestamp1 = 0
        oldlatitude1 = 0.0
        oldlongitude1 = 0.0
        timestamp2 = 0
        oldlatitude2 = 0.0
        oldlongitude2 = 0.0
        with open(trackfile, 'r', encoding='utf-8') as f:
            for line in f:
                pline = (endclean(line)).split(',')
                xtimestamp = pline[0]
                if (xtimestamp.isdigit()):
                    timestamp = int(xtimestamp)
                else:
                    print('Warning: Faulty timestamp in',trackfile,'of', \
                          xtimestamp)
                    continue
                latitude = float(pline[1])
                longitude = float(pline[2])
                dt = timestamp-timestamp2
                if (dt <= 0):
                    out.write(shipkey + ',timeorder,' + str(timestamp2) + \
                              ',' + str(timestamp) + '\n')
                    print('Timestamp out of order in',shipkey,'at',timestamp)
                elif (timestamp2 > 0) and (dt > timethreshes[shipkey]):
                    out.write(shipkey + ',timegap,' + str(timestamp2) + ',' + \
                              str(timestamp) + ',' + str(round(latitude,5)) + \
                              str(',') + str(round(longitude,5)) + '\n')
                    print('Large time',timestamp2,'-',timestamp, \
                          'at',latitude,longitude,'for',shipkey)
                elif (timestamp2 > 0) and (timestamp1 > 0) and \
                     (timestamp2 != timestamp1):
                    latadj = math.sqrt(1-(oldlatitude2*oldlatitude2/8100))
                    lataccel = (latitude-(2*oldlatitude2)+oldlatitude1) / \
                        (timestamp-timestamp1)
                    longaccel = (longitude-(2*oldlongitude2)+oldlongitude1) \
                        * latadj / (timestamp-timestamp1)
                    acceltmp = (lataccel*lataccel)+(longaccel*longaccel)
                    accelnorm = math.sqrt(max(0,acceltmp))
                    if (accelnorm > accelthresh):
                        out.write(shipkey + ',accelnorm,' + \
                                  str(timestamp2) + ',' + \
                                  str(round(accelnorm,6)) + ',' + \
                                  str(round(oldlatitude2,5)) + ',' + \
                                  str(round(oldlongitude2,5)) + '\n')
                        print('Acceleration norm',accelnorm, \
                              timestamp1,'-',timestamp2,timestamp,'at', \
                              latitude,longitude,'for',shipkey)
                timestamp1 = timestamp2
                oldlatitude1 = oldlatitude2
                oldlongitude1 = oldlongitude2
                timestamp2 = timestamp
                oldlatitude2 = latitude
                oldlongitude2 = longitude
    out.close()

if __name__=="__main__":
    dirname = sys.argv[1]
    find_track_delimitation_times(dirname)
