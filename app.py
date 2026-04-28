import numpy as np
import pandas as pd
import streamlit as st

from src.huckel import (
    build_huckel_hamiltonian,
    solve_huckel,
    estimate_bandgap,
    make_edge_aware_alpha,
)
from src.encoding import compare_encodings

st.set_page_config(page_title="GNR Quantum Prototype", layout="wide")

st.title("GNR Quantum Prototype")
st.markdown(
    """
This lightweight demo explores small Hückel Hamiltonians with **fixed** and **structure-aware**
parameters. It shows how changing local **alpha** values can affect **HOMO, LUMO, and bandgap**
estimates, while also comparing **Jordan-Wigner** and **compact encoding** in terms of qubit use.
"""
)

st.info(
    "This is an early proof-of-concept for a reproducible benchmark workflow connecting "
    "computational chemistry and near-term quantum methods."
)

left, right = st.columns([1, 1])

with left:
    st.subheader("System setup")
    system = st.selectbox("Choose a toy system", ["6-site linear chain", "4-site ring"])

    if system == "6-site linear chain":
        adjacency = np.array([
            [0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 1, 0],
        ], dtype=int)
        edge_indices = [0, 5]
        n_electrons = 6
    else:
        adjacency = np.array([
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0],
        ], dtype=int)
        edge_indices = [0, 1, 2, 3]
        n_electrons = 4

    n_orbitals = adjacency.shape[0]

    st.subheader("Model parameters")
    alpha_fixed = st.slider("Fixed alpha", -2.0, 2.0, 0.0, 0.1)
    alpha_interior = st.slider("Interior alpha", -2.0, 2.0, 0.0, 0.1)
    alpha_edge = st.slider("Edge alpha", -2.0, 2.0, 0.2, 0.1)
    beta = st.slider("Beta", -3.0, 0.0, -1.0, 0.1)

    st.caption(
        "Fixed Hückel uses one alpha for all sites. Edge-aware Hückel assigns a different alpha "
        "to edge sites as a simple proof-of-concept for local parameterization."
    )

# Fixed model
h_fixed = build_huckel_hamiltonian(
    adjacency=adjacency,
    alpha_default=alpha_fixed,
    beta_default=beta,
)
eigvals_fixed, _ = solve_huckel(h_fixed)
homo_f, lumo_f, gap_f = estimate_bandgap(eigvals_fixed, n_electrons)

# Edge-aware model
alpha_values = make_edge_aware_alpha(
    n=n_orbitals,
    edge_indices=edge_indices,
    edge_alpha=alpha_edge,
    interior_alpha=alpha_interior,
)
h_edge = build_huckel_hamiltonian(
    adjacency=adjacency,
    alpha_values=alpha_values,
    beta_default=beta,
)
eigvals_edge, _ = solve_huckel(h_edge)
homo_e, lumo_e, gap_e = estimate_bandgap(eigvals_edge, n_electrons)

encoding_info = compare_encodings(n_orbitals)

with right:
    st.subheader("Quick results")
    c1, c2, c3 = st.columns(3)
    c1.metric("Fixed bandgap", f"{gap_f:.4f}")
    c2.metric("Edge-aware bandgap", f"{gap_e:.4f}")
    c3.metric("Qubit savings", encoding_info["qubit_savings"])

    st.subheader("Encoding comparison")
    encoding_df = pd.DataFrame([encoding_info]).rename(columns={
        "n_orbitals": "Orbitals",
        "jordan_wigner_qubits": "Jordan-Wigner qubits",
        "compact_qubits": "Compact qubits",
        "qubit_savings": "Qubit savings",
    })
    st.dataframe(encoding_df, width="stretch")

st.subheader("Bandgap comparison")
comparison_df = pd.DataFrame([
    {"Model": "Fixed Hückel", "HOMO": homo_f, "LUMO": lumo_f, "Bandgap": gap_f},
    {"Model": "Edge-aware Hückel", "HOMO": homo_e, "LUMO": lumo_e, "Bandgap": gap_e},
])
st.dataframe(comparison_df, width="stretch")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fixed-model eigenvalues")
    fixed_df = pd.DataFrame({
        "Orbital": list(range(len(eigvals_fixed))),
        "Energy": eigvals_fixed,
    })
    st.dataframe(fixed_df, width="stretch")
    st.line_chart(fixed_df.set_index("Orbital"))

with col2:
    st.subheader("Edge-aware eigenvalues")
    edge_df = pd.DataFrame({
        "Orbital": list(range(len(eigvals_edge))),
        "Energy": eigvals_edge,
    })
    st.dataframe(edge_df, width="stretch")
    st.line_chart(edge_df.set_index("Orbital"))

with st.expander("What this prototype demonstrates"):
    st.markdown(
        """
- A simple **Hückel Hamiltonian workflow**
- A proof-of-concept for **structure-aware alpha parameterization**
- Classical estimates of **HOMO, LUMO, and bandgap**
- A resource comparison between **Jordan-Wigner** and **compact encoding**
- A starting point for a broader open-source benchmark toolkit
"""
    )