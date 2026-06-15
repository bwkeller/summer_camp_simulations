#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --partition=1computeq
#SBATCH --reservation=its_6
#SBATCH --job-name=merger
#SBATCH --time=00:15:00

./gasoline -sz 12 merger.param &> screen.log
