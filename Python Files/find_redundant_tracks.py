# find_redundant_tracks.py
# Check for tracks whose names are subsets of other names
import sys, os, os.path, glob

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S   

def extract_track(filename):
    k1 = max(filename.rfind('/'),filename.rfind('\\'))
    k2 = filename.rfind('.')
    return filename[k1+1:k2]

def find_redundant_tracks(dirname):
    xtrackfiles = glob.glob(dirname + '/*.csv')
    N = len(xtrackfiles)
    pairlist = []
    for i1 in list(range(N)):
        trackname1 = extract_track(xtrackfiles[i1])
        for i2 in list(range(i1+1,N)):
            trackname2 = extract_track(xtrackfiles[i2])
            if (trackname2.find(trackname1) > -1):
                pairlist.append(list([trackname1,trackname2]))
                print(trackname1,trackname2)
            elif (trackname1.find(trackname2) > -1):
                pairlist.append(list([trackname2,trackname1]))
                print(trackname2,trackname1)
                
if __name__=="__main__":
    dirname = sys.argv[1]
    find_redundant_tracks(dirname)
