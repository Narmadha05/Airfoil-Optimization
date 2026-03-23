import csv
from simulation.evaluate_blade import evaluate_blade


def run_batch(input_file="blades.csv", output_file="dataset.csv"):
    """
    Reads blade designs from a CSV, evaluates each one via XFOIL,
    and saves the results (including fitness) to a new CSV.
    
    Skips any blade that fails and continues with the rest.
    """

    # 1. Read input CSV
    try:
        with open(input_file, "r") as f:
            reader = csv.DictReader(f)
            blades = list(reader)
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.")
        return

    total = len(blades)
    print(f"Loaded {total} blade designs from '{input_file}'.\n")

    # 2. Process each blade and collect results
    results = []
    failed = 0

    for i, blade in enumerate(blades):
        blade_id = blade.get("id", i + 1)
        print(f"--- Blade {blade_id} of {total} ---")

        try:
            thickness = float(blade["thickness"])
            camber = float(blade["camber"])
            camber_pos = float(blade["camber_position"])

            fitness = evaluate_blade(thickness, camber, camber_pos)

            results.append({
                "id": blade_id,
                "thickness": thickness,
                "camber": camber,
                "camber_position": camber_pos,
                "fitness": round(fitness, 4)
            })

        except Exception as e:
            # Log the error but keep going
            print(f"  FAILED (Blade {blade_id}): {e}")
            failed += 1
            continue

    # 3. Save results to output CSV
    if results:
        headers = ["id", "thickness", "camber", "camber_position", "fitness"]
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(results)
        print(f"\nDone! Saved {len(results)} results to '{output_file}'.")
    else:
        print("\nNo successful results to save.")

    if failed > 0:
        print(f"Warning: {failed} blade(s) failed during evaluation.")


if __name__ == "__main__":
    run_batch()
