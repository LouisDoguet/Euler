import numpy as np
import matplotlib.pyplot as plt

from lib.space import Space
from lib.complexplot import ComPlot

class ConformalMapping:
    def __init__(self,space=Space(xlim=[-1,1],ylim=[0,1],Nx=400)):
        self.PHY = space.X
        self.PSI = space.Y
        self.W = self.PHY + 1j*self.PSI
        self._space = space

    def apply(self,f):
        self.W = f(self.W)

    def plot(self):
        ComPlot.fromMapping(self).plot(title='Conformal Mapping')
