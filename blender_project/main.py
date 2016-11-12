import bpy
import bpy_types
import numpy
import math
from math import e, pi
import itertools

filepath = "/u/gplatono/BlenderProjects/SRP/objects/"
link = False
scene = bpy.context.scene

class Entity:
    def __init__(self, main):
        self.constituents = [main]
        self.name = main.name
        self.span = self.get_span()
        self.bbox = self.get_bb()
        self.bbox_centroid = self.get_bb_centroid()
        self.faces = self.get_faces()
        queue = [main]
        while len(queue) != 0:
            par = queue[0]
            queue.pop(0)
            for ob in scene.objects:
                if ob.parent == par:
                    self.constituents.append(ob)
                    queue.append(ob)
                    
    def get_span(self):
        if(self.span is not None):
            return self.span
        else:
            return [min([obj.location.x - obj.dimensions.x / 2.0 for obj in self.constituents]),
                    max([obj.location.x + obj.dimensions.x / 2.0 for obj in self.constituents]),
                    min([obj.location.y - obj.dimensions.y / 2.0 for obj in self.constituents]),
                    max([obj.location.y + obj.dimensions.y / 2.0 for obj in self.constituents]),
                    min([obj.location.z - obj.dimensions.z / 2.0 for obj in self.constituents]),
                    max([obj.location.z + obj.dimensions.z / 2.0 for obj in self.constituents])]
                    
    def get_bbox(self):
        if(self.bbox is not None):
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

    def get_bbox_centroid(structure):
        if(self.bbox_centroid is not None):
            return self.bbox_centroid
        else:
            bbox = self.get_bbox_centroid()
            return [bbox[0][0] + (bbox[7][0] - bbox[0][0]) / 2,
                    bbox[0][1] + (bbox[7][1] - bbox[0][1]) / 2,
                    bbox[0][2] + (bbox[7][2] - bbox[0][2]) / 2]

    def get(self, property):
        return constituents[0].get(property)

    def get_faces(self):
        if(self.faces is not None):
            return self.faces
        else:
            return [ob.data.polygons for ob in self.constituents]

    def get_closest

    def print(self):
        print (self.name)

    def print_bb(self):
        print (self.bbox)

        

#with bpy.data.libraries.load(filepath + "001_table.blend", link = link) as (data_from, data_to):
#    data_to.objects = data_from.objects
#ob = None
#for obj in data_to.objects:
#    scene.objects.link(obj)
#    if obj.get('main') is not None:
#        ob = obj
def getGeometryCenter(obj):
    sumWCoord = [0,0,0]
    numbVert = 0
    if obj.type == 'MESH':
        for vert in obj.data.vertices:
            wmtx = obj.matrix_world
            worldCoord = vert.co * wmtx
            sumWCoord[0] += worldCoord[0]
            sumWCoord[1] += worldCoord[1]
            sumWCoord[2] += worldCoord[2]
            numbVert += 1
    sumWCoord[0] = sumWCoord[0]/numbVert
    sumWCoord[1] = sumWCoord[1]/numbVert
    sumWCoord[2] = sumWCoord[2]/numbVert
    return sumWCoord
	
def setOrigin(obj):
	oldLoc = obj.location
	newLoc = self.getGeometryCenter(obj)
	for vert in obj.data.vertices:
		vert.co[0] -= newLoc[0] - oldLoc[0]
		vert.co[1] -= newLoc[1] - oldLoc[1]
		vert.co[2] -= newLoc[2] - oldLoc[2]
	obj.location = newLoc

def cross_product(a, b):
    return (a[1] * b[2] - a[2] * b[1], b[0] * a[2] - b[2] * a[0], a[0] * b[1] - a[1] * b[0])

def get_normal(a, b, c):
    return cross_product((a[0] - b[0], a[1] - b[1], a[2] - b[2]), (c[0] - b[0], c[1] - b[1], c[2] - b[2]))

def get_distance_from_plane(point, a, b, c):
    normal = numpy.array(get_normal(a, b, c))
    return math.fabs((numpy.array(point).dot(normal) - numpy.array(a).dot(normal)) / numpy.linalg.norm(normal))
    
    
