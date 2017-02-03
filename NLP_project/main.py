import bpy
import bpy_types
import numpy
import math
import requests
import json
import xml.etree.ElementTree as ET
import re
import sys
from math import e, pi
import itertools
from subprocess import call
import os
filepath = os.path.dirname(os.path.abspath(__file__)) + "/"

scene = bpy.context.scene

COLORS = ['BLACK', 'GRAY', 'GREEN', 'RED', 'PINK', 'BROWN', 'YELLOW', 'ORANGE', 'BLUE', 'SKYBLUE', 'PURPLE', 'CYAN']

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

    def get_closest_face_distance(point):
        return min([get_distance_from_plane(point, face[0], face[1], face[2]) for face in self.faces])

    def get_faces(self):
        if(hasattr(self, 'faces') and self.faces is not None):
            return self.faces
        else:
            faces = []
            for ob in self.constituents:
                if ob.data is None:
                    continue
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

class Relation:
    def __init__(self, rel_type, figure, ground):
        self.rel_type = rel_type
        self.figure = figure
        self.ground = ground
        
    def printinfo(self):
        print ('TYPE: ' + str(self.rel_type))
        print ('FIGURE: ' + str([fig.name for fig in self.figure if fig is not None]))
        print ('GROUND: ' + str([gr.name for gr in self.ground if gr is not None]))
        

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

def sigmoid(x, a, b, c):
    return a / (1 + b * e ** (- c * x))

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

def ABOVE(a, b):
    bbox_a = a.get_bbox()
    bbox_b = b.get_bbox()
    center_a = a.get_bbox_centroid()
    center_b = b.get_bbox_centroid()
    return 0.33333 * (max(int(bbox_a[0][2] > bbox_b[7][2]), e ** (- math.fabs(bbox_a[0][2] - bbox_b[7][2]))) + sigmoid(5 * (center_a[2] - center_b[2]) / (0.01 + bbox_a[7][2] - bbox_a[0][2] + bbox_b[7][2] - bbox_b[0][2]), 1, 1, 1) + get_proj_intersection(a, b))
    
def BELOW(a, b):
    return ABOVE(b, a)

def NEAR(a, b):
    bbox_a = a.get_bbox()
    bbox_b = b.get_bbox()
    dist = dist_obj(a, b)
    if dist <= 0:
        return 0
    max_dim_a = max(bbox_a[7][0] - bbox_a[0][0],
                    bbox_a[7][1] - bbox_a[0][1],
                    bbox_a[7][2] - bbox_a[0][2])
    max_dim_b = max(bbox_b[7][0] - bbox_b[0][0],
                    bbox_b[7][1] - bbox_b[0][1],
                    bbox_b[7][2] - bbox_b[0][2])
    return 0.5 * (1 - min(1, 0.5 * dist / avg_dist) + e ** (- (0.005 * math.log(dist) / (0.001 + max_dim_a + max_dim_b))))
    
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

def ON(a, b):
    ret_val = 0.5 * (v_offset(a, b) + get_proj_intersection(a, b))
    return ret_val

def closer_than(a, b, pivot):
    return 1 if point_distance(a.get_bbox(), pivot.get_bbox()) < point_distance(b.get_bbox(), pivot.get_bbox()) else 0

def in_front_of_extr(a, b, observer):
    bbox_a = a.get_bbox()
    max_dim_a = max(bbox_a[7][0] - bbox_a[0][0],
                    bbox_a[7][1] - bbox_a[0][1],
                    bbox_a[7][2] - bbox_a[0][2]) + 0.0001
    dist = get_distance_from_line(observer.get_bbox_centroid(), b.get_bbox_centroid(), a.get_bbox_centroid())
    return 0.5 * (closer_than(a, b, observer) + e ** (-dist / max_dim_a))
    
#Parses the frames.xml and builds the list of frames representations
def build_frames(filename):
        frame_trees = ET.parse(filename).getroot().findall('frame')
        frames = []
        for frame_tree in frame_trees:
                frames.append([frame_tree.get('name')])
                for field in frame_tree.findall('field'):
                        frames[-1].append([field.get('name'),
                                           field.get('action'),                                           
                                           [[y.strip().upper() for y in x.split()] for x in field.get('pattern').split('|')],
                                           int(field.get('weight'))])
        return frames

#Extract the logical form from the output of the TRIPS parser
def get_lf(rdf):
    lf = {}
    for node in rdf.findall('rdf:Description', NS):
        dict = {}
        dict['id'] = '#' + node.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}ID')
        dict['indicator'] = node.find('LF:indicator', NS).text
        dict['type'] = node.find('LF:type', NS).text
        if node.find('LF:word', NS) is not None:
            dict['word'] = node.find('LF:word', NS).text
        dict['start'] = node.find('LF:start', NS).text
        roles = []
        for child in node.getchildren():
            if child.tag.startswith('{http://www.cs.rochester.edu/research/trips/role#}'):
                rolename = child.tag.split('}')[1]
                roleref = child.text if child.text is not None else child.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', NS)
                roles.append((rolename, roleref))
        dict['roles'] = roles
        lf[dict['id']] = dict
    return lf

