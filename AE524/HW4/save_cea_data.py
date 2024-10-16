import pandas as pd

# Data for the CEA Results (Equilibrium)
equilibrium_data = {
    "r": [8.0, 6.0, 4.7],
    "I_sp (s)": [402.55, 429.77, 441.28],
    "MW": [17.7204, 14.1191, 11.4891],
    "γ": [1.1295, 1.2191, 1.2661],
    "C_T": [1.7984, 1.7819, 1.7526],
    "C^*": [2196, 2366, 2470],
    "Y_OH": [0.15070, 0.00005, 0.00000]
}

# Data for the CEA Results (Frozen Chemistry)
frozen_data = {
    "r": [8.0, 6.0, 4.7],
    "I_sp": [413.75, 445.34, 464.87],
    "MW": [15.9028, 13.3114, 11.1861],
    "γ": [1.2525, 1.2643, 1.2880],
    "C_T": [1.7958, 1.7887, 1.7528],
    "C^*": [2151, 2323, 2437],
    "Y_OH": [0.11417, 0.06899, 0.02780]
}

# Create DataFrames
equilibrium_df = pd.DataFrame(equilibrium_data)
frozen_df = pd.DataFrame(frozen_data)

# Save to CSV files
equilibrium_df.to_csv('cea_results_equilibrium.csv', index=False)
frozen_df.to_csv('cea_results_frozen.csv', index=False)

equilibrium_df, frozen_df
