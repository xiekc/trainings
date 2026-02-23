<!-- omit in toc -->
# Hands-on Exercise: Running a Python Script on Hyak Klone

This hands-on exercise will guide you through the essential steps for running a Python script on Hyak Klone:

You’ll create a working directory, start an interactive job, load modules, build a Conda environment, connect that environment to Jupyter Notebook, and finally run a Python script using Jupyter on Open OnDemand (OOD).

> 🎯 **GOAL:** Learn how to build and run a simple workflow on Hyak Klone — from terminal to Jupyter.

**Overview**

- [0. Create Your Working Directory](#0-create-your-working-directory)
- [1. Start an Interactive Job](#1-start-an-interactive-job)
- [2. Load Conda Module and Create an Environment](#2-load-conda-module-and-create-an-environment)
- [3. Register the Conda Environment for Jupyter Notebook](#3-register-the-conda-environment-for-jupyter-notebook)
- [4. Launch JupyterLab from Open OnDemand](#4-launch-jupyterlab-from-open-ondemand)
- [5. Troubleshooting](#5-troubleshooting)
- [6. Cleanup](#6-cleanup)

## 0. Create Your Working Directory

All hands-on exercise should be done in your `/gscratch/scrubbed` directory. Let's start with creating your own directory in `/gscratch/scrubbed` and cloning the onboarding repository to your directory:

```bash
# Skip this step if you've already completed it.
mkdir /gscratch/scrubbed/$USER
cd /gscratch/scrubbed/$USER
git clone https://github.com/UWrc/jupyter-tutorial.git
```

> 📝 **NOTE:** The `$USER` variable automatically expands to your username.

## 1. Start an Interactive Job

> ⚠️ **WARNING:** All compute work must run on compute nodes — **never** on the login node.

Request an interactive session with 1 GPU for 1 hour:

```bash
salloc --partition=ckpt-all --time=01:00:00
```

Once resources are allocated, confirm you're on a compute node:

```bash
hostname
```

You should see the hostname change from `klone-login0*` to something like `n***`.

## 2. Load Conda Module and Create an Environment

> ⚠️ **WARNING:** To install GPU-aware packages (e.g., cupy, PyTorch, TensorFlow), always request a GPU node for the installation.

List available modules and locate Conda:

```bash
module avail
module spider conda
```

Load the system Conda module:

```bash
module load conda
```

To avoid Home disk quota exceeded, open the file `$HOME/.condarc`:

```bash
nano ~/.condarc
```

and edit it to include following lines:

```yaml
envs_dirs:
  - /gscratch/scrubbed/<UW NetID>/conda/envs
pkgs_dirs:
  - /gscratch/scrubbed/<UW NetID>/conda/pkgs
```

Please replace <UW NetID> with your own UW NetID. Save (^O) and exit (^X) before continue in the shell.

This will place all of your environments and package caches in the specified directories by default, and you won't have to worry about specifying the full prefix to your environment when installing it or activating it.

Create a Conda environment in your scrubbed directory:

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

You'll see the full path such as `/gscratch/scrubbed/$USER/myenv/bin/python`, and `python --version` returns "Python 3.11.11". That confirms your environment is isolated and stored safely in your workspace.

## 3. Register the Conda Environment for Jupyter Notebook

You can now use your Conda environment inside Jupyter via Open OnDemand (OOD).

Install the IPython kernel package `ipykernel` from a terminal on Tillicum:

```bash
module load conda
conda activate myenv
conda install ipykernel
```

Register your environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name myenv --display-name "Python (Demo)"
```

> 💡 **TIP:** You only need to register each environment once.

## 4. Launch JupyterLab from Open OnDemand

**Preparation:** By default, Jupyter sessions on OOD start in your Home directory. To access files outside your Home directory, we need to create a symbolic link in your Home directory which links to the actual working directory in `/gscratch/scrubbed/$USER`.

```bash
cd ~
ln -s /gscratch/scrubbed/$USER scrubbed
```

Then launch JupyterLab:

- Go to [**Hyak Klone Open OnDemand Portal**](https://ondemand.hyak.uw.edu/).
- Choose **Interactive Apps** > **Jupyter**.
- Configure:
    - **Account**: trainob2025
    - **Number of hours**: 1
    - **User Interface**: Jupyter Lab
- Click **Launch**, wait for resources to be allocated.
- Click **Connect to Jupyter** when resources are ready.
- In JupyterLab, click **Python (Demo)** under **Notebook** in **Launcher** tab to open a new notebook.
- Go to **Kernel** > **Change Kernel** > select **Python (Demo)** in the dropdown box.

Now your computing environment is ready. 

To test your environment, copy the following code snippet and paste it in a cell, and then run the cell with shift+enter:

## 5. Troubleshooting

## 6. Cleanup

When finished:

1. Close the Jupyter browser tab.
2. Return to OOD and click **Delete** on your running session card.

This release compute resources back to the cluster.

> ⚠️ **WARNING:** For Tillicum, leaving sessions running consumes GPU hours and counts toward your project usage.

To remove your temporary environment later, run from a terminal on Tillicum:

```bash
module load conda
conda env remove --name myenv
```

> 📝 **NOTE:** Make sure your environment is *deactivated* before removing it.