#For a figure or ground of the relation, get the textual description, such as adjectives, etc.
def get_arg_form(lf, rdf_id):
        arg = [rdf_id]
        for key in lf.keys():
                if lf[key]['id'] == rdf_id:
                        for role in lf[key]['roles']:
                                if role[0] == 'MOD' or role[0] == 'ASSOC-WITH' or role[0] == 'FIGURE':
                                        arg.append(resolve_reference(role[1]))
        return arg

#DUMMY: resolve reference tokens (such as pronouns, "one", etc.)
def resolve_reference(rdf_id):
        return rdf_id

#Generate the relation object with figure and ground from logical form
def get_relation(key):
    for frame in frames:
        for field in frame[1:]:
            for pattern in field[2]:
                if lf[key]['type'] == pattern[0]:
                    relation = Relation(None, None, None)
                    relation.rel_type = field[1]
                    for role in lf[key]['roles']:
                        if role[0] == 'FIGURE':
                            relation.figure = [get_entity([lf[token]['word'] for token in get_arg_form(lf, role[1]) if 'word' in lf[token].keys()])]                           
                        elif role[0] == 'GROUND':
                            relation.ground = [get_entity([lf[token]['word'] for token in get_arg_form(lf, role[1]) if 'word' in lf[token].keys()])]
                    return relation

#Generate a structured format of the given query
def get_formal_query(lf):
        query = []
        query_type = 'ID'
        for key in lf.keys():
                if lf[key]['type'] == 'SA_WH-QUESTION':
                    query_type = 'ID'
                elif lf[key]['type'] == 'SA_YN-QUESTION':
                    query_type = 'CONFIRM'
        query = [query_type]
        for key in lf.keys():
            relation = get_relation(key)
            if relation is not None:
                query.append(relation)
                '''if relation.figure[0] is None:
                    relation.figure = []
                    for entity in entities:
                        relation.figure.append(entity)
                if relation.ground[0] is None:
                    relation.ground = []
                    for entity in entities:
                        relation.ground.append(entity)
                for figure in relation.figure:
                    for ground in relation.ground:
                        query.append(Relation(relation[0], [figure], [ground])'''

        #ret_query = query[0]
        #for relation in query[1:]:
            #if relation.figure[0] == None:
            #    for 
            #    relation.figure[0] = 'X'
            #elif relation.ground[0] == None:
            #    relation.ground[0] = 'X'
            #else:
            #    ret_query.append(relation)
        return query

#Determine the entity by its textual description
def get_entity(textual_description):
    for entity in entities:
        if entity.get("COLOR") in textual_description:
            return entity

#Get the list of entities acceptable as the figure argument for the given relation
def figure_list(relation):
    figures = []
    for ground in relation.ground:
        for entity in entities:
            if globals()[relation.rel_type](entity, ground) > 0.7:
                figures.append(entity)
    return figures

#Get the list of entities acceptable as the ground argument for the given relation
def ground_list(relation):
    grounds = []
    for figure in relation.figure:
        for entity in entities:
            if globals()[relation.rel_type](figure, entity) > 0.7:
                grounds.append(entity)
    return grounds

#Given a formal query, evaluate it and generate the system response
def process_query(query):
    result = []
    if(query[0] == 'CONFIRM'):
        result = True
        for relation in query[1:]:
            if relation.figure[0] is None or relation.ground[0] is None:
                print ('ERROR: Figure or ground is not fully specified or has not been parsed properly.')
                return
            if globals()[relation.rel_type](relation.figure[0], relation.ground[0]) < 0.7:
                result = False
                break
        print ('RESULT:')
        if result == True:
            print ("YES")
        else:
            print ("NO")
    else:
        result = [ent for ent in entities if ent.name != 'plane']
        for relation in query[1:]:
            if len(relation.figure) == 0 or relation.figure[0] is None:
                result = [entity for entity in figure_list(relation) if entity in result]
            elif len(relation.ground) == 0 or relation.ground[0] is None:
                result = [entity for entity in ground_list(relation) if entity in result]
        print ('RESULT:')
        if len(result) == 0:
            print ('ERROR: No object satisfies given constraints.')
        else:
            for x in result:
                print ('THE' + " " + x.get('COLOR') + " " + x.get('TYPE'))

#List of objects in the scene
entities = []

parse_tree = []
NS = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
      'role': 'http://www.cs.rochester.edu/research/trips/role#',
      'LF': 'http://www.cs.rochester.edu/research/trips/LF#'}

for obj in scene.objects:
    if obj.get('main') is not None:
        entities.append(Entity(obj))
avg_dist = 0
for pair in itertools.combinations(entities, r = 2):
    avg_dist += dist_obj(pair[0], pair[1])
avg_dist = avg_dist * 2 / ((len(entities)-1) * (len(entities) - 2))

frames = build_frames(filepath + "frames.xml")
tests = [line for line in open(filepath + "tests", "r").readlines()]

for test in tests:
    print ('=======================================================================\n')    
    print ('QUERY: ' + test)
    print ("PROCESSING...")
    query_parse = requests.get("http://trips.ihmc.us/parser/cgi/parse?input=" + test)
    root = ET.fromstring(query_parse.text)
    lf = get_lf(root.find('utt').find('terms').find('rdf:RDF', NS))
    
    #for key in lf.keys():
    #    print (lf[key], '\n')
    query = get_formal_query(lf)
    #print (query[1].printinfo())
    process_query(query)
