import lib.complex as comp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import lib.lib_potential as pot
import copy

class AnalyticalFunction:

    def __init__(self,**kwargs):
        self._kwargs = kwargs
        self.function = __function__(**kwargs)
        self._kwargs.pop("f")

    def solve(self,**kwargs):
        if kwargs:
            self._kwargs = kwargs
        return comp.Complex(self.function(**self._kwargs))

    def phy(self):
        return self.function(**self._kwargs).real

    def psi(self):
        return self.function(**self._kwargs).imag

    def get_u(self):
        psi = self.psi()
        dy = self.Y[1][1]
        u = (psi[:][1:] - psi[:][:-1])/dy
        return u

    def grid_solve(self,X,Y):
        self.grid_generated=True
        self.X, self.Y = X, Y
        Z = X + 1j*Y
        GRD = self.function(**self._kwargs)
        self.Z = comp.Complex(GRD) 
        return self.Z


class Space:
    def __init__(self,xlim,ylim,Nx,Ny=None):
        if not Ny:
            Ny = Nx
        self.xmin = xlim[0]
        self.xmax = xlim[1]
        self.ymin = ylim[0]
        self.ymax = ylim[1]
        self.Nx = Nx
        self.Ny = Ny
        self._x = np.linspace(self.xmin,self.xmax,Nx)
        self._y = np.linspace(self.ymin,self.ymax,Ny)
        self.X, self.Y = np.meshgrid(self._x,self._y)
        self.Z = self.X+1j*self.Y

    def xy2rt(self,center):
        x0 = center[0]
        y0 = center[1]
        x = self.X - x0
        y = self.Y - y0
        theta = np.arctan(y/x)-np.pi/2
        r = x**2 + y**2
        return r, theta

    def plot(self,u,v,nfig=1,title=''):

        speed = np.sqrt(u**2 + v**2)

        fig = plt.figure(nfig)  # Reuse figure if it exists
        ax = fig.gca()
        ax.streamplot(self.X,self.Y,u,v,density=3,color=speed,linewidth=1,arrowsize=0.5,cmap='viridis',broken_streamlines=True)
        ax.set_aspect('equal')
        ax.set_title(title)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        return ax

class __Potential__:
    def __init__(self,space,offset=[0,0]):
        self._space = space
        self.offset = offset[0] + 1j*offset[1]
        self.W = None
        self._der = None
        self.u = None
        self.v = None
        self.patches = []

    def __add__(self,other):
        obj = __Potential__(self._space,[np.real(self.offset), np.imag(self.offset)] )
        obj.u = self.u + other.u
        obj.v = self.v + other.v
        obj.patches = self.patches + other.patches
        return obj

    def __sub__(self,other):
        obj = __Potential__(self._space,[np.real(self.offset), np.imag(self.offset)] )
        obj.u = self.u - other.u
        obj.v = self.v - other.v
        obj.patches = self.patches + other.patches
        return obj

    def getVelocities(self):
        return self._der.phy(), -self._der.psi()
    
    def getAX(self,nfig=1,title=''):
        return self._space.plot(self.u,self.v,nfig=nfig,title=title)
       
    def plot(self,nfig=1,title=''):
        ax = self.getAX(nfig=nfig,title=title)
        for p in self.patches:
            ax.add_artist(copy.copy(p))
        plt.show()

class Cylinder(__Potential__):
    def __init__(self, U, r, offset=[0,0], space=Space([-3,3],[-2,2],150,150)):
        super().__init__(space,offset)
        self.r = r
        self.U = U
        self.W = AnalyticalFunction(U=self.U, r=self.r, z=self._space.Z - self.offset, f=pot.Wcylinder)
        self._der = AnalyticalFunction(U=self.U, r=self.r, z=self._space.Z - self.offset, f=pot.derWcylinder)
        self.u, self.v = self.getVelocities()
        self.patches.append(
            mpatches.Circle((offset[0],offset[1]), self.r, color='0.8', ec="none")
        )

    def updateAX(self,nfig=1):
        ax = super().getAX(nfig=nfig,title='Potential flow : Cylinder')
        return AX

class FreeVortex(__Potential__):
    def __init__(self, rho, offset=[0,0], space=Space([-3,3],[-2,2],150,150)):
        super().__init__(space,offset)
        self.rho = rho
        self.W = AnalyticalFunction(rho=self.rho, z=self._space.Z - self.offset, f=pot.Wfreevortex)
        self._der = AnalyticalFunction(rho=self.rho, z=self._space.Z - self.offset, f=pot.derWfreevortex)
        self.u, self.v = self.getVelocities()
        r = 0.2 + abs(rho)/50 * 0.6      # outer radius increases
        width = 0.6*abs(rho)/50
        self.patches.append(
            mpatches.Annulus((offset[0],offset[1]),r,width, color='0.6', ec="none")
        )

    def updateAX(self,nfig=1):
        ax = super().getAX(nfig=nfig,title='Potential flow : Free vortex')
        return AX

def __function__(**kwargs):
    """
    Analytic function storing flow data
    """
    return kwargs["f"]
