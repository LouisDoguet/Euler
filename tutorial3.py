from lib import mapping as mp
from lib.space import Space
import numpy as np

q = 1/2
angle = 80
a = np.deg2rad(angle)/(2*np.pi)

def EXP(z,x):
    return np.exp(-x * z/q)

def div(z,x):
    return z / x

def slide(z,x):
    return x + z

def sqrt(z,x):
    return z**(1/x)

def pow(z,x):
    return z**x

def dWdz(z):
    return z**a

def tuto3(z):
    A = (1/2)*np.exp(-np.pi*z/q) + 1
    t = A - np.sqrt(A**2 - 1)
    return 2*t**a

contour = 1

dom = Space([0,1],[0.5,1],1000)


'''M = mp.ConformalMapping(space=dom)
M.plot()
M.animate(EXP,np.linspace(0,np.pi,100))
M.animate(div,np.linspace(1,2,100))
M.animate(slide,np.linspace(0,1,100))
M.animate(pow,np.linspace(1,2,100))
M.animate(slide,-np.linspace(0,1,100))
M.animate(sqrt,np.linspace(1,2,100))'''

M = mp.ConformalMapping(space=dom)
M.streamlines(xlabel=r'$\phi$', ylabel=r'$\psi$',title='$W(\phi,\psi)$')
M.apply(tuto3)
M.streamlines(xlabel='$u$',ylabel='$-v$',title='$dW/dz$')
M.plot()