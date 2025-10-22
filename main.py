from lib import pot, foppl
import numpy as np
import matplotlib.pyplot as plt

domain = pot.Space([-2,3],[-2,2],100)
zoom = pot.Space([-0,2],[-1.2,1.2],100)

r = 1.5
theta = 20
z0 = r*np.exp(1j*np.deg2rad(theta))

cyl = pot.Cylinder(U=1,r=1,space=domain)
F = foppl.Foppl(U=0.5, r=1, rho=3, z0=z0, space=domain)
Fzoom = F.updateSpace(zoom)

cyl.plot()
F.V2.plot()
(F.V1+F.V2+F.V3+F.V4).plot()
F.plot()
Fzoom.plot()
