"""
teleportation_qutip.py
-----------------------------------
Teleportation Simulation using QuTiP (Analytical verification)
"""

from qutip import basis, tensor, qeye, sigmax, sigmaz, hadamard_transform, cnot, fidelity
import numpy as np

def teleportation_qutip(theta=np.pi/4, phi=np.pi/2):
    """
    Analytical quantum teleportation using operator formalism.
    """
    # Qubit states
    zero = basis(2, 0)
    one = basis(2, 1)
    psi = np.cos(theta/2)*zero + np.exp(1j*phi)*np.sin(theta/2)*one

    # Entangled pair |Φ+>
    bell_pair = (tensor(zero, zero) + tensor(one, one)).unit()

    # Full system: |ψ> (Alice) ⊗ |Φ+> (shared)
    state = tensor(psi, bell_pair)

    # Bell measurement (apply CNOT and H)
    state = cnot(N=3, control=0, target=1) * state
    state = tensor(hadamard_transform(), qeye(2), qeye(2)) * state

    # Trace out Alice's qubits to get Bob's qubit
    rho = state.ptrace(2)

    # Fidelity between input |ψ⟩ and Bob’s ρ
    fid = fidelity(psi.proj(), rho)
    return fid


if __name__ == "__main__":
    print("QuTiP Teleportation Fidelity:", teleportation_qutip())
