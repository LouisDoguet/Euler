from lib import comp, ana
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3,3,150)
y = np.linspace(-2,2,100)
X,Y = np.meshgrid(x,y)
Z = X+1j*Y

def Wcylinder(U,r,z):
    return (z + r**2/z)*U

def Wcylindercirc(U,r,rho,z):
    return Wcylinder(U,r,z) * 1j * rho/(2*np.pi) * np.log(z)

W = ana.AnalyticalFunction(U=1, r=1, z=Z, f=Wcylinder)
W.grid_solve(X,Y)
W.plot()
