#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=acomputeq
#SBATCH --job-name=merger
#SBATCH --time=00:15:00

./gasoline -sz 8 merger.param &> screen.log
