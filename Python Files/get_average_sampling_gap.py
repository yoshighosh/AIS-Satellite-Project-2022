# get_average_sampling_gap.py
# Finds the average gap in timestamps between successive records of ship,
# and the associated standard deviation.  It uses the original raw records
# including the periods the ship was stationary.  Output file is
# sampling_gaps_stats.csv with four columns: number of ship records,
# average time gap, standard deviation of the time gap, and ship key.
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

def get_average_sampling_gap(dirname):
    targetstring = dirname + '/sorted_cleaned_raw_*.csv'
    filenames = glob.glob(dirname + '/sorted_cleaned_raw_*.csv')
    sums = {}
    for filename in filenames:
        print('Working on',filename)
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                pline = (endclean(line)).split(',')
                keyval = pline[0]
                timestamp = int(pline[1])
                tmpsums = sums.get(keyval,[0,0.0,0.0,0])
                if (tmpsums[3] == 0):
                    tmpsums[3] = timestamp
                    sums[keyval] = tmpsums
                else:
                    tmpsums[0] = tmpsums[0] + 1
                    dt = abs(timestamp-tmpsums[3])
                    tmpsums[1] = tmpsums[1] + dt
                    tmpsums[2] = tmpsums[2] + (dt*dt)
                    tmpsums[3] = timestamp
                    sums[keyval] = tmpsums
    out = open(dirname + '/sampling_gaps_stats.csv','w')
    for keyval in sorted(sums.keys()):
        tmpsums = sums[keyval]
        if (tmpsums[0] == 0):
            continue
        count = tmpsums[0]
        avgap = tmpsums[1]/count
        tmp1 = (tmpsums[2]/count)-(avgap*avgap)
        sdgap = math.sqrt(max(0,tmp1))
        out.write(str(count) + ',' + str(round(avgap)) + ',' + \
                  str(round(sdgap)) + ',' + keyval + '\n')
    out.close()

if __name__=="__main__":
    dirname = sys.argv[1]
    get_average_sampling_gap(dirname)


