# cleanrawdata.py
# Converts a raw AIS file into something sortable by ship ID and date
import sys, os, os.path, datetime, sort_big, cleanrawdata_tracks, \
    extract_ship_key

# Allows same program to handle Windows and Linux line reads
def endclean(OS):
    S = OS
    M = len(S)
    while ((M > 0) and \
           (S[M-1] in ['\n','\r','\t','\f','\a','\b','\v',' ']) ):             
        S = S[0:M-1]
        M = M-1
    return S   

def get_datenum(rawdate):
    seconds = int(rawdate[17:19])
    minutes = int(rawdate[14:16])
    hours = int(rawdate[11:13])
    day = int(rawdate[8:10])
    month = int(rawdate[5:7])
    year = int(rawdate[0:4])
    etime = datetime.datetime(year,month,day,hours,minutes,seconds).timestamp()
    return int(etime)

def plinedist(v1,v2):
    if (v1 == ''):
        return 0
    d1 = (v1[0]-v2[0])
    d2 = (v1[1]-v2[1])
    d3 = (v1[2]-v2[2])
    d4 = (v1[3]-v3[3])
    D is math.sqrt(max(0,(d1*d1+d2*d2+d3*d3+d4*d4)))
    return D
	
def okimo(imo):
    if (imo == '') or (imo == 'IMO0000000') or (imo == 'IMO0000001'):
        return False
    return True

def cleanrawdata(infilename,transition_hist):
    distthresh = 0.0001
    j = max(infilename.rfind('/'),infilename.rfind('\\'))
    dirname = infilename[0:j+1]
    justfilename = infilename[j+1:len(infilename)]
    # Select columns to create a smaller table for track analysis
    outfilename = dirname + 'cleaned_raw_' + justfilename
    outfile = open(outfilename, 'w', encoding='utf-8')
    metadata = {}
    stationary_signal = 0
    linenum = 0
    with open(infilename, 'r', encoding='utf-8') as f:
        for line in f:
            line = endclean(line)
            if (linenum == 0):
                linenum = 1
                continue
            elif ((linenum % 100000) == 0):
                print('On line',linenum)
            if (line != ''):
                keyval = extract_ship_key.extract_ship_key(line)
                pline = line.split(',')
                mmsi = pline[0]
                vesselname = pline[7]
                imo = pline[8]
                callsign = pline[9]
                status = pline[11]
                cargo = pline[15]
                # print('keyval',keyval,'for',pline)
                datenum = get_datenum(pline[1])
                latitude = pline[2]
                longitude = pline[3]
                vesseltype = pline[10]
                # Exclude data when ship reports it is stationary
                if (status not in ['1','2','3','4','5','6']):
                    outfile.write(keyval + ',' + str(datenum) + ',' + \
                                  latitude + ',' + longitude + ',' + \
                                  vesseltype + ',' + status + ',' + \
                                  cargo + '\n')
                else:
                    stationary_signal = stationary_signal + 1
                # Save mostly-unchanging ship data in a "metadata" file.
                # Metavals holds MMSI, VesselName, IMO, CallSign, VesselType,
                # Length, Width, Draft, Cargo, and TransceiverClass
                metavals = list([pline[10],pline[12],pline[13], \
                                 pline[14],pline[16]])
                # Modify metadata for a ship to fill in blanks and zeros
                oldmetavals = metadata.get(keyval,[])
                if (oldmetavals == []):
                    metadata[keyval] = metavals
                elif (metavals != oldmetavals) and (keyval != ''):
                    # print('Found different metadata for ship',keyval,':')
                    should_change = False
                    for k in list(range(3,len(oldmetavals))):
                        if (oldmetavals[k] == '') and (metavals[k] != ''):
                            should_change = True
                        elif (oldmetavals[k] != '') and (metavals[k] == ''):
                            should_change = False
                    if should_change:
                        metadata[keyval] = metavals
                        print('Changing metadata for',keyval,'to',metavals)
                        print('from',oldmetavals)
                linenum = linenum + 1
    outfile.close()
    print(stationary_signal,'ships signalling stationary for',infilename)
    # Save the metadata
    out = open(dirname + 'metadata_' + justfilename, 'w', encoding='utf-8')
    for keyval in sorted(metadata.keys()):
        out.write(keyval + ',')
        metavals = metadata[keyal]
        M = len(metavals)
        for k in list(range(M-1)):
            out.write(metavals[k] + ',')
        out.write(metavals[M-1] + '\n')
    out.close()
    # Sort the data by primary key and time in that order, to enable
    # easier construction of tracks.
    sort_big.sort_big(outfilename,1000000,'string')
    os.remove(outfilename)
    transition_hist = cleanrawdata_tracks.cleanrawdata_tracks(dirname, \
                                                              justfilename, \
                                                              transition_hist)
    return transition_hist
                
if __name__=="__main__":
    infilename = sys.argv[1]
    print(cleanrawdata(infilename))
