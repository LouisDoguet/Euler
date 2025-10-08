import lib.complex as comp
import matplotlib.pyplot as plt
import numpy as np

# Add the Complex numbers library

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

    def grid_solve(self,X,Y):
        self.grid_generated=True
        self.X, self.Y = X, Y
        Z = X + 1j*Y
        GRD = self.function(**self._kwargs)
        self.Z = comp.Complex(GRD) 
        return self.Z

    def plot(self, nlevels=300):
        if not self.grid_generated:
            raise ValueError("please .grid_solve(X,Y) before plotting")
        X = self.X
        Y = self.Y
        Z = self.Z
        fig, ax = plt.subplots()
        cr = ax.contour(X, Y, np.real(Z), nlevels, colors='red', linewidths=1)
        ci = ax.contour(X, Y, np.imag(Z), nlevels, colors='black', linewidths=1)

        # ax.clabel(cr, inline=True, fontsize=8, fmt='%1.2f')
        # ax.clabel(ci, inline=True, fontsize=8, fmt='%1.2f')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Isolines: psi (red), phi (black)')
        ax.set_aspect('equal')
        plt.grid(True)
        plt.show()


def __function__(**kwargs):
    """
    Analytic function storing flow data
    """
    return kwargs["f"]
