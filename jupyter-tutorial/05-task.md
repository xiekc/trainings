<!-- omit in toc -->
# Hands-on Exercise: Running Python in Jupyter on Hyak Klone

This hands-on exercise guides you through the essential steps for running **Python in Jupyter on Hyak Klone**.

You will:

- create a working directory
- start an interactive job
- build a Conda environment
- register that environment as a Jupyter kernel
- launch Jupyter through Open OnDemand
- run Python inside a Jupyter notebook

> 🎯 **GOAL:** Learn how to build and run a simple Python workflow on Hyak Klone — from terminal to Jupyter.

**Overview**

- [0. Create Your Working Directory](#0-create-your-working-directory)
- [1. Start an Interactive Job](#1-start-an-interactive-job)
- [2. Load Conda and Create an Environment](#2-load-conda-and-create-an-environment)
- [3. Register the Conda Environment as a Jupyter Kernel](#3-register-the-conda-environment-as-a-jupyter-kernel)
- [4. Launch JupyterLab through Open OnDemand](#4-launch-jupyterlab-through-open-ondemand)
- [5. Run Python in Jupyter](#5-run-python-in-jupyter)
- [6. Manage Packages in a Conda Environment](#6-manage-packages-in-a-conda-environment)
- [7. Cleanup](#7-cleanup)
- [8. Run a Python Script as a Slurm Job (Optional)](#8-run-a-python-script-as-a-slurm-job-optional)

## 0. Create Your Working Directory

If you have not already completed the preparations steps, please follow the instructions in [00-preparation.md](./00-preparation.md) to set up your Hyak account, log in to Klone, configure storage, and clone the git repository for this tutorial.

Navigate to your working directory for this tutorial:

```bash
cd /gscratch/scrubbed/$USER/jupyter-tutorial
```

## 1. Start an Interactive Job

> ⚠️ **WARNING:** All compute work must run on compute nodes — **never** on the login node.

Request an interactive session for 1 hour:

```bash
salloc -A uwit -p ckpt-all -N 1 --time=01:00:00
```

Once resources are allocated, confirm you are on a compute node:

```bash
hostname
```

The hostname should change from `klone-login0*` to something like `n***`.

> 💡 **TIP:** If you requested a GPU node, you can also verify GPU visibility:
> ```bash
> salloc -A uwit -p ckpt-all --gpus 1 --time=01:00:00
> nvidia-smi
>```

## 2. Load Conda and Create an Environment

**Load Conda Module**

First locate the Conda module:

```bash
module spider conda
```

Load the system Conda module:

```bash
module load conda
```

**Configure Conda Storage Location**

By default, Conda installs environments in your home directory, which only has a **10 GB quota**. We recommend storing environments in your project directory. But for this tutorial, we'll use the **scrubbed storage**.

Create or edit your Conda configuration file:

```bash
nano ~/.condarc
```

Add the following:

```yaml
envs_dirs:
  - /gscratch/scrubbed/$USER/conda/envs
pkgs_dirs:
  - /gscratch/scrubbed/$USER/conda/pkgs
```

Please replace `$USER` with your own UW NetID. Save (^O) and exit (^X) before continue in the shell.

This will place all of your environments and package caches in the specified directories by default, and you won't have to worry about specifying the full prefix to your environment when installing it or activating it.

**Create a Conda Environment**

Create a simple Python environment:

```bash
# Rename "myenv" to anything you prefer.
conda create --name myenv python=3.11 numpy scipy
```

Activate the environment:

```bash
conda activate myenv
```

Verify Python is ready in your environment:

```bash
which python
python --version
```

Example output:

```txt
/gscratch/scrubbed/$USER/conda/envs/myenv/bin/python
Python 3.11.x
```

This confirms your environment is now isolated and stored safely in your workspace.

> ⚠️ **WARNING:** To install GPU-aware packages (e.g., cupy, PyTorch, TensorFlow), always request a GPU node for the installation.

## 3. Register the Conda Environment as a Jupyter Kernel

To use this environment inside Jupyter, install the IPython kernel package `ipykernel` from a terminal on Klone:

```bash
conda install ipykernel
```

Register the environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name myenv --display-name "Python (Demo)"
```

> 💡 **TIP:** You only need to register each environment once.

You can verify that the kernel is registered:

```bash
jupyter kernelspec list
```

## 4. Launch JupyterLab through Open OnDemand

Launch JupyterLab:

- Log in to [**Hyak Klone Open OnDemand portal**](https://ondemand.hyak.uw.edu/).
- From the OOD dashboard top menu, select **Interactive Apps** > **Jupyter**.
- Configure the job:
    - **Account**: uwit
    - **Partition**: ckpt-all
    - **Server Environment**: "Module: jupyter/minimal"
    - **Memory (GB)**: 10
    - **Number of hours**: 1
- Click **Launch**, wait for resources to be allocated.
- Click **Connect to Jupyter** when job is ready.

Now your computing environment is ready.

## 5. Run Python in Jupyter

Once JupyterLab opens:

- In the **Launcher** tab, select **Python (Demo)** under **Notebook**.
- Alternatively, open an existing notebook and select **Kernel** > **Change Kernel** > **Python (Demo)** in the dropdown box to switch kernels.

This starts a new notebook using your Conda environment.

**Test Your Environment**

Copy the following code snippet and paste it in a new cell, and then run the cell with `Shift`+`Enter`:

```python
import sys
import numpy as np

print("Python executable:", sys.executable)
print("Python version:", sys.version)

x = np.random.rand(1000,1000)
print("Array shape:", x.shape)
print("Mean value:", x.mean())
```

The output confirms that:

- Python is running from your custom Conda environment
- NumPy is installed and working correctly

## 6. Manage Packages in a Conda Environment

Conda environments allow you to add or remove packages at any time as your workflow evolves.

Create a new cell in your notebook and run the following:

```python
import matplotlib.pyplot as plt

# Generate sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a plot
plt.figure()
plt.plot(x, y)
plt.title("Simple Sine Wave")
plt.xlabel("x")
plt.ylabel("sin(x)");
```

You should see an ImportError, which indicates that matplotlib is not yet installed in your environment.

To install it, return to your terminal session on Klone where the environment is activated:

```bash
conda activate myenv
conda install matplotlib
```

After installation finishes, return to your Jupyter notebook and run the cell again. You should now see a simple *sine* wave plot displayed in the notebook.

This demonstrates how packages installed in your Conda environment become immediately available to your Jupyter kernel.

## 7. Cleanup

When finished:

1. Save your notebook
2. Close the Jupyter browser tab
3. Return to the OOD dashboard
4. Click **Delete** on your running session card

This releases compute resources back to the cluster.

> ⚠️ **WARNING:** For Tillicum, leaving sessions running consumes GPU hours and counts toward your project usage.

## 8. Run a Python Script as a Slurm Job (Optional)

While Jupyter is useful for interactive exploration, many workflows on Hyak run as **Slurm batch jobs** so they can execute unattended. Batch jobs are ideal for longer computations, automated workflows, or jobs that do not require user interaction.

In this step, we will run a simple Python script using the **Slurm job scheduler**.

**Prepare Scipts**

Return to your terminal and navigate to the tutorial directory. First, inspect the Python script:

```bash
cat python_batch.py
```

This script performs a small numerical computation and prints the results.

Next, examine the Slurm job script:

```bash
cat python_batch.slurm
```

This script loads the Conda environment and runs the Python program on a compute node through Slurm.

**Submit the Job**

Submit the batch job to Slurm:

```bash
sbatch python_batch.slurm
```

Check the job status:

```bash
squeue -u $USER
```

Once the job has completed, view the standard output file generated by the job:

```bash
cat python_batch_*.out
```

The output should contain the printed results from the Python script.

**Remove the Demo Environment (Optional)**

If you no longer need the environment created during this tutorial, you can remove it from a terminal on Klone:

```bash
module load conda
conda deactivate
conda env remove -n myenv
```

> 📝 **NOTE:** Make sure your environment is *deactivated* before removing it.

> 💡 **Key takeaway:**
>
> You now know two common ways to run Python on Hyak:
> 
> - **Jupyter via Open OnDemand**: Interactive exploration, debugging, visualization
> - **Slurm batch jobs**: Large simulations, training runs, automated workflows
>
> Both approaches can use the same Conda environment, ensuring consistency between development and production runs on the cluster.