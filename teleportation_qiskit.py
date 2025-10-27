"""
teleportation_qiskit.py
-----------------------------------
Quantum Teleportation Simulation using Qiskit
Author: Sabir
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector, state_fidelity, DensityMatrix, partial_trace
from qiskit.visualization import plot_histogram, circuit_drawer
import matplotlib.pyplot as plt
import numpy as np
import os
from .utils import create_results_dir, save_plot


def prepare_psi(qc, qubit, theta=np.pi / 4, phi=np.pi / 2):
    """
    Prepare arbitrary single-qubit state |ψ⟩ = cos(theta/2)|0⟩ + e^(iφ)sin(theta/2)|1⟩
    
    Args:
        theta: Angle that determines superposition (0 to π)
               θ = 0: |0⟩ state
               θ = π/2: Equal superposition
               θ = π: |1⟩ state
        phi: Phase angle (0 to 2π) that affects the phase of superposition
    """
    # First create superposition with theta
    qc.ry(theta, qubit)
    # Then add phase with phi
    qc.rz(phi, qubit)
    # Add barrier to visualize state preparation
    qc.barrier()
    return qc


def build_teleportation_circuit(theta=np.pi/4, phi=np.pi/2):
    """
    Build quantum teleportation circuit (3 qubits, 3 classical bits)
    The three qubits are:
    - qubit 0: Alice's original qubit (state to teleport)
    - qubit 1: Alice's half of the entangled pair
    - qubit 2: Bob's half of the entangled pair
    """
    # Create circuit with 3 qubits and 3 classical bits
    qc = QuantumCircuit(3, 3)

    # Step 1: Prepare |ψ⟩ on qubit 0 (Alice's original qubit)
    prepare_psi(qc, 0, theta, phi)
    
    # Step 2: Create Bell pair between Alice's qubit 1 and Bob's qubit 2
    qc.h(1)     # Create superposition
    qc.cx(1, 2) # Entangle qubits 1 and 2
    qc.barrier()

    # Step 3: Bell measurement between Alice's qubits (0 and 1)
    qc.cx(0, 1)  # First part of Bell measurement
    qc.h(0)      # Second part of Bell measurement
    qc.barrier()

    # Step 4: Measure Alice's qubits
    qc.measure(0, 0)  # Measure first qubit
    qc.measure(1, 1)  # Measure second qubit
    qc.barrier()
    
    # Step 5: Apply quantum-controlled operations for Bob's corrections
    # If measurement 1 is |1⟩, apply X
    qc.cx(1, 2)
    # If measurement 0 is |1⟩, apply Z
    qc.cz(0, 2)
    qc.barrier()
    
    # Step 6: Measure Bob's final qubit
    qc.measure(2, 2)

    return qc


def run_simulation(theta=np.pi/4, phi=np.pi/2, shots=1024):
    """
    Run the teleportation circuit on Aer simulator and return results
    """
    qc = build_teleportation_circuit(theta, phi)
    simulator = Aer.get_backend('aer_simulator')

    # Execute using backend.run instead of execute()
    job = simulator.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Plot result
    create_results_dir("results/plots")
    plot_histogram(counts)
    save_plot("results/plots/teleportation_results.png")

    print("Simulation complete. Results saved in results/plots/")
    return qc, counts


def compute_fidelity(theta=np.pi/4, phi=np.pi/2):
    """
    Compute fidelity between input |ψ⟩ and teleported |ψ_out⟩
    """
    # Build the preparation circuit for |psi> and evolve the |0> state
    qc_psi = QuantumCircuit(1)
    qc_psi.ry(theta, 0)
    qc_psi.rz(phi, 0)
    ideal_input = Statevector.from_label('0').evolve(qc_psi)

    qc = build_teleportation_circuit(theta, phi)
    backend = Aer.get_backend('aer_simulator')
    qc.save_statevector()
    result = backend.run(qc).result()
    sv = result.get_statevector()

    # Extract Bob’s qubit (teleported state) by partial trace over qubits 0 and 1
    rho_full = DensityMatrix(sv)
    rho_bob = partial_trace(rho_full, [0, 1])
    fidelity = state_fidelity(ideal_input, rho_bob)

    return fidelity


if __name__ == "__main__":
    qc, counts = run_simulation()
    print("Counts:", counts)
    print("Fidelity:", compute_fidelity())
    circuit_drawer(qc, output='mpl', filename="results/plots/teleportation_circuit.png")
