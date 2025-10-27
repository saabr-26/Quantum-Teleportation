"""
noise_model.py
-----------------------------------
Quantum Teleportation with Noise (Qiskit Aer)
"""

from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from .teleportation_qiskit import build_teleportation_circuit
from .utils import create_results_dir, save_plot


def build_noise_model(noise_strength=0.02):
    """
    Create a simple depolarizing + relaxation noise model.
    
    Args:
        noise_strength (float): Base noise level for depolarizing error
    """
    noise_model = NoiseModel()

    # Scale noise parameters based on input strength
    dep_error = depolarizing_error(noise_strength, 1)
    cx_error = depolarizing_error(noise_strength * 2.5, 2)  # CX gates typically have higher error
    t1_time = 50e3 * (1/noise_strength)  # Longer T1 time = less noise
    t2_time = 70e3 * (1/noise_strength)  # Longer T2 time = less noise
    
    t1_error = thermal_relaxation_error(t1_time, t2_time, 50e-6)
    t2_error = thermal_relaxation_error(t1_time * 1.4, t2_time * 1.3, 50e-6)

    noise_model.add_all_qubit_quantum_error(dep_error, ['x', 'u3'])
    noise_model.add_all_qubit_quantum_error(cx_error, ['cx'])
    return noise_model


def run_noisy_simulation(noise_strength=0.02):
    """
    Run teleportation with added noise.
    
    Args:
        noise_strength (float): Strength of the noise (0 = no noise, 1 = maximum noise)
    """
    noise_model = build_noise_model(noise_strength)
    backend = Aer.get_backend('aer_simulator')
    backend.set_options(noise_model=noise_model)

    qc = build_teleportation_circuit()
    # Use backend.run(...) instead of execute(...)
    job = backend.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts()

    create_results_dir("results/plots")
    plot_histogram(counts)
    save_plot("results/plots/noisy_results.png")
    print("Noisy simulation complete. Results saved.")

    return counts


if __name__ == "__main__":
    run_noisy_simulation()
