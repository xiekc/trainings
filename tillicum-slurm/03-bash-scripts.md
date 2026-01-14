# Running Jobs with Bash Scripts

Bash scripts allow you to automate, reproduce, and document how your jobs run on Tillicum.

Instead of typing every command interactively, you can write your job instructions once and submit them as a batch script. Slurm will then execute the script for you on a compute node when resources become available.

In this section, you will learn how to use Bash scripts to organize your workflows, set variables, load environments, and run commands automatically with Slurm.

## Bash Script

A Bash script is simply a text file containing a sequence of commands that you could otherwise type directly into your terminal.
When you submit a script with `sbatch`, Slurm executes it line by line on the compute node.

**A simple script as a command proxy**

View the contents of the example script:

```bash
cat loop_script.sh
```

Ouput:

```bash
#!/bin/bash

start=$1  # Starting number (first argument)
end=$2    # Ending number or last iteration (second argument)

if [ -z "$start" ] || [ -z "$end" ]; then
  echo "Usage: $0 <starting_number> <ending_number>"
  exit 1
fi

for ((i=start; i<=end; i++)); do
  if [ $i -eq $end ]; then
    echo "Sequence complete! Iterations from $start to $end."
  fi
done
```

**Explanation:**
- `start=$1` and `end=$2`: Accept two command-line arguments - a starting point and an ending point.
- `if` condition: Checks whether both arguments are provided; if not, prints usage instructions and exits.
- `for` loop: Iterates from the start to the end value.
- `echo`: Prints a message once the loop completes.

To run it interactively, use `./` with the desired starting and ending values:

```bash
./loop_script.sh 0 1000000
```

Output:

```bash
Sequence complete! Iterations from 0 to 1000000.
```

You can measure runtime with the `time` command:

```bash
time ./loop_script.sh 0 1000000
```

The output should look something like this:

```bash
Sequence complete! Iterations from 0 to 1000000.

real	0m2.855s
user	0m2.848s
sys	    0m0.004s
```

We'll now run this same command as a batch job so it can run unattended through Slurm.

## Writing a Simple Slurm Job Script

A Bash script used for job submission usually includes three sections:

```bash
#!/bin/bash
# Job information (SBATCH directives)
# Environment setup (modules, virtual environment, variables)
# Commands or workflow steps
```

Let's look at a minimal working example `loop_job.slurm`:

```bash
#!/bin/bash

#SBATCH --job-name=loop_job
#SBATCH --qos=normal
#SBATCH --gpus=1
#SBATCH --mem=100G
#SBATCH --time=00:10:00
#SBATCH --output=logs/slurm-%j.out

# Print environment info
echo "Running on host: $(hostname)"
echo "Job started at: $(date)"

# Run your workflow
time ./loop_script.sh 0 1000000

echo "Job finished at: $(date)"
```

**Explanation**
- #!/bin/bash: Tells the system to use Bash to interpret this file.
- #SBATCH lines: Slurm directives that define resources and job options.
- Environment setup: Such as `module load conda`, `conda activate myenv`, `export PATH`
- Workflow commands: The actual computation or analysis.
- `echo` commands: Print logs and timestamps to track job progress.

> 💡 **TIP:** All #SBATCH directives must appear before the first executable command in the script.

Submit the job with:

```bash
sbatch loop_job.slurm
```

Check job output:

```bash
cat logs/slurm-<job_id>.out
```

Example output:

```bash
Running on host: g001
Job started at: Mon Oct 20 10:08:46 PDT 2025
Sequence complete! Iterations from 0 to 1000000.

real    0m2.762s
user    0m2.756s
sys     0m0.000s
Job finished at: Mon Oct 20 10:08:49 PDT 2025
```

> 💡 **TIP:** Use `less` or `tail -f` for large files or to monitor output in real time.

## Setting and Using Variables

Variables make your scripts more flexible, readable, and reusable.

Example `loop_var.slurm`:

```bash
#!/bin/bash

#SBATCH --job-name=loop_var
#SBATCH --qos=normal
#SBATCH --gpus=1
#SBATCH --mem=100G
#SBATCH --time=00:10:00
#SBATCH --output=logs/slurm-%j.out

# Define variables
WORKDIR="/gpfs/scrubbed/$USER/tillicum-slurm"
SCRIPT="loop_script.sh"

echo "Working directory: $WORKDIR"
cd $WORKDIR

# Run Bash script
time ./$SCRIPT 0 1000000

echo "Job completed successfully!"
```

## Loading Modules and Setting Environment

**Loading modules**

Most HPC software relies on modules and environment variables to configure runtime environments. See [Software Environment on Tillicum](https://hyak.uw.edu/docs/tillicum/environment) for more details on how modules are managed on Tillicum.

You can safely load them inside your job script before running commands.

Example:

```bash
# Unload ALL modules from the current session
module purge
# Load necessary modules
module load conda

# Print environment info
echo "Python path: $(which python)"
```

> 💡 **TIP:** Calling `module purge` at the beginning ensures a clean environment and prevents conflicts with previously loaded modules.

**Setting custom environment variables**

You can also export custom variables that your job needs:

```bash
# Example for OpenMP parallelization
export OMP_NUM_THREADS=8
```

These variables are inherited by all processes started during the job.

## Output and Error Files

By default, both standard output and standard error are directed to a file named `slurm-%j.out`, where the `%j` is replaced with your job ID. For job arrays, the default file name is `slurm-%A_%a.out`, where "%A" is replaced by the job ID and "%a" with the array index. 

Explicitly specify `--output` and `--error` flags to save standard output and error files separately:

```bash
#SBATCH --output=logs/slurm_%j.out
#SBATCH --error=logs/slurm_%j.err
```

This approach helps organize job logs by job ID under a designated directory such as `logs/`.

To control whether Slurm appends or overwrites existing files:

```bash
#SBATCH --open-mode={append|truncate}
```

Within your job script, you can also redirect the output of individual commands using standard shell redirection `>` (or `>>` for appending):

```bash
time ./$SCRIPT 0 1000000 > output.txt
```

This writes all standard output from the command to `output.txt`.
