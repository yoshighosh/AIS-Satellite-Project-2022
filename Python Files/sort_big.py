# sort_big.py
# Sort a large file by breaking it into pieces.
# Arguments are input file, partition size, and whether the sorting
# is as strings ('string'), integers ('integer'), or floats ('float').
# Output is input file name with "sorted_" in front.
# Author: Neil C. Rowe, 11/14
import sys, splitmergeproc, os, os.path

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):
        S = S[0:M-1]
        M = M-1
    return S

def smart_rename(file1,file2):
    if (os.path.exists(file2)):
        os.remove(file2)
    os.rename(file1,file2)
                 
def merge_sorted_files(infile1,infile2,outfile,sorttype):
    print('merging',infile1,'with',infile2)
    fid1 = open(infile1, 'r', encoding='utf-8')
    fid2 = open(infile2, 'r', encoding='utf-8')
    out = open(outfile, 'w', encoding='utf-8')
    line1 = fid1.readline()
    line2 = fid2.readline()
    while line1 and line2:
        line1 = endclean(line1)
        line2 = endclean(line2)
        if (line1 == line2):
            out.write(line1 + '\n')
            out.write(line2 + '\n')
            line1 = fid1.readline()
            line2 = fid2.readline()
        elif (sorttype != 'string') and (float(line1) < float(line2)):
            out.write(line1 + '\n')
            line1 = fid1.readline()
        elif (sorttype == 'string') and (line1 < line2):
            out.write(line1 + '\n')
            line1 = fid1.readline()
        else:
            out.write(line2 + '\n')
            line2 = fid2.readline()
    while line1:
        out.write(endclean(line1) + '\n')
        line1 = fid1.readline()
    while line2:
        out.write(endclean(line2) + '\n')
        line2 = fid2.readline()
    fid1.close()
    fid2.close()
    out.close()

def sort_big(infile,partsize,sorttype):
    print('Sorting',infile)
    ks = max(infile.rfind('/'),infile.rfind('\\'))
    dirname = infile[0:ks+1]
    justinfile = infile[ks+1:len(infile)]
    outfile = dirname + 'sorted_' + justinfile
    linecache = []
    linenum = 0
    partnum = 0
    with open(infile, 'r', encoding='utf-8') as f:
        for line in f:
            line = endclean(line)
            # When a batch of data is full, save its data as
            # splitpart_#.out where # is the batch number.  
            if ((linenum % partsize) == (partsize - 1)):
                linecache = sorted(linecache)
                out = open(dirname + 'splitpart' + str(partnum) + '-' + \
                           str(partnum) + '.out', 'w', encoding='utf-8')
                for line2 in linecache:
                    out.write(str(line2) + '\n')
                out.close()
                linecache = []
                partnum = partnum + 1
            # Add each line to the linecache
            if (sorttype == 'integer'):
                linecache.append(int(line))
            elif (sorttype == 'float'):
                linecache.append(float(line))
            else:
                linecache.append(line)
            linenum = linenum + 1
    # Write out the final batch of data
    linecache = sorted(linecache)
    out = open(dirname + 'splitpart' + str(partnum) + '-' + \
               str(partnum) + '.out', 'w', encoding='utf-8')
    for line2 in linecache:
        out.write(str(line2) + '\n')
    out.close()
    numparts = partnum + 1
    print(numparts,'parts made of',infile)

    # Now intersect the subfiles in the manner of a binary tree
    if (numparts == 1):
        outfiletmp = dirname + 'splitpart0-0.out'
    span = 1
    while (span < numparts):
        nummerges = 1 + ((numparts-1)//(2*span))
        for mergenum in list(range(nummerges)):
            mergenum1a = mergenum*2*span
            mergenum1b = (mergenum*2*span)+span-1
            mergenum2a = (mergenum*2*span)+span
            mergenum2b = (mergenum*2*span)+(2*span)-1
            if (mergenum2a < numparts):
                mergenum2b = min(mergenum2b,(numparts-1))
                infile1 = dirname + 'splitpart' + str(mergenum1a) + '-' + \
                          str(mergenum1b) + '.out'
                infile2 = dirname + 'splitpart' + str(mergenum2a) + '-' + \
                          str(mergenum2b) + '.out'
                outfiletmp = dirname + 'splitpart' + str(mergenum1a) + '-' + \
                          str(mergenum2b) + '.out'
                merge_sorted_files(infile1,infile2,outfiletmp,sorttype)
                os.remove(infile1)
                os.remove(infile2)
        span = span * 2
    smart_rename(outfiletmp, outfile)
    print(outfile,'written')

if __name__=="__main__":
    filename = sys.argv[1] 
    partsize = int(sys.argv[2])
    if (len(sys.argv) > 3):
        sorttype = sys.argv[3]
    else:
        sorttype = 'string'
    sort_big(filename,partsize,sorttype)
