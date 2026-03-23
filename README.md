# Airfoil-Optimization

This project presents an AI-driven aerodynamic optimization framework for vertical axis wind turbine (VAWT) airfoils operating at low Reynolds numbers. The system combines aerodynamic simulation, machine learning, and evolutionary optimization to automatically discover high-efficiency airfoil geometries.

The workflow uses XFOIL for aerodynamic analysis, a neural network surrogate model for performance prediction, and a genetic algorithm (GA) for design optimization.

## Methodology

The optimization pipeline follows a surrogate-based optimization workflow:

Latin Hypercube Sampling → XFOIL Simulation → Surrogate Neural Network → Genetic Algorithm Optimization → Physics-Based Validation

### Design Variables

The airfoil geometry is parameterized using three variables:

* Thickness (%)
* Camber (%)
* Camber Position (% chord)

### Aerodynamic Evaluation

Airfoils are evaluated using XFOIL at Reynolds number Re = 200,000.
Two aerodynamic performance metrics are used:

* Maximum Lift-to-Drag Ratio (CL/CD)
* Power Extraction Metric (CL^1.5/CD)

## Results

| Airfoil   | Thickness | Camber | Camber Position | CL/CD  |
| --------- | --------- | ------ | --------------- | ------ |
| Baseline  | 12        | 2      | 40              | 66.79  |
| Optimized | 8         | 6      | 50              | 100.71 |

The optimized airfoil shows:

* **50.8% improvement in CL/CD**
* **79% improvement in CL^1.5/CD**

This demonstrates that AI-based optimization can significantly improve aerodynamic efficiency for low-wind VAWT applications.

## How to Run the Project

### 1. Install dependencies
pip install -r requirements.txt


### 2. Generate airfoil dataset
python generate_blades.py
python simulation/evaluate_all_blades.py


### 3. Train surrogate model
python simulation/train_model.py


### 4. Run genetic algorithm optimization
python simulation/optimize_ga.py


### 5. Validate optimized airfoil
python validate_cl15.py


## Tools and Libraries
* Python
* XFOIL
* NumPy
* Pandas
* PyTorch
* Scikit-learn
* DEAP (Genetic Algorithm)
* Matplotlib / Seaborn

