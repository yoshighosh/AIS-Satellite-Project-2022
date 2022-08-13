# extractcols.py
# Makes a new file of the values in a set of columns of the input file.
# Args are input file, delimiter character, and the column numbers.
# Blank lines are ignored (which helps with Linux-Windows transitions).
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

def extractcols(infilename,delimchar,colnums):
    print('colnums:',colnums)
    numcolnums = len(colnums)
    printcolnums = 'firstTwoCols\\cols'
    for i in list(range(numcolnums)):
        printcolnums = printcolnums + '_' + str(colnums[i])
    j = max(infilename.rfind('/'),infilename.rfind('\\'))
    outname = infilename[12:j+1] + printcolnums + '_' + \
        infilename[j+1:len(infilename)]
    out = open(outname, 'w', encoding='utf-8')
    with open(infilename, 'r', encoding='utf-8') as f:
        for line in f:
            line = endclean(line)
            if (line != ''):
                pline = line.split(delimchar)
                outline = []
                for j in list(range(numcolnums)):
                    try:
                        out.write(pline[colnums[j]])
                    except:
                        print('Could not find column',j,'in pline',pline, \
                              'with delimiter',delimchar)
                    if (j < (numcolnums-1)):
                        out.write(delimchar)
                    else:
                        out.write('\n')
    out.close()

if __name__=="__main__":
    infilename = sys.argv[1]
    delimchar = sys.argv[2]
    colnums = []
    for i in list(range(3,len(sys.argv))):
        colnums.append(int(sys.argv[i]))
    extractcols(infilename,delimchar,colnums)
