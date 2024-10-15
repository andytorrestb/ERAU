import pandas as pd
import numpy as np
from comp_flow_calc import SupersonicFlowCalculator as CompFlowCalc

# Chemical properties DataFrame
chemical_properties = pd.DataFrame({
    'MolecularWeight': [2.016e-3, 32.00e-3, 18.015e-3],  # in kg/mol
    'Cp': [14.304, None, 1.872],  # in kJ/kg·K, O2's Cp not used
    'R': [4124, None, 461.5]  # in J/kg·K, O2's R not used
}, index=['H2', 'O2', 'H2O'])

def calculate_mass(moles: float, molecular_weight: float) -> float:
    """Calculate the mass of a substance."""
    return moles * molecular_weight

def calculate_phi(r: float) -> float:
    """Calculate the equivalence ratio (phi) based on the oxidizer-to-fuel ratio."""
    MW_O2 = chemical_properties.loc['O2', 'MolecularWeight']
    MW_H2 = chemical_properties.loc['H2', 'MolecularWeight']
    return (0.5 * MW_O2) / (r * MW_H2)

def oxidizer_to_fuel_ratio(phi: float) -> tuple:
    """Calculate the oxidizer-to-fuel ratio for the combustion reaction."""
    moles_H2 = phi  # Moles of H2
    moles_O2 = 0.5  # Moles of O2

    MW_H2 = chemical_properties.loc['H2', 'MolecularWeight']
    MW_O2 = chemical_properties.loc['O2', 'MolecularWeight']
    
    # Calculate the mass of H2 and O2
    mass_H2 = calculate_mass(moles_H2, MW_H2)
    mass_O2 = calculate_mass(moles_O2, MW_O2)
    
    # Calculate oxidizer-to-fuel ratio (by mass)
    return mass_O2 / mass_H2, mass_H2, mass_O2

def calculate_product_fractions(phi: float) -> tuple:
    """Calculate the mole and mass fractions of the products (H2O and remaining H2)."""
    # Calculate moles of products
    moles_H2O = 1  # 1 mole of H2O is produced
    moles_H2_remaining = max(0, phi - 1)  # Remaining H2 (if phi > 1)

    # Total moles of products
    total_moles_products = moles_H2O + moles_H2_remaining

    # Mole fractions of products
    mole_fraction_H2O = moles_H2O / total_moles_products
    mole_fraction_H2_remaining = moles_H2_remaining / total_moles_products if total_moles_products > 0 else 0

    # Calculate masses of products
    MW_H2O = chemical_properties.loc['H2O', 'MolecularWeight']
    MW_H2 = chemical_properties.loc['H2', 'MolecularWeight']
    mass_H2O = calculate_mass(moles_H2O, MW_H2O)
    mass_H2_remaining = calculate_mass(moles_H2_remaining, MW_H2)

    # Total mass of products
    total_mass_products = mass_H2O + mass_H2_remaining

    # Mass fractions of products
    mass_fraction_H2O = mass_H2O / total_mass_products if total_mass_products > 0 else 0
    mass_fraction_H2_remaining = mass_H2_remaining / total_mass_products if total_mass_products > 0 else 0

    return mole_fraction_H2O, mole_fraction_H2_remaining, mass_fraction_H2O, mass_fraction_H2_remaining

def calculate_cp_and_gamma(mole_fraction_H2O: float, mole_fraction_H2: float, mass_fraction_H2O: float, mass_fraction_H2: float) -> tuple:
    """Calculate the specific heat capacity (Cp) and gamma (γ) for the combustion products."""
    Cp_H2O = chemical_properties.loc['H2O', 'Cp']
    Cp_H2 = chemical_properties.loc['H2', 'Cp']

    R_H2O = chemical_properties.loc['H2O', 'R']
    R_H2 = chemical_properties.loc['H2', 'R']

    MW_O2 = chemical_properties.loc['O2', 'MolecularWeight']
    MW_H2 = chemical_properties.loc['H2', 'MolecularWeight']
    MW_H2O = chemical_properties.loc['H2O', 'MolecularWeight']

    MW_m = mole_fraction_H2O * MW_H2O + mole_fraction_H2 * MW_H2
    R_m = 8.314e-3 / MW_m

    # Weighted average Cp for the mixture
    Cp_mixture = mass_fraction_H2O * Cp_H2O + mass_fraction_H2 * Cp_H2

    # Weighted average Cv for the mixture
    Cv_H2O = Cp_H2O - R_H2O / 1000  # Converting R from J to kJ
    Cv_H2 = Cp_H2 - R_H2 / 1000  # Converting R from J to kJ
    Cv_mixture = mole_fraction_H2O * Cv_H2O + mole_fraction_H2 * Cv_H2

    # Gamma for the mixture
    gamma_mixture = Cp_mixture / (Cp_mixture - R_m)

    return Cp_mixture, gamma_mixture

