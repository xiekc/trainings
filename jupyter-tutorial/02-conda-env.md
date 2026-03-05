# Conda Environment

Conda allows you to create isolated environments that include specific versions of Python, libraries, and tools. This is essential in HPC environments, where reproducibility and dependency control are critical.

If you’re new to Conda, you may find this helpful: [Conda Cheatsheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)

## Load Conda Module

Hyak provides a minimal Miniforge (Conda) installation that you can utilize to build custom Conda environment. You must load it before using conda:

```bash
salloc -A uwit -p ckpt-all -N 1 --time=2:00:00
module load conda
```

The `conda` command becomes available now.

> 📝 **NOTE:** For Klone users, be sure to run the `module load` command on a compute node. After loading the system Conda module, you do not need to run `conda init` or modify your shell startup file (`$HOME/.bashrc`). The module handles environment setup for you.

## Create and Manage Conda Environments

### 1. Choose Where to Store Environments and Packages (Important)

By default, the system Conda stores environments in your home directory (`$HOME/.conda/envs`). However, your home directory on Hyak has a **10 GB** quota, which is often insufficient. 

We recommend installing Conda environments to your **project directory** under:

- Klone: `/gscratch/<myproject>/<myfolder>`
- Tillicum: `/gpfs/projects/<myproject>/<myfolder>`

**Option A (Recommended): Configure Defaults in `$HOME/.condarc`**

To store all of your environments and package caches in custom locations by default, edit (or create) your Conda configuration file:

```bash
nano ~/.condarc
```

Add to the file opened:

```yaml
envs_dirs:
  - /gscratch/<myproject>/<myfolder>/conda/envs
pkgs_dirs:
  - /gscratch/<myproject>/<myfolder>/conda/pkgs
always_copy: true
```

Replace <myproject> and <myfolder> with real paths.

**Option B: Use `--prefex` for Explicit Control**

Manually set the path to your Conda environment by `--prefix` and always activate your Conda environment with full path.

```bash
module load conda
conda create --prefix /gpfs/<myproject>/<myfolder>/myenv python=3.12
conda activate /gpfs/<myproject>/<myfolder>/myenv
```

This gives you complete control over where each environment lives.

### 2. Create a Conda environment

For example, create a custom Conda environment named "myenv" with Python 3.12 and other scientific packages installed:

```bash
module load conda
conda create -n myenv python=3.12 numpy scipy pandas matplotlib
```

Activate the environment:

```bash
conda activate myenv
```

Once activated, all `python`, `pip`, and `conda install` commands apply only to this environment. 

Conda has several default channels that will be used first for package installation with `conda install`. You can use another channel beyond the default channels, but we suggest that you select your channel carefully.

### 3. Manage Your Conda Environments

List installed packages in current environment:

```bash
conda list
```

List available Conda environments:

```bash
conda env list
```

Remove an environment:

```bash
conda env remove --name myenv
```

## Install Packages with `pip`

You can use `pip` inside a Conda environment to install Python packages. Anaconda provides some [best practices](https://www.anaconda.com/blog/using-pip-in-a-conda-environment) for using `pip` with Conda. Our suggested use of pip is inside a conda environment.

Example:
```bash
module load conda
conda activate myenv
pip install seaborn
```

This ensures that `pip` installs packages into the active Conda environment — **not globally** — making it easy to clean up completely when you are done.

See the [pip documentation](https://pip.pypa.io/en/stable/cli/pip_install/) for more information.

> 💡 **Best practices on Hayk:**
> 
> - Use separate environments for different projects
> - Use `pip install` inside a Conda environment
> - Install CUDA-aware packages on a **GPU node**, with compatible CUDA module/version loaded before installation.

## Containers (Optional)

Hyak supports Apptainer containers for portable, isolated software stacks. For complex GPU workflows, portable software stacks, or highly reproducible research, consider using Apptainer containers instead of Conda.

Useful resources:

- [NVIDIA's NGC Catalog](https://catalog.ngc.nvidia.com/?filters=&orderBy=weightPopularDESC&query=&page=&pageSize=) provides prebuilt containers with CUDA and NVIDIA drivers configured
- [Hyak Containers Documentation](https://hyak.uw.edu/docs/tools/containers)
- [Klone Containers Tutorial](https://hyak.uw.edu/docs/hyak101/containers/syllabus)
- [Tillicum Containers Tutorial](https://github.com/UWrc/tillicum-containers/)