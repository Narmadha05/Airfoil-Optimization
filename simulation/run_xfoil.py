import subprocess
import os
import shutil

def run_xfoil_simple():
    # Configuration
    xfoil_exe = os.path.join(os.path.dirname(__file__), "xfoil.exe")
    airfoil_file = "test_airfoil.dat"
    output_file = "polar.txt"
    reynolds_num = 200000
    
    # 1. Check for XFOIL executable
    if not shutil.which(xfoil_exe) and not os.path.exists(xfoil_exe):
        print(f"Error: '{xfoil_exe}' not found (or not in PATH).")
        return

    # 2. Cleanup old results
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except PermissionError:
            print(f"Error: Could not delete '{output_file}'. Is it open?")
            return

    # 3. Construct Commands Sequence
    # Ensure commands match exactly what you'd type in the shell.
    commands = [
        f"LOAD {airfoil_file}",  # Load the airfoil file
        "PANE",                  # Re-panel the airfoil (smooths points)
        "OPER",                  # Enter Operation Mode
        f"VISC {reynolds_num}",  # Set Viscous mode & Reynolds number
        "PACC",                  # Start Polar Accumulation
        f"{output_file}",        # Output Polar Filename
        "",                      # Skip Dump Filename (Press Enter)
        "ASEQ 0 10 1",           # Run Alpha Sequence (0 to 10 deg, step 1)
        "PACC",                  # Stop Polar Accumulation (closes file)
        "QUIT"                   # Exit XFOIL
    ]

    # Join commands with newlines
    input_str = "\n".join(commands) + "\n"

    print(f"Running XFOIL with '{airfoil_file}' at Re={reynolds_num}...")

    try:
        # 4. Execute Subprocess
        # 'input' handles stdin, 'text=True' handles string encoding
        # 'capture_output=True' grabs stdout/stderr so we can print it if needed
        process = subprocess.run(
            xfoil_exe,
            input=input_str,
            text=True,  # Handle strings (Python 3.7+)
            capture_output=True,
            timeout=30  # Safety timeout
        )

        # 5. Check Results
        if process.returncode == 0:
            print("XFOIL execution finished.")
            if os.path.exists(output_file):
                print(f"Success: Results saved to '{output_file}'")
            else:
                print(f"Warning: '{output_file}' not found. Check input file or XFOIL output.")
                # Print XFOIL output for debugging if file is missing
                print("\n--- XFOIL Output ---")
                print(process.stdout)
        else:
            print(f"Error: XFOIL exited with code {process.returncode}")
            print(process.stderr)

    except subprocess.TimeoutExpired:
        print("Error: XFOIL process timed out.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    run_xfoil_simple()
