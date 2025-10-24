# Euler — Potential Flow Toolbox

Small Python toolbox for constructing and visualising potential flows (cylinder, free vortex, Föppl configuration).

<p align="center">
<img width="288" height="222" alt="image" src="https://github.com/user-attachments/assets/cc874ff1-63d0-4835-b26e-7de50a72f56a" />
<img width="288" height="230" alt="image" src="https://github.com/user-attachments/assets/f0c8f900-d9bc-4b9b-b340-050ec62f462f" />
<img width="370" height="430" alt="image" src="https://github.com/user-attachments/assets/fc8ff763-c529-4c3d-b08e-ae1af4e9cfdf" />
</p>

## Quick start

Requirements:
- Python 3.7+
- numpy
- matplotlib

Install dependencies:
```sh
pip install numpy matplotlib
```

Run the demo:
```sh
python main.py
```

## Project structure

- main.py — demo script
- lib/ — library modules
  - lib/potential.py — core potential-flow objects and grid utilities
  - lib/foppl.py — Föppl vortex system
  - lib/lib_potential.py — analytic potential functions
  - lib/complex/ — complex helpers
