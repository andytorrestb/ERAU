import numpy as np
import matplotlib.pyplot as plt
from numpy import sin, cos, sinh, cosh, pi


def compute_theta(X,Y, theta_b, mask):
    """Calculate temperautre difference [θ(x,y)] given a θb, Assumes L=H=1"""
    print(type(X))
    # Cheeckily create an coordinate system filled with zero.
    theta = X-X

    for n in range(6):
        A = sinh(pi*(2*n+1)*(1-X))/sinh((2*n+1)*pi)
        B = sin((2*n+1)*pi*Y) / (2*n+1)
        theta = theta + A*B

    theta = ((4*theta_b)/pi)*theta
    return theta

def generate_grid(grid_size=100):
    """Generates a grid of points for x and y ranging from 0 to 1."""
    x = np.linspace(0, 1, grid_size)
    y = np.linspace(0, 1, grid_size)
    X, Y = np.meshgrid(x, y)
    return X, Y

def rotate_grid_90(X, Y):
    """Rotates the grid by 90 degrees counterclockwise."""
    X_rot = 1-Y  # New X is negative Y
    Y_rot = X   # New Y is the old X
    return X_rot, Y_rot

def apply_inequality(X, Y):
    """Applies the inequality y < -x + 1 and returns a mask for valid points."""
    return Y < (-X + 1)

def apply_rotated_inequality(X_rot, Y_rot):
    """Applies the transformed inequality for rotated data: y > x - 1."""
    return Y_rot > (X_rot - 1)

def compute_function(X, Y, mask, func=np.sin):
    """Computes the function (e.g., sin(xy), cos(xy)) only for the points that satisfy the mask."""
    Z = func(X * Y)
    Z = np.where(mask, Z, np.nan)  # Set points outside the mask to NaN
    return Z

def plot_grid_and_function(X, Y, Z, mask, label="Grid Points"):
    """Plots the grid and the function (sin or cos), only for points that satisfy the mask."""
    plt.scatter(X[mask], Y[mask], c='blue', marker='o', label=label)
    plt.contourf(X, Y, Z, cmap='viridis', alpha=0.6)  # Filled contour plot of the function
    plt.colorbar(label="Function Values")

def plot_rotated_grid_and_function(X_rot, Y_rot, Z_rot, mask_rot, label="Rotated Grid Points"):
    """Plots the rotated grid points and function cos(xy) with mask applied."""
    plt.scatter(X_rot[mask_rot], Y_rot[mask_rot], c='red', marker='x', label=label)
    plt.contourf(X_rot, Y_rot, Z_rot, cmap='plasma', alpha=0.6)  # Contour plot of cos(xy)
    plt.colorbar(label="θ(x,y)")

def save_plot(filename="grid_plot.png"):
    """Saves the plot to a file."""
    plt.title("θ(x,y)")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(False)
    
    # Set the aspect ratio to be square
    plt.gca().set_aspect('equal', adjustable='box')
    
    plt.legend()  # Add a legend for grid points
    plt.savefig(filename)
    plt.close()  # Close the plot to free up resources

def main():
    """Main function to run the grid generation, computation, plotting, and saving."""
    grid_size = 100
    
    # Original grid and sin(xy)
    X, Y = generate_grid(grid_size)
    mask = apply_inequality(X, Y)
    theta1 = compute_theta(X,Y, 50, mask)
    
    
    # Rotated grid and cos(xy)
    X_rot, Y_rot = rotate_grid_90(X, Y)
    mask_rot = apply_inequality(X_rot, Y_rot)  # Apply the transformed inequality to the rotated grid
    theta2 = compute_theta(X_rot, Y_rot, 50, mask_rot)

    theta = theta1+theta2
    
    plot_rotated_grid_and_function(X, Y, theta, mask)
    save_plot("theta.png")  # Save the plot for cos(xy)

if __name__ == "__main__":
    main()
