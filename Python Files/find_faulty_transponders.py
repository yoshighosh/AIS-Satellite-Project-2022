# find_faulty_transponders
# Makes a list of ship keys in raw data that have no track data, stores
# it in faulty_transponders.txt.  As a side effect, makes list of
# ship keys with at least some data, stores in all_ship_keys.txt.
import sys, os, os.path, glob, cleanrawdata, combine_metadata_files

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S   

def find_faulty_transponders(dirname):
    ship_keys = {}
    with open(dirname + '/all_metadata.csv', 'r', encoding='utf-8') as f:
        for line in f:
            line = endclean(line)
            pline = line.split(',')
            ship_key = pline[0]
            if not (ship_keys.get(pline[0],False)):
                ship_keys[pline[0]] = True
    keylist = sorted(ship_keys.keys())
    out = open(dirname + '/faulty_transponders.txt','w',encoding='utf-8')
    for ship_key in keylist:
        trackfile = dirname + '/tracks/track_' + ship_key + '.csv'
        if not (os.path.exists(trackfile)):
            out.write(str(ship_key) + '\n')
    out.close()
    out = open(dirname + '/all_ship_keys.txt', 'w', encoding='utf-8')
    for ship_key in keylist:
        out.write(ship_key + '\n')
    out.close()
            
if __name__=="__main__":
    dirname = sys.argv[1]
    find_faulty_transponders(dirname)
