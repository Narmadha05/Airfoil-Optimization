import sys

def calculate_max_cl_cd(filename):
    max_ratio = -1e9
    best_alpha = None
    found_data = False

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            
            # XFOIL polars usually have at least 7 columns
            # alpha, CL, CD, CDp, CM, Top_Xtr, Bot_Xtr
            if len(parts) < 3:
                continue

            try:
                # Try converting the first 3 columns to floats
                # This naturally filters out header lines with text
                alpha = float(parts[0])
                cl = float(parts[1])
                cd = float(parts[2])
                
                # Check for reasonable range or drag > 0 to avoid division by zero
                if cd <= 0.000001:  
                    continue
                    
                ratio = cl / cd
                found_data = True
                
                if ratio > max_ratio:
                    max_ratio = ratio
                    best_alpha = alpha

            except ValueError:
                # This catches lines containing text (headers)
                continue

        if found_data:
            print(f"Analysis of: {filename}")
            print(f"Max Cl/Cd:   {max_ratio:.4f}")
            print(f"At Alpha:    {best_alpha}")
        else:
            print(f"No valid numerical data found in {filename}")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Use command line argument or default to 'polar.txt'
    target_file = sys.argv[1] if len(sys.argv) > 1 else "polar.txt"
    calculate_max_cl_cd(target_file)
