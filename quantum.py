import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

import classical_main as main
import geometry as geo

def gaussian(r2, sigma):
    value = np.exp( -r2 / (2 * sigma**2) )
    return value

scan_points, scan_normals = geo.generate_circle_points()

Nx = 8
Ny = 8
size = 2

x = np.linspace(-size, size, Nx)
y = np.linspace(-size, size, Ny)

dx = x[1] - x[0]
dy = y[1] - y[0]

X, Y = np.meshgrid(x, y, indexing="ij")

grid_points = np.column_stack( (X.ravel(), Y.ravel()) )

grid_vectors = main.vector_field_tree(scan_points, scan_normals, grid_points, gaussian, sigma=0.1)

divergence = main.calculate_divergence(grid_vectors, Nx, Ny, dx, dy)


f = divergence


f_vector = f.flatten()

f_state = f_vector / np.linalg.norm(f_vector)

nx = int(np.log2(Nx))
ny = int(np.log2(Ny))


n_position_qubits = nx + ny
n_qubits = n_position_qubits + 1
ancilla = n_position_qubits

x_qubits = list(range(nx))
y_qubits = list(range(nx, nx + ny))

qc = QuantumCircuit(n_qubits)

qc.initialize(f_state, range(n_position_qubits))

qc.barrier()

qft_x = QFT(nx)
qft_y = QFT(ny)

qc.append(qft_x, x_qubits)
qc.append(qft_y, y_qubits)

qc.barrier()


lambdas = np.zeros((Nx, Ny))

for kx in range(Nx):

    for ky in range(Ny):

        lambda_x = (4.0 / dx**2 * np.sin(np.pi * kx / Nx)**2)
        lambda_y = (4.0 / dy**2 * np.sin(np.pi * ky / Ny)**2)

        lambdas[kx, ky] = (lambda_x + lambda_y)

nonzero_eigenvalues = lambdas[ lambdas > 1e-12 ]

lambda_min = np.min(nonzero_eigenvalues)

C = lambda_min

for kx in range(Nx):

    for ky in range(Ny):

        lam = lambdas[kx, ky]

        if lam < 1e-12:
            continue

        ratio = C / lam

        ratio = min(max(ratio, 0.0), 1.0)

        theta = (2.0 * np.arcsin(ratio))

        bits = []

        for bit in range(nx):
            bits.append((kx >> bit) & 1)

        for bit in range(ny):
            bits.append((ky >> bit) & 1)


        for q, bit in zip(x_qubits + y_qubits, bits):

            if bit == 0:
                qc.x(q)


        qc.mcry(-theta, x_qubits + y_qubits, ancilla, mode="noancilla")


        for q, bit in zip(x_qubits + y_qubits, bits):

            if bit == 0:
                qc.x(q)

        qc.barrier()


iqft_x = QFT(nx, inverse=True)
iqft_y = QFT(ny, inverse=True)

qc.append(iqft_x, x_qubits)
qc.append(iqft_y, y_qubits)

qc.barrier()



# print("\nQuantum circuit:")
# print( qc.draw() )


# qc.draw("mpl")
# plt.show()

from qiskit.quantum_info import Statevector

state = Statevector.from_instruction(qc)

amplitudes = state.data

solution_amplitudes = np.array([
    amplitudes[i]
    for i in range(len(amplitudes))
    if ((i >> ancilla) & 1) == 1
])

chi_grid = solution_amplitudes.reshape(Nx, Ny)

# chi_grid = chi.reshape(nx, ny)

from scipy.interpolate import RegularGridInterpolator

interpolator = RegularGridInterpolator((x, y), chi_grid)

chi_samples = interpolator(scan_points)

iso_value = np.mean(chi_samples)



plt.figure(figsize=(7, 7))

plt.contour(
    X,
    Y,
    chi_grid,
    levels=[iso_value],
    colors="blue"
)

#plt.scatter(
#    scan_points[:, 0],
#    scan_points[:, 1],
#    color="red",
#    s=50,
#    zorder=3
#)

#plt.quiver(
#    scan_points[:, 0],
#    scan_points[:, 1],    
#    scan_normals[:, 0],
#    scan_normals[:, 1],
#    color="black",
#    angles="xy",
#    scale_units="xy",
#    scale=1,
#    width=0.005,
#    zorder=4
#)

plt.contourf(X, Y, chi_grid, cmap="coolwarm", levels=20)
plt.contour(X, Y, chi_grid)

plt.axis("equal")
plt.xlabel("x")
plt.ylabel("y")
plt.title("PSR")

plt.show()


fig, ax = plt.subplots(figsize=(7, 7))

contour = ax.contour(
    X,
    Y,
    chi_grid,
    levels=[iso_value]
)

ax.scatter(
    scan_points[:, 0],
    scan_points[:, 1],
    color="red",
    s=1,
    zorder=1
)

ax.axis("equal")
plt.show()