# cleanrawdata_tracks.py
# Apportions cleaned data to individual files for each ship key.
# This is the last part of cleanrawdata.py.
import sys, os, os.path, math, sort_big

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S   

# Identify for removal those track points within 0.001 degree (364 feet) 
# of last point (since the ship speed is within random error), and points 
# that imply a speed greater than 100 knots from the last point.
def ok_transition(v1,v2):
    if (v1 == ''):
        return 'null_transition'
    latitude1 = float(v1[2])
    longitude1 = float(v1[3])
    latitude2 = float(v2[2])
    longitude2 = float(v2[3])
    avlat = 0.5*(latitude1+latitude2)
    dlat = (latitude2-latitude1)
    dlong = (longitude2-longitude1) / \
            (math.sqrt(1-(avlat*avlat)/8100))
    D = math.sqrt(max(0,((dlat*dlat)+(dlong*dlong))))
    if (D < 0.001):
        return 'stationary'
    timestamp1 = float(v1[1])
    timestamp2 = float(v2[1])
    dt = timestamp2-timestamp1
    if (dt == 0):
        return 'null_transition'
    speed = D / dt
    if (speed > 0.00046):
        return 'too_fast'
    return 'ok'
	
def cleanrawdata_tracks(dirname,justfilename,transition_hist):
    distthresh = 0.001
    # Move data for each ship to a separate file under ship IMO and callsign
    sortedfile = dirname + 'sorted_cleaned_raw_' + justfilename
    print('sortedfile:',sortedfile)
    currentoutfile = ''
    currentpline = ''
    out = open('dummy.out','w')
    with open(sortedfile, 'r', encoding='utf-8') as f:
        for line in f:
            pline = (endclean(line)).split(',')
            outfile = dirname + 'tracks/track_' + pline[0] + '.csv' 
            if (currentoutfile != outfile):
                # print('Starting on tracks for',pline[0])
                out.close()
                if (os.path.exists(outfile)):
                    out = open(outfile, 'a', encoding='utf-8')
                else:
                    out = open(outfile, 'w', encoding='utf-8')
                currentoutfile = outfile
                currentpline = pline
            else:
                reason = ok_transition(currentpline,pline)
                transition_hist[reason] = transition_hist.get(reason,0) + 1
                if (reason == 'ok'):
                    out.write(currentpline[1] + ',' + currentpline[2] + ',' + \
                              currentpline[3] + ',' + currentpline[4] + '\n')
                    currentpline = pline
    out.close()
    if (os.path.getsize(currentoutfile) == 0):
        os.remove(currentoutfile)
    print('Current transition histogram:',transition_hist)
    return transition_hist
                
if __name__=="__main__":
    infilename = sys.argv[1]
    j = max(infilename.rfind('/'),infilename.rfind('\\'))
    dirname = infilename[0:j+1]
    justfilename = infilename[j+20:len(infilename)]
    print(cleanrawdata_tracks(dirname,justfilename))
