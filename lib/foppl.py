import numpy as np
import lib.potential as pot 

class Foppl(pot.__Potential__):
    def __init__(self,U,r,rho,z0,space=pot.Space([-1,5],[0,3],1000)):
        
        super().__init__(space)
        self.r = r
        self.U = U
        self.rho = rho
        self.cylinder = pot.Cylinder(U=U,r=r,space=space)
        
        self.z0 = z0
        self.conjz0 = np.conjugate(z0)
        self.offsetV1 = [np.real(self.z0), np.imag(self.z0)]
        self.offsetV2 = [np.real(self.r**2/self.conjz0), np.imag(self.r**2/self.conjz0)]
        self.offsetV3 = [np.real(self.conjz0), np.imag(self.conjz0)]
        self.offsetV4 = [np.real(self.r**2/self.z0), np.imag(self.r**2/self.z0)]

        self.V1 = pot.FreeVortex(self.rho, self.offsetV1, space=space)
        self.V2 = pot.FreeVortex(-self.rho, self.offsetV2, space=space)
        self.V3 = pot.FreeVortex(-self.rho, self.offsetV3, space=space)
        self.V4 = pot.FreeVortex(self.rho, self.offsetV4, space=space)

        self.__object__ = self.cylinder + (self.V1 + self.V2 + self.V3 + self.V4)

    def updateSpace(self,space):
        return Foppl(U=self.U, r=self.r, rho=self.rho, z0=self.z0, space=space)


    def plot(self):
        self.__object__.plot()
