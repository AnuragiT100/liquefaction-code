# DEM Simulation of Soil Behavior Using YADE

This repository contains YADE (Discrete Element Method) simulations for analyzing various aspects of soil behavior under cyclic loading conditions. The simulations focus on comparing properties of Babai River (loose, fine-grained soil) and Bansilaghat River (dense, coarse-grained soil).

##  Files Included
- `soil_simulation.py`: Main YADE script containing simulations for all five research topics.
- `*_kinetic_energy.csv` and `*_porosity.csv`: Output data for each simulation topic.
- `README.md`: This file.

## Simulation Topics

1. **Particle Shape Effect**  
   - Simulates different particle shapes: `spherical`, `angular`, and `flake` (via packing changes).
   - Based on Babai river soil characteristics.

2. **Grain Size Distribution Effect**  
   - Simulates `uniform`, `well_graded`, and `poorly_graded` soils.
   - Helps assess effect of gradation on energy dissipation and porosity.

3. **Cyclic Loading Frequency & Amplitude Effect**  
   - Studies the effect of different loading frequencies (0.5 Hz, 1.0 Hz, 2.0 Hz) and amplitudes (0.01, 0.02, 0.04).
   - Useful in liquefaction potential assessments.

4. **Density & Confining Pressure Effect**  
   - Varies soil density (1800, 2000, 2200 kg/m³).
   - Reflects differences in compaction and pre-consolidation.

5. **Direct Cyclic Shear Force on Surface Particles**  
   - Applies sinusoidal shear force to particles on the surface.
   - Compares loose Babai vs. dense Bansilaghat soil behavior.

## Software Requirements
- [YADE](https://yade-dem.org/)
- Python libraries: `numpy`

##  How to Run
1. Open YADE and load the script:
   ```bash
   yade soil_simulation.py
