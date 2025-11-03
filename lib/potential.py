import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm
from matplotlib import colors
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np

import lib.lib_potential as pot
from lib.space import Space

import copy

def normalize(val):
    """
    `[-pi,pi]` -> `[0,1]`
    """
    return (val + np.pi)/(2*np.pi)

class AnalyticalFunction:
    '''
    Analytic function storing flow data
    '''

    def __init__(self,**kwargs):
        '''
        Create analytic function with given parameters.
        Entries in kwargs depend on the function used.
        1. U : Free stream velocity
        2. r : radius (for cylinder)
        3. rho : strength (for vortex)
        4. z : complex grid
        '''
        self._kwargs = kwargs
        self.function = __function__(**kwargs)
        self._kwargs.pop("f")

    def solve(self,**kwargs):
        '''
        Solve the analytic function at given parameters.
        Uptate internal parameters if kwargs are given.
        Returns complex potential
        '''
        if kwargs:
            self._kwargs = kwargs
        return self.function(**self._kwargs)

    def phy(self):
        '''
        Return the stream function (real part)
        '''
        return self.function(**self._kwargs).real

    def psi(self):
        '''
        Return the potential function (imaginary part)'''
        return self.function(**self._kwargs).imag

    def grid_solve(self,X,Y):
        '''
        Solve the analytic function on a given grid (X,Y)
        Return complex potential on the grid
        Saves the grid internally in the AnalyticalFunction object.

        @param X: 2D array of x-coordinates
        @param Y: 2D array of y-coordinates
        '''
        self.grid_generated=True
        self.X, self.Y = X, Y
        Z = X + 1j*Y
        GRD = self.function(**self._kwargs)
        self.Z = GRD
        self.__cm__ = np.angle(self.Z)
        return self.Z
    
    
    def plot(self)->None:
        """
        Displays wavefunction in 3D.

        - Re(phy) is plotted over Z axis
        - Im(phy) corresponds to the color
        """
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111, projection='3d')

        module = np.absolute(self.Z)
        phase = np.angle(self.Z)

        norm = colors.Normalize(vmin=0, vmax=2*np.pi)
        cmap = cm.twilight
        facecolors = cmap(norm(phase))

        surf = ax.plot_surface(self.X, self.Y, module, facecolors=facecolors, rcount=self.X.shape[0], ccount=self.X.shape[1])

        ax.set_xlabel(r'$x$')
        ax.set_ylabel('$y$')
        ax.set_zlabel('|z|')
        ax.set_title('Analytical Function')

        mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
        mappable.set_array(phase)
        cbar = fig.colorbar(mappable, ax=ax, fraction=0.046, pad=0.04, label='arg($z$)')

        cbar.set_ticks([0.0, np.pi, 2*np.pi])
        cbar.set_ticklabels([r'0', r'$\pi$', r'$2\pi$'])

        plt.show()


class __Potential__:
    def __init__(self,space=Space([-2,3],[-2,2],100),offset=[0,0]):
        '''
        Base class for potential flow objects.
        
        @param space: Space object defining the computational grid
        @param offset: list [x_offset, y_offset] defining the position offset of the object
        '''

        self._space = space
        self.offset = offset[0] + 1j*offset[1]
        self.W = None
        self._der = None
        self.u = None
        self.v = None
        self.patches = []

    def __add__(self,other):
        '''
        Add two potential flow objects together.

        @param other: another __Potential__ object
        @return: new __Potential__ object representing the combined flow
        '''
        obj = __Potential__(self._space,[np.real(self.offset), np.imag(self.offset)] )
        obj.u = self.u + other.u
        obj.v = self.v + other.v
        obj.patches = self.patches + other.patches
        return obj

    def __sub__(self,other):
        '''
        Subtract one potential flow object from another.

        @param other: another __Potential__ object
        @return: new __Potential__ object representing the resulting flow
        '''
        obj = __Potential__(self._space,[np.real(self.offset), np.imag(self.offset)] )
        obj.u = self.u - other.u
        obj.v = self.v - other.v
        obj.patches = self.patches + other.patches
        return obj

    def getVelocities(self):
        '''
        Compute the velocity field from the derivative of the complex potential.

        @return: tuple (u, v) of 2D arrays representing the x and y velocity components
        '''
        return self._der.phy(), -self._der.psi()
    
    def getAX(self,nfig=1,title=''):
        '''
        Get the axis object for plotting the velocity field.

        @param nfig: figure number
        @param title: title of the plot
        @return: matplotlib axis object
        '''
        return self._space.plot(self.u,self.v,nfig=nfig,title=title)
       
    def plot(self,nfig=1,title=''):
        '''
        Plot the potential flow object with its patches.

        @param nfig: figure number
        @param title: title of the plot
        '''
        ax = self.getAX(nfig=nfig,title=title)
        for p in self.patches:
            ax.add_artist(copy.copy(p))
        plt.show()



