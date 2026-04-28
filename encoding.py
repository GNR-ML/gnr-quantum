import math


def jordan_wigner_qubits(n_orbitals: int) -> int:
    return n_orbitals


def compact_encoding_qubits(n_orbitals: int) -> int:
    if n_orbitals < 1:
        raise ValueError("Number of orbitals must be positive.")
    return math.ceil(math.log2(n_orbitals))


def compare_encodings(n_orbitals: int) -> dict:
    jw = jordan_wigner_qubits(n_orbitals)
    compact = compact_encoding_qubits(n_orbitals)
    savings = jw - compact
    return {
        "n_orbitals": n_orbitals,
        "jordan_wigner_qubits": jw,
        "compact_qubits": compact,
        "qubit_savings": savings,
    }