import bpy
import bpy_types
import bpy_extras
import numpy
import math
from math import e, pi
import itertools
import os
import sys
import random

filepath = os.path.dirname(os.path.abspath(__file__)) + "/"
print (filepath)
sys.path.insert(0, filepath)
#filepath = filepath[0:filepath.rfind("/") + 1]

from entity import Entity
from geometry_utils import *
from parser import *

#filepath = "/u/gplatono/BlenderProjects/SRP/objects/"
#import geometry_utils
link = False
scene = bpy.context.scene

relation_list = ['near', 'in', 'on' , 'touching', 'front', 'behind', 'right', 'left', 'at', 'over', 'under', 'above', 'below', 'between']
color_mods = ['black', 'red', 'blue', 'brown', 'green', 'yellow', 'north', 'west', 'east']
types = []

rf_mapping = {'near': 'near', 'on': 'on', 'above': 'above', 'below': 'below', 'over': 'over', 'under': 'under', 'in': 'inside', 'touching': 'touching', 'right': 'to_the_right_of_extr', 'left': 'to_the_left_of_extr', 'at': 'at', 'front': 'in_front_of_extr', 'behind': 'behind_extr', 'between': 'between'}

def match_pattern(pattern, input_list):
	#print (pattern, input_list)
    for i in range(len(pattern)):
        if (pattern[i] != input_list[i]):
            return False
    return True

def get_types():
	ret_val = []
	for entity in entities:
		if entity.get_type_structure() is not None:
			for elem in entity.get_type_structure():
				if elem not in ret_val:
					ret_val.append(elem)
	return ret_val

class Token:
	def __init__(self, token):
		self.token = token

	def readable(self):
		return self.token

class Argument(Token):
	def __init__(self, argument, color_mod=None):
		super().__init__(argument)
		self.argument = argument
		self.color_mod = color_mod

	def readable(self):
		return [self.color_mod.readable(), self.token] if self.color_mod is not None else self.token

class Relation(Token):
	def __init__(self, relation, relatum=None, referent_list=None, entity_list=None):
		super().__init__(relation)
		self.relation = relation
		self.relatum = relatum
		if referent_list is None:
			self.referent_list = []
		self.entity_list = entity_list

	def readable(self):
		return [self.token, self.relatum, [ref.readable() for ref in self.referent_list]]

class Mod(Token):
	def __init__(self, mod_type, value):
		super().__init__(value)
		self.mod_type = mod_type
		self.value = value

def parse_response(response):
	parse_stack = []
	for word in response.split():
		if word in relation_list:
			parse_stack.append(Relation(word))
		elif word in color_mods:
			parse_stack.append(Mod('color_mod', word))
		elif word in types:
			arg = Argument(word)
			if len(parse_stack) > 0 and type(parse_stack[-1]) is Mod:
				arg.color_mod = parse_stack.pop()
			if len(parse_stack) > 0 and type(parse_stack[-1]) is Relation:
				parse_stack[-1].referent_list.append(arg)
			else:
				parse_stack.append(arg)
	return parse_stack

'''def parse_response(response):
	ret_val = []
	relation = {'relation': None, 'relatum_mod': None, 'relatum_type': None, 'referents': [], 'color_mod': []}
	response = response.lower()
	rel_count = 0
	color_count = 0
	curr_color = None
	for word in response.split():
		if word in relation_list:
			if relation['relation'] is not None:
				ret_val.append(relation)
			relation = {'relation': word, 'relatum_mod': None, 'relatum_type': None, 'referents': [], 'color_mod': []}
			rel_count = rel_count + 1
			curr_color = None
		elif word in color_mods:
			if rel_count >= 1:
				ret_val['color_mod'].append(word)
				curr_color = word
				color_count = color_count + 1
		elif rel_count >= 1:
			for entity in entities:
				name = entity.name.lower().split()
				print ("*", word, entity.get_type_structure(), curr_color, entity.get_color_mod())
				if name[0] == word and match_pattern(name, response[response.index(word):]) or word in entity.get_type_structure():			
					if curr_color == None or curr_color == entity.get_color_mod():
						ret_val['referents'].append(entity)					
	return ret_val'''

#with bpy.data.libraries.load(filepath + "001_table.blend", link = link) as (data_from, data_to):
#    data_to.objects = data_from.objects
#ob = None
#for obj in data_to.objects:
#    scene.objects.link(obj)
#    if obj.get('main') is not None:
#        ob = obj

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
	ret_val = max(ret_val, 0.5 * (above(a, b) + touching(a, b)))
    #for ob in b:
    #    if ob.get('working_surface') is not None or ob.get('planar') is not None:
    #        ret_val = max(ret_val, 0.5 * (v_offset(a, ob) + get_proj_intersection(a, ob)))
    #        ret_val = max(ret_val, 0.5 * (int(near(a, ob) > 0.99) + larger_than(ob, a)))         
    #if ret_val >= 0.6:
    #    return 0.5 * (ret_val + larger_than(b, a))
	return ret_val

