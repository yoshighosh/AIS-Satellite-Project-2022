# histcol.py
# Draws a histogram of the values in kth column of a table as a text file
# Input file is first arg, k is second arg.
import sys, matplotlib, random
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def histcol(infilename,colnum,delimiter,samplingratio, name):
    ks = infilename.rfind('/')
    dirname = infilename[0:ks+1]
    filename = infilename[ks+1:len(infilename)]
    kp = filename.rfind('.')
    justfilename = filename[0:kp]
    datacol = []
    row = 0
    with open(infilename, 'r') as f:
        for line in f:
            if (row != 0):
                pline = line.split(delimiter);
                if (random.random() < samplingratio):
                    datacol.append(float(pline[colnum]))
            row += 1
    numstats = len(datacol)
    print(numstats,'items found')
    mindata = min(datacol)
    maxdata = max(datacol)
    print('count',numstats,'min',mindata,'max',maxdata)
    if (mindata < maxdata):
        xlabeltext = name
        ylabeltext = 'Counts out of ' + str(numstats)
        figurename = dirname + 'hist_' + name + '_' + \
                     justfilename + '.png'
        plt.figure(1)
        plt.xlabel(xlabeltext)
        plt.ylabel(ylabeltext)
        plt.hist(datacol,bins=200,label=xlabeltext)
        plt.savefig(figurename)
        plt.clf()
        plt.close()

if __name__=="__main__":
    infilename = sys.argv[1]
    colnum = int(sys.argv[2])
    delimiter = sys.argv[3]
    samplingratio = float(sys.argv[4])
    name = sys.argv[5]
    histcol(infilename,colnum,delimiter,samplingratio, name)
