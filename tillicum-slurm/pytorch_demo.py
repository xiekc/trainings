#!/usr/bin/env python3
"""
Example script for running multiple PyTorch tasks in parallel using Slurm array jobs on Tillicum.
"""

import os
import time
import torch

def main():
    # Get SLURM array task ID
    task_id = int(os.getenv("SLURM_ARRAY_TASK_ID", 0))

    # Example: different learning rates for each task
    learning_rates = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2]
    lr = learning_rates[task_id % len(learning_rates)]

    print(f"Starting PyTorch Array Task {task_id}")
    print(f"Learning rate: {lr}")

    print(f"Hostname: {os.uname().nodename}")
    print(f"CUDA available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device("cpu")
        print("Running on CPU.")

    # Simulated computation
    start = time.time()
    x = torch.rand((10000, 10000), device=device)
    y = torch.mm(x, x)
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    elapsed = time.time() - start

    checksum = float(y.sum().item())
    print(f"\nComputation complete! Result checksum: {checksum:.3e}")
    print(f"Elapsed time: {elapsed:.2f} seconds\n")

    # Save results
    with open(f"./logs/results_task_{task_id}.txt", "w") as f:
        f.write(f"Task {task_id}\nLearning rate: {lr}\nTime: {elapsed:.2f}s\nChecksum: {checksum:.3e}\n")

    print(f"Results saved to results_task_{task_id}.txt")

if __name__ == "__main__":
    main()