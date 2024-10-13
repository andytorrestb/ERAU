# Complete Python script incorporating all requested changes

import numpy as np
import matplotlib.pyplot as plt

# Grid size
nx, ny = 10, 10  # 10x10 grid
dx = dy = 0.25 / (nx - 1)  # Spacing between nodes

# Initialize temperature grid with new boundary conditions
T = np.zeros((nx, ny))

# Boundary conditions
T[:, 0] = 600  # Left boundary (x=0) is 600°C
T[0, :] = 150  # Top boundary (y=0) is 150°C
# Right and bottom boundaries are insulated (no heat flux)

# Convergence criteria
tolerance = 1e-6
max_iterations = 10000
iteration = 0
error = 1.0

# Iteratively solving the temperature distribution
while error > tolerance and iteration < max_iterations:
    T_new = T.copy()
    error = 0
    
    for i in range(1, nx-1):
        for j in range(1, ny-1):
            T_new[i, j] = 0.25 * (T[i+1, j] + T[i-1, j] + T[i, j+1] + T[i, j-1])
            error = max(error, abs(T_new[i, j] - T[i, j]))
    
    # Insulated right boundary: dT/dx = 0 (T at i+1 is the same as at i-1)
    T_new[1:-1, -1] = T_new[1:-1, -2]  # Right boundary
    # Insulated bottom boundary: dT/dy = 0 (T at j-1 is the same as at j+1)
    T_new[-1, 1:-1] = T_new[-2, 1:-1]  # Bottom boundary
    
    T = T_new
    iteration += 1

# Plotting the updated temperature distribution
plt.figure(figsize=(6, 6))
plt.contourf(T, cmap='hot', levels=50)
plt.colorbar(label="Temperature (°C)")
plt.title(f'Temperature Distribution (Iterations: {iteration})')
plt.xlabel('X')
plt.ylabel('Y')

# Save the plot
file_path_final = '2d_conduction_finite_diference.png'
plt.savefig(file_path_final)

file_path_final
