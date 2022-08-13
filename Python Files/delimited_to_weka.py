# delimited_to_weka.py
# Converts a text file in a delimited format like CSV of TSV
# to a file in Weka input format.  First argument is file name to convert,
# second is the delimiter character (so use "," for CSV files), and remaining
# arguments are the labels for the columns of the data.
# This program should be run from a command line interface.
# Note: if the file you are processing has a first line listing the
# attributes, you should delete that line from the file before using
# it with this program.
import sys

def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S

def split_line(line,delimiter):
    words = []
    buffer = ''
    quoteflag = False
    for i in list(range(len(line))):
        if (line[i] == '\"'):
            quoteflag = not quoteflag            
        elif (line[i] == delimiter) and not quoteflag:
            words.append(buffer)
            buffer = ''
        else:
            buffer = buffer + line[i]
    words.append(buffer)
    return words

def classify_type(S):
    try:
        K = int(S)
        return 'numeric'
    except:
        try:
            K = float(S)
            return 'real'
        except:
            return S
    return S

def delimited_to_weka(infilename,delimiter,labels):
    numlabels = len(labels)
    print(numlabels,'labels were given')
    ks = infilename.rfind('/')
    dirname = infilename[0:ks+1]
    justfilename = infilename[ks+1:len(infilename)]
    kp = justfilename.rfind('.')
    relationname = justfilename[0:kp]
    # First infer the types of each column of data, and associate
    # each with the column label
    attributedata = {}
    with open(infilename,'r',encoding='utf-8') as f:
        for line in f:
            line = endclean(line)
            pline = split_line(line,delimiter)
            # print('line',line,'pline',pline)
            if (len(pline) > len(labels)):
                print('You have',len(labels), \
                      'labels in your command line but need', \
                      len(pline))
            for i in list(range(len(pline))):
                key = labels[i]
                val = pline[i]
                typedescr = attributedata.get(key,[])
                typeval = classify_type(val)
                if (typeval == 'numeric'):
                    if (typedescr == []):
                        attributedata[key] = 'numeric'
                elif (typeval == 'real'):
                    if ((typedescr == []) or (typedescr == 'numeric')):
                        attributedata[key] = 'real'
                elif (isinstance(typedescr,list)):
                    if (typeval not in typedescr):
                        typedescr.append(typeval)
                        attributedata[key] = typedescr
    # Write the header information
    out = open(dirname + 'weka_' + relationname + '.arff', \
               'w', encoding='utf-8')
    out.write('@relation ' + relationname + '\n')
    print('attributedata:',attributedata)
    for key in labels:
        typedescr = attributedata.get(key,[])
        if (typedescr == []) or (typedescr == '') or (typedescr == ['']):
            xtypedescr = 'string'
        elif (isinstance(typedescr,list)) and (len(typedescr) < 50):
            xtypedescr = '{'
            for i in list(range(len(typedescr)-1)):
                xtypedescr = xtypedescr + typedescr[i] + ','
            xtypedescr = xtypedescr + typedescr[len(typedescr)-1] + '}'
        elif (isinstance(typedescr,list)):
            xtypedescr = 'string'
        else:
            xtypedescr = typedescr
        out.write('@attribute ' + key + ' ' + xtypedescr + '\n')
        # print('key',key,'typedescr',typedescr,'xtypedescr',xtypedescr)
    # Write the data
    out.write('@data\n')
    with open(infilename,'r',encoding='utf-8') as f:
        for line in f:
            line = endclean(line)
            pline = split_line(line,delimiter)
            for i in list(range(len(pline)-1)):
                out.write(pline[i] + ',')
            out.write(pline[len(pline)-1] + '\n')
    out.close()

if __name__=="__main__":
    infilename = sys.argv[1]
    delimiter = sys.argv[2]
    labels = []
    for i in list(range(3,len(sys.argv))):
        labels.append(sys.argv[i])
    delimited_to_weka(infilename,delimiter,labels)
