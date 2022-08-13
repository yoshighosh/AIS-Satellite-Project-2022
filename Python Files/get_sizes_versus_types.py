# get_sizes_versus_types.py
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

def ship_type_description(typecode):
    if (typecode == 0):
        return 'none'
    if (typecode in [21,22,31,32,52]):
        return 'tug'
    if (typecode in [23,24,25,26,27,28,29]):
        return 'wing_in_ground'
    if (typecode == 30):
        return 'fishing'
    if (typecode == 33):
        return 'dredging'
    if (typecode == 34):
        return 'diving'
    if (typecode == 35):
        return 'military'
    if (typecode == 36):
        return 'sailing'
    if (typecode == 37):
        return 'pleasure_craft'
    if (typecode in [40,41,42,43,44,45,46,47,48,49]):
        return 'high_speed_craft'
    if (typecode == 50):
        return 'pilot_vessel'
    if (typecode == 51):
        return 'search_and_rescue'
    if (typecode == 53):
        return 'port_tender'
    if (typecode == 54):
        return 'antipollution_equipment'
    if (typecode == 55):
        return 'law_enforcement'
    if (typecode == 58):
        return 'medical_transport'
    if (typecode in [60,61,62,63,64,65,66,67,68,69]):
        return 'passenger_craft'
    if (typecode in [70,71,72,73,74,75,76,77,78,79]):
        return 'cargo'
    if (typecode in [80,81,82,83,84,85,86,87,88,89]):
        return 'tanker'
    return 'other'

def get_sizes_versus_types(dirname):
    typemap = {}
    datafiles = glob.glob(dirname + '/sorted_cleaned_raw*.csv')
    for datafile in datafiles:
        print('Working on',datafile)
        k1 = max(datafile.rfind('/'),datafile.rfind('\\'))
        dataname = datafile[k1+19:len(datafile)-4]
        with open(datafile, 'r', encoding='utf-8') as f:
            for line in f:
                pline = (endclean(line)).split(',')
                key = pline[0]
                shiptype = pline[6]
                if (shiptype.isdigit()):
                    typemap[key] = shiptype
                else:
                    typemap[key] = '0'
    sizetotals = {}
    with open(dirname + '/all_metadata.csv', 'r', encoding='utf-8') as f:
        for line in f:
            pline = (endclean(line)).split(',')
            key = pline[0]
            shiptype = typemap.get(key,'0')
            try:
                length = math.log(float(pline[1]))
            except:
                length = 0
            try:
                width = math.log(float(pline[2]))
            except:
                width = 0
            try:
                depth = math.log(float(pline[3]))
            except:
                depth = 0
            if (length > 0) and (width > 0) and (depth > 0):
                totals = sizetotals.get(shiptype,[0.0,0.0,0.0,0])
                totals[0] = totals[0] + length
                totals[1] = totals[1] + width
                totals[2] = totals[2] + depth
                totals[3] = totals[3] + 1
                sizetotals[shiptype] = totals
    print('All totals:',sizetotals)
    out = open('size_averages_by_type.txt', 'w')
    typekeys = sizetotals.keys()
    inttypekeys = []
    for typekey in typekeys:
        inttypekeys.append(int(typekey))
    inttypekeys = sorted(inttypekeys)
    for inttypekey in inttypekeys:
        typekey = str(inttypekey)
        typename = ship_type_description(inttypekey)
        totals = sizetotals[typekey]
        avlength = round(math.exp(totals[0]/totals[3]),1)
        avwidth = round(math.exp(totals[1]/totals[3]),1)
        avdepth = round(math.exp(totals[2]/totals[3]),1)
        out.write(typekey + ',' + typename + ',' + \
                  str(avlength) + ',' + str(avwidth) + ',' + \
                  str(avdepth) + ',' + str(totals[3]) + '\n')
    out.close()
                
if __name__=="__main__":
    dirname = sys.argv[1]
    get_sizes_versus_types(dirname)
