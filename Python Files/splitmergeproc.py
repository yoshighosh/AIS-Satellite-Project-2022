# splitmergeproc.py
# Generalized split-merging distributed processing.
# Arguments are the function applied to each part; the file whose rows
# will be processed one at a time; the number of rows in each part of
# the second argument to be processed; the merging function for rows
# of the parts; and the output file name.
# The first-argument function takes two arguments, a hash table
# and a line of the input table to process.  It returns a modified
# hash table.
# The fourth-argument function takes two arguments, lists of the keys and
# items in the hash table for two given items.  It returns a consensus
# new hash table line.
# Author: Neil C. Rowe, 11/14
import sys, os, os.path, copy_file_general

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

def merge_files(mergefunc,infile1,infile2,outfile):
    print('merging',infile1,'with',infile2)
    out = open(outfile, 'w', encoding='utf-8')
    fid2 = open(infile2, 'r', encoding='utf-8')
    line2 = fid2.readline()
    with open(infile1, 'r', encoding='utf-8') as f:
        for line1 in f:
            line1 = endclean(line1)
            if not line2:
                out.write(line1 + '\n')
            else:
                pline1 = line1.split('|')
                pline1 = pline1[0:len(pline1)-1]
                keyval1 = pline1[0]
                pline2 = (endclean(line2)).split('|')
                pline2 = pline2[0:len(pline2)-1]
                keyval2 = pline2[0]
                while line2 and (keyval1 > keyval2):
                    out.write(endclean(line2) + '\n')
                    line2 = fid2.readline()
                    if line2:
                        pline2 = (endclean(line2)).split('|')
                        pline2 = pline2[0:len(pline2)-1]
                        if (len(pline2) == 0):
                            print('Faulty merge line2:',line2,pline2)
                            print('Attempting merge with',line1,pline1)
                        else:
                            keyval2 = pline2[0]
                if line2 and (keyval1 == keyval2):
                    xpline1 = pline1[1:len(pline1)]
                    xpline2 = pline2[1:len(pline2)]
                    # This assumes merging is done on lists of items
                    # and returns a list of items
                    newpline = mergefunc(xpline1,xpline2)
                    # print('merge of',xpline1,'with',xpline2,'giving', \
                    #        newpline,'for keyval',keyval1)
                    out.write(keyval1 + '|')
                    for i in list(range(len(newpline))):
                        out.write(newpline[i] + '|')
                    out.write('\n')
                    line2 = fid2.readline()
                else:
                    out.write(line1 + '\n')
    while line2:
        out.write(endclean(line2) + '\n')
        line2 = fid2.readline()
    fid2.close()
    out.close()

def splitmergeproc(basicfunc,infile,partsize,mergefunc,outfile):
    print('splitmergeproc started on',infile,'with function',basicfunc)
    ks = infile.rfind('/')
    if (ks > -1):
        dirname = infile[0:ks+1]
        filename = infile[ks+1:len(infile)]
    else:
        dirname = ''
        filename = infile
    kp = filename.rfind('.')
    if (kp > -1):
        filename = filename[0:kp]
    strfunc = str(basicfunc)
    k1 = strfunc.find(' ')
    k2 = strfunc.find(' at ')
    strfunc = strfunc[k1+1:k2]
    tag = strfunc + '_' + filename + '_'
    procdata = {}
    linenum = 0
    partnum = 0
    with open(infile, 'r', encoding='utf-8') as f:
        for line in f:
            line = endclean(line)
            # When a batch of data is full, save its data as
            # splitpart_#.out where # is the batch number.  
            if ((linenum % partsize) == (partsize - 1)):
                keylist = []
                for val in procdata.keys():
                    keylist.append(val)
                keylist = sorted(keylist)
                out = open(dirname + tag + 'splitpart' + \
                           str(partnum) + '-' + \
                           str(partnum) + '.out', 'w', encoding='utf-8')
                for keyval in keylist:
                    hashedrow = procdata[keyval]
                    out.write(keyval + '|')
                    # This assumes hash table stores lists
                    for hasheditem in hashedrow:
                        out.write(str(hasheditem) + '|')
                    out.write('\n')
                out.close()
                procdata = {}
                partnum = partnum + 1
            # For each line, run the function
            procdata = basicfunc(procdata,line)
            linenum = linenum + 1
    # Write out the final batch of data
    keylist = []
    for val in procdata.keys():
        keylist.append(val)
    keylist = sorted(keylist)
    out = open(dirname + tag + 'splitpart' + \
               str(partnum) + '-' + str(partnum) + '.out', \
               'w', encoding='utf-8')
    for keyval in keylist:
        hashedrow = procdata[keyval]
        out.write(keyval + '|')
        for hasheditem in hashedrow:
            out.write(str(hasheditem) + '|')
        out.write('\n')
    out.close()
    procdata = {}
    numparts = partnum + 1
    print(numparts,'parts made of',infile)

    # Now merge the subfiles in the manner of a binary tree
    if (numparts == 1):
        outfiletmp = dirname + tag + 'splitpart0-0.out'
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
                infile1 = dirname + tag + 'splitpart' + \
                    str(mergenum1a) + '-' + str(mergenum1b) + '.out'
                infile2 = dirname + tag + 'splitpart' + \
                    str(mergenum2a) + '-' + str(mergenum2b) + '.out'
                outfiletmp = dirname + tag + \
                    'splitpart' + str(mergenum1a) + '-' + \
                    str(mergenum2b) + '.out'
                merge_files(mergefunc,infile1,infile2,outfiletmp)
                os.remove(infile1)
                os.remove(infile2)
        span = span * 2
    smart_rename(outfiletmp, outfile)
    print(outfile,'written')

if __name__=="__main__":
    basicfunc = sys.argv[1]
    infile = sys.argv[2]
    partsize = int(sys.argv[3])
    mergefunc = sys.argv[4]
    outfile = sys.argv[5]
    splitmergeproc(basicfunc,infile,partsize,mergefunc,outfile)
