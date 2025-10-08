import numpy as np
import matplotlib.pyplot as plt

class Complex:
    def __init__(self, npobj):
        self._npobj = np.asarray(npobj, dtype=complex)

    @property
    def real(self):
        return np.real(self._npobj)

    @property
    def imag(self):
        return np.imag(self._npobj)

    def __add__(self, other):
        if isinstance(other, Complex):
            other = other._npobj
        return Complex(self._npobj + other)

    def __sub__(self, other):
        if isinstance(other, Complex):
            other = other._npobj
        return Complex(self._npobj - other)

    def __mul__(self, other):
        if isinstance(other, Complex):
            other = other._npobj
        return Complex(self._npobj * other)

    def __truediv__(self, other):
        if isinstance(other, Complex):
            other = other._npobj
        return Complex(self._npobj / other)

    def modulus(self):
        return np.abs(self._npobj)

    def argument(self):
        return np.angle(self._npobj)

    def conjugate(self):
        return Complex(np.conj(self._npobj))

    def to_polar(self):
        return self.modulus(), self.argument()

    @staticmethod
    def from_polar(r, theta):
        return Complex(r * np.exp(1j * theta))
    
    def plot_grd(self,X,Y):
        Z = self._npobj
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Real part → surface height
        surf = ax.plot_surface(
            X, Y, np.real(Z),
            facecolors=plt.cm.viridis(
                (np.imag(Z) - np.min(np.imag(Z))) / (np.max(np.imag(Z)) - np.min(np.imag(Z)))
            ),
            rstride=1, cstride=1, linewidth=0, antialiased=False
        )

        mappable = plt.cm.ScalarMappable(cmap='viridis')
        mappable.set_array(np.imag(Z))
        fig.colorbar(mappable, ax=ax, shrink=0.6, pad=0.1, label='Imaginary Part')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Re[f(X,Y)]')
        plt.title('Complex Function Surface')
        plt.show()

    def plot(self):
        plt.figure()
        plt.scatter(self.real, self.imag, marker='o')
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')
        plt.grid()
        plt.title('Complex Plane')
        plt.xlabel('Real')
        plt.ylabel('Imag')
        plt.show()

    def __getitem__(self, item):
        return self._npobj[item]

    def __repr__(self):
        return f"Complex({self._npobj})"
