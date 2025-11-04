import numpy as np
import matplotlib.pyplot as plt

from lib.space import Space
from lib.complexplot import ComPlot

class ConformalMapping:
    def __init__(self,space=Space(xlim=[-1,1],ylim=[0,1],Nx=400)):
        self.PHY = space.X
        self.PSI = space.Y
        self.W = self.PHY + 1j*self.PSI
        self._space:Space = space

    def apply(self,f):
        self.W = f(self.W)

    def plot(self):
        ComPlot.fromMapping(self).plot(title='Conformal Mapping')

    def streamlines(self,xlabel='',ylabel='',title=''):
        ax = self._space.plot(np.real(self.W),-np.imag(self.W),title=title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.show()

    def animate(self, f, var_arg):
        ComPlot.fromMapping(self).animate(f,var_arg)
        def ff(z):
            return f(z,var_arg[-1])
        self.apply(ff)
