import os
import shutil
from pytipsy import rtipsy, wtipsy

def setup_rundir(sim_name, h,g,d,s):
    os.makedirs(f"run_{sim_name}", exist_ok=True)
    run_script_content = f"""
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --partition=acomputeq
#SBATCH --job-name=merger
#SBATCH --time=00:15:00
#SBATCH --reservation=its_12

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
    wtipsy(os.path.join(f"run_{sim_name}", f'{sim_name}.tipsy'), h, g, d, s, STANDARD=True)
    print(f"\n[Success] experiment directory 'run_{sim_name}' has been created and prepared!")
    print(f"To run your simulation, type:")
    print(f"    cd run_{sim_name}")
    print(f"    sbatch run.sh")
