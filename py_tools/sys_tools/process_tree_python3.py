#!/usr/bin/env python3

"""
This script prints the hierarchy of processes in a tree-like format.

It uses the 'ps' command to retrieve the parent process ID (PPID), process ID (PID),
and command name for each process. The hierarchy is then printed starting from the
init process (PID 1) to the leaf processes.

The script is compatible with Python 3.x.

Author: Massamba Sow
Date: 2024-05-06
Usage: python3 process_tree_python3.py

"""

import subprocess
import os
import re
from collections import defaultdict

def get_process_info():
    """
    Generator that yields process status information for each running process.

    Executes the 'ps' system command to retrieve and yield the parent process ID (PPID),
    process ID (PID), and command name for each process.
    """
    command = ['ps', 'axo', 'ppid,pid,comm']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)  # Updated for Python 3
    next(process.stdout)  # Skip the header line
    for line in process.stdout:
        yield line.rstrip().split(None, 2)

def print_hierarchy(processes, pid, prefix=''):
    """
    Recursive function to print the hierarchy of processes starting from a given PID.

    Parameters:
    - processes: Dictionary containing process information.
    - pid: Process ID from which to start printing the hierarchy.
    - prefix: String prefix to visualize the hierarchy level.
    """
    process_cmd = processes[pid]['command']
    if os.path.exists(process_cmd):
        process_name = os.path.basename(process_cmd)
    else:
        process_name = process_cmd

    parent_pid = processes[pid]['parent_pid']
    try:
        grandparent_pid = processes[parent_pid]['parent_pid']
        # Adjust the prefix if this process is the last child of its grandparent
        if processes[grandparent_pid]['children'][-1] == parent_pid:
            prefix = re.sub(r'^(\s+\|.+)[\|`](\s+\|- )$', r'\1 \2', prefix)
    except IndexError:
        pass
    try:
        if processes[parent_pid]['children'][-1] == pid:
            prefix = re.sub(r'\|- $', '`- ', prefix)
    except IndexError:
        pass

    print(f'{prefix}{process_name}({pid})')
    if processes[pid]['children']:
        prefix = prefix.replace('-', ' ')
        for child_pid in processes[pid]['children']:
            print_hierarchy(processes, child_pid, prefix + ' |- ')

if __name__ == '__main__':
    # Initialize the dictionary to store process information.
    processes = defaultdict(lambda: {"command": "", "children": [], 'parent_pid': None})
    # Populate the processes dictionary with information from the 'ps' command.
    for parent_pid, pid, command in get_process_info():
        parent_pid = int(parent_pid)
        pid = int(pid)
        processes[pid]["command"] = command
        processes[pid]['parent_pid'] = parent_pid
        processes[parent_pid]['children'].append(pid)

    # Start printing the hierarchy from PID 1 (usually the init process).
    print_hierarchy(processes, 1, '')
