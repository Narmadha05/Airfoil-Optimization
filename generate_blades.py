import csv
from scipy.stats.qmc import LatinHypercube, scale

def generate_blades(filename='blades.csv', count=1000):
    # Parameter bounds: [lower, upper]
    # Thickness:        8 to 25
    # Camber:           1 to 6
    # Camber Position: 30 to 50
    lower_bounds = [8,  1,  30]
    upper_bounds = [25, 6,  50]

    # Generate LHS samples in [0, 1] for 3 dimensions
    sampler = LatinHypercube(d=3, seed=42)
    samples = sampler.random(n=count)

    # Scale samples from [0, 1] to actual parameter ranges
    scaled = scale(samples, lower_bounds, upper_bounds)

    # Write to CSV
    headers = ['id', 'thickness', 'camber', 'camber_position']
    data = []
    for i in range(count):
        row = {
            'id': i + 1,
            'thickness':      round(scaled[i][0], 2),
            'camber':         round(scaled[i][1], 2),
            'camber_position': round(scaled[i][2], 2)
        }
        data.append(row)

    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"Generated {count} blade designs using SciPy LHS in {filename}")

if __name__ == "__main__":
    generate_blades()
