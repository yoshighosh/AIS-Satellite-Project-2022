# linear_fit_general.py
# Fits curve y = c1*x + c2 given a set of (x,y) pairs as a text file
# (first arg) where items on each line are delimited by the second arg.
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

def linear_fit_general(xypairs):
    if (xypairs == []):
        print('Empty list given for linear fit')
        return 0,0,0
    SX = 0.0 # sum of x
    SY = 0.0 # sum of y
    SXX = 0.0 # sum of x squared
    SXY = 0.0 # sum of x*y
    SYY = 0.0 # sum of y squared
    N = 0 # number of coordinates
    print(xypairs)
    for xypair in xypairs:
        X = xypair[0]
        Y = xypair[1]
        SX = SX + X
        SY = SY + Y
        SXX = SXX + (X*X)
        SXY = SXY + (X*Y)
        SYY = SYY + (Y*Y)
        N = N + 1
    denom = (N*SXX)-(SX*SX) 
    if (denom > 0.0):
        M = ((N*SXY)-(SX*SY)) / denom # average slope
    else:
        print('Could not calculate linear fit on single-point range')
        M = 0
    B = (SY/N)-(M*SX/N) # average y-intercept
    SE = 0.0 # standard error
    for xypair in xypairs:
        X = xypair[0]
        Y = xypair[1]
        SE = SE + abs(Y-(M*X)-B)
    error = SE/N # average error
    SDX2 = max(0,((SXX/N)-(SX*SX/(N*N)))) # standard deviation of x squared
    SDY2 = max(0,((SYY/N)-(SY*SY/(N*N)))) # standard deviation of y squared
    SD = math.sqrt(SDX2+SDY2) # standard deviation from the line
    print(str(M) + '*X + '+ str(B) + ' with mean error ' + str(error))
    print('N',N,'SX',SX,'SY',SY,'SXX',SXX,'SXY',SXY,'SYY',SYY, \
          'denom',denom,'sd',SD)
    return M,B,error,SD
    
if __name__=="__main__":
	infile = sys.argv[1]
	delim = sys.argv[2]
	xypairs = []
	with open(infile, 'r') as f:
		for line in f:
			pline = (endclean(line)).split(delim)
			xypairs.append(list([float(pline[0]),float(pline[1])]))
	M,B,error,SD = linear_fit_general(xypairs)
    