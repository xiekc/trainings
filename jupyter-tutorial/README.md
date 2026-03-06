# Managing Python Environments with Conda in Jupyter on Hyak

## Overview

This tutorial focuses on managing Python environments with Conda and using them effectively inside Jupyter Notebooks on Hyak via Open OnDemand.

> 💡 **TIP:** While examples are demonstrated on **Klone**, the same workflow applies to **Tillicum** with minor modifications (e.g., using QOS instead of partition for Slurm).

Working with Conda in an HPC environment can feel confusing at first — especially when combining:

- Lmod software modules
- Conda environments
- Slurm job scheduling
- Jupyter via Open OnDemand

This tutorial is designed to connect all of these pieces into one coherent workflow that you can reuse for your research projects.

🎯 **By completing this tutorial, you’ll learn how to:**

- Load software using LMOD modules
- Create and manage isolated Conda environments
- Register Conda environments as Jupyter kernels
- Launch and run Jupyter through Open OnDemand
- Run Python scripts interactively and via Slurm batch jobs

## Repository Structure

Each topic in this tutorial is contained in its own Markdown file for easy navigation:

| Section | Description |
| :- | :- |
| [00-preparation.md](./00-preparation.md) | Account and access prerequisites |
| [01-modules.md](./01-modules.md) | Using Lmod to load software modules |
| [02-conda-env.md](./02-conda-env.md) | Creating, activating, and managing Conda environments on Hyak |
| [03-python.md](./03-python.md) | Running Python scripts via Slurm (interactive and batch) |
| [04-ood-jupyter.md](./04-ood-jupyter.md) | Launching Jupyter via Open OnDemand and switching kernels |
| [05-task.md](./05-task.md) | Hands-on exercise: build an environment and use it in Jupyter |

## Introduction Video

An optional introduction video accompanies this tutorial and provides a high-level walkthrough of the concepts covered:

**March 5, 2026 Managing Python Environments with Conda in Jupyter on Hyak Workshop** will be added here when available.

[Slide Deck](https://github.com/UWrc/jupyter-tutorial/blob/main/slides_python_jupyter.pdf) from live tutorial on March 5, 2026

## Feedback

We’d love your feedback to help improve this tutorial and future Hyak trainings. After completing the tutorial or attending the workshop, please take a moment to fill out our [feedback form](https://forms.office.com/r/dNAQwnc6rY).

## Additional Resources

- [Hyak Documentation](https://hyak.uw.edu/docs)
- [Conda Documentation for Managing Environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [Jupyter Documentation for Kernels](https://docs.jupyter.org/en/latest/projects/kernels.html)
> 🗓️ **Stay tuned:** Check our [Research Computing Calendar](https://calendar.washington.edu/sea_uwit-rc) for upcoming training events.