def over(a, b):
    bbox_a = a.get_bbox()
    bbox_b = b.get_bbox()
    return 0.5 * above(a, b) + 0.2 * get_proj_intersection(a, b) + 0.3 * near(a, b)

def under(a, b):
	return over(b, a)

def closer_than(a, b, pivot):
    return 1 if point_distance(a.get_bbox(), pivot.get_bbox()) < point_distance(b.get_bbox(), pivot.get_bbox()) else 0

def in_front_of_extr(a, b):
#def in_front_of_extr(a, b, observer):
    bbox_a = a.get_bbox()
    max_dim_a = max(bbox_a[7][0] - bbox_a[0][0],
                    bbox_a[7][1] - bbox_a[0][1],
                    bbox_a[7][2] - bbox_a[0][2]) + 0.0001
    dist = get_distance_from_line(observer.get_bbox_centroid(), b.get_bbox_centroid(), a.get_bbox_centroid())
    return 0.5 * (closer_than(a, b, observer) + e ** (-dist / max_dim_a))

def behind_extr(a, b):
	return in_front_of_extr(b, a)

def touching(a, b):	
	bbox_a = a.get_bbox()
	bbox_b = b.get_bbox()
	center_a = a.get_bbox_centroid()
	center_b = b.get_bbox_centroid()
	rad_a = max(bbox_a[7][0] - bbox_a[0][0],
                    bbox_a[7][1] - bbox_a[0][1],
                    bbox_a[7][2] - bbox_a[0][2]) / 2
	rad_b = max(bbox_b[7][0] - bbox_b[0][0],
                    bbox_b[7][1] - bbox_b[0][1],
                    bbox_b[7][2] - bbox_b[0][2]) / 2
	
	#if a.name == "Apple 1" and b.name == "Bowl":
	#	print (center_a, center_b)

	for point in bbox_a:
		if a.name == "Apple 1" and b.name == "Bowl":
			print (point_distance(point, center_b))	
		if point_distance(point, center_b) < rad_b:
			return 1
	for point in bbox_b:
		if point_distance(point, center_a) < rad_a:
			return 1
	return 0

def to_the_right_of_deic(a, b):
	center_a = a.get_bbox_centroid()
	center_b = b.get_bbox_centroid()	
	return sigmoid(center_b[1] - center_a[1], 1.0, 1.3)

def to_the_left_of_deic(a, b):
	return to_the_right_of_extr(b, a)

def inside(a, b):
	return 1

def at(a, b):
	return 0.8 * near(a, b) + 0.2 * touching(a, b)

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
#scene.objects['Observer'].location = (-14, 0, 6)
#scene.update()
#observer = Entity(scene.objects['Observer'])
#observer.set_frontal(-scene.objects['Observer'].location)
#observer.set_longitudinal((0, 1, 4))        

#gen_data("above")
#gen_data("near")
#gen_data("on")

def add_props():
    lamp = bpy.data.lamps.new("Lamp", type = 'POINT')
    lamp.energy = 30
    cam = bpy.data.cameras.new("Camera")

    if bpy.data.objects.get("Lamp") is not None:
        lamp_obj = bpy.data.objects["Lamp"]
    else:
        lamp_obj = bpy.data.objects.new("Lamp", lamp)
        scene.objects.link(lamp_obj)
    if bpy.data.objects.get("Camera") is not None:
        cam_ob = bpy.data.objects["Camera"]
    else:
        cam_ob = bpy.data.objects.new("Camera", cam)
        scene.objects.link(cam_ob)    

    lamp_obj.location = (-20, 0, 10)
    cam_ob.location = (-15.5, 0, 7)
    cam_ob.rotation_mode = 'XYZ'
    cam_ob.rotation_euler = (1.1, 0, -1.57)
    bpy.data.cameras['Camera'].lens = 20

    bpy.context.scene.camera = scene.objects["Camera"]
    scene.update()
    
def get_entity_by_name(name):
    for entity in entities:
        #print(name, entity.name)
        if entity.name.lower() == name:
            return entity
    return None

def place_entity(entity, position=(0,0,0), rotation=(0,0,0)):
    obj = entity.constituents[0]
    obj.location = position
    obj.rotation_mode = 'XYZ'
    obj.rotation_euler = rotation
    scene.update()

def arrange_entities(reg, collection):
    for entity in collection:
        if entity.get('fixed') is None:
            print (entity.name)
            if reg[4] == reg[5]:
                pos = (random.uniform(reg[0], reg[1]), random.uniform(reg[2], reg[3]), reg[4])#entity.get_parent_offset()[2])
            else:
                pos = (random.uniform(reg[0], reg[1]), random.uniform(reg[2], reg[3]), random.uniform(reg[4], reg[5]))
            place_entity(entity, pos, (math.pi,0,0))
            while check_collisions(entity):
                print (entity.name, pos)
                if reg[4] == reg[5]:
                    pos = (random.uniform(reg[0], reg[1]), random.uniform(reg[2], reg[3]), reg[4])#entity.get_parent_offset()[2])
                else:
                    pos = (random.uniform(reg[0], reg[1]), random.uniform(reg[2], reg[3]), random.uniform(reg[4], reg[5]))
                place_entity(entity, pos, (math.pi,0,0))

