import math

def distance(coord1, coord2):
    r_x = (coord1[0] - coord2[0])**2
    r_y = (coord1[1] - coord2[1])**2
    r =  math.sqrt(r_x + r_y)
#   r = r_x + r_y
    return r

""" 
def calculate_vector_field(scan_points, scan_normals, grid_points, sigma, cutoff_distance):
    
    V = np.zeros((len(grid_points), 2))

    for i, x in enumerate(grid_points):
        
        diff = scan_points - x
        distances = np.linalg.norm(diff, axis=1)

        for r, n in zip(distances, scan_normals):
            weight = gaussian(r, sigma, cutoff_distance)
            V[i] += weight * n

    return V
"""