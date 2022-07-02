import numpy as np
import time
from scipy.optimize import brentq
import math
from mechanics.utilities import *
from mechanics.hyperbolic_elements import *

class Orbit:
    def __init__(self, entity):
        self.entity = entity

def elliptical_elements_to_pos(entity, mean_anomaly):
    entity.eccentric_anomaly = brentq(eccentric_anomaly,-0.1,6.3,args=(entity.eccentricity, mean_anomaly),xtol=1e-8)
    entity.true_anomaly = 2*np.arctan2(entity.sqrtp*np.sin(0.5*entity.eccentric_anomaly),entity.sqrtm*np.cos(0.5*entity.eccentric_anomaly))
    entity.rel_dist = entity.semi_major_axis*(1-entity.eccentricity*np.cos(entity.eccentric_anomaly))
    return entity.rel_dist * np.matmul(entity.rotation_matrix,np.array([np.cos(entity.true_anomaly),np.sin(entity.true_anomaly)]))

def elliptical_elements_to_vel(entity):
    plane_velocity = np.array([-np.sin(entity.eccentric_anomaly),np.sqrt(entity.omes)*np.cos(entity.eccentric_anomaly)])
    #return np.matmul(entity.rotation_matrix,plane_velocity) * np.sqrt(entity.primary_SGP*entity.semi_major_axis) / entity.rel_dist
    return np.matmul(entity.rotation_matrix,plane_velocity) * np.sqrt(entity.primary.SGP*entity.semi_major_axis) / entity.rel_dist

def state_to_elliptical_elements(entity, centre, timev):
    entity.rel_dist = np.linalg.norm(centre.rpos)
    entity.momentum_vec = np.cross(centre.rpos,centre.rvel)
    #entity.semi_major_axis = 1/((2/entity.rel_dist)-((np.linalg.norm(centre.rvel)**2)*entity.primary_inverse_SGP))
    entity.semi_major_axis = 1/((2/entity.rel_dist)-((np.linalg.norm(centre.rvel)**2)*entity.primary.inverse_SGP))
    #entity.sqrta3omu = np.sqrt(entity.primary_inverse_SGP*entity.semi_major_axis**3)
    entity.sqrta3omu = np.sqrt(entity.primary.inverse_SGP*entity.semi_major_axis**3)
    entity.period = 2*np.pi*entity.sqrta3omu
    entity.inclination = np.arccos(entity.momentum_vec[2]/np.linalg.norm(entity.momentum_vec))
    #entity.eccentricity_vec = np.cross(centre.rvel,entity.momentum_vec)*entity.primary_inverse_SGP - centre.rpos/entity.rel_dist
    entity.eccentricity_vec = np.cross(centre.rvel,entity.momentum_vec)*entity.primary.inverse_SGP - centre.rpos/entity.rel_dist
    entity.eccentricity = np.linalg.norm(entity.eccentricity_vec)
    if entity.eccentricity > 1:
        state_to_hyperbolic_elements(entity, centre, timev)
    entity.periapsis = entity.semi_major_axis*(1-entity.eccentricity)

    entity.semi_minor_axis = entity.semi_major_axis*np.sqrt(entity.omes)
    entity.ascending_node = np.cross(np.array([0,0,1]),entity.momentum_vec)
    entity.ascending = np.linalg.norm(entity.ascending_node)
    entity.long_ascending = np.arccos(entity.ascending_node[0]/entity.ascending) + entity.nodal_precession
    entity.arg_periapsis = np.arccos(np.dot(entity.ascending_node, entity.eccentricity_vec)/(entity.ascending*entity.eccentricity))
    entity.true_anomaly = np.arccos(np.dot(entity.eccentricity_vec,centre.rpos)/(entity.eccentricity*entity.rel_dist))
    if entity.eccentricity_vec[2] < 0: entity.arg_periapsis = math.tau - entity.arg_periapsis
    if entity.ascending_node[1] < 0: entity.long_ascending = math.tau - entity.long_ascending
    if np.dot(centre.rpos,centre.rvel) < 0: entity.true_anomaly = math.tau - entity.true_anomaly
    #entity.mean_motion = np.sqrt(entity.primary_SGP/entity.semi_major_axis**3)
    entity.mean_motion = np.sqrt(entity.primary.SGP/entity.semi_major_axis**3)
    entity.eccentric_anomaly = 2*np.arctan(np.tan(entity.true_anomaly*0.5)/np.sqrt((1+entity.eccentricity)/(1-entity.eccentricity)))
    entity.epoch_anomaly = entity.eccentric_anomaly-entity.eccentricity*np.sin(entity.eccentric_anomaly)
    entity.epoch_time = timev
    rotation_constants(entity)
