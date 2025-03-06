"""
This script provides functions to calculate the required UPS capacity, battery capacity,
and backup time for a given load power and backup duration. It also provides an interactive mode
to input the parameters and generate a detailed report.

The following functions are provided:

1. calculate_ups_capacity(load_power, power_factor=0.8, safety_margin=0.25):
    Calculate the required UPS capacity in VA with a safety margin.

2. calculate_battery_capacity(total_energy, voltage=48):
    Calculate the battery capacity required for a given energy and voltage.

3. calculate_backup_time(total_battery_capacity, voltage, load_power):
    Calculate the backup time provided by a battery system.

4. interactively_calculate_and_report():

    Interactively asks the user for parameters to calculate UPS capacity, battery capacity,
    and backup time, and prints a detailed report.

Usage:
    To use the functions directly, import them into your script and call them with the required
    parameters. To run the interactive mode, execute the script directly.

Example:

    # Import the functions
    from ups_battery_calculator import calculate_ups_capacity, calculate_battery_capacity

    # Calculate UPS capacity
    ups_capacity = calculate_ups_capacity(500)
    print(ups_capacity)
    # Output: {'ups_capacity': 625.0, 'ups_capacity_with_margin': 781.25}

    # Calculate battery capacity
    battery_capacity = calculate_battery_capacity(2400)
    print(battery_capacity)
    # Output: 50.0

    # Run the interactive mode
    python ups_battery_calculator.py

Author:
    Massamba Sow

Date:
    2024-12-28
"""

import math

def calculate_ups_capacity(load_power, power_factor=0.8, safety_margin=0.25):
    """
    Calculate the required UPS capacity in VA with a safety margin.

    Args:
        load_power (float): Total load power in watts (W).
        power_factor (float): Power factor of the UPS (default 0.8).
        safety_margin (float): Additional safety margin percentage (default 25%).

    Returns:
        dict: A dictionary with 'ups_capacity' and 'ups_capacity_with_margin'.
    """
    ups_capacity = load_power / power_factor
    ups_capacity_with_margin = ups_capacity * (1 + safety_margin)
    return {
        "ups_capacity": ups_capacity,
        "ups_capacity_with_margin": ups_capacity_with_margin
    }

def calculate_battery_capacity(total_energy, voltage=48):
    """
    Calculate the battery capacity required for a given energy and voltage.

    Args:
        total_energy (float): Total energy required in watt-hours (Wh).
        voltage (float): Battery system voltage (default 48V).

    Returns:
        float: Battery capacity in ampere-hours (Ah).
    """
    return total_energy / voltage

def calculate_backup_time(total_battery_capacity, voltage, load_power):
    """
    Calculate the backup time provided by a battery system.

    Args:
        total_battery_capacity (float): Total battery capacity in ampere-hours (Ah).
        voltage (float): Battery system voltage (V).
        load_power (float): Load power in watts (W).

    Returns:
        float: Backup time in hours.
    """
    total_energy = total_battery_capacity * voltage
    return total_energy / load_power

def interactively_calculate_and_report():
    """
    Interactively asks the user for parameters to calculate UPS capacity, battery capacity,
    and backup time, and prints a detailed report.

    Returns:
        None
    """
    print("=== UPS and Battery Sizing Calculator ===")
    load_power = float(input("Enter total load power in watts (W): "))
    backup_duration = float(input("Enter required backup time in hours: "))
    battery_voltage = float(input("Enter battery system voltage (e.g., 12V or 48V): "))
    battery_capacity_per_unit = float(input("Enter capacity of a single battery in Ah: "))

    # Calculate UPS capacity
    ups_results = calculate_ups_capacity(load_power)

    # Calculate total energy required
    total_energy = load_power * backup_duration

    # Calculate required battery capacity
    total_battery_capacity = calculate_battery_capacity(total_energy, battery_voltage)
    number_of_batteries = math.ceil(total_battery_capacity / battery_capacity_per_unit)
    number_of_strings = number_of_batteries // (battery_voltage // 12)

    # Calculate backup time
    backup_time = calculate_backup_time(
        total_battery_capacity,
        battery_voltage,
        load_power
    )

    # Print the report
    print("\n=== Calculation Report ===")
    print(f"Load Power: {load_power} W")
    print(f"Required Backup Time: {backup_duration} hours")
    print(f"UPS Capacity (without margin): {ups_results['ups_capacity']:.2f} VA")
    print(f"UPS Capacity (with 25% margin): {ups_results['ups_capacity_with_margin']:.2f} VA")
    print(f"Total Energy Required: {total_energy:.2f} Wh")
    print(f"Total Battery Capacity Required: {total_battery_capacity:.2f} Ah")
    print(f"Number of Batteries Required: {number_of_batteries} (in {number_of_strings} strings)")
    print(f"Calculated Backup Time: {backup_time:.2f} hours")
    print("===========================================")

if __name__ == "__main__":
    interactively_calculate_and_report()
