<!-- omit in toc -->
# Hands-on Exercise: Running Jobs on Tillicum

This hands-on exercise walks you through the essential steps of submitting and monitoring jobs on Tillicum.

You’ll learn how to start an interactive job, load the Conda module, run Python code (both interactively and in batch mode), launch an array job for parallel tasks, and check your resource usage.

> 🎯 **GOAL:** Learn how to load your computing environment and run jobs efficiently on Tillicum.

**Overview**

- [0. Preparation](#0-preparation)
- [1. Start an Interactive Job](#1-start-an-interactive-job)
- [2. Load the Conda Module](#2-load-the-conda-module)
- [3. Run a Simple Python Script](#3-run-a-simple-python-script)
- [4. Submit a Batch Job](#4-submit-a-batch-job)
- [5. Run an Array Job](#5-run-an-array-job)
- [6. Check Efficiency \& Usage](#6-check-efficiency--usage)
- [Optional: Cleanup](#optional-cleanup)

## 0. Preparation

If you haven't already, follow the instructions in [00-preparation](./00-preparation.md) to log in to Tillicum and set up your working directory for the following exercise.

## 1. Start an Interactive Job

> ⚠️ **WARNING: All compute work must be done on compute nodes.**

Request an interactive session with 1 GPU for 1 hour:

```bash
salloc --qos=interactive --gpus=1 --time=01:00:00
```

Once resources are allocated, confirm you’re on a compute node:

```bash
hostname
```

Then verify your GPU is visible:

```bash
nvidia-smi
```

You should see GPU details (e.g., NVIDIA H200 with driver and CUDA versions)

## 2. Load the Conda Module

Tillicum provides a shared Miniforge (Conda) module with Python preinstalled.

Load Conda module with:

```bash
module load conda
```

You can explore available softwares with `module avail` or `module spider`. See [Software Environment on Tillicum](https://hyak.uw.edu/docs/tillicum/environment) for more details on how modules are managed on Tillicum.

Activate Conda base environment

```bash
conda activate
```

Confirm that Python is available:

```bash
python --version
which python
```

You’ll see the system Miniforge Python path under /gpfs/software/miniforge3/25.3.1-3/.

## 3. Run a Simple Python Script

Run the provided example Python script:

```
python python_demo.py
```

Expected output:

```bash
Starting Tillicum Python demo job...
Python version: 3.12.11
Checking CUDA availability...
PyTorch not installed; skipping GPU check.
Job completed successfully.
```

> 📝 **NOTE:** In the base Conda environment, CUDA may appear unavailable because GPU-enabled libraries (e.g., PyTorch or TensorFlow) are not installed. That’s expected for this exercise.

## 4. Submit a Batch Job

Exit the interactive shell:

```bash
exit
```

Check the Python script which uses PyTorch:

```bash
nano pytorch_demo.py
```

This script demonstrates how to use PyTorch with Slurm array jobs to run multiple GPU-enabled tasks in parallel on Tillicum. 
Each array task automatically receives a unique SLURM_ARRAY_TASK_ID, which the script uses to select a different learning rate from a predefined list — simulating a simple hyperparameter sweep. 
The script performs a short GPU computation (a large matrix multiplication) to verify GPU functionality and measure elapsed time. 
After completing the computation, it writes a summary file (results_task_<ID>.txt) to the logs directory, recording the task ID, learning rate, runtime, and a numerical checksum for verification.

In practice, this same pattern can be adapted for parameter scans, dataset splits, or training multiple models in parallel — one of the most common HPC use cases for deep learning workflows.

Exit the text editor with `Ctrl+X`.

We'll first perform a test run with a single Slurm job. Open provided Slurm batch script:

```bash
nano pytorch_demo.slurm
```

Confirm it looks like this:

```bash
#!/bin/bash

#SBATCH --job-name=pytorch
#SBATCH --qos=normal
#SBATCH --gpus=1
#SBATCH --mem=100G
#SBATCH --time=00:10:00
#SBATCH --output=logs/%x_%j.out

# Define paths
PYTORCH=/gpfs/scrubbed/training_slurm/pytorch.sif
WORKDIR=/gpfs/scrubbed/$USER/tillicum-slurm
SCRIPT=pytorch_demo.py

# Run your workflow
apptainer exec --nv --bind /gpfs $PYTORCH python ${WORKDIR}/${SCRIPT}
```

> 📝 **About this script:** 
> 
> Tillicum supports **Apptainer containers** for running portable, reproducible software stacks. The example above uses a prebuilt container (pytorch.sif) with PyTorch and CUDA preinstalled.
>
> **Command breakdown:**
> - `apptainer exec container.sif command`: Run a command inside a container.
> - `--nv`: Enable NVIDIA GPU support inside the container to run a CUDA enabled application.
> - `--bind`: Bind /gpfs path on the host to the same path in the container.
> 
> 🗓️ **Stay Tuned:** 
> 
> We will hold separate, hands-on training sessions for building and running containers on Tillicum. Check our [Research Computing Calendar](https://calendar.washington.edu/sea_uwit-rc) for upcoming training events.

Submit the job:

```bash
sbatch pytorch_demo.slurm
```

Check the status of the job:

```bash
squeue -u $USER
```

After it finishes, view the standard output of the job:

```bash
cat logs/pytorch_*.out
```

Example output:

```bash
Starting PyTorch Array Task 0
Learning rate: 0.0001
Hostname: g001
PyTorch version: 2.4.0a0+3bcc3cddb5.nv24.07
CUDA available: True
GPU detected: NVIDIA H200

Computation complete! Result checksum: 2.499e+11
Elapsed time: 0.29 seconds

Results saved to results_task_0.txt
```

Then check the file written by the Python script:

```bash
cat logs/results_task_0.txt
```

Example output:

```bash
Task 0
Learning rate: 0.0001
Time: 0.29s
Checksum: 2.499e+11
```

## 5. Run an Array Job

Job arrays are an efficient way to submit and manage multiple similar jobs in parallel.

Open the array script:

```bash
nano pytorch_array.slurm
```

Make sure it includes:

```bash
#SBATCH --array=0-4%2
#SBATCH --output=logs/%x_%A_%a.out
```

Submit the job:

```bash
sbatch pytorch_array.slurm
```

Monitor progress:

```bash
watch -n 5 squeue -u $USER
```

Use `Ctrl+C` to stop watching.

After completion, list and inspect the outputs:

```bash
ls logs/
cat logs/results_task_*.txt
```

Each output file corresponds to one array task — you’ll see that each task used a distinct learning rate.

## 6. Check Efficiency & Usage

Check efficiency metrics for any completed job:

```bash
seff <job_id>
```

The output will help you optimize the parameters used to request resources.

In the end, review you usage summary:

```bash
hyakusage
```

> 📝 **NOTE:** `hyakusage` is updated hourly. Real-time usage tracking will be available in a future release.

## Optional: Cleanup

When done, remove logs and temporary files:

```bash
rm -rf logs
```