#bbox = [x_min, y_min, z_min, 
def get_bb(objects):
    if type(objects) is bpy_types.Object:
        objects = [objects]
    span = [min([obj.location.x - obj.dimensions.x / 2.0 for obj in objects]),
            max([obj.location.x + obj.dimensions.x / 2.0 for obj in objects]),
            min([obj.location.y - obj.dimensions.y / 2.0 for obj in objects]),
            max([obj.location.y + obj.dimensions.y / 2.0 for obj in objects]),
            min([obj.location.z - obj.dimensions.z / 2.0 for obj in objects]),
            max([obj.location.z + obj.dimensions.z / 2.0 for obj in objects])]
    return [(span[0], span[2], span[4]), 
            (span[0], span[2], span[5]), 
            (span[0], span[3], span[4]),
            (span[0], span[3], span[5]),
            (span[1], span[2], span[4]),
            (span[1], span[2], span[5]),
            (span[1], span[3], span[4]),
            (span[1], span[3], span[5])]
        
def get_bb_centroid(structure):
    bbox = get_bb(structure)
    return [bbox[0][0] + (bbox[7][0] - bbox[0][0]) / 2,
            bbox[0][1] + (bbox[7][1] - bbox[0][1]) / 2,
            bbox[0][2] + (bbox[7][2] - bbox[0][2]) / 2]

def dist_obj(a, b):
    local_dist = 1e10
    if type(a) is bpy_types.Object:
        a = [a]
    if type(b) is bpy_types.Object:
        b = [b]
    bbox_a = a.get_bbox()#get_bb(a)
    bbox_b = b.get_bbox()#get_bb(b)
    center_a = a.get_bbox_centroid()#get_bb_centroid(a)
    center_b = b.get_bbox_centroid()#get_bb_centroid(b)
    #print (a[0].name, b[0].name)    
    if a[0].get('extended') is not None:
        for ob in a:
            for face in ob.data.polygons:
                verts = [ob.matrix_world * ob.data.vertices[i].co for i in face.vertices]
                v1 = [verts[0][0], verts[0][1], verts[0][2]]
                v2 = [verts[1][0], verts[1][1], verts[1][2]]
                v3 = [verts[2][0], verts[2][1], verts[2][2]]
                local_dist = min(local_dist, get_distance_from_plane(center_b, v1, v2, v3))
        return local_dist
    if b[0].get('extended') is not None:
        for ob in b:
            for face in ob.data.polygons:
                verts = [ob.matrix_world * ob.data.vertices[i].co for i in face.vertices]
                v1 = [verts[0][0], verts[0][1], verts[0][2]]
                v2 = [verts[1][0], verts[1][1], verts[1][2]]
                v3 = [verts[2][0], verts[2][1], verts[2][2]]
                local_dist = min(local_dist, get_distance_from_plane(center_a, v1, v2, v3))
        return local_dist
    return dist_p(center_a, center_b)
    
def get_dimensions(structure):
    bbox = get_bb(structure)
    return [bbox[7][0] - bbox[0][0], bbox[7][1] - bbox[0][1], bbox[7][2] - bbox[0][2]]

def dist_p(a, b):
    return numpy.linalg.norm(numpy.array(a) - numpy.array(b))

def gaussian(x, mu, sigma):
    return e ** (- 0.5 * ((float(x) - mu) / sigma) ** 2) / (math.fabs(sigma) * math.sqrt(2.0 * pi))

def sigmoid(x, a, b, c):
    return a / (1 + b * e ** (- c * x))

def get_proj_intersection(a, b):
    bbox_a = get_bb(a)
    bbox_b = get_bb(b)
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
    #if a[0].name == 'apple1' and b[0].name == 'book1' or b[0].name == 'apple1' and a[0].name == 'book1':
    #    print ('dim1 = ', dim1, 'dim2 = ', dim2, 'area = ', area)
    
    return e ** ((area - min((axmax - axmin) * (aymax - aymin), (bxmax - bxmin) * (bymax - bymin))) / 
                    min((axmax - axmin) * (aymax - aymin), (bxmax - bxmin) * (bymax - bymin)))

