import bpy
import bpy_types
import numpy
import math
from math import e, pi
import itertools
import os

filepath = os.path.dirname(os.path.abspath(__file__))
filepath = filepath[0:filepath.rfind("/") + 1]


#filepath = "/u/gplatono/BlenderProjects/SRP/objects/"
#import geometry_utils
link = False
scene = bpy.context.scene

class Entity:
    def __init__(self, main):
        self.constituents = [main]
        self.name = main.name
        self.span = self.get_span()
        self.bbox = self.get_bbox()
        self.bbox_centroid = self.get_bbox_centroid()
        self.dimensions = self.get_dimensions()
        self.faces = self.get_faces()
        self.longitudinal = []
        self.frontal = []
        queue = [main]
        while len(queue) != 0:
            par = queue[0]
            queue.pop(0)
            for ob in scene.objects:
                if ob.parent == par:
                    self.constituents.append(ob)
                    queue.append(ob)

    def set_longitudinal(self, direction):
        self.longitudinal = direction

    def set_frontal(self, direction):
        self.frontal = direction        
                    
    def get_span(self):
        if(hasattr(self, 'span') and self.span is not None):
            return self.span
        else:
            return [min([obj.location.x - obj.dimensions.x / 2.0 for obj in self.constituents]),
                    max([obj.location.x + obj.dimensions.x / 2.0 for obj in self.constituents]),
                    min([obj.location.y - obj.dimensions.y / 2.0 for obj in self.constituents]),
                    max([obj.location.y + obj.dimensions.y / 2.0 for obj in self.constituents]),
                    min([obj.location.z - obj.dimensions.z / 2.0 for obj in self.constituents]),
                    max([obj.location.z + obj.dimensions.z / 2.0 for obj in self.constituents])]
                    
    def get_bbox(self):
        if(hasattr(self, 'bbox') and self.bbox is not None):
            return self.bbox
        else:
            span = self.get_span()
            return [(span[0], span[2], span[4]),
                    (span[0], span[2], span[5]),
		    (span[0], span[3], span[4]),
		    (span[0], span[3], span[5]),
		    (span[1], span[2], span[4]),
		    (span[1], span[2], span[5]),
		    (span[1], span[3], span[4]),
		    (span[1], span[3], span[5])]

    def get_bbox_centroid(self):
        if(hasattr(self, 'bbox_centroid') and self.bbox_centroid is not None):
            return self.bbox_centroid
        else:
            bbox = self.get_bbox()
            return [bbox[0][0] + (bbox[7][0] - bbox[0][0]) / 2,
                    bbox[0][1] + (bbox[7][1] - bbox[0][1]) / 2,
                    bbox[0][2] + (bbox[7][2] - bbox[0][2]) / 2]

    def get_dimensions(self):
        if(hasattr(self, 'dimensions') and self.dimensions is not None):
            return self.dimensions
        else:
            bbox = self.get_bbox()
            return [bbox[7][0] - bbox[0][0], bbox[7][1] - bbox[0][1], bbox[7][2] - bbox[0][2]]

    def get(self, property):
        return self.constituents[0].get(property)

    def get_closest_face_distance(self, point):
        return min([get_distance_from_plane(point, face[0], face[1], face[2]) for face in self.faces])

    def get_faces(self):
        if(hasattr(self, 'faces') and self.faces is not None):
            return self.faces
        else:
            faces = []
            for ob in self.constituents:
                for face in ob.data.polygons:
                    faces.append([ob.matrix_world * ob.data.vertices[i].co for i in face.vertices])
            return faces

    def print(self):
        print (self.name)

    def show_bbox():
        mesh = bpy.data.meshes.new(self.name + '_mesh')
        obj = bpy.data.objects.new(self.name + '_bbox', mesh)
        bpy.context.scene.objects.link(obj)
        bpy.context.scene.objects.active = obj
        bbox = self.get_bbox()
        mesh.from_pydata(bbox, [], [(0, 1, 3, 2), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5), (4, 5, 7, 6)])
        mesh.update()

