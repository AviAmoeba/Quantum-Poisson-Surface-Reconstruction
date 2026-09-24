
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector

from qiskit.circuit.library.arithmetic.piecewise_chebyshev import PiecewiseChebyshev


import classical_main as main
import funcs.geometry as geo

def gaussian(r2, sigma):
    value = np.exp( -r2 / (2 * sigma**2) )
    return value

scan_points, scan_normals = geo.generate_circle_points()

Nx = 8
Ny = 8

size = 2.0

x = np.linspace(-size, size, Nx)
y = np.linspace(-size, size, Ny)

dx = x[1] - x[0]
dy = y[1] - y[0]

X, Y = np.meshgrid(x, y, indexing="ij")

n_x = int(np.log2(Nx))
n_y = int(np.log2(Ny))

grid_points = np.column_stack( (X.ravel(), Y.ravel()) )

grid_vectors = main.vector_field_tree(scan_points, scan_normals, grid_points, gaussian, sigma=0.1)

divergence = main.calculate_divergence(grid_vectors, Nx, Ny, dx, dy)


f_grid = divergence

f_vector = f_grid.flatten()

f_vector = f_vector - np.mean(f_vector)

norm_f = np.linalg.norm(f_vector)

f_state = f_vector / norm_f


x_qubits = list(range(n_x))
y_qubits = list(range(n_x, n_x + n_y))

position_qubits = x_qubits + y_qubits

n_position_qubits = n_x + n_y

ancilla = n_position_qubits

n_qubits = n_position_qubits + 1

qc = QuantumCircuit(n_qubits)

qc.initialize(f_state, position_qubits)

qc.barrier()

qft_x = QFT(n_x, inverse=False).to_gate(label="QFT_x")
qft_y = QFT(n_y, inverse=False).to_gate(label="QFT_y")

qc.append(qft_x, x_qubits)
qc.append(qft_y, y_qubits)

qc.barrier()


def laplacian_eigenvalue(kx, ky, Nx, Ny, dx, dy):

    lambda_x = (4.0 / dx**2 * np.sin(np.pi * kx / Nx)**2)
    lambda_y = (4.0 / dy**2 * np.sin(np.pi * ky / Ny)**2)

    return lambda_x + lambda_y

lambdas = np.zeros((Nx, Ny))

for kx in range(Nx):

    for ky in range(Ny):

        lambdas[kx, ky] = laplacian_eigenvalue(kx, ky, Nx, Ny, dx, dy)


lambdas[0, 0] = 0.0

nonzero_eigenvalues = lambdas[lambdas > 1.0e-12]

lambda_min = np.min(nonzero_eigenvalues)
lambda_max = np.max(nonzero_eigenvalues)

C = lambda_min

def theta_exact_from_index(index):
    index = np.asarray(index)

    kx = index // Ny
    ky = index % Ny

    lam = laplacian_eigenvalue(kx, ky, Nx, Ny, dx, dy)
    theta = np.zeros_like(lam, dtype=float)

    mask = lam > 1.0e-12

    ratio = np.zeros_like(lam, dtype=float)

    ratio[mask] = C / lam[mask]

    ratio = np.clip(ratio, 0.0, 1.0)

    theta[mask] = np.arcsin(ratio[mask])

    if theta.ndim == 0:
        return float(theta)

    return theta


N_position = Nx * Ny

eps = 1.0e-6


breakpoints = [0, 1, 2, 4, 8, 16, 32, 64, 128, N_position]

breakpoints = sorted(
    set(
        b for b in breakpoints
        if 0 <= b <= N_position
    )
)

degree = 6

pw_approximation = PiecewiseChebyshev(
    theta_exact_from_index,
    degree,
    breakpoints,
    n_position_qubits
)

pw_approximation._build()

pw_gate = pw_approximation.to_instruction()

pw_gate.label = "2D Chebyshev"

required_pw_qubits = pw_approximation.num_qubits


if required_pw_qubits > n_qubits:

    n_total = required_pw_qubits

    qc = QuantumCircuit(n_total)

    qc.initialize(f_state, position_qubits)

    qc.barrier()

    qc.append(qft_x, x_qubits)
    qc.append(qft_y, y_qubits)

    qc.barrier()

pw_qubits = list(range(pw_approximation.num_qubits))


qc.append(pw_gate, pw_qubits)

qc.barrier()

qc.append(qft_x.inverse(), x_qubits)
qc.append(qft_y.inverse(), y_qubits)

qc.barrier()



print("Running statevector simulation...")


state = Statevector.from_instruction(qc)

amplitudes = state.data

n_total = qc.num_qubits
n_position = n_position_qubits

chi_vector = np.zeros(Nx * Ny, dtype=complex)

for index in range(Nx * Ny):
    chi_vector[index] = amplitudes[index]

chi_grid = chi_vector.reshape(Nx, Ny)


qc.draw("mpl", scale=0.5)
plt.show()


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

