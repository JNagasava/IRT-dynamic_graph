from numpy import linspace
from math import exp

class IRT:

    def __init__(self, a=2.0, b=0.0, c=0.0, theta_min=-3.0, theta_max=3.0):

        self.a = a
        self.b = b
        self.c = c
        self.theta_min = theta_min
        self.theta_max = theta_max

    def icc(self, theta=float) -> float:
        return self.c + ( 1.0 - self.c ) / ( 1.0 + exp( -1.0 * self.a * ( theta - self.b ) ) )
    
    def icc_xy(self, dots=1001):
        x = linspace(self.theta_min, self.theta_max, dots)
        y = [self.icc(k) for k in x]
        return x, y