#with bpy.data.libraries.load(filepath + "001_table.blend", link = link) as (data_from, data_to):
#    data_to.objects = data_from.objects
#ob = None
#for obj in data_to.objects:
#    scene.objects.link(obj)
#    if obj.get('main') is not None:
#        ob = obj
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

def dist_obj(a, b):
    if type(a) is not Entity or type(b) is not Entity:
        return -1
    bbox_a = a.get_bbox()
    bbox_b = b.get_bbox()
    center_a = a.get_bbox_centroid()
    center_b = b.get_bbox_centroid()
    if a.get('extended') is not None:
        return a.get_closest_face_distance(center_b)
    if b.get('extended') is not None:
        return b.get_closest_face_distance(center_a)
    return point_distance(center_a, center_b)

def gaussian(x, mu, sigma):
    return e ** (- 0.5 * ((float(x) - mu) / sigma) ** 2) / (math.fabs(sigma) * math.sqrt(2.0 * pi))

def sigmoid(x, a, b):
    return a / (1 + e ** (- b * x)) if b * x > -100 else 0

def get_proj_intersection(a, b):
    bbox_a = a.get_bbox()
    bbox_b = b.get_bbox()
    axmin = bbox_a[0][0]
    axmax = bbox_a[7][0]
    aymin = bbox_a[0][1]
    aymax = bbox_a[7][1]
    bxmin = bbox_b[0][0]
    bxmax = bbox_b[7][0]
    bymin = bbox_b[0][1]
    bymax = bbox_b[7][1]
    dim1 = max(axmax, bxmax) - min(axmin, bxmin) - (axmax - axmin + bxmax - bxmin)
    dim2 = max(aymax, bymax) - min(aymin, bymin) - (aymax - aymin + bymax - bymin)
    area = math.fabs(dim1 * dim2)
    if dim1 >= 0 or dim2 >= 0:
        area = -area
    return e ** ((area - min((axmax - axmin) * (aymax - aymin), (bxmax - bxmin) * (bymax - bymin))) / 
                    min((axmax - axmin) * (aymax - aymin), (bxmax - bxmin) * (bymax - bymin)))

def get_planar_orientation(a):
    dims = a.get_dimensions()
    if dims[0] == min(dims):
        return (1, 0, 0)
    elif dims[1] == min(dims):
        return (0, 1, 0)
    else: return (0, 0, 1)

def above(a, b):
    bbox_a = a.get_bbox()
    bbox_b = b.get_bbox()
    center_a = a.get_bbox_centroid()
    center_b = b.get_bbox_centroid()
    return 0.33333 * (max(int(bbox_a[0][2] > bbox_b[7][2]), e ** (- math.fabs(bbox_a[0][2] - bbox_b[7][2]))) + sigmoid(5 * (center_a[2] - center_b[2]) / (0.01 + bbox_a[7][2] - bbox_a[0][2] + bbox_b[7][2] - bbox_b[0][2]), 1, 1) + get_proj_intersection(a, b))
    
def below(a, b):
    return above(b, a)

def near(a, b):
    bbox_a = a.get_bbox()
    bbox_b = b.get_bbox()
    dist = dist_obj(a, b)
    max_dim_a = max(bbox_a[7][0] - bbox_a[0][0],
                    bbox_a[7][1] - bbox_a[0][1],
                    bbox_a[7][2] - bbox_a[0][2])
    max_dim_b = max(bbox_b[7][0] - bbox_b[0][0],
                    bbox_b[7][1] - bbox_b[0][1],
                    bbox_b[7][2] - bbox_b[0][2])   
    return 0.5 * (1 - min(1, dist / avg_dist) + e ** (- (0.005 * math.log(dist) / (max_dim_a + max_dim_b))))

