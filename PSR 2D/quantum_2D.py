import numpy as np
from scipy.interpolate import RegularGridInterpolator

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector

import classical_2D as main

class QuantumFunction:

    def __init__(self, Nx, Ny, dx, dy, x_qubits, y_qubits, ancilla):
        self.Nx = Nx
        self.Ny = Ny
        self.dx = dx
        self.dy = dy
        self.x_qubits = x_qubits
        self.y_qubits = y_qubits
        self.ancilla = ancilla

    def compute_eigenvalues(self):

        lambdas = np.zeros((self.Nx, self.Ny))

        for kx in range(self.Nx):
            for ky in range(self.Ny):

                lambda_x = 4.0 / self.dx**2 * np.sin(np.pi * kx / self.Nx)**2
                lambda_y = 4.0 / self.dy**2 * np.sin(np.pi * ky / self.Ny)**2

                lambdas[kx, ky] = lambda_x + lambda_y

        return lambdas

    def apply(self, qc):

        lambdas = self.compute_eigenvalues()

        nonzero_eigenvalues = lambdas[lambdas > 1e-12]
        C = np.min(nonzero_eigenvalues)

        for kx in range(self.Nx):
            for ky in range(self.Ny):

                lam = lambdas[kx, ky]

                if lam < 1e-12:
                    continue

                ratio = C / lam

                ratio = np.clip(ratio, 0.0, 1.0)

                theta = 2.0 * np.arcsin(ratio)

                bits = []

                for bit in range(len(self.x_qubits)):
                    bits.append((kx >> bit) & 1)

                for bit in range(len(self.y_qubits)):
                    bits.append((ky >> bit) & 1)

                controls = self.x_qubits + self.y_qubits

                for q, bit in zip(controls, bits):
                    if bit == 0:
                        qc.x(q)

                qc.mcry(-theta, controls, self.ancilla, mode="noancilla")

                for q, bit in zip(controls, bits):
                    if bit == 0:
                        qc.x(q)
                
                qc.barrier()

        return qc






def quantum_poisson_solver(divergence, Nx, Ny, dx, dy):

    div_vector = divergence.flatten()
    div_state = div_vector / np.linalg.norm(div_vector)

    nx = int(np.log2(Nx))
    ny = int(np.log2(Ny))


    n_position_qubits = nx + ny
    n_qubits = n_position_qubits + 1
    ancilla = n_position_qubits

    x_qubits = list(range(nx))
    y_qubits = list(range(nx, nx + ny))

    qc = QuantumCircuit(n_qubits)

    qc.initialize(div_state, range(n_position_qubits))

    qc.barrier()

    qft_x = QFT(nx)
    qft_y = QFT(ny)

    qc.append(qft_x, x_qubits)
    qc.append(qft_y, y_qubits)

    qc.barrier()

    qf = QuantumFunction(
    Nx=Nx,
    Ny=Ny,
    dx=dx,
    dy=dy,
    x_qubits=x_qubits,
    y_qubits=y_qubits,
    ancilla=ancilla
    )

    qf.apply(qc)

    iqft_x = QFT(nx, inverse=True)
    iqft_y = QFT(ny, inverse=True)

    qc.append(iqft_x, x_qubits)
    qc.append(iqft_y, y_qubits)

    qc.barrier()

    state = Statevector.from_instruction(qc)

    amplitudes = state.data

    solution_amplitudes = np.array([
        amplitudes[i]
        for i in range(len(amplitudes))
        if ((i >> ancilla) & 1) == 1
    ])

    chi_grid = solution_amplitudes.reshape(Nx, Ny)

    return chi_grid

def quantum_reconstruction(scan_points, scan_normals, size, nx, ny, Smoothing_Kernal, **kwargs):
    
    x = np.linspace(-size, size, nx)
    y = np.linspace(-size, size, ny)

    dx = x[1] - x[0]
    dy = y[1] - y[0]

    X, Y = np.meshgrid(x, y, indexing="ij")

    grid_points = np.column_stack( (X.ravel(), Y.ravel()) )

    grid_vectors = main.vector_field_tree(scan_points, scan_normals, grid_points, Smoothing_Kernal, **kwargs)

    divergence = main.calculate_divergence(grid_vectors, nx, ny, dx, dy)

    chi = quantum_poisson_solver(divergence, nx, ny, dx, dy)

    chi_grid = chi.reshape(nx, ny)

    interpolator = RegularGridInterpolator((x, y), chi_grid)

    chi_samples = interpolator(scan_points)

    iso_value = np.mean(chi_samples)

    return chi_grid, iso_value




