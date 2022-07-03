import numpy as np
import time
from OpenGL.GL import *

def mouse_precision(x, a, b):
    return a*b*(-x/(b+x**2) + x/b)

def model_to_projection(camera, apos):
    coordinate_array = np.array([*apos,1])
    proj = np.dot(coordinate_array, glGetFloatv(GL_PROJECTION_MATRIX))
    return np.array([proj[0],proj[1],proj[2]])/proj[3]

def camera_to_model(camera):
    pos = camera.pos*camera.inverse_scale_factor
    modelview_matrix = glGetFloatv(GL_PROJECTION_MATRIX)
    return pos

def render_detail(camera, universe, object):
    '''
    camera_pos = camera_to_model(camera)
    if object is universe.focus_entity:
        distance = camera.camera_distance
    elif object is universe.focus_entity.local_planet:
        distance = max(universe.focus_entity.semi_major_axis,camera.camera_distance-object.semi_major_axis)
    else:
        distance = np.abs(camera.camera_distance-object.semi_major_axis)
    camera_angle = np.arctan(object.mean_radius/distance)/np.deg2rad(camera.fov)
    object.render_detail = np.clip(int(200*camera_angle),8,256)
    '''
    if object.primary.object.name == 'Sol':
        object.render_detail = 64
    else:
        object.render_detail = 16

def specific_strength(camera, universe, object, global_strength):
    if object is universe.focus_entity:
        object.specific_strength = 1
    else:
        if object.primary is universe.focus_entity.primary:
            distance = max(universe.focus_entity.semi_major_axis,camera.camera_distance-object.semi_major_axis)
        else:
            distance = camera.camera_distance
        inner_strength = 2*distance/object.inner_label_distance - 1
        outer_strength = 2 - distance/object.outer_label_distance
        object.specific_strength = np.clip(min([inner_strength,outer_strength,global_strength]),0,1)
    object.label.recalculate_color()
