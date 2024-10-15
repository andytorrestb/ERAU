import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class SupersonicFlowCalculator:
    def __init__(self, gamma):
        """Initialize with the specific heat ratio gamma."""
        self.gamma = gamma

    def area_ratio_mach(self, M):
        """Calculate the area ratio A/A* for a given Mach number."""
        gamma = self.gamma
        return (1 / M) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2))**((gamma + 1) / (2 * (gamma - 1)))

    def pressure_ratio_mach(self, M):
        """Calculate the pressure ratio P/P0 for a given Mach number."""
        gamma = self.gamma
        return (1 + ((gamma - 1) / 2) * M**2)**(-gamma / (gamma - 1))

    def solve_supersonic_mach_for_area_ratio(self, area_ratio):
        """Solve for the supersonic Mach number given A/A*."""
        # Solve for supersonic Mach number (initial guess M > 1)
        supersonic_mach = fsolve(lambda M: self.area_ratio_mach(M) - area_ratio, 2.0)[0]
        return supersonic_mach

    def solve_supersonic_area_ratios(self, area_ratios):
        """Solve for supersonic Mach numbers corresponding to a range of A/A*."""
        supersonic_mach_numbers = []
        for ar in area_ratios:
            supersonic_mach = self.solve_supersonic_mach_for_area_ratio(ar)
            supersonic_mach_numbers.append(supersonic_mach)
        return supersonic_mach_numbers

    def solve_pressure_ratios(self, supersonic_mach_numbers):
        """Solve for pressure ratios (P/P0) corresponding to the supersonic Mach numbers."""
        pressure_ratios = []
        for M in supersonic_mach_numbers:
            pressure_ratio = self.pressure_ratio_mach(M)
            pressure_ratios.append(pressure_ratio)
        return pressure_ratios

    def plot_supersonic_mach_vs_area_ratio(self, area_ratios, supersonic_mach_numbers, filename):
        """Plot supersonic Mach number vs A/A* and save it to a file."""
        plt.figure(figsize=(10, 6))
        plt.plot(area_ratios, supersonic_mach_numbers, label="Supersonic Mach", color='red')
        plt.title(f'Supersonic Mach Number vs A/A* (Gamma = {self.gamma})')
        plt.xlabel('A/A* (Area Ratio)')
        plt.ylabel('Mach Number (Supersonic)')
        plt.grid(True)
        plt.legend()
        plt.savefig(filename)
        print(f"Plot saved as {filename}")
        plt.close()  # Close the plot after saving.

    def plot_pressure_ratio_vs_area_ratio(self, area_ratios, pressure_ratios, filename):
        """Plot exit pressure ratio (P/P0) vs A/A* and save it to a file."""
        plt.figure(figsize=(10, 6))
        plt.plot(area_ratios, pressure_ratios, label="Pressure Ratio (P/P0)", color='blue')
        plt.title(f'Pressure Ratio (P/P0) vs A/A* (Gamma = {self.gamma})')
        plt.xlabel('A/A* (Area Ratio)')
        plt.ylabel('Pressure Ratio (P/P0)')
        plt.grid(True)
        plt.legend()
        plt.savefig(filename)
        print(f"Plot saved as {filename}")
        plt.close()  # Close the plot after saving.

if __name__ == "__main__":
    # Ask the user for the specific heat ratio (gamma)
    gamma = float(input("Enter the value of gamma (specific heat ratio): "))

    # Define the range of area ratios (A/A*) from 1 to 40
    area_ratios = np.linspace(1, 40, 100)

    # Initialize the supersonic flow calculator object
    calculator = SupersonicFlowCalculator(gamma)

    # Solve for supersonic Mach numbers corresponding to these area ratios
    supersonic_mach_numbers = calculator.solve_supersonic_area_ratios(area_ratios)

    # Solve for pressure ratios corresponding to these supersonic Mach numbers
    pressure_ratios = calculator.solve_pressure_ratios(supersonic_mach_numbers)

    # Plot and save supersonic Mach number vs A/A*
    filename_mach = "supersonic_mach_vs_area_ratio_plot.png"
    calculator.plot_supersonic_mach_vs_area_ratio(area_ratios, supersonic_mach_numbers, filename_mach)

    # Plot and save pressure ratio vs A/A*
    filename_pressure = "pressure_ratio_vs_area_ratio_plot.png"
    calculator.plot_pressure_ratio_vs_area_ratio(area_ratios, pressure_ratios, filename_pressure)
