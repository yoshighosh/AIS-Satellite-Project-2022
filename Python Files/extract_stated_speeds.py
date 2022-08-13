# extract_stated_speeds.py
import sys, glob, math, histcol, random, extract_ship_key

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S

def extract_stated_speeds(dirname,samplingratio):
    filenames = glob.glob(dirname + '/AIS*.csv')
    speedfile = dirname + '/stated_speeds.txt'
    out = open(speedfile, 'w')
    for filename in filenames:
        print('Working on',filename)
        with open(filename, 'r') as f:
            for line in f:
                pline = (endclean(line)).split(',')
                speed = pline[4]
                if (speed == 'SOG'):
                    continue
                fspeed = float(speed)
                if (fspeed >= 1.0) and (fspeed <= 60):
                    out.write(speed + '\n')
    out.close()
    histcol.histcol(speedfile,0,',',samplingratio)

    filenames = glob.glob(dirname + '/AIS*.csv')
    stats = {}
    for filename in filenames:
        print('Working on',filename)
        with open(filename, 'r') as f:
            for line in f:
                pline = (endclean(line)).split(',')
                speed = pline[4]
                if (speed == 'SOG'):
                    continue
                fspeed = float(speed)
                if (fspeed >= 1.0) and (fspeed <= 60):
                    keyval = extract_ship_key.extract_ship_key(line)
                    statpair = stats.get(keyval,[0.0,0.0,0])
                    statpair[0] = statpair[0] + fspeed
                    statpair[1] = statpair[1] + (fspeed*fspeed)
                    statpair[2] = statpair[2] + 1
                    stats[keyval] = statpair
    shipspeedfile = dirname + '/stated_speeds_per_ship.txt'
    out = open(shipspeedfile, 'w')
    keyvals = sorted(stats.keys())
    for keyval in keyvals:
        statpair = stats[keyval]
        count = statpair[2]
        avspeed = statpair[0]/count
        tmpsd = max(0,(statpair[1]/count) - (avspeed*avspeed))
        sdspeed = math.sqrt(tmpsd)
        out.write(keyval + ',' + str(round(avspeed,2)) + ',' + \
                  str(round(sdspeed,2)) + ',' + str(count) + '\n')
    out.close()
    histcol.histcol(shipspeedfile,1,',',1)
    histcol.histcol(shipspeedfile,2,',',1)

if __name__=="__main__":
    dirname = sys.argv[1]
    samplingratio = float(sys.argv[2])
    extract_stated_speeds(dirname,samplingratio)

