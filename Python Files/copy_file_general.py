# copy_file_general.py
# Author: Neil C. Rowe, 12/12
import sys
# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):              
        S = S[0:M-1]
        M = M-1
    return S   

def copy_file_general(file1,file2):
    outfid = open(file2, 'w', encoding='utf-8')
    with open(file1,'r',encoding='utf-8') as f:
        for line in f:
            outfid.write(endclean(line) + '\n')
    outfid.close()
   
if __name__=="__main__":
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    copy_file_general(file1,file2)