def get_planar_orientation(a):
    dims = get_dimensions(a)
    if dims[0] == min(dims):
        return (1, 0, 0)
    elif dims[1] == min(dims):
        return (0, 1, 0)
    else: return (0, 0, 1)

def above(a, b):
    bbox_a = get_bb(a)
    bbox_b = get_bb(b)
    center_a = get_bb_centroid(a)
    center_b = get_bb_centroid(b)
    #if b[0].name == 'blue_cube':
    #print (a[0].name, b[0].name, sigmoid(5 * (center_a[2] - center_b[2]) / (0.01 + bbox_a[7][2] - bbox_a[0][2] + bbox_b[7][2] - bbox_b[0][2]), 1, 1, 1))
    return 0.33333 * (max(int(bbox_a[0][2] > bbox_b[7][2]), e ** (- math.fabs(bbox_a[0][2] - bbox_b[7][2]))) + sigmoid(5 * (center_a[2] - center_b[2]) / (0.01 + bbox_a[7][2] - bbox_a[0][2] + bbox_b[7][2] - bbox_b[0][2]), 1, 1, 1) + get_proj_intersection(a, b))
    
def below(a, b):
    return above(b, a)


def near(a, b):
    bbox_a = get_bb(a)
    bbox_b = get_bb(b)
    dist = dist_obj(a, b)

    #dist = dist_p(get_bb_centroid(a), get_bb_centroid(b))
    max_dim_a = max(bbox_a[7][0] - bbox_a[0][0],
                    bbox_a[7][1] - bbox_a[0][1],
                    bbox_a[7][2] - bbox_a[0][2])
    max_dim_b = max(bbox_b[7][0] - bbox_b[0][0],
                    bbox_b[7][1] - bbox_b[0][1],
                    bbox_b[7][2] - bbox_b[0][2])
    
    avg = 0
    for pair in itertools.combinations(entities, r = 2):        
        avg += dist_obj(structures[pair[0]], structures[pair[1]])
    avg = avg * 2 / (len(entities) * (len(entities) - 1))
    #print (a[0].name, b[0].name, max_dim_a + max_dim_b, dist)
    #min(max_dim_a, max_dim_b)
    #print (a[0].name, b[0].name, dist, max_dim_a, max_dim_b)
    '''numpy.sign(max_dim_b - max_dim_a) *'''
    #print (a[0].name, b[0].name, 0.5 * (1 - min(1, dist / avg) + e ** (- (0.005 * math.log(dist) / (max_dim_a + max_dim_b)))))
    return 0.5 * (1 - min(1, dist / avg) + e ** (- (0.005 * math.log(dist) / (max_dim_a + max_dim_b))))
    #gaussian(0.000001 * dist / (max_dim_a + max_dim_b), 0, 2 / math.sqrt(2*pi)) 
    #math.e ** (-dist / (max_dim_a + max_dim_b))
    
def between(a, b, c):
    center_a = get_bb_centroid(a)
    center_b = get_bb_centroid(b)
    center_c = get_bb_centroid(c)
    

def v_align(a, b):
    dim_a = get_dimensions(a)    
    dim_b = get_dimensions(b)
    center_a = get_bb_centroid(a)
    center_b = get_bb_centroid(b)
    return gaussian(0.9 * dist_p((center_a[0], center_a[1], 0), (center_b[0], center_b[1], 0)) / 
                                (max(dim_a[0], dim_a[1]) + max(dim_b[0], dim_b[1])), 0, 1 / math.sqrt(2*pi))
 
def v_offset(a, b):
    dim_a = get_dimensions(a)    
    dim_b = get_dimensions(b)
    center_a = get_bb_centroid(a)
    center_b = get_bb_centroid(b)
    #z_dist = center_a[2] - center_b[2]
    h_dist = math.sqrt((center_a[0] - center_b[0]) ** 2 + (center_a[1] - center_b[1]) ** 2)    
    return gaussian(2 * (center_a[2] - center_b[2] - 0.5*(dim_a[2] + dim_b[2])) / (1e-6 + dim_a[2] + dim_b[2]), 0, 1 / math.sqrt(2*pi))

