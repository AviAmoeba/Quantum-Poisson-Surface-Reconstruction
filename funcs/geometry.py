import numpy as np


# 2D geomtries

def generate_square_points(n_per_side=25, size=1.0):

    points = []
    normals = []

    for x in np.linspace(-size, size, n_per_side, endpoint=False):
        points.append([x, -size])
        normals.append([0, -1])

    for y in np.linspace(-size, size, n_per_side, endpoint=False):
        points.append([size, y])
        normals.append([1, 0])

    for x in np.linspace(size, -size, n_per_side, endpoint=False):
        points.append([x, size])
        normals.append([0, 1])

    for y in np.linspace(size, -size, n_per_side, endpoint=False):
        points.append([-size, y])
        normals.append([-1, 0])

    points = np.array(points, dtype=float)
    normals = np.array(normals, dtype=float)

    return points, normals

def generate_square_wedge_points( n_per_side=20, n_per_wedge=15, size=1.0, ):

    points = []
    normals = []

    for x in np.linspace(-size, size, n_per_side, endpoint=False):
        points.append([x, -size])
        normals.append([0, -1])

    for y in np.linspace(-size, -0.3 * size, n_per_side, endpoint=False):
        points.append([size, y])
        normals.append([1, 0])

    p1 = np.array([size, -0.3 * size])
    p2 = np.array([0.0, 0.0])

    direction = p2 - p1
    length = np.linalg.norm(direction)

    normal = np.array([direction[1], -direction[0]]) / length

    for t in np.linspace(0, 1, n_per_wedge, endpoint=False):
        p = p1 + t * direction
        points.append(p)
        normals.append(normal)

    p1 = np.array([0.0, 0.0])
    p2 = np.array([size, 0.3 * size])

    direction = p2 - p1
    length = np.linalg.norm(direction)

    normal = np.array([direction[1], -direction[0]]) / length

    for t in np.linspace(0, 1, n_per_wedge, endpoint=False):
        p = p1 + t * direction
        points.append(p)
        normals.append(normal)

    for y in np.linspace(0.3 * size, size, n_per_side, endpoint=False):
        points.append([size, y])
        normals.append([1, 0])

    for x in np.linspace(size, -size, n_per_side, endpoint=False):
        points.append([x, size])
        normals.append([0, 1])

    for y in np.linspace(size, -size, n_per_side, endpoint=False):
        points.append([-size, y])
        normals.append([-1, 0])

    points = np.array(points, dtype=float)
    normals = np.array(normals, dtype=float)

    return points, normals

def generate_circle_points(n=25):

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    points = np.column_stack((np.cos(angles), np.sin(angles)))
    normals = points.copy()

    return points, normals

def generate_circle_wedge_points( n_per_circle=50, n_per_wedge=15, radius=1.0, wedge_angle=np.pi / 3 ):

    points = []
    normals = []

    half_angle = wedge_angle / 2

    angles = np.linspace(
        half_angle,
        2 * np.pi - half_angle,
        n_per_circle,
        endpoint=False,
    )

    for theta in angles:

        p = radius * np.array([
            np.cos(theta),
            np.sin(theta),
        ])

        normal = p / radius

        points.append(p)
        normals.append(normal)

    theta = half_angle

    p1 = np.array([0.0, 0.0])

    p2 = radius * np.array([
        np.cos(theta),
        np.sin(theta),
    ])

    direction = p2 - p1

    normal = np.array([
        direction[1],
        -direction[0],
    ])

    normal /= np.linalg.norm(normal)

    for t in np.linspace(
        0,
        1,
        n_per_wedge,
        endpoint=False,
    ):

        p = p1 + t * direction

        points.append(p)
        normals.append(normal)

    theta = -half_angle

    p1 = np.array([0.0, 0.0])

    p2 = radius * np.array([
        np.cos(theta),
        np.sin(theta),
    ])

    direction = p2 - p1

    normal = np.array([
        -direction[1],
        direction[0],
    ])

    normal /= np.linalg.norm(normal)

    for t in np.linspace( 0, 1, n_per_wedge, endpoint=False ):

        p = p1 + t * direction

        points.append(p)
        normals.append(normal)
    
    points = np.array(points, dtype=float)
    normals = np.array(normals, dtype=float)

    return points, normals



def generate_pentagon_points(n_per_side=25, size=1.0):

    points = []
    normals = []

    angles = np.linspace(
        np.pi / 2,
        np.pi / 2 + 2 * np.pi,
        6,
    )[:-1]

    vertices = size * np.column_stack((
        np.cos(angles),
        np.sin(angles),
    ))

    for i in range(5):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % 5]

        direction = p2 - p1

        normal = np.array([
            direction[1],
            -direction[0],
        ])

        normal /= np.linalg.norm(normal)

        for t in np.linspace(
            0,
            1,
            n_per_side,
            endpoint=False,
        ):
            p = p1 + t * direction

            points.append(p)
            normals.append(normal)

    points = np.array(points, dtype=float)
    normals = np.array(normals, dtype=float)

    return points, normals



# 3D geometry

def generate_sphere_points(n=100, radius=1.0):

    # Fibonacci sphere
    indices = np.arange(n)

    phi = np.arccos( 1 - 2 * (indices + 0.5) / n )

    theta = np.pi * (1 + np.sqrt(5)) * indices

    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)

    points = radius * np.column_stack((x, y, z))

    normals = points / radius

    return points, normals


def generate_cube_points(n_per_side=25, size=1.0):
    
    points = []
    normals = []

    values = np.linspace(-size, size, n_per_side, endpoint=False)

    for y in values:
        for z in values:
            points.append([-size, y, z])
            normals.append([-1, 0, 0])

    for y in values:
        for z in values:
            points.append([size, y, z])
            normals.append([1, 0, 0])

    for x in values:
        for z in values:
            points.append([x, -size, z])
            normals.append([0, -1, 0])

    for x in values:
        for z in values:
            points.append([x, size, z])
            normals.append([0, 1, 0])

    for x in values:
        for y in values:
            points.append([x, y, -size])
            normals.append([0, 0, -1])

    for x in values:
        for y in values:
            points.append([x, y, size])
            normals.append([0, 0, 1])

    points = np.array(points, dtype=float)
    normals = np.array(normals, dtype=float)

    return points, normals

