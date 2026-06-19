#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=acomputeq
#SBATCH --job-name=single
#SBATCH --time=00:15:00

./gasoline -sz 8 single.param &> screen.log
