#!/bin/bash

#SBATCH --job-name=pytorch
#SBATCH --account=uwit
#SBATCH --partition=ckpt-all
#SBATCH --gpus=1
#SBATCH --mem=20G
#SBATCH --time=00:10:00
#SBATCH --output=%x_%j.out

# Define paths
PYTORCH=/gscratch/scrubbed/jupyter-tutorial/pytorch.sif
WORKDIR=/gscratch/scrubbed/$USER/jupyter-tutorial
SCRIPT=pytorch_demo.py

# Run your workflow
apptainer exec --nv --bind /gscratch $PYTORCH python ${WORKDIR}/${SCRIPT}