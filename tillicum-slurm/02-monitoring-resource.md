# Monitoring Resource Usage on Tillicum

Efficient use of Tillicum’s GPUs and compute resources starts with understanding how to monitor your jobs and usage:
- Slurm provides several built-in tools for checking job status, performance, and resource efficiency.
- Tillicum also provides the `hyakusage` utility for monitoring costs and budgets.

## Checking Job Accounting with `sacct`

`sacct` displays accounting data for all jobs and job steps in the Slurm database. It’s useful for reviewing job history, including elapsed time, resource requests, and job states. 

See the [sacct manual](https://slurm.schedmd.com/sacct.html) for a full list of format options. The man pages can also be viewed on Tillicum by running `man <command>`. Exit the man command with `q`.

**View all running jobs:**

```bash
sacct -s running -a -X -o user,jobid,elapsed,account,qos,node,reqtres%50
```

- `-a`: show jobs for all users (omit or use -u <net_id> for specific users).
- `-o`: customize output columns (in this case: user, jobid, elapsed time, etc.).

> 💡 **TIP:** You can adjust column widths with % (e.g., reqtres%50) to fit long text values.

**View all pending jobs:**

```bash
sacct -s pending -a -X -o user,jobid,elapsed,account,qos,node,reqtres%50
```

**View the batch script for a job:**

```bash
sacct -j <job_id> -B
```

## Checking Job Details with `scontrol`

`scontrol` is used to view or modify Slurm configuration including: job, job step, node, partition, time, reservation, and overall system configuration. *While most of the commands can only be executed by user root or an Administrator, users can still use it to inspect their own jobs.* See the [scontrol manual](https://slurm.schedmd.com/scontrol.html) for a full list of format options.

**Check details for a running job (e.g., resouces requested, working directory, command, and I/O paths)**

```bash
scontrol show job <job_id>
```

Example output snippet:

```bash
JobId=19157 JobName=myjob
   UserId=UWNetID(123456) GroupId=all(226269)
   Priority=1 Nice=0 Account=trainslurm2025 QOS=normal
   JobState=RUNNING Reason=None Dependency=(null)
   ...
   StartTime=... EndTime=... Deadline=N/A
   ...
   Command=/gpfs/scrubbed/kcxie/tillicum-slurm/job.slurm
   WorkDir=/gpfs/scrubbed/kcxie/tillicum-slurm
   StdErr=/gpfs/scrubbed/kcxie/tillicum-slurm/slurm-19157.out
   StdIn=...
   StdOut=/gpfs/scrubbed/kcxie/tillicum-slurm/slurm-19157.out
   ...
```

## Evaluating Job Efficiency with `seff`

Tillicum includes the `seff` utility, which reports resource efficiency for completed jobs. It helps identify jobs that used significantly less memory or GPU time than requested — an opportunity to optimize future runs.

Example usage:

```bash
seff 19157
```

Example output:

```bash
Job ID: 19157
Cluster: tillicum
User/Group: kcxie/all
State: CANCELLED (exit code 0)
Nodes: 1
Cores per node: 16
CPU Utilized: 00:00:00
CPU Efficiency: 0.00% of 00:25:36 core-walltime
Job Wall-clock time: 00:01:36
Memory Utilized: 16.45 MB
Memory Efficiency: 0.00% of 400.00 GB (400.00 GB/node)
```

> 💡 **TIP:** Requesting more memory or GPUs than your job actually needs can lead to longer queue times, reduced cluster efficiency, and higher job costs.

## Tracking Usage and Costs with `hyakusage`

Tillicum provides a convenient utility called `hyakusage`, which summarizes resource usage and associated costs across users, accounts, and QOS levels. It queries job accounting data and presents results in an user friendly, easy-to-read table format.

> ⚠️ **WARNING: Users are responsible for monitoring their own usage.**

### Default

Running `hyakusage` with no arguments prints a usage report for the **current billing cycle** for the **current user**, grouped by **account** and **QOS**.

```bash
hyakusage
```

**Key features:**
- Displays usage for all accounts you have access to.
- Shows total GPU-hours and costs per account at the bottom of each account.
- Integrates account-level budgets (if set) to show progress toward limits.

Example output:

```bash
  * Usage is counted by job END date.
  * Costs are calculated by base rate ($ 0.9/h) x billable GPU hours, where
      billable GPU hours = raw GPU hours x QOS multiplier.
  * Costs are rounded down to nearest cent.

Usage Report for Account trainslurm2025 (2025-10-01 to 2025-10-21)
╭────────────────────────┬────────────────────────┬────────────────────────╮
│ USER                   │ GPU Hours (hrs)        │ Jobs                   │
├────────────────────────┼────────────────────────┼────────────────────────┤
╰────────────────────────┴────────────────────────┴────────────────────────╯
╭────────────────────────┬────────────────────────┬────────────────────────╮
│ QOS       (multiplier) │ GPU Hours (hrs)        │ Cost (USD)             │
├────────────────────────┼────────────────────────┼────────────────────────┤
├────────────────────────┼────────────────────────┼────────────────────────┤
│ total (selected users) │         0.00           │        $0.00           │
╰────────────────────────┴────────────────────────┴────────────────────────╯
CURRENT MONTH total (all users, all qos): 0.00 GPU hours, $0.00

Usage Report for Account uwit (2025-10-01 to 2025-10-21)
╭────────────────────────┬────────────────────────┬────────────────────────╮
│ USER                   │ GPU Hours (hrs)        │ Jobs                   │
├────────────────────────┼────────────────────────┼────────────────────────┤
│ kcxie                  │         1.26           │     12                 │
╰────────────────────────┴────────────────────────┴────────────────────────╯
╭────────────────────────┬────────────────────────┬────────────────────────╮
│ QOS       (multiplier) │ GPU Hours (hrs)        │ Cost (USD)             │
├────────────────────────┼────────────────────────┼────────────────────────┤
│ interactive    (x 1.0) │         0.16           │        $0.14           │
│ normal         (x 1.0) │         1.10           │        $0.99           │
├────────────────────────┼────────────────────────┼────────────────────────┤
│ total (selected users) │         1.26           │        $1.13           │
╰────────────────────────┴────────────────────────┴────────────────────────╯
CURRENT MONTH total (all users, all qos): 1.34 GPU hours, $1.21
MONTHLY BUDGET:      $1.21 /   $1000.00  [░░░░░░░░░░] 0%
```

## Options

The `hyakusage` program has a rich set of command line arguments for more complex queries.

```bash
$ hyakusage --help
Print GPU usage and costs on Tillicum.
usage: hyakusage [options]

optional arguments:
  -u, -user      comma-separated list of users (default: current user)
  -s, -start     start date YYYY-MM-DD (default: 1st of this month)
  -e, -end       end date YYYY-MM-DD inclusive (default: today)
  -a, -account   comma-separated list of accounts (default: all available)
  -q, -qos       comma-separated list of QOS (default: all available)
  -h, -help      show this help message and exit

Notes:
  * Usage is counted by job END date.
  * Costs are rounded down to nearest cent.
  * You can only see accounts you have access to.
```

Example:

```bash
# To audit all users' resource usage from your group
hyakusage -u all

# To view resource usage for a given time period
hyakusage -s 2025-10-19 -e 2025-10-21
```