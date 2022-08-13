# combine_metadata_files.py
import sys, glob

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S   

def combine_metadata_files(dirname):
    metadata = []
    filenames = glob.glob(dirname + '/metadata*.csv')
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                metadata.append(endclean(line))
    metadata = sorted(metadata)
    out = open(dirname + '/all_metadata.csv', 'w', encoding='utf=8')
    lastmetadatum = ''
    lastkey = ''
    for metadatum in metadata:
        if (metadatum != lastmetadatum):
            k = metadatum.find(',')
            key = metadatum[0:k]
            if (key == lastkey):
                print('Discrepancy:')
                print(metadatum)
                print(lastmetadatum)
            else:
                out.write(metadatum + '\n')
        lastmetadatum = metadatum
        lastkey = key
    out.close()
                
if __name__=="__main__":
    dirname = sys.argv[1]
    combine_metadata_files(dirname)