def main() -> None:
    """
    Main function to run the program. Repeats the calculation for a list of
    oxidizer-to-fuel ratio values (r = [8.0, 6.0, 4.7]), calculates phi for each,
    then calculates the oxidizer-to-fuel ratio, mole fractions, mass fractions,
    specific heat capacity (Cp), and gamma (γ) of the products, and stores them in a DataFrame.
    """
    # List of oxidizer-to-fuel ratio values.
    r_values = [8.0, 6.0, 4.7]

    # Create a list to store the results.
    results_list = []

    # Loop over each value of r and perform the calculations.
    for r in r_values:
        print(f"\nCalculating for r = {r:.1f}")
        
        # Calculate phi based on the input ratio (r).
        phi = calculate_phi(r)
        
        # Calculate oxidizer-to-fuel ratio and masses.
        oxidizer_fuel_ratio, mass_H2, mass_O2 = oxidizer_to_fuel_ratio(phi)
        
        # Calculate mole and mass fractions of the products.
        mole_fraction_H2O, mole_fraction_H2_remaining, mass_fraction_H2O, mass_fraction_H2_remaining = calculate_product_fractions(phi)

        # Calculate Cp and gamma for the mixture.
        Cp_mixture, gamma_mixture = calculate_cp_and_gamma(
            mole_fraction_H2O, mole_fraction_H2_remaining,
            mass_fraction_H2O, mass_fraction_H2_remaining
        )

        # Calculate the combustion temperature for the mixture.
        Qf = 241.8e6 / (18+2*mole_fraction_H2_remaining)
        T1 = Qf / (Cp_mixture*1e3)

        flow_calc = CompFlowCalc(gamma_mixture)
        Me = flow_calc.solve_supersonic_mach_for_area_ratio(25)
        P2P1 = float(flow_calc.pressure_ratio_mach(Me))
        a = (gamma_mixture-1)/gamma_mixture
        Isp = (2*Cp_mixture*T1*(1-(P2P1)**a))**0.5

        MW_O2 = chemical_properties.loc['O2', 'MolecularWeight']
        MW_H2 = chemical_properties.loc['H2', 'MolecularWeight']
        MW_H2O = chemical_properties.loc['H2O', 'MolecularWeight']
        MW_m = mole_fraction_H2O * MW_H2O + mole_fraction_H2_remaining * MW_H2
        R_m = 8.314 / MW_m
        g = gamma_mixture
        C_star = np.sqrt((R_m*T1)/g)*(1+0.5*(g-1))**(g/(g-1)-0.5)

        # Calculate equivalent exhaust velocity (c)
        g_0 = 9.81  # Gravitational acceleration (m/s²)
        C = Isp * g_0  # Exhaust velocity in m/s

        CT = C_star/C

        # Append the results to the list
        results_list.append({
            'r': r,
            'phi': phi,
            # 'Oxidizer-to-Fuel Ratio': oxidizer_fuel_ratio,
            # 'Mass H2 (kg)': mass_H2,
            # 'Mass O2 (kg)': mass_O2,
            # 'Mole Fraction H2O': mole_fraction_H2O,
            # 'Mole Fraction H2': mole_fraction_H2_remaining,
            # 'Mass Fraction H2O': mass_fraction_H2O,
            # 'Mass Fraction H2': mass_fraction_H2_remaining,
            'Cp (kJ/kg·K)': Cp_mixture,
            'Gamma (γ)': gamma_mixture,
            'R_m': R_m,
            'T1': T1,
            'MW_m': MW_m,
            'C_star': C_star,
            'Isp': Isp,
            'C (m/s)': C,
            'CT': CT
        })

    # Convert the list to a DataFrame
    results_df = pd.DataFrame(results_list)

    # Display the results DataFrame
    print("\nResults DataFrame:")
    print(results_df)

# Call the main function
if __name__ == "__main__":
    main()
