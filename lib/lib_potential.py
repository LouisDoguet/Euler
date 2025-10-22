import numpy as np

def Wcylinder(U,r,z):
    return (z + r**2/z)

def Wfreevortex(rho,z):
    return -rho/(2*np.pi) * np.log(z)

def derWfreevortex(rho,z):
    return 1j*rho/(2*np.pi*z)

def Wcylindercirc(U,r,rho,z):
    return Wcylinder(U,r,z) + 1j * rho/(2*np.pi) * np.log(z)

def derWcylinder(U,r,z):
    return U*(1-r**2/z**2)

def get(str_type):
    match str_type:
        case 'cyl':
            return Wcylinder
        case 'dcyl':
            return derWcylinder
        case 'cyl_circ':
            return Wcylindercirc
        case _:
            raise ValueError()
