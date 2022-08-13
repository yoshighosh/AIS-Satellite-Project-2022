# cleanrawdata_all.py
# Cleans a set of raw AIS files by deleting stationary periods and
# too-large position transitions, then writes out the position data
# into individual track files for each ship provided they are have
# some data.  Also computes the average and standard deviation of the
# reporting interval for each ship, and finds inflection (unusual)
# points in ship tracks.
import sys, os, os.path, glob, cleanrawdata, combine_metadata_files, \
    get_average_sampling_gap, find_track_delimitation_times

def cleanrawdata_all(dirname):
    xfilenames = sorted(glob.glob(dirname + '/AIS*.csv'))
    filelist = []
    print('Dates:')
    for xfilename in xfilenames:
        ks = max(xfilename.rfind('/'),xfilename.rfind('\\'))
        year = xfilename[ks+5:ks+9]
        month = xfilename[ks+10:ks+12]
        day = xfilename[ks+13:ks+15]
        print(year,'-',month,'-',day)
        datenum = 366*int(year) + 31*int(month) + int(day)
        filelist.append(list([datenum,xfilename]))
    transition_hist = {}
    filelist = sorted(filelist)
    for fileitem in filelist:
        filename = fileitem[1]
        print('Working on file',filename)
        transition_hist = cleanrawdata.cleanrawdata(filename,transition_hist)
    print('Final transition histogram:',transition_hist)
    out = open('final_track_transition_histogram.txt', 'w')
    for keyval in transition_hist.keys():
        out.write(keyval + '|' + str(transition_hist[keyval]) + '\n')
    out.close()
    trackfiles = glob.glob(dirname + '/tracks/track_*')
    for trackfile in trackfiles:
        if (os.path.getsize(trackfile) == 0):
            print('Removing empty file',trackfile)
            os.remove(trackfile)
    combine_metadata_files.combine_metadata_files(dirname)
    get_average_sampling_gap.get_average_sampling_gap(dirname)
    find_track_delimitation_times.find_track_delimitation_times(dirname)

if __name__=="__main__":
    dirname = sys.argv[1]
    cleanrawdata_all(dirname)
