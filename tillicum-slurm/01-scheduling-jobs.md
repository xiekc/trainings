# Scheduling Jobs on Tillicum

When you first log in to Tillicum, you land on a shared login node (`tillicum-login01`). Login nodes are for light activity like navigating the file system, transferring data, setting up your software environment, or preparing job scripts.

> ⚠️ **WARNING:** **Do not run compute-heavy work on login nodes.** All compute work must be run through the job scheduler, Slurm.

Slurm (Simple Linux Utility for Resource Management) is the workload manager used on Hyak and Tillicum. It allocates compute resources (CPUs, GPUs, and memory) on the cluster, determines when jobs start, and decides where they run. Slurm ensures efficient sharing of the cluster among all users.

For reference, see the [Slurm documentation](https://slurm.schedmd.com/documentation.html)

## Understanding Job Types

There are two main ways to run work on Tillicum:

| Job Type            | Command  | Best For                     | Runs On                                         |
| ------------------- | -------- | ---------------------------- | ----------------------------------------------- |
| **Interactive Job** | `salloc` | Exploratory or hands-on work | A compute node you connect to directly          |
| **Batch Job**       | `sbatch` | Long or unattended jobs      | Scheduled automatically when resources are available |

## Quality of Service (QOS)

Each Tillicum job is submitted under a "Quality-of-Service" or **QOS**, which defines limits such as wall time, GPU count, and concurrent jobs. 

All Tillicum compute nodes have 8 NVIDIA H200 GPUs (141 GB each) and are provisioned with ~200 GB system RAM per GPU and 8 CPUs per GPU.

| QOS             | Max Time   | Max GPUs per Job | Concurrent GPU Limit | Notes                                 |
| --------------- | ---------- | ---------------- | -------------------- | ------------------------------------- |
| **normal**      | 24 hours   | 16               | 48 GPUs              | Default QOS. Standard production work |
| **debug**       | 1 hour     | 1                | 1 job                | Quick testing and setup               |
| **interactive** | 8 hours    | 2                | 2 jobs               | Real-time work or debugging           |
| **long**        | by request | details TBA      | details TBA          | Extended runs upon approval           |
| **wide**        | by request | details TBA      | details TBA          | Distributed multi-node jobs           |

> 💡 **TIP:** You must request **at least 1 GPU**. *CPU-only jobs are not allowed on Tillicum.*

## Job Cost Estimates

Tillicum provides usage-based billing:

> 💡 **Tillicum Billing Formula**
>
> ***GPU Hours*** = Elapsed Time × ***N*** GPUs
> 
> **Rate: $0.90 per GPU-hour**
> 
> Billing is processed monthly through UW-IT’s ITBill system. The billing cycle closes at the end of day on the **25th** of each month.
> 
> 💡 **QOS Cost Factor** 
> 
> The **urgent** QOS (not yet implemented) will apply a multiplier (TBA) to the raw GPU hours when calculating charges.

When you submit a job, Slurm displays an estimated cost:

```bash
salloc:     GPUs: 1
salloc:     CPUs: 1
salloc:     MEM: 200 GB
salloc:     TIME: 1.00 hrs
salloc: *** COST: $0.90 (Est.)
```

The estimated cost is based on the full requested runtime. This will help you understand the maximum charge for each job.

## Common Slurm Arguments

The following arguments are commonly used and recommended for any job submission:

| Arguments | Command Flags | Notes |
| :- | :- | :- |
| Account | `-A`, `--account` | Specifies which project or lab account to charge. Default: your available account. |
| QOS | `-q`, `--qos` | Quality of service (QOS). Default: normal.|
| Nodes | `-N`, `--nodes` | Number of compute nodes to request. Most jobs use 1. Multi-node jobs are possible if supported by your code. |
| GPUs | `-G`, `--gpus` | Number of GPUs to request (**min: -G 1**). Note that not all codes can make use of multiple GPUs; scaling is not always linear with more GPUs. |
| Memory | `--mem` | Memory per node (**max: --mem=200G per GPU**). This is in the format `size[units]`. Units may be `M`, `G`, or `T` for megabyte, gigabyte, and terabyte. Default: Megabyte. |
| Time | `-t`, `--time` | Maximum runtime. Formats include `HH:MM:SS`, `D-HH`, and `minutes`. |

For more options, see the [salloc](https://slurm.schedmd.com/salloc.html) and [sbatch](https://slurm.schedmd.com/sbatch.html) manual.

## Interactive Jobs with `salloc`

Interactive jobs give you a live shell on a compute node — great for testing or exploring.

Start an interactive session using 1 GPU for 1 hour in interactive queue:

```bash
salloc --qos=interactive --gpus=1 --time=01:00:00
```

The job will wait in the queue. When the job starts, you’ll see messages similar to:

```bash
salloc: job 18973 has been allocated resources
salloc: Granted job allocation 18973
salloc: Waiting for resource configuration
salloc: Nodes g001 are ready for job
```

> 💡 **TIP:** Keep track of your jobID (e.g., 18973) — it helps us troubleshoot issues if your job fails. 

Once resources are allocated, confirm you're on a compute node:

```bash
hostname
```

The hostname changed from `tillicum-login0*` to `g001` or another Tillicum compute node (`g001`-`g024`). You are now on a compute node. 

Check GPU availability:

```bash
nvidia-smi
```

If you see GPU details (e.g., NVIDIA H200 with driver and CUDA versions), you're ready to compute.

To end the session and release the resources, type:

```bash
exit
```

## Batch Jobs with `sbatch`

Batch jobs run automatically without supervision. Resource requirements and commands are defined in a **Slurm job script**. 

View the example job script that can be used to schedule a job on Tillicum:

```bash
cat job.slurm
```

Output:

```bash
#!/bin/bash

#SBATCH --job-name=myjob
#SBATCH --qos=normal
#SBATCH --gpus=2
#SBATCH --cpus-per-task=16
#SBATCH --mem=400G
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%j.out

hostname
nvidia-smi
sleep 1200
```

Submit the job with:

```bash
sbatch job.slurm
```

Slurm will assign a job ID and queue it for execution. When resources become available, the job will start automatically.

To cancel a pending or running job, run:

```bash
# Replace <job_id> with the real jobID returned by Slurm.
scancel <job_id>
```

## Monitoring Jobs with `squeue`

Use `squeue` to check your running and pending jobs:

```bash
squeue -u $USER
```

Watch your queue refreshed every 10 seconds:

```bash
watch -n 10 squeue -u $USER
```

`watch` command can be terminated with a keyboard interrupt `Ctrl+C`.

`squeue -u $USER` lists all your running or queued jobs. To understand `squeue` output:

| Column | Description |
| :- | :- |
| **JOBID** | A unique number assigned to your job. Use this to reference it in other commands. |
| **PARTITION** | The resource pool or QOS (e.g., `normal`, `interactive`). |
| **NAME** | Job name specified with `--job-name`. |
| **ST** | Job status: <br> `PD` (Pending), `R` (Running), `CG` (Completing), `CD` (Completed). |
| **TIME** | Runtime duration. |
| **NODELIST(REASON)** | Node(s) assigned to the job or reason for pending (e.g., “Resources” or “Priority”) |

For more details or to customize the output format of `squeue`, refer to [squeue manual](https://slurm.schedmd.com/squeue.html).


Use `sinfo -r` to check cluster-wide node availability:

```bash
$ sinfo -r
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
gpu-h200*    up   infinite      2   down g[023-024]
gpu-h200*    up   infinite      3    mix g[001,005-006]
gpu-h200*    up   infinite     19   idle g[002-004,007-022]
```