#determines whether a is between b and c
def between(a, b, c):
    bbox_a = a.get_bbox()
    bbox_b = a.get_bbox()
    bbox_c = c.get_bbox()
    center_a = a.get_bbox_centroid()
    center_b = b.get_bbox_centroid()
    center_c = c.get_bbox_centroid()
    dist = get_distance_from_line(center_b, center_c, center_a)
    max_dim_a = max(bbox_a[7][0] - bbox_a[0][0],
                    bbox_a[7][1] - bbox_a[0][1],
                    bbox_a[7][2] - bbox_a[0][2])
    return 1
    
    
def v_align(a, b):
    dim_a = a.get_dimensions()
    dim_b = b.get_dimensions()
    center_a = a.get_bbox_centroid()
    center_b = b.get_bbox_centroid()
    return gaussian(0.9 * point_distance((center_a[0], center_a[1], 0), (center_b[0], center_b[1], 0)) / 
                                (max(dim_a[0], dim_a[1]) + max(dim_b[0], dim_b[1])), 0, 1 / math.sqrt(2*pi))
 
def v_offset(a, b):
    dim_a = a.get_dimensions()    
    dim_b = b.get_dimensions()
    center_a = a.get_bbox_centroid()
    center_b = b.get_bbox_centroid()
    h_dist = math.sqrt((center_a[0] - center_b[0]) ** 2 + (center_a[1] - center_b[1]) ** 2)    
    return gaussian(2 * (center_a[2] - center_b[2] - 0.5*(dim_a[2] + dim_b[2])) / (1e-6 + dim_a[2] + dim_b[2]), 0, 1 / math.sqrt(2*pi))

def larger_than(a, b):
    bbox_a = a.get_bbox()
    bbox_b = b.get_bbox()
    return 1 / (1 + e ** (bbox_b[7][0] - bbox_b[0][0] + bbox_b[7][1] - bbox_b[0][1] + bbox_b[7][2] - bbox_b[0][2] - (bbox_a[7][0] - bbox_a[0][0] + bbox_a[7][1] - bbox_a[0][1] + bbox_a[7][2] - bbox_a[0][2])))

def on(a, b):
    ret_val = 0.5 * (v_offset(a, b) + get_proj_intersection(a, b))
    #for ob in b:
    #    if ob.get('working_surface') is not None or ob.get('planar') is not None:
    #        ret_val = max(ret_val, 0.5 * (v_offset(a, ob) + get_proj_intersection(a, ob)))
    #        ret_val = max(ret_val, 0.5 * (int(near(a, ob) > 0.99) + larger_than(ob, a)))         
    if ret_val >= 0.6:
        return 0.5 * (ret_val + larger_than(b, a))
    return ret_val

def over(a, b):
    bbox_a = a.get_bbox()
    bbox_b = b.get_bbox()
    return 0.5 * above(a, b) + 0.2 * get_proj_intersection(a, b) + 0.3 * near(a, b)

def closer_than(a, b, pivot):
    return 1 if point_distance(a.get_bbox(), pivot.get_bbox()) < point_distance(b.get_bbox(), pivot.get_bbox()) else 0

def in_front_of_extr(a, b, observer):
    bbox_a = a.get_bbox()
    max_dim_a = max(bbox_a[7][0] - bbox_a[0][0],
                    bbox_a[7][1] - bbox_a[0][1],
                    bbox_a[7][2] - bbox_a[0][2]) + 0.0001
    dist = get_distance_from_line(observer.get_bbox_centroid(), b.get_bbox_centroid(), a.get_bbox_centroid())
    return 0.5 * (closer_than(a, b, observer) + e ** (-dist / max_dim_a))
    
relations = {}

