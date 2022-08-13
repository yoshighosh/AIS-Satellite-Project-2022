# logistic_function.py
import sys, math

def logistic_function(x,center,slope):
    x = float(x)
    center = float(center)
    slope = float(slope)
    pow = -slope*(x-center)
    if (pow < 15.0):
        return (1.0/(1.0+math.exp(pow)))
    else:
        return 0.0
         
if __name__=="__main__":
    x = float(sys.argv[1])
    center = float(sys.argv[2])
    slope = float(sys.argv[3])
    print(logistic_function(x,center,slope))
