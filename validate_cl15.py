"""
Computes CL^1.5/CD for the five validated blade designs.
Uses hardcoded XFOIL results from the user's validation runs.
"""

validated_blades = [
    {"thickness": 8.0,  "camber": 6.0, "camber_pos": 50.0, "cl_cd": 100.71},
    {"thickness": 8.2,  "camber": 5.9, "camber_pos": 50.0, "cl_cd":  99.97},
    {"thickness": 8.5,  "camber": 5.8, "camber_pos": 49.0, "cl_cd":  98.29},
    {"thickness": 8.8,  "camber": 5.6, "camber_pos": 49.0, "cl_cd":  97.15},
    {"thickness": 9.0,  "camber": 5.5, "camber_pos": 48.0, "cl_cd":  95.76},
]

# Baseline
baseline = {"thickness": 12.0, "camber": 2.0, "camber_pos": 40.0, "cl_cd": 66.79}


def compute_cl15_cd_from_polar(filename):
    """Read a polar file and compute max CL^1.5/CD."""
    max_val = 0.0
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) < 3:
                    continue
                try:
                    cl = float(parts[1])
                    cd = float(parts[2])
                    if cl > 0 and cd > 0:
                        val = (cl ** 1.5) / cd
                        if val > max_val:
                            max_val = val
                except ValueError:
                    continue
    except FileNotFoundError:
        print(f"Warning: {filename} not found, skipping.")
    return max_val


if __name__ == "__main__":
    print("=" * 70)
    print(f"{'Blade':>30s}  |  {'CL/CD':>8s}  |  {'CL^1.5/CD':>10s}")
    print("=" * 70)

    # Try to read polar files if available, otherwise note they are needed
    # Expected polar filenames: polar_8_6_50.txt, etc.
    import os

    for blade in validated_blades:
        t, m, p = blade["thickness"], blade["camber"], blade["camber_pos"]
        cl_cd = blade["cl_cd"]

        polar_name = f"polar_{t}_{m}_{p}.txt"
        if os.path.exists(polar_name):
            cl15_cd = compute_cl15_cd_from_polar(polar_name)
        else:
            # Estimate: if we don't have the raw polar, we can't compute exact CL^1.5/CD
            # Print a note instead
            cl15_cd = None

        label = f"({t}, {m}, {p})"
        if cl15_cd is not None:
            print(f"{label:>30s}  |  {cl_cd:8.2f}  |  {cl15_cd:10.4f}")
        else:
            print(f"{label:>30s}  |  {cl_cd:8.2f}  |  {'(need polar)':>10s}")

    print("-" * 70)
    t, m, p = baseline["thickness"], baseline["camber"], baseline["camber_pos"]
    cl_cd = baseline["cl_cd"]
    polar_name = f"polar_{t}_{m}_{p}.txt"
    if os.path.exists(polar_name):
        cl15_cd = compute_cl15_cd_from_polar(polar_name)
        print(f"{'Baseline (' + f'{t},{m},{p}' + ')':>30s}  |  {cl_cd:8.2f}  |  {cl15_cd:10.4f}")
    else:
        print(f"{'Baseline (' + f'{t},{m},{p}' + ')':>30s}  |  {cl_cd:8.2f}  |  {'(need polar)':>10s}")

    print("=" * 70)
    print("\nNote: To get exact CL^1.5/CD values, place XFOIL polar files named")
    print("      polar_<t>_<m>_<p>.txt in this directory and re-run.")
