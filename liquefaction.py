from yade import pack, plot, qt
from yade import FrictMat, ForceResetter, InsertionSortCollider, InteractionLoop, \
    Ig2_Sphere_Sphere_ScGeom, Ig2_Box_Sphere_ScGeom, Ip2_FrictMat_FrictMat_FrictPhys, \
    Law2_ScGeom_FrictPhys_CundallStrack, NewtonIntegrator, Bo1_Sphere_Aabb, Bo1_Box_Aabb, PyRunner
from yade.utils import aabbWalls
from math import radians, sin, pi
import os

O.reset()

# Babai River soil parameters (finer sand with some fines)
babai_soil = FrictMat(
    young=5e6,                # Softer soil than Bansilaghat (lower Young's modulus)
    poisson=0.3,
    frictionAngle=radians(28),  # Lower friction angle for silty sands
    density=1700,             # Lower density reflecting sand with fines
)
soilId = O.materials.append(babai_soil)

sp = pack.SpherePack()
sp.makeCloud(
    minCorner=(0, 0, 0),
    maxCorner=(0.1, 0.1, 0.1),
    rMean=0.002,      # Smaller mean radius ~2 mm for finer sands
    rRelFuzz=0.5,     # More variability in size (poorly graded to well graded)
    num=1500,         # More particles to reflect finer grains
    seed=5
)
sp.toSimulation(material=soilId)

walls = aabbWalls(thickness=0.005, material=soilId)
wallIds = O.bodies.append(walls)

O.engines = [
    ForceResetter(),
    InsertionSortCollider([Bo1_Sphere_Aabb(), Bo1_Box_Aabb()]),
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom(), Ig2_Box_Sphere_ScGeom()],
        [Ip2_FrictMat_FrictMat_FrictPhys()],
        [Law2_ScGeom_FrictPhys_CundallStrack()]
    ),
    NewtonIntegrator(damping=0.2, gravity=(0, 0, -9.81)),
]

frequency = 0.5
amplitude = 2000      # Lower amplitude representing lower loading or weaker soil
duration = 60
steps_per_cycle = 50
total_steps = int(duration * frequency * steps_per_cycle)

settlement_data = []
force_data = []
settlement_rate_data = []
prev_settlement = None

def applyCyclicLoad():
    t = O.time
    force = amplitude * sin(2 * pi * frequency * t)
    O.forces.setPermF(wallIds[5], (0, 0, -force))
    force_data.append((t, force))

def get_top_layer_settlement():
    top_particles_z = [b.state.pos[2] for b in O.bodies if b.shape and b.state.pos[2] > 0.095]
    if top_particles_z:
        avg_z = sum(top_particles_z) / len(top_particles_z)
        return 0.1 - avg_z
    else:
        return 0.0

def monitorSettlementAndRate():
    global prev_settlement
    t = O.time
    settlement = get_top_layer_settlement()
    settlement_data.append((t, settlement))

    if prev_settlement is None:
        rate = 0.0
    else:
        dt = t - settlement_data[-2][0]
        rate = (settlement - prev_settlement) / dt if dt > 0 else 0.0
    settlement_rate_data.append((t, rate))
    prev_settlement = settlement

    print(f"Time: {t:.3f}s, Settlement: {settlement:.6f} m, Rate: {rate:.6f} m/s, Force: {force_data[-1][1]:.2f} N")

# Color particles based on radius to visualize grading
for b in O.bodies:
    if b.shape:  # skip walls or non-spheres
        r = b.shape.radius
        # Normalize radius for coloring between min (rMean*(1-rRelFuzz)) and max (rMean*(1+rRelFuzz))
        r_min = 0.002 * (1 - 0.5)
        r_max = 0.002 * (1 + 0.5)
        color_factor = (r - r_min) / (r_max - r_min)
        color_factor = min(max(color_factor, 0), 1)
        b.state.color = (color_factor, 0, 1 - color_factor)  # Red to Blue gradient

plot.plots = {'time': ['settlement', 'force', 'rate']}

O.engines += [
    PyRunner(command='applyCyclicLoad()', iterPeriod=1),
    PyRunner(command='monitorSettlementAndRate()', iterPeriod=steps_per_cycle),
]

qt.View()

O.run(total_steps, True)

desktop = os.path.expanduser("~/Desktop/Babai")
os.makedirs(desktop, exist_ok=True)

with open(os.path.join(desktop, "settlement.csv"), "w") as f:
    f.write("Time,Settlement\n")
    for t, s in settlement_data:
        f.write(f"{t},{s}\n")

with open(os.path.join(desktop, "force.csv"), "w") as f:
    f.write("Time,Force\n")
    for t, force in force_data:
        f.write(f"{t},{force}\n")

with open(os.path.join(desktop, "settlement_rate.csv"), "w") as f:
    f.write("Time,SettlementRate\n")
    for t, rate in settlement_rate_data:
        f.write(f"{t},{rate}\n")

print(f"✅ Data saved in: {desktop}")
