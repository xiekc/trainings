#!/bin/bash

#SBATCH --job-name=loop_var
#SBATCH --qos=normal
#SBATCH --gpus=1
#SBATCH --mem=100G
#SBATCH --time=00:10:00
#SBATCH --output=logs/slurm-%j.out

# Define variables
WORKDIR="/gpfs/scrubbed/$USER/tillicum-slurm"
SCRIPT="loop_script.sh"

echo "Working directory: $WORKDIR"
cd $WORKDIR

# Run Bash script
time ./$SCRIPT 0 1000000

echo "Job completed successfully!"