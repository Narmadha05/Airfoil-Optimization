import random
import numpy as np
import torch
import torch.nn as nn
import joblib
from deap import base, creator, tools, algorithms


# --------------------------------------------------
# 1. Rebuild the same network architecture from training
# --------------------------------------------------
class FitnessNet(nn.Module):
    def __init__(self):
        super(FitnessNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.net(x)


# --------------------------------------------------
# 2. Load trained model and scalers
# --------------------------------------------------
model = FitnessNet()
model.load_state_dict(torch.load("fitness_model.pth", map_location="cpu"))
model.eval()

scaler_X = joblib.load("scaler_X.pkl")
scaler_y = joblib.load("scaler_y.pkl")

print("Loaded model and scalers.\n")


# --------------------------------------------------
# 3. Fitness function
# --------------------------------------------------
def predict_fitness(individual):

    X = np.array(individual).reshape(1, -1)
    X_scaled = scaler_X.transform(X)

    with torch.no_grad():
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
        y_scaled = model(X_tensor).numpy()

    y_pred = scaler_y.inverse_transform(y_scaled)

    return (y_pred[0][0],)


# --------------------------------------------------
# 4. Parameter bounds
# --------------------------------------------------
BOUNDS = {
    "thickness": (8.0, 25.0),
    "camber": (1.0, 6.0),
    "camber_position": (30.0, 50.0)
}


def create_individual():
    return [
        random.uniform(*BOUNDS["thickness"]),
        random.uniform(*BOUNDS["camber"]),
        random.uniform(*BOUNDS["camber_position"])
    ]


def clamp(individual):

    bounds_list = [
        BOUNDS["thickness"],
        BOUNDS["camber"],
        BOUNDS["camber_position"]
    ]

    for i in range(len(individual)):
        lo, hi = bounds_list[i]
        individual[i] = max(lo, min(hi, individual[i]))

    return individual


# --------------------------------------------------
# 5. DEAP Setup
# --------------------------------------------------
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", predict_fitness)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=[2.0, 0.5, 2.0], indpb=0.3)
toolbox.register("select", tools.selTournament, tournsize=3)


# --------------------------------------------------
# 6. Run GA
# --------------------------------------------------
def run_ga():


    pop_size = 50
    n_gen = 80
    cx_prob = 0.7
    mut_prob = 0.2

    pop = toolbox.population(n=pop_size)

    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("max", np.max)
    stats.register("avg", np.mean)
    stats.register("min", np.min)

    hof = tools.HallOfFame(1)

    print(f"GA Settings: pop={pop_size}, gen={n_gen}, cx={cx_prob}, mut={mut_prob}")
    print("=" * 60)

    pop, logbook = algorithms.eaSimple(
        pop,
        toolbox,
        cxpb=cx_prob,
        mutpb=mut_prob,
        ngen=n_gen,
        stats=stats,
        halloffame=hof,
        verbose=True
    )

    # --------------------------------------------------
    # Show TOP 5 blades
    # --------------------------------------------------
    print("\n" + "=" * 60)
    print("TOP 5 BLADES FOUND")
    print("=" * 60)

    top5 = tools.selBest(pop, k=5)

    for i, blade in enumerate(top5, start=1):

        blade = clamp(list(blade))
        fitness = predict_fitness(blade)[0]

        print(f"\nBlade {i}")
        print(f"  Thickness:       {blade[0]:.2f}%")
        print(f"  Camber:          {blade[1]:.2f}%")
        print(f"  Camber Position: {blade[2]:.2f}%")
        print(f"  Predicted CL/CD: {fitness:.4f}")

    print("\n" + "=" * 60)

    return top5


if __name__ == "__main__":
    run_ga()