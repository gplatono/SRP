import math
import numpy

def cross_product(a, b):
    return (a[1] * b[2] - a[2] * b[1], b[0] * a[2] - b[2] * a[0],
            a[0] * b[1] - a[1] * b[0])

def get_normal(a, b, c):
    return cross_product((a[0] - b[0], a[1] - b[1], a[2] - b[2]),
                         (c[0] - b[0], c[1] - b[1], c[2] - b[2]))

def get_distance_from_plane(point, a, b, c):
    normal = numpy.array(get_normal(a, b, c))
    return math.fabs((numpy.array(point).dot(normal) - numpy.array(a).dot(normal)) / numpy.linalg.norm(normal))

#distance from x3 to the line connecting x1 to x2
def get_distance_from_line(x1, x2, x3):
    t = (x3[0] - x1[0]) * (x2[0] - x1[0]) + (x3[1] - x1[1]) * (x2[1] - x1[1]) * (x3[2] - x1[2]) * (x2[2] - x1[2])
    t = t / (point_distance(x1, x2) ** 2)
    x0 = (x1[0] + (x2[0] - x1[0]) * t, x1[1] + (x2[1] - x1[1]) * t, x1[2] + (x2[2] - x1[2]) * t)
    return point_distance(x0, x3)

#Euclidean distance between two points
def point_distance(a, b):
    return numpy.linalg.norm(numpy.array(a) - numpy.array(b))

def get_2d_bbox(points):
    min_x = 1e9
    min_y = 1e9
    max_x = -1e9
    max_y = -1e9
    for p in points:
        min_x = min(min_x, p[0])
        min_y = min(min_y, p[1])
        max_x = max(max_x, p[0])
        max_y = max(max_y, p[1])       
    return [min_x, max_x, min_y, max_y]

#Bounding box centroid distance
def get_centroid_distance(ent_a, ent_b):
    a_centroid = ent_a.get_bbox_centroid()
    b_centroid = ent_b.get_bbox_centroid()
    return point_distance(a_centroid, b_centroid)


def get_centroid_distance_scaled(ent_a, ent_b):
    a_max_dim = max(ent_a.get_dimensions())
    b_max_dim = max(ent_b.get_dimensions())

    #add a small number to denominator in order to
    #avoid division by zero in the case when a_max_dim + b_max_dim == 0
    return get_centroid_distance(ent_a, ent_b) / (a_max_dim + b_max_dim + 0.0001)

def get_line_distance_scaled(ent_a, ent_b):
    a_dims = ent_a.get_dimensions()
    b_dims = ent_b.get_dimensions()
    a_bbox = a.get_bbox()
    dist = 0
    if a_dims[0] >= 1.4 * (a_dims[1] + a_dims[2]):
        dist = min(get_distance_from_line(a_bbox[0], a_bbox[4], b.centroid),
                   get_distance_from_line(a_bbox[1], a_bbox[5], b.centroid),
                   get_distance_from_line(a_bbox[2], a_bbox[6], b.centroid),
                   get_distance_from_line(a_bbox[3], a_bbox[7], b.centroid))
        dist /= ((a_dims[1] + a_dims[2]) / 2 + max(b_dims))
    elif a_dims[1] >= 1.4 * (a_dims[0] + a_dims[2]):
        dist = min(get_distance_from_line(a_bbox[0], a_bbox[2], b.centroid),
                   get_distance_from_line(a_bbox[1], a_bbox[3], b.centroid),
                   get_distance_from_line(a_bbox[4], a_bbox[6], b.centroid),
                   get_distance_from_line(a_bbox[5], a_bbox[7], b.centroid))
        dist /= ((a_dims[0] + a_dims[2]) / 2 + max(b_dims))
    elif a_dims[2] >= 1.4 * (a_dims[1] + a_dims[0]):
        dist = min(get_distance_from_line(a_bbox[0], a_bbox[1], b.centroid),
                   get_distance_from_line(a_bbox[2], a_bbox[3], b.centroid),
                   get_distance_from_line(a_bbox[4], a_bbox[5], b.centroid),
                   get_distance_from_line(a_bbox[6], a_bbox[7], b.centroid))
        dist /= ((a_dims[0] + a_dims[1]) / 2 + max(b_dims))
    return dist

