
import numpy as np
from scipy.interpolate import RegularGridInterpolator


def vector_field_tree(scan_points, scan_normals, grid_points, Smoothing_Kernal, **kwargs):

    V = np.zeros((len(grid_points), 3))

    for i, x in enumerate(grid_points):
        
        for j, p in enumerate(scan_points):

            r2 = np.sum((x - p) ** 2)

            n = scan_normals[j]

            weight = Smoothing_Kernal(r2, **kwargs)

            V[i] += weight * n

    return V


def calculate_gradient_3d(Vx, Vy, Vz, dx, dy, dz):

    dVx_dx = np.zeros_like(Vx)
    dVy_dy = np.zeros_like(Vy)
    dVz_dz = np.zeros_like(Vz)

    dVx_dx[:-1, :, :] = ( Vx[1:, :, :] - Vx[:-1, :, :] ) / dx
    dVx_dx[-1, :, :] = ( Vx[-1, :, :] - Vx[-2, :, :] ) / dx

    dVy_dy[:, :-1, :] = ( Vy[:, 1:, :] - Vy[:, :-1, :] ) / dy
    dVy_dy[:, -1, :] = ( Vy[:, -1, :] - Vy[:, -2, :] ) / dy

    dVz_dz[:, :, :-1] = ( Vz[:, :, 1:] - Vz[:, :, :-1] ) / dz
    dVz_dz[:, :, -1] = ( Vz[:, :, -1] - Vz[:, :, -2] ) / dz

    return dVx_dx, dVy_dy, dVz_dz


def calculate_divergence(grid_vectors, nx, ny, nz, dx, dy, dz):

    Vx = grid_vectors[:, 0].reshape(nx, ny, nz)
    Vy = grid_vectors[:, 1].reshape(nx, ny, nz)
    Vz = grid_vectors[:, 2].reshape(nx, ny, nz)

    dVx_dx = np.gradient(Vx, dx, axis=0)
    dVy_dy = np.gradient(Vy, dy, axis=1)
    dVz_dz = np.gradient(Vz, dz, axis=2)

    divergence = dVx_dx + dVy_dy + dVz_dz

    return divergence.ravel()


def poisson_solver_3d(divergence, nx, ny, nz, dx, dy, dz):

    divergence_grid = divergence.reshape(nx, ny, nz)

    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
    kz = 2 * np.pi * np.fft.fftfreq(nz, d=dz)

    KX, KY, KZ = np.meshgrid( kx, ky, kz, indexing="ij" )

    laplacian_eigenvalues = - ( KX**2 + KY**2 + KZ**2 )

    divergence_hat = np.fft.fftn(divergence_grid)

    chi_hat = np.zeros_like(divergence_hat, dtype=complex)

    mask = laplacian_eigenvalues != 0

    chi_hat[mask] = divergence_hat[mask] / laplacian_eigenvalues[mask]

    chi_hat[0, 0, 0] = 0

    chi_grid = np.real(np.fft.ifftn(chi_hat))

    return chi_grid.ravel()


def surface_reconstruction_3d(scan_points, scan_normals, size, nx, ny, nz, Smoothing_Kernal, **args):

    x = np.linspace(-size, size, nx)
    y = np.linspace(-size, size, ny)
    z = np.linspace(-size, size, nz)

    dx = x[1] - x[0]
    dy = y[1] - y[0]
    dz = z[1] - z[0]

    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    grid_points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

    grid_vectors = vector_field_tree(scan_points, scan_normals, grid_points, Smoothing_Kernal, **args)

    divergence = calculate_divergence(grid_vectors, nx, ny, nz, dx, dy, dz)

    chi = poisson_solver_3d(divergence, nx, ny, nz, dx, dy, dz)

    chi_grid = chi.reshape(nx, ny, nz)

    interpolator = RegularGridInterpolator((x, y, z), chi_grid, bounds_error=False, fill_value=None)

    chi_samples = interpolator(scan_points)

    iso_value = np.mean(chi_samples)

    return chi_grid, iso_value




def gaussian(r2, sigma):
    value = np.exp( -r2 / (2 * sigma**2) )
    return value


import geometry as geo

scan_points, scan_normals = geo.generate_sphere_points()

size = 2

nx = 8
ny = 8
nz = 8

chi_grid, iso_value = surface_reconstruction_3d(scan_points, scan_normals, size, nx, ny, nz, gaussian, sigma=0.2)









import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-size, size, nx)
y = np.linspace(-size, size, ny)
z = np.linspace(-size, size, nz)

X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

tolerance = 0.02

mask = np.abs(chi_grid - iso_value) < tolerance

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")

ax.scatter(
    X[mask],
    Y[mask],
    Z[mask],
    s=5,
    alpha=0.5
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

print("show")

plt.show()