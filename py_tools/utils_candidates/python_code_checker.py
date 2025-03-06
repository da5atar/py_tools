'''
python_code_checker.py

This script analyzes Python code files in a directory using various tools:
- Black: Code formatter
- Flake8: Linter
- Bandit: Security analysis tool

To run the script, specify the directory containing Python files to analyze.
The script will run each tool on the Python files and save the reports in a 'reports' folder.

Note: You need to have the 'black', 'flake8', and 'bandit' tools installed to run this script.

Usage:
1. Specify the directory containing Python files to analyze.
2. Run the script to analyze the Python files.
3. Check the 'reports' folder for the analysis reports.

Example:
python python_code_checker.py --directory /path/to/python/files
'''
import os
import subprocess

def analyze_code(directory):
    """Analyze Python code files in the specified directory using Black, Flake8, and Bandit."""
    # List Python files in the directory
    python_files = [file for file in os.listdir(directory) if file.endswith('.py')]
    if not python_files:
        print("No Python files found in the specified directory.")
        return
    report_dir = os.path.join(directory, "reports")
    os.makedirs(report_dir, exist_ok=True)

    for file in python_files:
        print(f"Analyzing file: {file}")
        file_path = os.path.join(directory, file)

        # Run Black (code formatter)
        print("\nRunning Black...")
        black_command = f"black {file_path} --check"
        subprocess.run(black_command, shell=True)

        # Run Flake8 (linter)
        print("\nRunning Flake8...")
        flake8_output_file = os.path.join(report_dir, f"{file}_flake8_report.txt")
        with open(flake8_output_file, "w") as flake8_output:
            flake8_command = f"flake8 {file_path}"
            subprocess.run(flake8_command, shell=True, stdout=flake8_output, stderr=subprocess.STDOUT)
        print(f"Flake8 report saved to {flake8_output_file}")

        # Run Bandit (security analysis)
        print("\nRunning Bandit...")
        bandit_output_file = os.path.join(report_dir, f"{file}_bandit_report.txt")
        with open(bandit_output_file, "w") as bandit_output:
            bandit_command = f"bandit -r {file_path}"
            subprocess.run(bandit_command, shell=True, stdout=bandit_output, stderr=subprocess.STDOUT)
        print(f"Bandit report saved to {bandit_output_file}")
        print(f"Analyzing file: {file} Completed!!!!")
        print('================'*5)
        print('================'*5)
if __name__ == "__main__":
    DIRECTORY = r"" # Enter the directory path containing Python files
    analyze_code(DIRECTORY)
