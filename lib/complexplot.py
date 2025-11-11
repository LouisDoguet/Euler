import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import copy

class ComPlot:
    def __init__(self,X,Y,Z):
        self.Z = Z
        self.X = X
        self.Y = Y

    @classmethod
    def fromMapping(cls, conformal_mapping):
        x = conformal_mapping.PHY
        y = conformal_mapping.PSI
        z = conformal_mapping.W 
        return cls(x,y,z)

    def __plot__(self,title='',xlabel='x',ylabel='y',levels=50):

        fig, ax = plt.subplots(figsize=(12, 6))

        phase = np.angle(self.Z)

        module = np.abs(self.Z)
        module /= module.max()
        module = module**(1/10)

        ext = (self.X.min(), self.X.max(), self.Y.min(), self.Y.max())
        im = ax.imshow(phase, extent=ext, origin='lower', cmap='hsv', alpha=module, vmin=-np.pi, vmax=np.pi)
        cont = ax.contour(self.X, self.Y, np.imag(self.Z), levels=levels, colors='black', linewidths=0.5)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        cbar = fig.colorbar(im, ticks=[-3,0,3])
        cbar.ax.set_yticklabels([r'-$\pi$','0',r'$\pi$'])

        return fig, ax, im, cont
    
    def plot(self,title='',xlabel='x',ylabel='y',levels=50):
        self.__plot__(title=title,xlabel=xlabel,ylabel=ylabel,levels=levels)
        plt.show()

    def animate(self,f,var_arg,title=''):

        fig, ax, im, cont = self.__plot__()
        ax.set_title(title)

        def update(frame):

            nonlocal cont
            nonlocal im
            nonlocal ax

            for c in ax.collections:
                c.remove()

            # recompute field for parameter frame
            tmpZ = f(self.Z,var_arg[int(frame)])

            phase = np.angle(tmpZ)
            module = np.abs(tmpZ)
            module /= module.max()
            module = module**(1/2)

            im.set_data(phase)
            im.set_alpha(module)

            cont = ax.contour(self.X, self.Y, np.imag(tmpZ),levels=50, colors='black', linewidths=0.5)

            return ax
        
        ani = FuncAnimation(fig, update, frames=np.linspace(0,len(var_arg)-1), blit=False, repeat=False, interval=1)

        plt.show()