def axis_collision(int_a, int_b):
    return int_a[1] <= int_b[1] and int_a[1] >= int_b[0] or \
int_a[0] >= int_b[0] and int_a[0] <= int_b[1] or \
int_b[0] >= int_a[0] and int_b[0] <= int_a[1] or \
int_b[1] >= int_a[0] and int_b[1] <= int_a[1]

def check_collisions(a):
    for entity in entities:
        if entity != a and check_collision(a, entity):
            print (entity.name, a.name)
            return True
    return False            

def check_collision(a, b):
    span_a = a.get_span()
    span_b = b.get_span()
    return axis_collision((span_a[0], span_a[1]), (span_b[0], span_b[1])) and axis_collision((span_a[2], span_a[3]), (span_b[2], span_b[3])) and axis_collision((span_a[4], span_a[5]), (span_b[4], span_b[5]))

def put_on_top(a, b):
    pass

def save_screenshot():
    add_props()
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.use_border = False
    scene.render.image_settings.file_format = 'JPEG'
    current_scene = bpy.data.filepath.split("/")[-1].split(".")[0]
    scene.render.filepath = filepath + current_scene + ".jpg"
    bpy.ops.render.render(write_still=True)


def get_argument_entities(arg):
    #print ("ARG = ", arg, arg.mod.det, arg.mod.adj)
    ret_val = [get_entity_by_name(arg.token)]    
    if ret_val == [None]:
        ret_val = []
        if arg.mod != None and arg.mod.det == 'a':
            #print (entities)
            for entity in entities:
                print ("ARG: ", arg.token, entity.name, entity.get_type_structure(), entity.color_mod)
                if arg.token in entity.type_structure and (arg.mod.adj == "" or arg.mod.adj is None or entity.color_mod == arg.mod.adj):
                    ret_val += [entity]
    #print ("RETVAL: ", ret_val) 
    return ret_val


def proj(obj, cam):
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, obj.location)
    print("2D Coords:", co_2d)
    render_scale = scene.render.resolution_percentage / 100
    render_size = (int(scene.render.resolution_x * render_scale), int(scene.render.resolution_y * render_scale),)
    print("Pixel Coords:", (round(co_2d.x * render_size[0]),round(co_2d.y * render_size[1]),))
    return co_2d

def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    init_parser([entity.name for entity in entities])
    if len(args) != 2:
        result = "*RESULT: MALFORMED*"
    else:
        print (args[1])
        rel_constraint = parse(args[1])
        print (rel_constraint)
        #print (rel_constraint)
        refs = []
        if rel_constraint is None:
            return "*RESULT: NO RELATIONS*"
        for ref in rel_constraint.referents:
            print (ref.token)
            refs += get_argument_entities(ref)
        print ([ref.name for ref in refs])
        relation = rel_constraint.token
        #print (bpy.context.scene.cursor_location)
        for entity in entities:
            if entity.name == "Table" and bpy.data.objects.get("Camera") is not None:
                print (proj(entity.constituents[0], bpy.data.objects["Camera"]))
        
        
        
        
        '''global types
        types = get_types()
        relatum = args[0].lower()
        raw_response = args[1].lower()
        relatum = relatum.replace('cube', 'block')
        raw_response = raw_response.replace('cube', 'block')
        relatum = get_entity_by_name(relatum)
        response = parse_response(raw_response)
        for item in response:
            if type(item) is Relation:
                ref_list = []
                for entity in entities:
                    for ref in item.referent_list:
                        if ref.token in entity.get_type_structure() and (ref.color_mod is None or ref.color_mod.token == entity.color_mod) and entity not in ref_list:
                            ref_list.append(entity)
                            #print (item.referent_list, ref_list)
                            item.entity_list = ref_list

        print ("*ORIGINAL: ", relatum.name, ", " ,raw_response)
        print ("*PARSED STRUCTURE: ", [r.readable() for r in response])
        best_target_value = 0
        for item in response:
            if type(item) is Relation:
                best_candidate = None
                target_value = 0
                best_target_value = 0
                for entity in item.entity_list:
                    if id(relatum) != id(entity):
                        target_value = globals()[rf_mapping[item.token]](relatum, entity)
                        if target_value > best_target_value:
                            best_target_value = target_value
                            best_candidate = entity
                            #print (best_candidate)
            print ("*FINAL: ", relatum.name, item.token, best_candidate.name, best_target_value)
        result = "*RESULT: OK*"
        for item in response:
            if type(item) is Relation:
                print ('*RELATION:', item.token, best_target_value, '*')
        print (result)'''

if __name__ == "__main__":
    # save_screenshot()
    #print (one, two)
    #print ([entity.name for entity in entities])
    #print (check_collision(entities[0], entities[8]))
    # print (entities[0].get_span())
    # print (entities[4].get_span())
    #for entity in entities:
    #    print ("CONST: ", entity.constituents[0].name)
    #    print (entity.constituents[0]['id'], entity.get_type_structure())
    main()


