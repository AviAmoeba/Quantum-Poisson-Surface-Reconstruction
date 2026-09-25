import numpy as np
from scipy.interpolate import RegularGridInterpolator

def vector_field_tree(scan_points, scan_normals, grid_points, Smoothing_Kernal, **kwargs):

    V = np.zeros((len(grid_points), 2))

    for i, x in enumerate(grid_points):

        for j, p in enumerate(scan_points):

            r2 = np.sum((x - p) ** 2)

            n = scan_normals[j]

            weight = Smoothing_Kernal(r2, **kwargs)

            V[i] += weight * n

    return V

def calculate_gradient(Vx, Vy, dx, dy):

    dVx_dx = np.zeros_like(Vx)
    dVy_dy = np.zeros_like(Vy)

    dVx_dx[:-1, :] = (Vx[1:, :] - Vx[:-1, :]) / dx
    dVx_dx[-1, :] = (Vx[-1, :] - Vx[-2, :]) / dx

    dVy_dy[:, :-1] = (Vy[:, 1:] - Vy[:, :-1]) / dy
    dVy_dy[:, -1] = (Vy[:, -1] - Vy[:, -2]) / dy

    return dVx_dx, dVy_dy

def calculate_divergence(grid_vectors, nx, ny, dx, dy):

    Vx = grid_vectors[:, 0].reshape(nx, ny)
    Vy = grid_vectors[:, 1].reshape(nx, ny)
    
    dVx_dx = np.gradient(Vx, dx, axis=0)
    dVy_dy = np.gradient(Vy, dy, axis=1)

    divergence = dVx_dx + dVy_dy

    return divergence.ravel()

def poisson_solver(divergence, nx, ny, dx, dy):

    divergence_grid = divergence.reshape(nx, ny)

    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)

    KX, KY = np.meshgrid(kx, ky, indexing="ij")

    laplacian_eigenvalues = -(KX**2 + KY**2)

    divergence_hat = np.fft.fft2(divergence_grid)

    chi_hat = np.zeros_like(divergence_hat, dtype=complex)

    mask = laplacian_eigenvalues != 0

    chi_hat[mask] = ( divergence_hat[mask] / laplacian_eigenvalues[mask] )

    chi_hat[0, 0] = 0

    chi_grid = np.real(np.fft.ifft2(chi_hat))

    return chi_grid.ravel()

def surface_reconstruction(scan_points, scan_normals, size, nx, ny, Smoothing_Kernal, **kwargs):
    
    x = np.linspace(-size, size, nx)
    y = np.linspace(-size, size, ny)

    dx = x[1] - x[0]
    dy = y[1] - y[0]

    X, Y = np.meshgrid(x, y, indexing="ij")

    grid_points = np.column_stack( (X.ravel(), Y.ravel()) )

    grid_vectors = vector_field_tree(scan_points, scan_normals, grid_points, Smoothing_Kernal, **kwargs)

    divergence = calculate_divergence(grid_vectors, nx, ny, dx, dy)

    chi = poisson_solver(divergence, nx, ny, dx, dy)

    chi_grid = chi.reshape(nx, ny)

    interpolator = RegularGridInterpolator((x, y), chi_grid)

    chi_samples = interpolator(scan_points)

    iso_value = np.mean(chi_samples)

    return chi_grid, iso_value


