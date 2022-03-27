import numpy as np
from OpenGL.GL import *

def mouse_precision(x, a, b):
    return a*b*(-x/(b+x**2) + x/b)

def model_to_projection(camera, apos):
    b = np.dot(np.array([*apos,1]), glGetFloatv(GL_PROJECTION_MATRIX))
    return np.array([b[0],b[1],b[2]])/b[3]

def render_detail(camera, universe, object):
    if object is universe.focus_entity:
        distance = camera.camera_distance
    elif object is universe.focus_entity.local_planet:
        distance = max(universe.focus_entity.semi_major_axis,camera.camera_distance-object.semi_major_axis)
    else:
        distance = np.abs(camera.camera_distance-object.semi_major_axis)
    object.render_detail = int(4**np.clip(1000*np.arctan(object.mean_radius/distance)/np.deg2rad(camera.fov),1,2.5))
    #print(object.name, distance, object.render_detail)

def specific_strength(camera, universe, object, global_strength):
    if object.primary is universe.focus_entity.primary:
        distance = max(universe.focus_entity.semi_major_axis,camera.camera_distance-object.semi_major_axis)
    else:
        distance = camera.camera_distance
    inner_strength = 2*distance/object.inner_label_distance - 1
    outer_strength = 2 - distance/object.outer_label_distance
    object.specific_strength = np.clip(min([inner_strength,outer_strength,global_strength]),0,1)
    object.label.color = (*(object.color*object.specific_strength).astype(int), 255)
