# main.py
import numpy as np
from scripts.teleportation_qiskit import run_simulation, compute_fidelity
from scripts.utils import print_header

def get_user_input():
    print("\nEnter parameters for quantum teleportation:")
    print("-------------------------------------------")
    print("Theta angle (in degrees):")
    print("  0° = |0⟩ state")
    print("  90° = Equal superposition")
    print("  180° = |1⟩ state")
    theta_deg = float(input("Enter theta (0-180°): "))
    
    print("\nPhi angle (in degrees):")
    print("  0° = Real superposition")
    print("  90° = Imaginary phase")
    print("  180° = Negative real")
    print("  270° = Negative imaginary")
    phi_deg = float(input("Enter phi (0-360°): "))
    
    shots = int(input("\nNumber of shots (e.g., 1024): "))
    
    # Convert degrees to radians
    theta_rad = np.deg2rad(theta_deg)
    phi_rad = np.deg2rad(phi_deg)
    
    return theta_rad, phi_rad, shots

def main():
    print_header("Quantum Teleportation Project - Sabir")

    # Get parameters from user
    theta, phi, shots = get_user_input()

    print(f"\nSimulating with parameters:")
    print(f"θ = {theta*180/np.pi:.1f}°")
    print(f"φ = {phi*180/np.pi:.1f}°")
    print(f"Number of shots: {shots}")

    # Run quantum teleportation
    qc, counts = run_simulation(theta=theta, phi=phi, shots=shots)
    print("\nTeleportation Results:")
    print("---------------------")
    print("Measurement counts:", counts)
    print("State fidelity:", compute_fidelity(theta=theta, phi=phi))

if __name__ == "__main__":
    main()
