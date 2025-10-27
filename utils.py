"""
utils.py
-----------------------------------
Utility functions for Quantum Teleportation Project
"""

import os
import matplotlib.pyplot as plt

def create_results_dir(path="results"):
    """
    Create results directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)

def save_plot(filename):
    """
    Save the current matplotlib figure to file.
    """
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def print_header(title):
    """
    Print formatted headers for logs
    """
    print("="*60)
    print(title)
    print("="*60)