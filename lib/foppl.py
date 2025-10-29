import numpy as np
import lib.potential as pot 

class Foppl(pot.__Potential__):
    def __init__(self,U,r,rho,z0,space=pot.Space([-2,3],[-2,2],100)):
        ''' 
        Foppl vortex system around a cylinder.
        Created by superimposing a cylinder and four free vortices.

        @param U: free stream velocity
        @param r: radius of the cylinder
        @param rho: strength of the vortices
        @param z0: Upper vortex position (complex number)
        @param space: (Optional) Space object defining the computational grid
        '''

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

        self.vortices = self.V1 + self.V2 + self.V3 + self.V4

        self.__object__ = self.cylinder + (self.V1 + self.V2 + self.V3 + self.V4)

    def updateSpace(self,space):
        '''
        Update the computational space of the Foppl vortex system.

        @param space: new Space object
        '''
        return Foppl(U=self.U, r=self.r, rho=self.rho, z0=self.z0, space=space)

    def plot_cylinder(self):
        '''
        Plot only the cylinder vortex system.
        '''
        self.cylinder.plot(title='Cylinder in Foppl Vortex System \n U={}, r={}'.format(self.U,self.r))

    def plot_vortices(self):
        '''
        Plot only the free vortices in the Foppl vortex system.
        '''
        (self.V1 + self.V2 + self.V3 + self.V4).plot(title='Free Vortices in Foppl Vortex System \n ρ={}, z0={:.2f}'.format(self.rho,self.z0))


    def plot(self):
        '''
        Plot the Foppl vortex system.

        @param title: title of the plot
        '''
        self.__object__.plot(title='Foppl Vortex System \n U={}, r={}, ρ={}, z0={:.2f}'.format(self.U,self.r,self.rho,self.z0))
