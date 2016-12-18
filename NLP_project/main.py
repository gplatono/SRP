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

#    def get_closest_distance(point):
        

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
    
entities = []
for obj in scene.objects:
    if obj.get('main') is not None:
        entities.append(Entity(obj))
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

parse_tree = []
NS = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
      'role': 'http://www.cs.rochester.edu/research/trips/role#',
      'LF': 'http://www.cs.rochester.edu/research/trips/LF#'}

#stores the ontology entries in the format ontology[concept] = [concept, [parents], [related concepts (W:: stuff)]]
#note that ontology contains both concepts and words (ONT::'s and W::'s), for words the '[related concepts]'-list is empty
ontology = {}

#for each entry in ontology (all ONT::'s and W::'s) stores the list of all ancestors
#for words it is concepts to which they are related and their ancestors
supertypes = {}

#recursively obtains the list of ancestors of the given ontology entry and assigns it to supertypes[entry]
def add_supertypes(concept, ontology, supertypes):
        #get all parents
        ancestors = ontology[concept][1]

        #get parents of parents and so on, recursively
        for parent in ontology[concept][1]:
                if(parent not in supertypes.keys()):
                        supertypes = add_supertypes(parent, ontology, supertypes)
                ancestors = ancestors + supertypes[parent]

        #remove duplicates and assign the ontology entry
        supertypes[concept] = list(set(ancestors))
        
        return supertypes

#parses the TRIPS ontology file and builds custom ontology and supertypes dictionaries
def build_ontology(filename):
        onto_concepts = {}
        onto_words = {}
        onto_all = {}
        supertypes = {}

        #get the entries for 'ONT::' nodes and fill in the concept ontology
        for concept in ET.parse(filename).getroot().findall('concept'):
                onto_concepts[concept.get('name').strip().upper()] = [concept.get('name').strip().upper(),
                                             [parent.text.strip().upper() for parent in concept.findall("relation[@label='inherit']")],
                                             [word.text.strip().upper() for word in concept.findall("relation[@label='word']")]]
                
        #for each 'ONT::' concept, extract all related words ('W::') and fill in the ontology for words
        for concept in onto_concepts.keys():
                for related in onto_concepts[concept][2]:
                        if(related not in onto_words.keys()):
                                onto_words[related] = [related, [concept], []]
                        else: onto_words[related][1].append(concept)
                        
        #merge them together to get a unified ontology
        onto_all = {**onto_concepts, **onto_words}

        #form the supertype ontology
        for concept in onto_all.keys():
                if concept not in supertypes.keys():
                        supertypes = add_supertypes(concept, onto_all, supertypes)
                        
        return (onto_all, supertypes)

#parses the frames.xml and builds the list of frames representations
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

def get_arg_form(lf, rdf_id):
        arg = [rdf_id]
        for key in lf.keys():
                if lf[key]['id'] == rdf_id:
                        for role in lf[key]['roles']:
                                if role[0] == 'MOD':
                                        arg.append(resolve_reference(role[1]))
        return arg

def resolve_reference(rdf_id):
        return rdf_id

def get_formal_query(lf):
        query = []
        relations = []
        global frames        
        isYN = False
        for key in lf.keys():
                if lf[key]['indicator'] == 'SPEECHACT' and ('PUNCTYPE', 'YNQ') in lf[key]['roles']:
                        isYN = True
        for key in lf.keys():
                for frame in frames:
                        if lf[key]['type'] == frame[0]:
                                relations.append([frame[0]])                                
                                for role in lf[key]['roles']:
                                        if role[0] == 'FIGURE' or role[0] == 'GROUND':
                                                relations[-1].append([role[0]] + get_arg_form(lf, role[1]))
        query = []
        for relation in relations:
                query.append([relation[0]])
                for arg in relation[1:]:
                        new_arg = [arg[0]]
                        for token in arg[1:]:
                                new_arg.append(lf[token]['word'])
                        query[-1].append(new_arg)
        return query

def get_arg_entity(arg):
    results = []
    for entity in entities:
        if len(arg) >= 3 and entity.get("TYPE") == arg[1] and entity.get("COLOR") == arg[2]:
            results.append(entity)
    return results

def figure_list(relation, grounds):
    figures = []
    for ground in grounds:
        for entity in entities:
            if globals()[relation](entity, ground) > 0.7:
                figures.append(entity)
    return figures

def ground_list(relation, figures):
    grounds = []
    for figure in figures:
        for entity in entities:
            if globals()[relation](figure, entity) > 0.7:
                grounds.append(entity)
    return grounds

def get_relation_arguments(relation):
    rel_type = relation[0]
    figures = []
    grounds = []
    for arg in relation[1:]:
        if arg[0] == 'FIGURE':
            figures = get_arg_entity(arg)
        elif arg[0] == 'GROUND':
            grounds = get_arg_entity(arg)
    if figures == []:
        figures = figure_list(rel_type, grounds)
    elif grounds == []:
        grounds = ground_list(rel_type, figures)
    return (figures, grounds)

def generate_response(relations):
    print (relations)
    response = relations[0][0][0].get("COLOR") + " " + relations[0][0][0].get("TYPE")
    for entity in relations[0][0][1:]:
        response = response + ", " +  entity.get("COLOR") + " " + entity.get("TYPE")
    if len(relations[0][0]) == 1:
        response = response + " is "
    else:
        response = response + " are "
    response = response + relations[0][1][0]    
    response = response + relations[0][1][1].get("COLOR") + " " + relations[0][1][1].get("TYPE")
    for entity in relations[0][1][2:]:
        response = response + ", " +  entity.get("COLOR") + " " + entity.get("TYPE")
    return response
    
def process_query(query):
    infix_relations = []
    figures = []
    grounds = []
    for relation in query:
        figures, grounds = get_relation_arguments(relation)
        print (figures[0].name, grounds[0].name)
    infix_relations.append(figures)
    infix_relations.append(query[0][0])
    infix_relations.append(grounds)   
   # return generate_response(infix_relations)
    
ontology, supertypes = build_ontology(filepath + "trips-ont-lex.xml")
frames = build_frames(filepath + "frames.xml")
tests = [line for line in open(filepath + "tests", "r").readlines()]
result = requests.get("http://trips.ihmc.us/parser/cgi/parse?input=" + tests[1])
root = ET.fromstring(result.text)
lf = get_lf(root.find('utt').find('terms').find('rdf:RDF', NS))

for key in lf.keys():
    print (lf[key], '\n')   

query = get_formal_query(lf)

print (query)

print (process_query(query))
