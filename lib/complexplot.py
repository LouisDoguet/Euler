import numpy as np
import matplotlib.pyplot as plt

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

    def plot(self,title=''):

        fig, ax = plt.subplots(figsize=(12, 6))

        # Phase plot
        phase = np.angle(self.Z)
        module = np.abs(self.Z)
        module /= module.max()
        module = module**(1/50)
        ext = (self.X.min(), self.X.max(), self.Y.min(), self.Y.max())
        im = ax.imshow(phase, extent=ext, origin='lower', cmap='hsv', alpha=module, vmin=-np.pi, vmax=np.pi)
        ax.contour(self.X, self.Y, np.imag(self.Z), levels=50, colors='black', linewidths=0.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(title)
        cbar = fig.colorbar(im, ticks=[-3,0,3])
        cbar.ax.set_yticklabels([r'-$\pi$','0',r'$\pi$'])

        plt.show()
