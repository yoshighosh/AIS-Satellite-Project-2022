# extract_ship_key.py
# Given a line of raw AIS data in CSV format, construct a primary key for
# the ship of the IMO number, the call sign, and the MMSI mobile number;
# omit those that are missing.
import sys

def okimo(imo):
    if (imo == '') or (imo == 'IMO0000000') or (imo == 'IMO0000001'):
        return False
    return True

def extract_ship_key(line):
    pline = line.split(',')
    if (len(pline) < 16):
        return ''
    mmsi = pline[0]
    vesselname = pline[7]
    imo = pline[8]
    callsign = pline[9]
    status = pline[11]
    cargo = pline[15]
    if (okimo(imo)) and (callsign != '') and (mmsi != ''):
        keyval = imo + '_CALL' + callsign + '_MMSI' + mmsi
    elif (okimo(imo)) and (callsign != ''):
        keyval = imo + '_CALL' + callsign 
    elif (okimo(imo)) and (mmsi != ''):
        keyval = imo + '_MMSI' + mmsi
    elif (callsign != '') and (mmsi != ''):
        keyval = 'CALL' + callsign + '_MMSI' + mmsi
    elif (okimo(imo)):
        keyval = imo
    elif (callsign != ''):
        keyval = 'CALL' + callsign 
    elif (mmsi != ''):
        keyval = 'MMSI' + mmsi 
    else:
        keyval = ''
    # Eliminate possible troublesome characters in ship keyvals
    keyval = keyval.replace('/','_')
    keyval = keyval.replace('\\','_')
    keyval = keyval.replace('\"','_')
    keyval = keyval.replace('\'','_')
    keyval = keyval.replace('&',' and ')
    keyval = keyval.replace('|',' ')
    return keyval
         
if __name__=="__main__":
    line = sys.argv[1]
    print(extract_ship_key(line))
