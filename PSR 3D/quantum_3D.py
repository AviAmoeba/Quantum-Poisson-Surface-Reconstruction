import numpy as np
from scipy.interpolate import RegularGridInterpolator

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector

import classical_3D as main

class QuantumFunction:

    def __init__(self, Nx, Ny, Nz, dx, dy, dz, x_qubits, y_qubits, z_qubits, ancilla):
        self.Nx = Nx
        self.Ny = Ny
        self.Nz = Nz

        self.dx = dx
        self.dy = dy
        self.dz = dz

        self.x_qubits = x_qubits
        self.y_qubits = y_qubits
        self.z_qubits = z_qubits

        self.ancilla = ancilla

    def compute_eigenvalues(self):

        lambdas = np.zeros((self.Nx, self.Ny, self.Nz))

        for kx in range(self.Nx):
            for ky in range(self.Ny):
                for kz in range(self.Nz):

                    lambda_x = 4.0 / self.dx**2 * np.sin(np.pi * kx / self.Nx)**2
                    lambda_y = 4.0 / self.dy**2 * np.sin(np.pi * ky / self.Ny)**2
                    lambda_z = 4.0 / self.dz**2 * np.sin(np.pi * kz / self.Nz)**2

                    lambdas[kx, ky, kz] = lambda_x + lambda_y + lambda_z

        return lambdas

    def apply(self, qc):

        lambdas = self.compute_eigenvalues()

        nonzero_eigenvalues = lambdas[lambdas > 1e-12]
        C = np.min(nonzero_eigenvalues)

        controls = (
            self.x_qubits
            + self.y_qubits
            + self.z_qubits
        )

        for kx in range(self.Nx):
            for ky in range(self.Ny):
                for kz in range(self.Nz):

                    lam = lambdas[kx, ky, kz]

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

                    for bit in range(len(self.z_qubits)):
                        bits.append((kz >> bit) & 1)

                    for q, bit in zip(controls, bits):
                        if bit == 0:
                            qc.x(q)

                    qc.mcry(-theta, controls, self.ancilla, mode="noancilla")

                    for q, bit in zip(controls, bits):
                        if bit == 0:
                            qc.x(q)

                    qc.barrier()

        return qc
    

def quantum_poisson_solver(divergence, Nx, Ny, Nz, dx, dy, dz):

    div_vector = divergence.flatten()
    div_state = div_vector / np.linalg.norm(div_vector)

    nx = int(np.log2(Nx))
    ny = int(np.log2(Ny))
    nz = int(np.log2(Nz))

    n_position_qubits = nx + ny + nz
    n_qubits = n_position_qubits + 1
    ancilla = n_position_qubits

    x_qubits = list(range(nx))
    y_qubits = list(range(nx, nx + ny))
    z_qubits = list(range(nx + ny, nx + ny + nz))

    qc = QuantumCircuit(n_qubits)

    qc.initialize(div_state, range(n_position_qubits))

    qc.barrier()

    qft_x = QFT(nx)
    qft_y = QFT(ny)
    qft_z = QFT(nz)

    qc.append(qft_x, x_qubits)
    qc.append(qft_y, y_qubits)
    qc.append(qft_z, z_qubits)

    qc.barrier()

    qf = QuantumFunction(
        Nx=Nx,
        Ny=Ny,
        Nz=Nz,
        dx=dx,
        dy=dy,
        dz=dz,
        x_qubits=x_qubits,
        y_qubits=y_qubits,
        z_qubits=z_qubits,
        ancilla=ancilla
    )

    qf.apply(qc)

    iqft_x = QFT(nx, inverse=True)
    iqft_y = QFT(ny, inverse=True)
    iqft_z = QFT(nz, inverse=True)

    qc.append(iqft_x, x_qubits)
    qc.append(iqft_y, y_qubits)
    qc.append(iqft_z, z_qubits)

    qc.barrier()

    state = Statevector.from_instruction(qc)

    amplitudes = state.data

    solution_amplitudes = np.array([
        amplitudes[i]
        for i in range(len(amplitudes))
        if ((i >> ancilla) & 1) == 1
    ])

    chi_grid = solution_amplitudes.reshape(Nx, Ny, Nz)

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



