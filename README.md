# YADE Cyclic Settlement Simulations for Babai and Bansilaghat Rivers

This repository contains YADE discrete element method (DEM) simulation scripts to analyze **cyclic settlement behavior** of soils from two rivers in Nepal:

- **Babai River:** Cohesive soil (clayey, silty sands)
- **Bansilaghat River:** Granular soil (gravelly sands)

---

## Overview

These scripts simulate soil response under cyclic vertical loading, recording settlement, settlement rate, and applied force over time, along with a live 3D particle view.

---

## Files

- `babai_river_sim.py`  
  Simulates **cohesive soil** typical of Babai River with lower stiffness, lower friction angle, and finer particles.

- `bansilaghat_river_sim.py`  
  Simulates **granular soil** typical of Bansilaghat River with higher stiffness, higher friction angle, and coarser particles.

---

## Requirements

- [YADE DEM software](https://yade-dem.org/) installed on Linux
- Python 3.x (YADE comes with embedded Python)
- Basic familiarity with running YADE scripts

---

## How to Run

1. Place the scripts on your Linux Desktop or preferred folder.

2. Open terminal and run:

   ```bash
   yade ~/Desktop/babai_river_sim.py
