from lib import comp, ana, foppl
import numpy as np
import matplotlib.pyplot as plt

domain = ana.Space([-2,3],[-2,2],1000)
zoom = ana.Space([-0,2],[-1.2,1.2],1000)

r = 1.5
theta = 20
z0 = r*np.exp(1j*np.deg2rad(theta))

F = foppl.Foppl(U=2, r=1, rho=5, z0=z0, space=domain)
Fzoom = F.updateSpace(zoom)
F.plot()
Fzoom.plot()
