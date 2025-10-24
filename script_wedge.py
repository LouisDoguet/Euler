from lib import pot

domain = pot.Space((-1,1),(0,1),Nx=100)
wedge = pot.Wedge(U=1,m=1.3,space=domain)
wedge.plot()
