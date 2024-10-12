import numpy as np
import matplotlib.pyplot as plt

# Set grid resolution
grid_size = 100  # Increase the number of points for smoother function plot

# Generate points
x = np.linspace(0, 1, grid_size)
y = np.linspace(0, 1, grid_size)

# Create a meshgrid for X and Y
X, Y = np.meshgrid(x, y)

# Apply the inequality condition y < -x + 1
mask = Y < (-X + 1)

# Calculate Z as a function of X and Y (sin(xy)), only where the condition is satisfied
Z = np.sin(X * Y)
Z = np.where(mask, Z, np.nan)  # Set values that don't meet the condition to NaN

# Plot the grid points that satisfy the condition
plt.scatter(X[mask], Y[mask], c='blue', marker='o', label="Grid Points")

# Plot the function sin(xy) as a contour plot, only where the condition is satisfied
plt.contourf(X, Y, Z, cmap='viridis', alpha=0.6)  # Filled contour plot of sin(xy)
plt.colorbar(label="sin(xy)")  # Add a color bar

plt.title("Square Grid of Points and sin(xy) (y < -x + 1)")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.grid(True)

# Set the aspect ratio to be square
plt.gca().set_aspect('equal', adjustable='box')

# Save the plot to a file
plt.savefig("square_grid_with_sin_xy_condition.png")  # Save the figure as a PNG file
plt.close()  # Close the plot after saving to free up resources
