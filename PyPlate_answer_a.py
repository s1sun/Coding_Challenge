#(a) [optional]
# Import necessary libraries
from pyplate import Substance, Container, Plate, Recipe
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define constants
num_reactions = 12
temperatures = [60, 80]
ligands = ['XPhos', 'SPhos', 'dppf']
solvents = ['toluene', 'glyme', 'TBME', 'dichloroethane']
solvent_weight = {"toluene": 92.14, "glyme":90.12, "TBME": 88.15, "dichloroethane": 98.96}
solvent_density = {"toluene": 0.866, "glyme":0.867, "TBME": 0.740, "dichloroethane": 1.25}


triethylamine = Substance.liquid(name="triethylamine", mol_weight=101.19, density=0.726)

# Generate random molecular weights for Ai and Bi
molecular_weights = {f"A{i+1}": np.random.uniform(100, 200) for i in range(num_reactions)}
molecular_weights.update({f"B{i+1}": np.random.uniform(100, 200) for i in range(num_reactions)})

# Real molecular weights for Pd(OAc)2 and ligands
molecular_weights.update({
    "Pd(OAc)2": 224.5,
    "XPhos": 354.3,
    "SPhos": 398.5,
    "dppf": 745.6
})

# Define the total reaction volume
total_volume_uL = 200

# Prepare DataFrame to hold the experimental conditions
columns = ['Reaction', 'Temperature (°C)', 'Solvent', 'Ligand', 'A (mmol)', 'B (mmol)', 'Pd(OAc)2 (mol%)', 'Ligand (mol%)', 'Total Volume (uL)']
experiment_conditions = []

# Fill the DataFrame with the experimental design
for reaction in range(1, num_reactions + 1):
    for temp in temperatures:
        for solvent in solvents:
            mysolvent = Substance.liquid(name=solvent, mol_weight=solvent_weight[solvent], density=solvent_density[solvent])
                
            triethylamine_50mM = Container.create_solution(solute=triethylamine, solvent=mysolvent, concentration='50 mM',total_quantity='200 mL')

            plate = Plate(name='plate', max_volume_per_well='500 uL')

            recipe = Recipe().uses(triethylamine_50mM, plate)
            recipe.transfer(source=triethylamine_50mM, destination=plate[1:8, 1:12], quantity='200 uL')
            results = recipe.bake()
            triethylamine_50mM = results[triethylamine_50mM.name]
            plate = results[plate.name]
            
            # Visualize the design using PyPlate
            recipe.visualize(what=plate, mode='final', unit='uL', timeframe=0)
            for ligand in ligands:
                experiment_conditions.append([
                    f"Reaction {reaction}",
                    temp,
                    solvent,
                    ligand,
                    0.1,  # Ai is the limiting reagent
                    0.1 * 1.1,  # Bi is 1.1 equivalents of Ai
                    10,  # 10 mol% of Pd(OAc)2
                    15,  # 15 mol% of ligand
                    total_volume_uL
                ])

                

# Convert to DataFrame
experiment_df = pd.DataFrame(experiment_conditions, columns=columns)

# Save the experiment design to a file
experiment_df.to_csv('experimental_design.csv', index=False)

#(a) [optional] end
