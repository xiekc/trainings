# Modules

Hyak uses the [Lmod](https://lmod.readthedocs.io/en/latest/) environment module system to manage software.

Each loaded module dynamically modifies your shell environment (e.g. `PATH`, `LD_LIBRARY_PATH`) so that the corresponding executables and libraries become available.

Instead of manually editing environment variables, you simply load or unload modules.

## Understanding Your Environment

When you log in, your shell environment combines: 

- System defaults — environment variables and functions defined globally for all users.
- User customizations — variables or aliases defined in your startup files (e.g., `$HOME/.bashrc`, `$HOME/.bash_profile`).
- Loaded modules — software stacks that modify your environment dynamically.

Two especially important environment variables are:

- `PATH` — a colon-separated list of directory paths that the system searches for executables.
- `LD_LIBRARY_PATH` — a similar list where the system looks for shared libraries.

View the value of the `PATH` environment variable:
```bash
echo $PATH
```

When you load a module, it typically *prepends* new paths to these variables so your system uses the correct version of software.

## What is Lmod?

Lmod is a Lua-based implementation of the environment modules system. Through modulefiles, it allows you to:

- Switch between different software versions
- Maintain software stacks
- Use compiler/MPI-compatible builds
- Avoid manual environment configuration

Lmod supports hierarchical module structures through `MODULEPATH`, which help prevent incompatible software combinations.

> 📝 **NOTE:** On **Klone**, module commands are disabled on login nodes. Request a compute node before searching or loading any modules.

## Core Module Commands

The module command sets the appropriate environment variable independent of your shell.

| Command | Description|
|:-----|:-----|
| `module list` | List active modules in the current environment |
| `module avail` | List available modules in the current environment |
| `module spider [module]`| Search all installed modules (deep search across all module hierarchies) |
| `module load [modules]` | Load modules |
| `module swap [module1] [module2]` | Replace `module1` with `module2` |
| `module unload [modules]` | Unload specific modules |
| `module purge` | Unload ALL modules from the current environment |
| `module show [module]` | Show functions performed by loading module |
| `module help [module]` | Show module-specific help message |
| `module use [-a] [path]` | Prepend or append path to `MODULEPATH` |

Lmod provides a convenient shortcut command [`ml`](https://lmod.readthedocs.io/en/latest/010_user.html#ml-a-convenient-tool) for the `module` command.

> 💡 **TIP:** `ml` can be used instead of module, module load, or module list depending on the situation.

| Example | Equivalent|
|:-----|:-----|
| `ml` | `module list` |
| `ml [module]` | `module load [module]` |
| `ml -[module]` | `module unload [module]` |
| `ml avail` | `module avail` |

Any module sub-commands (e.g., avail, spider, show, etc.) can be written as `ml subcommand arg1 arg2`.

## Finding Modules

### Using `module avail`

List all modules visible in your current environment after starting an interactive session:

```bash
salloc -A uwit -p ckpt-all -N 1 --time=2:00:00
module avail
```

> 💡 **TIP:** **Klone** provides a shared directory under `/sw/contrib/mylab-src` where each group can install software intended for shared use across Klone users. See the [Hyak documentation](https://hyak.uw.edu/docs/tools/modules#how-do-i-create-shared-lmod-modules-on-klone) for instructions on creating and managing user-contributed Lmod modules.

To narrow results, for instance, if you want to see all `gcc` modules:

```bash
module avail gcc
```

> 📝 **NOTE:** `module avail` doesn't show modules from all trees in the hierarchical system, which is the case for **Tillicum**.

### Using `module spider` (Recommended)

The `module spider` command performs a **deep search** across all module hierarchies, even ones not currently visible:

```bash
module spider cuda
```

For detailed loading instructions:

```bash
module spider cuda/12.9.1
```

The above output also indicates a modulefile's complete name includes its name and version. An installed application can have several versions. If dependencies exist, `module spider` will also show them.

> 📝 **NOTE:** `module spider` is the most reliable way to search installed software and learn what prerequisites must be loaded first. **Always use `module spider` instead of `module avail` to find out how to `module load`.**

## Loading Modules on Klone

To load a module on Klone, run:

```bash
module load cuda/12.9.1
```

> ⚠️ **WARNING:** Do not include `module load` commands in your startup files (e.g., `$HOME/.bashrc` and `$HOME/.bash_profile`). This can cause conflicts when switching environments in batch jobs and interactive sessions.

### What Happens When You Load a Module?

You can inspect what a module changes:

```bash
module show jupyter/minimal
```

Key functions:

- `prepend_path` — adds directories to environment variables
- `setenv` — sets environment variables

This is how modules safely modify your runtime environment.

## Module Hierarchies on Tillicum (Optional)

Tillicum uses a hierarchical module structure to ensure compatibility between software stacks.

**Hierarchy Levels**

In Lmod module hierarchy, each compiler module adds to the `MODULEPATH` a compiler version modulefile directory. Only modulefiles that exist in that directory are packages that have been built with that compiler. Similarly, applications that use libraries depending on MPI implementations must be built with the same compiler - MPI pairing. This leads to modulefile hierarchy.

**Steps to Load Modules**

- Load a compiler (e.g., GCC) — only the modules built with that compiler becomes visible with `module avail`
- Load MPI built with that compiler
- Load applications built with that compiler + MPI stack

This prevents mixing incompatible builds.

**Example**

With a clean environment `module avail` lists only the available core modules which include compilers.

```bash
module avail
```

Once you load a particular compiler, you will only see the modules that depend on that compiler with `module avail`.

```bash
module load gcc/13.4.0
module avail
```

Now CUDA modules built with GCC 13.4.0 become visible.

```bash
module load cuda/13.0.0
module list
```

Then load CUDA and MPI:

```bash
module load gcc cuda openmpi/5.0.8
module list
```

If you swap compilers, Lmod automatically unloads any modules that depends on the old compiler and reloads those modules that are dependent on the new compiler.

```bash
module load gcc/11.5.0 
```

## User Collections (Optional)

You can save and restore commonly used modules using [user collections](https://lmod.readthedocs.io/en/latest/010_user.html#user-collections). Note that Lmod can load only one user collection at a time.