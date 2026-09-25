
import numpy as np


from scipy.spatial.distance import cdist

def chamfer_cdist(A, B):
    
    distences = cdist(A, B, metric="euclidean")

    min_A_to_B = distences.min(axis=1)
    min_B_to_A = distences.min(axis=0)

    chamfer_distance = min_A_to_B.mean() + min_B_to_A.mean()
    return chamfer_distance


from scipy.spatial import cKDTree

def chamfer_kdtree(points_a, points_b):

    points_a = np.asarray(points_a)
    points_b = np.asarray(points_b)

    tree_a = cKDTree(points_a)
    tree_b = cKDTree(points_b)


    dist_a_to_b, _ = tree_b.query(points_a)
    dist_b_to_a, _ = tree_a.query(points_b)

    return np.mean(dist_a_to_b) + np.mean(dist_b_to_a)






from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from skimage.measure import find_contours


def iso_contour_to_polygons(chi_grid, iso_value, x, y):

    contours = find_contours(chi_grid, level=iso_value)

    polygons = []

    for contour in contours:

        xi = np.interp(contour[:, 0], np.arange(len(x)), x)
        yi = np.interp(contour[:, 1], np.arange(len(y)), y)

        points = np.column_stack((xi, yi))

        polygon = Polygon(points)

        if polygon.is_valid and polygon.area > 0:
            polygons.append(polygon)

    return polygons


def circle_vs_isosurface_iou(chi_grid, iso_value, x, y, circle_radius=1, circle_resolution=256):

    circle = Point(0, 0).buffer(circle_radius, resolution=circle_resolution)

    polygons = iso_contour_to_polygons(chi_grid, iso_value, x, y)

    iso_shape = unary_union(polygons)

    intersection_area = circle.intersection(iso_shape).area
    union_area = circle.union(iso_shape).area

    return intersection_area / union_area


