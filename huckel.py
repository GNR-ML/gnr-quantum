import numpy as np


def build_huckel_hamiltonian(
    adjacency: np.ndarray,
    alpha_default: float = 0.0,
    beta_default: float = -1.0,
    alpha_values: np.ndarray | None = None,
    beta_matrix: np.ndarray | None = None,
) -> np.ndarray:
    n = adjacency.shape[0]
    h = np.zeros((n, n), dtype=float)

    if alpha_values is None:
        alpha_values = np.full(n, alpha_default, dtype=float)

    for i in range(n):
        h[i, i] = alpha_values[i]

    for i in range(n):
        for j in range(i + 1, n):
            if adjacency[i, j] != 0:
                beta = beta_default if beta_matrix is None else beta_matrix[i, j]
                h[i, j] = beta
                h[j, i] = beta

    return h


def solve_huckel(h: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    eigvals, eigvecs = np.linalg.eigh(h)
    return eigvals, eigvecs


def estimate_bandgap(eigvals: np.ndarray, n_electrons: int) -> tuple[float, float, float]:
    occupied_orbitals = n_electrons // 2
    homo_idx = occupied_orbitals - 1
    lumo_idx = occupied_orbitals

    if homo_idx < 0 or lumo_idx >= len(eigvals):
        raise ValueError("Invalid electron count for available orbitals.")

    homo = eigvals[homo_idx]
    lumo = eigvals[lumo_idx]
    gap = lumo - homo
    return homo, lumo, gap


def make_edge_aware_alpha(n: int, edge_indices: list[int], edge_alpha: float, interior_alpha: float) -> np.ndarray:
    alpha = np.full(n, interior_alpha, dtype=float)
    for idx in edge_indices:
        alpha[idx] = edge_alpha
    return alpha