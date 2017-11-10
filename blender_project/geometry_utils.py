import math
import numpy

def cross_product(a, b):
    return (a[1] * b[2] - a[2] * b[1], b[0] * a[2] - b[2] * a[0], a[0] * b[1] - a[1] * b[0])

def get_normal(a, b, c):
    return cross_product((a[0] - b[0], a[1] - b[1], a[2] - b[2]), (c[0] - b[0], c[1] - b[1], c[2] - b[2]))

def get_distance_from_plane(point, a, b, c):
    normal = numpy.array(get_normal(a, b, c))
    return math.fabs((numpy.array(point).dot(normal) - numpy.array(a).dot(normal)) / numpy.linalg.norm(normal))

#distance from x3 to the line connecting x1 to x2
def get_distance_from_line(x1, x2, x3):
    t = (x3[0] - x1[0]) * (x2[0] - x1[0]) + (x3[1] - x1[1]) * (x2[1] - x1[1]) * (x3[2] - x1[2]) * (x2[2] - x1[2])
    t = t / (point_distance(x1, x2) ** 2)
    x0 = (x1[0] + (x2[0] - x1[0]) * t, x1[1] + (x2[1] - x1[1]) * t, x1[2] + (x2[2] - x1[2]) * t)
    return point_distance(x0, x3)

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
