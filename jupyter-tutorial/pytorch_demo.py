#!/usr/bin/env python3
"""
Example script for running PyTorch task in parallel using Slurm batch job on Tillicum.
"""

import os
import time
import torch

def main():

    # Example: different learning rates for each task
    learning_rates = 1e-4

    print(f"Starting PyTorch task with learning rate: {learning_rates}")

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
    with open(f"./results.txt", "w") as f:
        f.write(f"Learning Rate: {learning_rates}\nTime: {elapsed:.2f}s\nChecksum: {checksum:.3e}\n")

    print(f"Results saved to results.txt")

if __name__ == "__main__":
    main()