# Euler — Potential Flow Toolbox

Small Python toolbox for constructing and visualising potential flows (cylinder, free vortex, Föppl configuration).

<p align="center">
<img width="288" height="222" alt="image" src="https://github.com/user-attachments/assets/cc874ff1-63d0-4835-b26e-7de50a72f56a" />
<img width="288" height="230" alt="image" src="https://github.com/user-attachments/assets/f0c8f900-d9bc-4b9b-b340-050ec62f462f" />
<img width="370" height="430" alt="image" src="https://github.com/user-attachments/assets/fc8ff763-c529-4c3d-b08e-ae1af4e9cfdf" />
</p>


Display/Animation of transformation for complex Conformal mapping (Kirchhoff flows in convergent pipe)
<p align="center">
<img width="410" height="200" alt="image" src="https://github.com/user-attachments/assets/27aa003d-f6db-45cb-b1af-4a7785a96cc0" />
<img width="330" height="200" alt="image" src="https://github.com/user-attachments/assets/0e4216d5-9266-498e-a895-9f4575b78edd" />
<img width="600" height="300" alt="image" src="https://github.com/user-attachments/assets/a597ee06-7f7f-4ee4-9cd3-90efe5955123" />

</p>

## Quick start

Requirements:
- Python 3.7+
- numpy
- matplotlib
- scipy

Install dependencies:
```sh
pip install numpy matplotlib scipy
```

Run the demo:
```sh
python 'your script'.py
```

## Project structure

- main.py — demo script
- script_foppl.py — Foppl flow
- script_wedge.py — Wedge flow
- script_kirchhoff.py — K flow
- lib/ — library modules
  - lib/potential.py — Core potential-flow objects
  - lib/complexplot.py — Complex plotting structure
  - lib/mapping.py — Conformal mapping structure
  - lib/space.py — Grid utilities
  - lib/foppl.py — Föppl vortex system
  - lib/lib_potential.py — Analytic potential functions
