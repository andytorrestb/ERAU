import numpy as np
import matplotlib.pyplot as plt

# Function to perform the finite difference method with specified grid size
def solve_heat_conduction(nx, ny):
    dx = dy = dz = 0.25 / (nx - 1)  # Spacing between nodes, assume dz = dx = dy
    k = 0.25  # Thermal conductivity (W/mK)
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

    return T, dx, dy, dz, k

# Solve for the finest grid
best_grid_size = 80  # Set finest grid size
T_best, dx, dy, dz, k = solve_heat_conduction(best_grid_size, best_grid_size)

# Calculate heat transfer in x- and y-directions using Fourier's law
qx = np.zeros_like(T_best)
qy = np.zeros_like(T_best)

# Cross-sectional area A = dz * dx (or dy)
A = dz * dx

# Temperature gradient calculation
for i in range(1, best_grid_size-1):
    for j in range(1, best_grid_size-1):
        # dT/dx (central difference)
        dT_dx = (T_best[i+1, j] - T_best[i-1, j]) / (2 * dx)
        # dT/dy (central difference)
        dT_dy = (T_best[i, j+1] - T_best[i, j-1]) / (2 * dy)
        
        # qx and qy
        qx[i, j] = -k * A * dT_dx
        qy[i, j] = -k * A * dT_dy

# Calculate total heat flux at the left boundary using forward difference
for j in range(1, best_grid_size-1):
    dT_dx_left = (T_best[1, j] - T_best[0, j]) / dx  # Forward difference
    qx[0, j] = -k * A * dT_dx_left

# Calculate total heat flux through the left boundary
total_heat_flux_left_boundary = np.sum(qx[0, :])  # Summing heat flux along the left boundary

# Output the total heat flux at the left boundary
print(f'Total heat flux through the left boundary: {total_heat_flux_left_boundary} W/m^2')

# Plot temperature distribution
plt.figure(figsize=(6, 6))
x = np.linspace(0, 0.25, best_grid_size)
y = np.linspace(0, 0.25, best_grid_size)
X, Y = np.meshgrid(x, y)
contour = plt.contourf(X, Y, T_best, cmap='hot', levels=50)
plt.colorbar(contour, label="Temperature (°C)")
plt.title(f'Temperature Distribution for Grid Size {best_grid_size}x{best_grid_size}')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.savefig('temperature_distribution.png')

# Plot heat transfer in the x-direction
plt.figure(figsize=(6, 6))
plt.contourf(qx, cmap='coolwarm', levels=50)
plt.colorbar(label="Heat Transfer (W) in x-direction")
plt.title(f'Heat Transfer in X-Direction for Grid Size {best_grid_size}x{best_grid_size}')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.savefig('heat_transfer_x_direction.png')

# Plot heat transfer in the y-direction
plt.figure(figsize=(6, 6))
plt.contourf(qy, cmap='coolwarm', levels=50)
plt.colorbar(label="Heat Transfer (W) in y-direction")
plt.title(f'Heat Transfer in Y-Direction for Grid Size {best_grid_size}x{best_grid_size}')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.savefig('heat_transfer_y_direction.png')

# Save heat transfer results to local files
np.savetxt("heat_transfer_x_direction.csv", qx, delimiter=",", header="Heat Transfer (W) in X-direction")
np.savetxt("heat_transfer_y_direction.csv", qy, delimiter=",", header="Heat Transfer (W) in Y-direction")

print('Results saved to local files: "temperature_distribution.png", "heat_transfer_x_direction.png", "heat_transfer_y_direction.png", and corresponding CSV files.')
