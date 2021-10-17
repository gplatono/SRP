import bpy
import bpy_types
import numpy
import math
from math import e, pi
import itertools
import os
import sys
import random
from geometry_utils import *

class Entity:
    scene = bpy.context.scene
    
    def __init__(self, main):
        self.constituents = [main]
        self.name = main.name
        self.color_mod = self.get_color_mod()
        self.type_structure = self.get_type_structure()
        self.span = self.get_span()
        self.bbox = self.get_bbox()
        self.bbox_centroid = self.get_bbox_centroid()
        self.dimensions = self.get_dimensions()
        self.faces = self.get_faces()
        self.longitudinal = []
        self.frontal = []
        self.parent_offset = self.get_parent_offset()
        queue = [main]
        while len(queue) != 0:
            par = queue[0]
            queue.pop(0)
            for ob in Entity.scene.objects:
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
            #bpy.context.scene.update()
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

    def get_closest_distance(self, other_entity):
        this_faces = self.get_faces()
        other_faces = other_entity.get_faces()
            
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

    def show_bbox(self):
        mesh = bpy.data.meshes.new(self.name + '_mesh')
        obj = bpy.data.objects.new(self.name + '_bbox', mesh)
        bpy.context.scene.objects.link(obj)
        bpy.context.scene.objects.active = obj
        bbox = self.get_bbox()
        mesh.from_pydata(bbox, [], [(0, 1, 3, 2), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5), (4, 5, 7, 6)])
        mesh.update()

    def get_type_structure(self):
        if not hasattr(self, 'type_structure') or self.type_structure is None:
            if hasattr(self.constituents[0], 'id'):
                self.type_structure = self.constituents[0]['id'].split(".")
            else: self.type_structure = None
        return self.type_structure
	
    def get_color_mod(self):
        if not hasattr(self, 'color_mod') or self.color_mod is None:
            if self.constituents[0].get('color_mod') is not None:
                self.color_mod = self.constituents[0]['color_mod'].lower()
            else:
                self.color_mod = None
        return self.color_mod

    def get_parent_offset(self):
        span = self.get_span()
        if span is not None:
            return self.constituents[0].location.x - span[0], self.constituents[0].location.y - span[2], self.constituents[0].location.z - span[4]
        else:
            return None
