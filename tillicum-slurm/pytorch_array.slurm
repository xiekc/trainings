#!/bin/bash

#SBATCH --job-name=pytorch_array
#SBATCH --qos=normal
#SBATCH --gpus=1
#SBATCH --mem=100G
#SBATCH --time=00:10:00
#SBATCH --array=0-4%2
#SBATCH --output=logs/%x_%A_%a.out

# Define paths
PYTORCH=/gpfs/scrubbed/training_slurm/pytorch.sif
WORKDIR=/gpfs/scrubbed/$USER/tillicum-slurm
SCRIPT=pytorch_demo.py

# Run your workflow
apptainer exec --nv --bind /gpfs $PYTORCH python ${WORKDIR}/${SCRIPT}