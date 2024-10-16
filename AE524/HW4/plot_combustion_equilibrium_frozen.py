
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create a 'results' directory if it doesn't exist
results_dir = 'results'
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Load data
equilibrium_df = pd.read_csv('cea_results_equilibrium.csv')
frozen_df = pd.read_csv('cea_results_frozen.csv')
combustion_df = pd.read_csv('combustion_results.csv')

# Plotting function
def co_plot_with_combustion(equilibrium_df, frozen_df, combustion_df, parameter, equilibrium_param=None, frozen_param=None, combustion_param=None):
    plt.figure(figsize=(8, 6))
    equilibrium_param = equilibrium_param if equilibrium_param else parameter
    frozen_param = frozen_param if frozen_param else parameter
    combustion_param = combustion_param if combustion_param else parameter
    plt.plot(equilibrium_df["r"], equilibrium_df[equilibrium_param], label=f'Equilibrium {equilibrium_param}', marker='o')
    plt.plot(frozen_df["r"], frozen_df[frozen_param], label=f'Frozen {frozen_param}', marker='x')
    # Ensure the combustion_param exists in the combustion data
    if combustion_param in combustion_df.columns:
        plt.plot(combustion_df["r"], combustion_df[combustion_param], label=f'Combustion {combustion_param}', marker='s')
    else:
        print(f"Warning: {combustion_param} not found in combustion data")
    plt.xlabel('r')
    plt.ylabel(parameter)
    plt.title(f'{parameter} vs r')
    plt.legend()
    plt.grid(True)
    plt.show()

# Also update to save the plots locally to the results folder
def save_plot_with_combustion(equilibrium_df, frozen_df, combustion_df, parameter, equilibrium_param=None, frozen_param=None, combustion_param=None, file_name="plot.png"):
    plt.figure(figsize=(8, 6))
    equilibrium_param = equilibrium_param if equilibrium_param else parameter
    frozen_param = frozen_param if frozen_param else parameter
    combustion_param = combustion_param if combustion_param else parameter
    plt.plot(equilibrium_df["r"], equilibrium_df[equilibrium_param], label=f'Equilibrium {equilibrium_param}', marker='o')
    plt.plot(frozen_df["r"], frozen_df[frozen_param], label=f'Frozen {frozen_param}', marker='x')
    if combustion_param in combustion_df.columns:
        plt.plot(combustion_df["r"], combustion_df[combustion_param], label=f'Combustion {combustion_param}', marker='s')
    else:
        print(f"Warning: {combustion_param} not found in combustion data")
    plt.xlabel('r')
    plt.ylabel(parameter)
    plt.title(f'{parameter} vs r')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, file_name))
    plt.close()

# Plot and save the data for I_sp
co_plot_with_combustion(equilibrium_df, frozen_df, combustion_df, 'I_sp', equilibrium_param='I_sp (s)', frozen_param='I_sp', combustion_param='I_sp (s)')
save_plot_with_combustion(equilibrium_df, frozen_df, combustion_df, 'I_sp', equilibrium_param='I_sp (s)', frozen_param='I_sp', combustion_param='I_sp (s)', file_name="I_sp_vs_r.png")

# Plot and save the data for remaining parameters, including MW
parameters_with_combustion_corrected_final = ["MW", "γ", "C_T", "C^*", "Y_OH"]

# Plot and save the data for remaining parameters
for param in parameters_with_combustion_corrected_final:
    combustion_param = 'CT' if param == 'C_T' else param  # use 'CT' for combustion and 'C_T' for others
    co_plot_with_combustion(equilibrium_df, frozen_df, combustion_df, param, combustion_param=combustion_param)
    save_plot_with_combustion(equilibrium_df, frozen_df, combustion_df, param, combustion_param=combustion_param, file_name=f"{param}_vs_r.png")
