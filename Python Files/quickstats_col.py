# quickstats_col.py
# Calculates mean, st. dev., max, and min for a given column
# of data in a text file delimited by spaces.
# Author: Neil Rowe, ncrowe@nps.edu, 1/21
import sys, math
# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):                        
        S = S[0:M-1]
        M = M-1
    return S  

def quickstats_col(file,colnum,delimiter, out):
    fid = open(file, 'r')
    line = fid.readline()
    pline = (endclean(line)).split(delimiter)
    M = len(pline)
    count = 0
    sum = 0
    sq = 0
    minval = 1000000
    maxval = -1000000
    nonnumcount = 0
    hist = {}
    while line:
        pline = (endclean(line)).split(delimiter)
        if (len(pline) > 0):
            numflag = True
            try:
                val = float(pline[colnum])
            except:
                numflag = False
                nonnumcount = nonnumcount + 1
                hist[pline[colnum]] = hist.get(pline[colnum],0) + 1
            if numflag:
                count = count + 1
                sum = sum + val
                sq = sq + val*val
                minval = min(minval,val)
                maxval = max(maxval,val)
            line = fid.readline()
    ks = file.rfind('/')
    dirname = file[0:ks+1]
    print('Column',colnum,'Number of numeric values:',count, \
          'Number of nonnumeric values:',nonnumcount)
    out.write('Column ' + str(colnum) + ': Number of numeric values: ' + \
              str(count) + ' Number of nonnumeric values: ' + \
              str(nonnumcount) + '\n')
    if (count > 0):
        av = sum/count
        std = math.sqrt((sq/count)-(av*av))
        print('sum',sum,'mean',av,'st. dev.',std,'min',minval,'max',maxval)
        out.write('sum ' + str(sum) + ' mean ' + str(av) + \
                  ' st. dev. ' + str(std) + ' min ' + \
                  str(minval) + ' max ' + str(maxval) + '\n')
        return std
    print('Histogram of nonnumeric values:',hist)
    out.write('Histogram of nonnumeric values:\n')
    for key in hist.keys():
        out.write('Value ' + str(key) + ' has count ' + \
                  str(hist[key]) + '\n')
    
if __name__=="__main__":
   file = sys.argv[1]
   colnum = int(sys.argv[2])
   delimiter = sys.argv[3]
   out = open('quickstats_col' + str(colnum) + '.txt', 'w')
   quickstats_col(file,colnum,delimiter,out)
   out.close()
