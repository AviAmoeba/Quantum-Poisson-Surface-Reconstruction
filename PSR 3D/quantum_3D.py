

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector

from scipy.interpolate import RegularGridInterpolator

import classical_3D as main
import funcs.geometry as geo


def gaussian(r2, sigma):
    value = np.exp( -r2 / (2 * sigma**2) )
    return value


scan_points, scan_normals = geo.generate_sphere_points()

size = 2

Nx = 8
Ny = 8
Nz = 8


x = np.linspace(-size, size, Nx)
y = np.linspace(-size, size, Ny)
z = np.linspace(-size, size, Nz)

dx = x[1] - x[0]
dy = y[1] - y[0]
dz = z[1] - z[0]

X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

grid_points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

grid_vectors = main.vector_field_tree(scan_points, scan_normals, grid_points, gaussian, 0.1)

divergence = main.calculate_divergence(grid_vectors, Nx, Ny, Nz, dx, dy, dz)


f = divergence

f_vector = f.flatten()

norm = np.linalg.norm(f_vector)

f_state = f_vector / norm

nx = int(np.log2(Nx))
ny = int(np.log2(Ny))
nz = int(np.log2(Nz))

n_position_qubits = nx + ny + nz

n_qubits = n_position_qubits + 1

ancilla = n_position_qubits

x_qubits = list(range(nx))
y_qubits = list(range(nx, nx + ny))
z_qubits = list(range(nx + ny, nx + ny + nz))

position_qubits = x_qubits + y_qubits + z_qubits

qc = QuantumCircuit(n_qubits)

qc.initialize(f_state, position_qubits)

qc.barrier()

qft_x = QFT(nx)
qft_y = QFT(ny)
qft_z = QFT(nz)

qc.append(qft_x, x_qubits)
qc.append(qft_y, y_qubits)
qc.append(qft_z, z_qubits)

qc.barrier()

lambdas = np.zeros((Nx, Ny, Nz))


for kx in range(Nx):
    lambda_x = 4.0 / dx**2 * np.sin(np.pi * kx / Nx)**2

    for ky in range(Ny):
        lambda_y = 4.0 / dy**2 * np.sin(np.pi * ky / Ny)**2

        for kz in range(Nz):
            lambda_z = 4.0 / dz**2 * np.sin(np.pi * kz / Nz)**2

            lambdas[kx, ky, kz] = lambda_x + lambda_y + lambda_z

nonzero_eigenvalues = lambdas[lambdas > 1e-12]

lambda_min = np.min(nonzero_eigenvalues)

C = lambda_min

for kx in range(Nx):
    for ky in range(Ny):
        for kz in range(Nz):

            lam = lambdas[kx, ky, kz]

            if lam < 1e-12:
                continue

            ratio = C / lam

            ratio = min(max(ratio, 0.0), 1.0)

            theta = 2.0 * np.arcsin(ratio)

            bits = []

            for bit in range(nx):
                bits.append((kx >> bit) & 1)

            for bit in range(ny):
                bits.append((ky >> bit) & 1)

            for bit in range(nz):
                bits.append((kz >> bit) & 1)

            for q, bit in zip(position_qubits, bits):
                if bit == 0:
                    qc.x(q)


            qc.mcry(-theta, position_qubits, ancilla, mode="noancilla")

            for q, bit in zip(position_qubits, bits):
                if bit == 0:
                    qc.x(q)


qc.barrier()

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


interpolator = RegularGridInterpolator((x, y, z), chi_grid, bounds_error=False, fill_value=None)

chi_samples = interpolator(scan_points)

iso_value = np.mean(chi_samples)

import matplotlib.pyplot as plt
from skimage.measure import marching_cubes

verts, faces, normals, values = marching_cubes(
    chi_grid,
    level=iso_value,
    spacing=(x[1] - x[0],
             y[1] - y[0],
             z[1] - z[0])
)

verts[:, 0] += x[0]
verts[:, 1] += y[0]
verts[:, 2] += z[0]

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")

ax.plot_trisurf(
    verts[:, 0],
    verts[:, 1],
    faces,
    verts[:, 2],
    alpha=0.7,
    edgecolor="none"
)

ax.scatter(
    scan_points[:, 0],
    scan_points[:, 1],
    scan_points[:, 2],
    color="red",
    s=5
)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_xlim(-size, size)
ax.set_ylim(-size, size)
ax.set_zlim(-size, size)

ax.set_box_aspect((1, 1, 1))

plt.show()