class Cylinder(__Potential__):
    def __init__(self, U, r, offset=[0,0], space=Space([-2,3],[-2,2],100)):
        '''
        Create a cylinder potential flow object.

        @param U: free stream velocity
        @param r: radius of the cylinder
        @param offset: list [x_offset, y_offset] defining the position of the cylinder
        @param space: (Optional) Space object defining the computational grid
        '''
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
        ''' 
        Update the axis for plotting the cylinder potential flow.
        
        @param nfig: figure number
        @return: matplotlib axis object
        '''
        AX = super().getAX(nfig=nfig,title='Potential flow : Cylinder')
        return AX

class FreeVortex(__Potential__):
    def __init__(self, rho, offset=[0,0], space=Space([-2,3],[-2,2],100)):
        '''
        Create a free vortex potential flow object.

        @param rho: strength of the vortex
        @param offset: list [x_offset, y_offset] defining the position of the vortex
        @param space: (Optional) Space object defining the computational grid
        '''

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
        '''
        Update the axis for plotting the free vortex potential flow.

        @param nfig: figure number
        @return: matplotlib axis object
        '''
        
        AX = super().getAX(nfig=nfig,title='Potential flow : Free vortex')
        return AX
    
class Wedge(__Potential__):
    def __init__(self, U, m, offset=[0,0], space=Space([-2,3],[-2,2],100)):
        '''
        Create a wedge potential flow object.

        @param U: free stream velocity
        @param n: wedge exponent
        @param offset: list [x_offset, y_offset] defining the position of the wedge
        @param space: (Optional) Space object defining the computational grid
        '''
        super().__init__(space,offset)
        self.U = U
        self.m = m
        self.W = AnalyticalFunction(U=self.U, m=self.m, z=self._space.Z - self.offset, f=pot.Wwedge)
        self._der = AnalyticalFunction(U=self.U, m=self.m, z=self._space.Z - self.offset, f=pot.derWwedge)
        self.u, self.v = self.getVelocities()
        if m != 1:
            self.alpha = np.rad2deg(np.pi/(2*(self.m-1)))
        else:
            self.alpha = None

    def updateAX(self,nfig=1):
        '''
        Update the axis for plotting the wedge potential flow.

        @param nfig: figure number
        @return: matplotlib axis object
        '''
        
        AX = super().getAX(nfig=nfig,title='Potential flow : Wedge')
        return AX

def __function__(**kwargs):
    """
    Analytic function storing flow data
    """
    return kwargs["f"]


class Source(__Potential__):    
    
    def __init__(self, m, offset=[0,0], space=Space([-2,3],[-2,2],100)):
        '''
        Create a source potential flow object.

        @param m: strength of the source
        @param offset: list [x_offset, y_offset] defining the position of the source
        @param space: (Optional) Space object defining the computational grid
        '''
        super().__init__(space,offset)
        self.m = m
        self.W = AnalyticalFunction(m=self.m, z=self._space.Z - self.offset, f=pot.Wsource)
        self._der = AnalyticalFunction(m=self.m, z=self._space.Z - self.offset, f=pot.derWsource)
        self.u, self.v = self.getVelocities()
        r = 0.2 + abs(m)/50 * 0.6      # outer radius increases
        width = 0.6*abs(m)/50
        self.patches.append(
            mpatches.Annulus((offset[0],offset[1]),r,width, color='0.6', ec="none")
        )
