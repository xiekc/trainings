# Python on Hyak

Python is a widely used general-purpose programming language with a rich ecosystem of scientific and machine learning libraries. On Hyak, Python is mostly used for frameworks such as PyTorch, TensorFlow, and other machine learning and data analysis tools, but it is also widely used for general scientific computing, data processing, and automation.

Since Hyak is a shared HPC platform and you do not have root or administrative access, you will need to install and manage packages carefully within user-controlled environments. On Hyak, Python environments are typically managed in one of two ways:

- Conda environments (recommended for most workflows)
- Containers (e.g., Apptainer) for complex or GPU-dependent software stacks

## Python Versions on Hyak

Hyak comes with a system Python installation, but it is typically not intended for user computational workloads:

```bash
which python3
python3 --version
```

Hyak also provides a shared Miniforge (Conda) module with Python preinstalled.

```bash
salloc -A uwit -p ckpt-all -N 1 --time=2:00:00
module load conda
conda activate base

which python
python --version
```

You should see a Python executable located within the system Miniforge Python path.

The recommended workflow is to create and manage your own custom Conda environments, where you control the Python version and installed packages.

## Run a Simple Python Script

### Run with an Interactive Job

In the [Python Versions on Hyak](./03-python.md/#python-versions-on-hyak) section above, you already requested an interactive job and were allocated to a compute node.

Now run the provided example Python script using the Conda base environment:

```
cd /gscratch/scrubbed/$USER/jupyter-tutorial
python python_demo.py
```

Expected output:

```txt
Starting Klone Python demo job...
Python version: 3.12.12
Checking CUDA availability...
PyTorch not installed; skipping GPU check.
Job completed successfully.
```

> 📝 **NOTE:** In the base Conda environment, CUDA may appear unavailable because GPU-enabled libraries (e.g., PyTorch or TensorFlow) are not installed. This is expected.

When finished, exit the interactive session:

```bash
exit
```

## Submit a Batch Job

Next, we will run a Python script as a Slurm batch job, which allows it to execute unattended on the cluster.

First examine the Python script used in this example:

```bash
cat pytorch_demo.py
```

This script performs a small GPU-enabled computation using PyTorch.

Then, inspect the batch script:

```bash
cat pytorch_demo.slurm
```

Confirm it looks like this:

```bash
#!/bin/bash

#SBATCH --job-name=pytorch
#SBATCH --account=uwit
#SBATCH --partition=ckpt-all
#SBATCH --gpus=rtx6k:1
#SBATCH --mem=20G
#SBATCH --time=00:10:00
#SBATCH --output=%x_%j.out

# Define paths
PYTORCH=/gscratch/scrubbed/jupyter-tutorial/pytorch.sif
WORKDIR=/gscratch/scrubbed/$USER/jupyter-tutorial
SCRIPT=pytorch_demo.py

# Run your workflow
apptainer exec --nv --bind /gscratch $PYTORCH python ${WORKDIR}/${SCRIPT}
```

> 📝 **About this script:** 
> 
> Hyak supports **Apptainer containers** for running portable, reproducible software stacks. In this example, we use a prebuilt container (pytorch.sif) that includes PyTorch and CUDA installation.
>
> **Command breakdown:**
> 
> - `apptainer exec container.sif [command]`: Runs a command inside the container.
> - `--nv`: Enables NVIDIA GPU support inside the container so CUDA-enabled applications can access the GPU.
> - `--bind`: Binds /gscratch path on the host to the same path in the container so your data and scripts remain accessible.

Submit the batch job:

```bash
sbatch pytorch_demo.slurm
```

Check the job status:

```bash
squeue -u $USER
```

After it finishes, view the standard output of the job:

```bash
cat pytorch_*.out
```

Example output:

```txt
Starting PyTorch task with learning rate: 0.0001
Hostname: g3013
CUDA available: True
GPU detected: Quadro RTX 6000

Computation complete! Result checksum: 2.500e+11
Elapsed time: 0.73 seconds

Results saved to pytorch_results.txt
```

The Python script also writes a results file:

```bash
cat pytorch_results.txt
```

Example output:

```txt
Learning Rate: 0.0001
Time: 0.73s
Checksum: 2.500e+11
```