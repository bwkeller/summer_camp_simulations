#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=acomputeq
#SBATCH --job-name=merger
#SBATCH --time=00:10:00

./gasoline -sz 4 merger.param &> screen.log