def get_planar_distance_scaled(ent_a, ent_b):
    a_dims = ent_a.get_dimensions()
    b_dims = ent_b.get_dimensions()
    a_bbox = a.get_bbox()
    dist = 0
    if a_dims[0] <= 0.2 * a_dims[1] and a_dims[0] <= 0.2 * a_dims[2]:
        dist = min(get_distance_from_plane(b.centroid, a_bbox[0], a_bbox[1], a_bbox[2]),
                   get_distance_from_plane(b.centroid, a_bbox[4], a_bbox[5], a_bbox[6]))
        dist /= (a_dims[0] + max(b_dims))
    elif a_dims[1] <= 0.2 * a_dims[0] and a_dims[1] <= 0.2 * a_dims[2]:
        dist = min(get_distance_from_plane(b.centroid, a_bbox[0], a_bbox[1], a_bbox[4]),
                   get_distance_from_plane(b.centroid, a_bbox[2], a_bbox[3], a_bbox[5]))
        dist /= (a_dims[1] + max(b_dims))
    elif a_dims[2] <= 0.2 * a_dims[0] and a_dims[2] <= 0.2 * a_dims[1]:
        dist = min(get_distance_from_plane(b.centroid, a_bbox[0], a_bbox[2], a_bbox[4]),
                   get_distance_from_plane(b.centroid, a_bbox[1], a_bbox[3], a_bbox[5]))
        dist /= (a_dims[2] + max(b_dims))
    return dist


def closest_mesh_distance(ent_a, ent_b):
    min_dist = 10e9
    for v in ent_a.total_mesh:
        for u in ent_b.total_mesh:
            min_dist = min(min_dist, point_distance(u, v))
    return min_dist

def closest_mesh_distance_scaled(ent_a, ent_b):
    a_dims = ent_a.get_dimensions()
    b_dims = ent_b.get_dimensions()
    return closest_mesh_distance(ent_t, ent_b) / (max(a_dims) + max(b_dims) + 0.0001)

def get_bbox_intersection(ent_a, ent_b):
    span_a = ent_a.span
    span_b = ent_b.span
    x_int = 0
    y_int = 0
    z_int = 0
    if span_a[0] >= span_b[0] and span_a[1] <= span_b[1]:
        int_x = span_a[1] - span_a[0]
    elif span_b[0] >= span_a[0] and span_b[1] <= span_a[1]:
        int_x = span_b[1] - span_b[0]
    elif span_a[0] <= span_b[0] and span_a[1] >= span_b[0] and span_a[1] <= span_b[1]:
        int_x = span_a[1] - span_b[0]
    elif span_a[0] >= span_b[0] and span_a[0] <= span_b[1] and span_a[1] >= span_b[1]:
        int_x = span_b[1] - span_a[0]

    if span_a[2] >= span_b[2] and span_a[3] <= span_b[3]:
        int_y = span_a[3] - span_a[2]
    elif span_b[2] >= span_a[2] and span_b[3] <= span_a[3]:
        int_y = span_b[3] - span_b[2]
    elif span_a[2] <= span_b[2] and span_a[3] >= span_b[2] and span_a[3] <= span_b[3]:
        int_y = span_a[3] - span_b[2]
    elif span_a[2] >= span_b[2] and span_a[2] <= span_b[3] and span_a[3] >= span_b[3]:
        int_y = span_b[3] - span_a[2]

    if span_a[4] >= span_b[4] and span_a[5] <= span_b[5]:
        int_z = span_a[5] - span_a[4]
    elif span_b[4] >= span_a[4] and span_b[5] <= span_a[5]:
        int_z = span_b[5] - span_b[4]
    elif span_a[4] <= span_b[4] and span_a[5] >= span_b[4] and span_a[5] <= span_b[5]:
        int_z = span_a[5] - span_b[4]
    elif span_a[4] >= span_b[4] and span_a[4] <= span_b[5] and span_a[5] >= span_b[5]:
        int_z = span_b[5] - span_a[4]

    return int_x * int_y * int_z


def isVertical(ent_a):
    return ent_a.dims[0] < 0.5 * ent_a.dims[2] or ent_a.dims[1] < 0.5 * ent_a.dims[2]
