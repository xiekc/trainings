#!/bin/bash

#SBATCH --job-name=python_batch
#SBATCH --account=uwit
#SBATCH --partition=ckpt-all
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10G
#SBATCH --time=00:10:00
#SBATCH --output=%x_%j.out

# Load necessary modules and activate your conda environment
module load conda
conda activate myenv

# Run your workflow
python python_batch.py