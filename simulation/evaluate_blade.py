# evaluate_blade.py
# Ties together: generate_naca_dat + run_xfoil_simple + compute_fitness

import os

# Import the three building-block functions from your existing files
from geometry.naca_airfoil import generate_naca_dat
from simulation.run_xfoil import run_xfoil_simple
from simulation.compute_fitness import compute_fitness


def evaluate_blade(thickness, camber, camber_pos):
    """
    End-to-end evaluation of a single blade design.
    
    Steps:
        1. Generate the airfoil shape -> test_airfoil.dat
        2. Run XFOIL on it           -> polar.txt
        3. Read polar.txt            -> max CL/CD
    
    Args:
        thickness (float):   Max thickness in % (e.g., 12)
        camber (float):      Max camber in % (e.g., 2)
        camber_pos (float):  Position of max camber in % (e.g., 40)
        
    Returns:
        float: The maximum CL/CD ratio (fitness). Returns 0.0 on failure.
    """
    
    airfoil_file = "test_airfoil.dat"
    polar_file = "polar.txt"
    
    # Step 1: Generate the airfoil .dat file
    print(f"Generating airfoil: t={thickness}, m={camber}, p={camber_pos}")
    generate_naca_dat(thickness, camber, camber_pos, filename=airfoil_file)
    
    # Step 2: Run XFOIL (reads test_airfoil.dat, writes polar.txt)
    run_xfoil_simple()
    
    # Step 3: Read polar.txt and compute max CL/CD
    if os.path.exists(polar_file):
        fitness = compute_fitness(polar_file)
        print(f"Fitness (max CL/CD): {fitness:.4f}")
        return fitness
    else:
        print("Warning: polar.txt was not created. Returning fitness = 0.0")
        return 0.0


# Quick test
if __name__ == "__main__":
    # Example: 12% thick, 2% camber, 40% camber position
    result = evaluate_blade(12, 2, 40)
    print(f"\nFinal Result: {result:.4f}")
