from lib import mapping as mp
from lib.space import Space
import numpy as np

# Kirchoff Parameters
q = 1/2
angle = 50
a = np.deg2rad(angle)/(2*np.pi)


# Transformations applied to the streamfield W
def exp(z,x):
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


# Kirchoff mapping
def kirchoff_flow(z):
    A = (1/2)*np.exp(-np.pi*z/q) + 1
    t = A - np.sqrt(A**2 - 1)
    return 2*t**a
'''
# Animations for transformation
dom = Space([0,2],[-0.5,0.5],100)
M = mp.ConformalMapping(space=dom)
M.plot()
M.animate(exp,np.linspace(0,np.pi,100),title='$e^{-[\pi] w / q}$')
M.animate(div,np.linspace(1,2,100),title='$\\frac{1}{[2]} e^{-\pi w / q}$')
M.animate(slide,np.linspace(0,1,100),title='$[1] + \\frac{1}{2} e^{-\pi w / q}$')
M.animate(pow,np.linspace(1,2,100),title='$ ( 1 + \\frac{1}{2} e^{-\pi w / q} )^{[2]} $')
M.animate(slide,-np.linspace(0,1,100),title='$ ( 1 + \\frac{1}{2} e^{-\pi w / q} )^{2} - [1] $')
M.animate(sqrt,np.linspace(1,2,100),title='$ [ \sqrt{ ( 1 + \\frac{1}{2} e^{-\pi w / q} )^{2} - 1 } ]$')
'''
# Kirchhoff mapping
dom = Space([0,2],[0,0.5],1000)
M = mp.ConformalMapping(space=dom)
M.apply(kirchoff_flow)
M.plot()

# Kirchhoff streamplots
dom = Space([0,2],[-0.5,0.5],1000)
M = mp.ConformalMapping(space=dom)
M.apply(kirchoff_flow)
M.streamlines(xlabel='$u$',ylabel='$v$',title='$dW/dz$')