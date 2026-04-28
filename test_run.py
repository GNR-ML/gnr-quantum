import numpy as np
from src.huckel import build_huckel_hamiltonian, solve_huckel, estimate_bandgap
from src.encoding import compare_encodings

adjacency = np.array([
    [0, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 1, 0],
], dtype=int)

h = build_huckel_hamiltonian(adjacency, alpha_default=0.0, beta_default=-1.0)
eigvals, _ = solve_huckel(h)
homo, lumo, gap = estimate_bandgap(eigvals, n_electrons=6)

print("Eigenvalues:", eigvals)
print("HOMO:", homo)
print("LUMO:", lumo)
print("Bandgap:", gap)
print("Encoding:", compare_encodings(6))