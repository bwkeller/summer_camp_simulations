#!/usr/bin/env python
import argparse
import numpy as np
import pynbody as pyn
from pytipsy import rtipsy, wtipsy
import os
import shutil

nbulge = 65536

if __name__ == "__main__":
    # 1. Set up the argument parser with help text and boundaries
    parser = argparse.ArgumentParser(
        description="Build initial conditions for a Milky Way galaxy merger.",
        epilog="Example: ./make_merger.py 45 90 --mass_ratio 3 --distance 250"
    )

    # Required positional arguments (the angles)
    parser.add_argument("theta", type=float,
                        help="Rotation angle of the second galaxy around the X-axis (0 to 360 degrees)")
    parser.add_argument("phi", type=float,
                        help="Rotation angle of the second galaxy around the Z-axis (0 to 360 degrees)")

    # Optional arguments with physical bounds and defaults
    parser.add_argument("--distance", type=float, default=200.0,
                        help="Initial separation distance between galaxies in kpc [Allowed: 50.0 to 300.0, Default: 200.0]")

    parser.add_argument("--mass_ratio", type=float, default=1.0,
                        help="Mass ratio of Galaxy 1 to Galaxy 2 (e.g., 3 means Galaxy 2 is 1/3 the mass) [Allowed: 1.0 to 5.0, Default: 1.0]")

    parser.add_argument("--impact_param", type=float, default=0.0,
                        help="Impact parameter / sideways velocity factor. Higher = wider flyby, 0 = head-on [Allowed: 0.0 to 1.5, Default: 0.0]")

    parser.add_argument("--name", type=str, default="merger",
                        help="Unique name for this experiment directory and files [Default: merger]")

    args = parser.parse_parser_args() if hasattr(parser, 'parse_parser_args') else parser.parse_args()

    # 2. Enforce Physical Bounds (Guards to keep the simulation stable)
    if not (50.0 <= args.distance <= 300.0):
        print(f"Error: Distance ({args.distance} kpc) is out of bounds (50 to 300). Galaxies will either overlap or never meet!")
        exit(1)

    if not (1.0 <= args.mass_ratio <= 5.0):
        print(f"Error: Mass ratio ({args.mass_ratio}) must be between 1.0 (equal mass) and 5.0 (minor merger).")
        exit(1)

    if not (0.0 <= args.impact_param <= 1.5):
        print(f"Error: Impact parameter ({args.impact_param}) must be between 0.0 (head-on) and 1.5 (fly-by).")
        exit(1)

    # 3. Apply the Physics constants
    d0 = args.distance
    v0 = 200.0  # km/s base velocity
    v0 /= 20.7403

    h, g, d, s = rtipsy('mw.tipsy')
    n_particles = len(d['x'])
    h_new = h.copy()
    h_new['n'] = n_particles * 2
    h_new['ndark'] = 0
    h_new['nstar'] = n_particles * 2

    g_new = {}
    d_new = {}
    s_new = {}
    for k in d.keys():
        s_new[k] = np.tile(d[k], 2)

    # Set up star properties
    s_new['tform'] = np.ones(s_new['mass'].shape)
    s_new['tform'][:nbulge] -= 1
    s_new['tform'][n_particles:n_particles+nbulge] -= 1
    s_new['metals'] = np.zeros(s_new['mass'].shape)

    # Prepare the rotated disk data for Galaxy 2
    snap = pyn.snapshot.new(star=n_particles)
    snap['x'], snap['y'], snap['z'] = d['x'], d['y'], d['z']
    snap['vx'], snap['vy'], snap['vz'] = d['vx'], d['vy'], d['vz']
    snap.rotate_x(args.theta)
    snap.rotate_z(args.phi)

    # Galaxy 1: Unrotated, static baseline (First half)
    s_new['x'][:n_particles] = d['x']
    s_new['y'][:n_particles] = d['y']
    s_new['z'][:n_particles] = d['z']
    s_new['vx'][:n_particles] = d['vx']
    s_new['vy'][:n_particles] = d['vy']
    s_new['vz'][:n_particles] = d['vz']

    # Galaxy 2: Rotated, dynamic target (Second half)
    s_new['x'][n_particles:] = snap['x']
    s_new['y'][n_particles:] = snap['y']
    s_new['z'][n_particles:] = snap['z']
    s_new['vx'][n_particles:] = snap['vx']
    s_new['vy'][n_particles:] = snap['vy']
    s_new['vz'][n_particles:] = snap['vz']

    # 3. Apply Virial scaling exclusively to Galaxy 2 (Second half)
    if args.mass_ratio > 1.0:
        # Scale down mass
        s_new['mass'][n_particles:] /= args.mass_ratio

        # Scale down internal velocity structure so it stays bound
        internal_velocity_scaling = np.sqrt(1.0 / args.mass_ratio)
        s_new['vx'][n_particles:] *= internal_velocity_scaling
        s_new['vy'][n_particles:] *= internal_velocity_scaling
        s_new['vz'][n_particles:] *= internal_velocity_scaling

    # 4. Handle global orbital dynamics (Approach velocities and placement)
    # Move them apart safely within our new capped screen space
    s_new['x'][:n_particles] += d0 / 2   # Moves Galaxy 1 to the right (+X)
    s_new['x'][n_particles:] -= d0 / 2   # Moves Galaxy 2 to the left (-X)

    # Direct head-on collision component (closing velocity)
    s_new['vx'][:n_particles] -= v0 / 2  # Galaxy 1 moves left (-VX)
    s_new['vx'][n_particles:] += v0 / 2  # Galaxy 2 moves right (+VX)

    # Sideways component (Impact Parameter)
    s_new['vy'][:n_particles] -= args.impact_param
    s_new['vy'][n_particles:] += args.impact_param
    sim_name = args.name
    os.makedirs(f"run_{sim_name}", exist_ok=True)
    run_script_content = f"""
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --partition=icomputeq
#SBATCH --job-name=merger
#SBATCH --time=00:15:00

./gasoline -sz 12 {sim_name}.param &> screen.log
"""
    with open(os.path.join(f"run_{sim_name}", f"run.sh"), "w") as f:
        f.write(run_script_content.strip())

    param_content = f"""
achInFile               = {sim_name}.tipsy
achOutName              = galaxy
bStandard               = 1
iOutInterval            = 1
iLogInterval            = 1
dDelta                  = 0.2
dSoft                   = 0.02
nSteps                  = 300
dTheta                  = 0.7
dMsolUnit               = 1e8
dKpcUnit                = 1
"""
    with open(os.path.join(f"run_{sim_name}", f"{sim_name}.param"), "w") as f:
        f.write(param_content.strip())

    shutil.copy('gasoline', f'run_{sim_name}') 
    wtipsy(os.path.join(f"run_{sim_name}", f'{sim_name}.tipsy'), h_new, g_new, d_new, s_new, STANDARD=True)
    print(f"\n[Success] experiment directory 'run_{sim_name}' has been created and prepared!")
    print(f"To run your simulation, type:")
    print(f"    cd run_{sim_name}")
    print(f"    sbatch run.sh")