def compute_at(entities):
    obj = [[x, [y for y in entities if x != y and near(y, x) > 0.8]] for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is at the " + x[0].name for x in obj if x[1] != [])

def compute_near(entities):
    obj = [[x, [y for y in entities if x != y and near(y, x) > 0.6]] for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is near the " + x[0].name for x in obj if x[1] != [])

def compute_on(entities):
    obj = [[x, [y for y in entities if x != y and on(y, x) > 0.8]] for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is on the " + x[0].name for x in obj if x[1] != [])

def compute_above(entities):
    obj = [[x, [y for y in entities if x != y and above(y, x) > 0.7]] for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is above the " + x[0].name for x in obj if x[1] != [])

def compute_below(entities):
    obj = [[x, [y for y in entities if x != y and below(y, x) > 0.7]] for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is below the " + x[0].name for x in obj if x[1] != [])

def compute_over(entities):
    obj = [[x, [y for y in entities if x != y and over(y, x) > 0.7]] for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is over the " + x[0].name for x in obj if x[1] != [])

def gen_data(func_name):
    pos = 100.0
    neg = 100.0
    data = open(func_name + ".train", "w")
    index = 0
    for pair in itertools.permutations(entities, r = 2):
        if index < 1000:
            a, b = pair
            if a.name != 'plane' and b.name != 'plane':
                a_bbox_str = " ".join([" ".join([str(x) for x in y]) for y in a.get_bbox()])
                b_bbox_str = " ".join([" ".join([str(x) for x in y]) for y in b.get_bbox()])
                a_cen = a.get_bbox_centroid()
                b_cen = b.get_bbox_centroid()
                outstr = a_bbox_str + " " + b_bbox_str #" ".join([str(x) for x in a_cen]) + " " + " ".join([str(x) for x in b_cen])            
                if globals()[func_name](a, b) > 0.7: # and float(pos) / (pos + neg) <= 0.6:
                    outstr = outstr + " 1\n"
                    #pos = pos + 1
                    data.write(outstr)
                else: #if neg / (pos + neg) <= 0.6:
                    outstr = outstr + " -1\n"
                    #neg = neg + 1
                    data.write(outstr)
                index = index + 1
    data.close()
    
entities = []
for obj in scene.objects:
    if obj.get('main') is not None:
        entities.append(Entity(obj))
if len(entities) != 0 :
    avg_dist = 0
    for pair in itertools.combinations(entities, r = 2):
        avg_dist += dist_obj(pair[0], pair[1])
    avg_dist = avg_dist * 2 / (len(entities) * (len(entities) - 1))
#scene.objects.link(bpy.data.objects.new('Observer', None))
#scene.objects['Observer'].location = (0, -20, 5)
#scene.update()
#observer = Entity(scene.objects['Observer'])
#observer.set_frontal((0, 0, 0) - (0, -20, 5))
#observer.set_longitudinal((0, 1, 4))        

#gen_data("above")
#gen_data("near")
#gen_data("on")

def add_props():
    lamp = bpy.data.lamps.new("Lamp", type = 'POINT')
    lamp.energy = 30
    cam = bpy.data.cameras.new("Camera")

    lamp_obj = bpy.data.objects.new("Lamp", lamp)
    cam_ob = bpy.data.objects.new("Camera", cam)

    lamp_obj.location = (-20, 0, 10)
    cam_ob.location = (-20, 0, 10)
    cam_ob.rotation_mode = 'XYZ'
    cam_ob.rotation_euler = (1.1, 0, -1.57)
    bpy.data.cameras['Camera'].lens = 20
    
    scene.objects.link(lamp_obj)
    scene.objects.link(cam_ob)    

    bpy.context.scene.camera = scene.objects["Camera"]
    scene.update()

add_props()
scene.render.filepath = filepath + 'image.jpg'
bpy.ops.render.render( write_still=True )

print ('')
print (compute_above(entities))
'''
print ('init...')
print ('')
print (compute_at(entities))
print ('')
print (compute_near(entities))
print ('')
print (compute_over(entities))
#print ('')
#print (compute_on(entities))
print ('')
print (compute_above(entities))
print ('')
print (compute_below(entities))
'''
