import math


def compute_fitness(filename):
    """
    Reads an XFOIL polar file and returns:
      - max_cl_cd:   maximum CL/CD
      - max_cl15_cd: maximum CL^1.5 / CD

    Args:
        filename (str): Path to the XFOIL polar file (e.g., 'polar.txt')

    Returns:
        tuple: (max_cl_cd, max_cl15_cd). Returns (0.0, 0.0) if no valid data.
    """
    max_cl_cd = 0.0
    max_cl15_cd = 0.0

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            parts = line.split()

            if len(parts) < 3:
                continue

            try:
                cl = float(parts[1])
                cd = float(parts[2])

                if cd > 0:
                    # Standard CL/CD
                    cl_cd = cl / cd
                    if cl_cd > max_cl_cd:
                        max_cl_cd = cl_cd

                    # Power-efficiency metric CL^1.5 / CD
                    if cl > 0:
                        cl15_cd = (cl ** 1.5) / cd
                        if cl15_cd > max_cl15_cd:
                            max_cl15_cd = cl15_cd

            except ValueError:
                continue

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

    return max_cl_cd, max_cl15_cd


# Quick test when run directly
if __name__ == "__main__":
    cl_cd, cl15_cd = compute_fitness("polar.txt")
    print(f"Max CL/CD:       {cl_cd:.4f}")
    print(f"Max CL^1.5/CD:   {cl15_cd:.4f}")
