import numpy as np
import matplotlib.pyplot as plt

from lib.space import Space
from lib.complexplot import ComPlot

import copy
from scipy.integrate import cumulative_trapezoid

class ConformalMapping:
    def __init__(self,space=Space(xlim=[-1,1],ylim=[0,1],Nx=400)):
        self.PHY = space.X
        self.PSI = space.Y
        self.W = self.PHY + 1j*self.PSI
        self._initW = copy.copy(self.W)
        self._space:Space = space
        self._list_function = []

    def apply(self,f):
        self._list_function.append(f)
        self.W = f(self.W)

    def plot(self):
        ComPlot.fromMapping(self).plot(title='Conformal Mapping')

    def streamlines(self,xlabel='',ylabel='',title=''):
        ax = self._space.plot(np.real(self.W),-np.imag(self.W),title=title,density=1)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.show()

    def animate(self, f, var_arg,title=''):
        ComPlot.fromMapping(self).animate(f,var_arg,title=title)
        def ff(z):
            return f(z,var_arg[-1])
        self.apply(ff)

    def integrate(self):
        Wint = cumulative_trapezoid(self.W, self.PSI[:, 0], axis=0, initial=0)
        self.W = Wint
        ComPlot.fromMapping(self).plot(title='Integration')
        self.streamlines()
