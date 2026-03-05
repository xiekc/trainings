import sys
import numpy as np
import time

print("Starting batch Python job")
print("Python executable:", sys.executable)

start = time.time()

x = np.random.rand(2000,2000)
y = x @ x

elapsed = time.time() - start

print("Matrix shape:", y.shape)
print("Checksum:", y.sum())
print("Elapsed time:", elapsed, "seconds")

print("Job finished successfully")