def show_bbox(structure):
    mesh = bpy.data.meshes.new(structure[0].name + '_mesh')
    obj = bpy.data.objects.new(structure[0].name + '_bbox', mesh)
    bpy.context.scene.objects.link(obj)
    bpy.context.scene.objects.active = obj
    bbox = get_bb(structure)
    mesh.from_pydata(bbox, [], [(0, 1, 3, 2), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5), (4, 5, 7, 6)])
    mesh.update()
    
    
entities = []
structures = {}
for obj in scene.objects:
    if obj.get('main') is not None:
        entities.append(obj)
        list = [obj]
        queue = [obj]
        while len(queue) != 0:
            par = queue[0]
            queue.pop(0)
            for ob in scene.objects:
                if ob.parent == par:
                    list.append(ob)
                    queue.append(ob)
        structures[obj] = list

def larger_than(a, b):
    bbox_a = get_bb(a)
    bbox_b = get_bb(b)
    return 1 / (1 + e ** (bbox_b[7][0] - bbox_b[0][0] + bbox_b[7][1] - bbox_b[0][1] + bbox_b[7][2] - bbox_b[0][2] - (bbox_a[7][0] - bbox_a[0][0] + bbox_a[7][1] - bbox_a[0][1] + bbox_a[7][2] - bbox_a[0][2])))
    #return 1 / (1 + e ** ((bbox_b[7][0] - bbox_b[0][0]) * (bbox_b[7][1] - bbox_b[0][1]) * (bbox_b[7][2] - bbox_b[0][2]) - (bbox_a[7][0] - bbox_a[0][0]) * (bbox_a[7][1] - bbox_a[0][1]) * (bbox_a[7][2] - bbox_a[0][2])))

def on(a, b):
    #print (a[0].name, b[0].name, get_proj_intersection(a, b))
    ret_val = 0.5 * (v_offset(a, b) + get_proj_intersection(a, b))
    for ob in b:
        if ob.get('working_surface') is not None or ob.get('planar') is not None:
            #orient_vector = get_planar_orientation(ob)
            #if orient_vector == (1, 0, 0) or orient_vector == (0, 1, 0):                           
            ret_val = max(ret_val, 0.5 * (v_offset(a, ob) + get_proj_intersection(a, ob)))
            ret_val = max(ret_val, 0.5 * (int(near(a, ob) > 0.99) + larger_than(ob, a)))         
    if ret_val >= 0.6:
        return 0.5 * (ret_val + larger_than(b, a))
    return ret_val

def over(a, b):
    bbox_a = get_bb(a)
    bbox_b = get_bb(b)
    return 0.5 * above(a, b) + 0.2 * get_proj_intersection(a, b) + 0.3 * near(a, b)

#print (entities)  
#for ob in entities:
#    show_bbox(structures[ob])
def compute_at(entities, structures):
    obj = [
    [x, 
    [y for y in entities if x != y and near(structures[y], structures[x]) > 0.8]]
     for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is at the " + x[0].name for x in obj if x[1] != [])

def compute_near(entities, structures):
    obj = [
    [x, 
    [y for y in entities if x != y and near(structures[y], structures[x]) > 0.6]]
     for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is near the " + x[0].name for x in obj if x[1] != [])

def compute_on(entities, structures):
    obj = [
    [x, 
    [y for y in entities if x != y and on(structures[y], structures[x]) > 0.8]]
     for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is on the " + x[0].name for x in obj if x[1] != [])

def compute_above(entities, structures):
    obj = [
    [x, 
    [y for y in entities if x != y and above(structures[y], structures[x]) > 0.7]]
     for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is above the " + x[0].name for x in obj if x[1] != [])

def compute_below(entities, structures):
    obj = [
    [x, 
    [y for y in entities if x != y and below(structures[y], structures[x]) > 0.7]]
     for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is above the " + x[0].name for x in obj if x[1] != [])


def compute_over(entities, structures):
    obj = [
    [x, 
    [y for y in entities if x != y and over(structures[y], structures[x]) > 0.7]]
     for x in entities]
    return "\n".join(", ".join(y.name for y in x[1]) + " is over the " + x[0].name for x in obj if x[1] != [])

#print ('init...')
print ('')
print (compute_at(entities, structures))
print ('')
print (compute_on(entities, structures))
print ('')
print (compute_above(entities, structures))
x = Entity(entities[0])
