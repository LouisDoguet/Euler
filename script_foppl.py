from lib import pot, foppl
import numpy as np
import matplotlib.pyplot as plt

# Define computational spaces
domain = pot.Space([-2,3],[-2,2],100)
zoom = pot.Space([-0,2],[-1.2,1.2],100)

# Define Foppl vortex offset parameters
r = 1.5
theta = 20
z0 = r*np.exp(1j*np.deg2rad(theta))

# Create and plot potential flow objects
val_rho = 3
val_U = 1
val_r = 1
cylinder = pot.Cylinder(U=val_U,r=val_r,space=domain)
freevortex = pot.FreeVortex(rho=val_rho,space=domain)
foppl_flow = foppl.Foppl(U=val_U, r=val_r, rho=3, z0=z0, space=domain)
foppl_flow_zoom = foppl_flow.updateSpace(zoom) 


foppl_flow.plot_cylinder()
foppl_flow.plot_vortices()
foppl_flow.plot()
foppl_flow_zoom.plot()
