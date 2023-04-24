import os
import shutil
from tqdm import tqdm

# Define path to the OpenFOAM case files
path = "/home/ilya/Documents/openfoam/tutorials/incompressible/simpleFoam/phystechData/simpleCar_Diteail"

# Define list of initial velocities
velocities = list(range(1, 101))

# Loop over each velocity and create a copy of the case files
for vel in tqdm(velocities):
    # Create copy of the case directory
    new_path = f"/home/ilya/Documents/openfoam/tutorials/incompressible/simpleFoam/phystechData/hig_dim/vel{vel}"
    if not os.path.exists(new_path):
        shutil.copytree(path, new_path)
        print(f"Created {new_path}")
    
    else:
        print(f"Directory {new_path} already exists")

    # Update the initial velocity in the copied case files
    U_file = f"{new_path}/0.orig/U"
    with open(U_file, "r") as f:
        lines = f.readlines()

    # Update the velocity value in the "internalField" section
    for i, line in enumerate(lines):
        if "internalField   uniform" in line:
            lines[i] = f"internalField   uniform ({vel} 0 0);\n"

    with open(U_file, "w") as f:
        f.writelines(lines)

    # Run the simulation for the current velocity
    os.chdir(new_path)
    os.system("./Allrun")
