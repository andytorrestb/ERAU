import numpy as np
import matplotlib.pyplot as plt

# Function to perform the finite difference method with specified grid size
def solve_heat_conduction(nx, ny):
    dx = dy = 0.25 / (nx - 1)  # Spacing between nodes
    T = np.zeros((nx, ny))

    # Boundary conditions
    T[:, 0] = 600  # Left boundary (x=0) is 600°C
    T[0, :] = 150  # Top boundary (y=0) is 150°C

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

    return T, iteration

# Mesh sensitivity study with different grid sizes
grid_sizes = [10, 20, 40, 80]
iterations_list = []
max_temp_list = []

for size in grid_sizes:
    T, iterations = solve_heat_conduction(size, size)
    iterations_list.append(iterations)
    max_temp_list.append(np.max(T))  # Save the max temperature for sensitivity analysis

# Plotting the temperature distribution for the finest grid (largest size)
best_grid_size = grid_sizes[-1]  # The finest grid is the last one in the list
T_best, _ = solve_heat_conduction(best_grid_size, best_grid_size)

# Create X, Y coordinates (0 to 0.25)
x = np.linspace(0, 0.25, best_grid_size)
y = np.linspace(0, 0.25, best_grid_size)
X, Y = np.meshgrid(x, y)

plt.figure(figsize=(6, 6))  # Set the figure size to square
contour = plt.contourf(X, Y, T_best, cmap='hot', levels=50)
plt.colorbar(contour, label="Temperature (°C)")
plt.title(f'Temperature Distribution for Grid Size {best_grid_size}x{best_grid_size}')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')

# Ensure the aspect ratio is square
plt.gca().set_aspect('equal', adjustable='box')

# Save the plot for the finest grid
file_path_best_grid = 'finest_grid_temperature_distribution_square.png'
plt.tight_layout()
plt.savefig(file_path_best_grid)

print(f'Temperature distribution for finest grid saved to: {file_path_best_grid}')
