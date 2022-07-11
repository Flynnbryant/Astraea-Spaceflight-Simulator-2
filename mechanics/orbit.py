import numpy as np
import time
from scipy.optimize import brentq
import math
from mechanics.rotations import *
from numba import njit

@njit
def eccentric_anomaly(E, e, M):
    return E - e*np.sin(E) - M

@njit
def hyperbolic_anomaly(H, e, M):
    return e*np.sinh(H) - H - M

@njit
def faster_elements_to_pos(sqrtp, eccentric_anomaly, sqrtm, semi_major_axis, eccentricity, rotation_matrix):
    true_anomaly = 2*np.arctan2(sqrtp*np.sin(0.5*eccentric_anomaly),sqrtm*np.cos(0.5*eccentric_anomaly))
    rel_dist = semi_major_axis*(1-eccentricity*np.cos(eccentric_anomaly))
    return true_anomaly, rel_dist, rel_dist * np.dot(rotation_matrix,np.array([np.cos(true_anomaly),np.sin(true_anomaly)]))

@njit
def faster_hyperbolic_elements_to_pos(sqrtp, eccentric_anomaly, sqrtm, semi_major_axis, eccentricity, rotation_matrix):
    true_anomaly = 2*np.arctan2(sqrtp*np.sin(0.5*eccentric_anomaly),sqrtm*np.cos(0.5*eccentric_anomaly))
    rel_dist = semi_major_axis*(1-eccentricity*np.cos(eccentric_anomaly))
    return true_anomaly, rel_dist, rel_dist * np.dot(rotation_matrix,np.array([np.cos(true_anomaly),np.sin(true_anomaly)]))

class Orbit:
    def __init__(self, entity):
        self.entity = entity
        self.nodal_precession = 0.

    def elliptical_elements_to_pos(self, mean_anomaly):
        self.eccentric_anomaly = brentq(eccentric_anomaly,-0.1,6.3,args=(self.eccentricity, mean_anomaly),xtol=1e-8)
        self.true_anomaly, self.rel_dist, pos = faster_elements_to_pos(self.sqrtp, self.eccentric_anomaly, self.sqrtm, self.semi_major_axis, self.eccentricity, self.rotation_matrix)
        return pos

    def hyperbolic_elements_to_pos(self, mean_anomaly):
        return self.entity.barycentre.rpos

    def elliptical_elements_to_vel(self):
        plane_velocity = np.array([-np.sin(self.eccentric_anomaly),np.sqrt(self.omes)*np.cos(self.eccentric_anomaly)])
        return np.dot(self.rotation_matrix,plane_velocity) * np.sqrt(self.entity.primary.SGP*self.semi_major_axis) / self.rel_dist

    def hyperbolic_elements_to_vel(self):
        pass

    def state_to_elements(self, centre, timev):
        self.rel_dist = np.linalg.norm(centre.rpos)
        self.momentum_vec = np.cross(centre.rpos,centre.rvel)
        self.semi_major_axis = 1/((2/self.rel_dist)-((np.linalg.norm(centre.rvel)**2)*self.entity.primary.inverse_SGP))
        self.sqrta3omu = np.sqrt(self.entity.primary.inverse_SGP*self.semi_major_axis**3)
        self.period = 2*np.pi*self.sqrta3omu
        self.inclination = np.arccos(self.momentum_vec[2]/np.linalg.norm(self.momentum_vec))
        self.eccentricity_vec = np.cross(centre.rvel,self.momentum_vec)*self.entity.primary.inverse_SGP - centre.rpos/self.rel_dist
        self.eccentricity = np.linalg.norm(self.eccentricity_vec)
        if self.eccentricity < 1:
            self.state_to_elliptical_elements(centre, timev)
        else:
            self.state_to_hyperbolic_elements(centre, timev)

    def state_to_elliptical_elements(self, centre, timev):
        self.periapsis = self.semi_major_axis*(1-self.eccentricity)
        self.semi_minor_axis = self.semi_major_axis*np.sqrt(self.omes)
        self.ascending_node = np.cross(np.array([0,0,1]),self.momentum_vec)
        self.ascending = np.linalg.norm(self.ascending_node)
        self.long_ascending = np.arccos(self.ascending_node[0]/self.ascending) + self.nodal_precession
        self.arg_periapsis = np.arccos(np.dot(self.ascending_node, self.eccentricity_vec)/(self.ascending*self.eccentricity))
        self.true_anomaly = np.arccos(np.dot(self.eccentricity_vec,centre.rpos)/(self.eccentricity*self.rel_dist))
        if self.eccentricity_vec[2] < 0: self.arg_periapsis = math.tau - self.arg_periapsis
        if self.ascending_node[1] < 0: self.long_ascending = math.tau - self.long_ascending
        if np.dot(centre.rpos,centre.rvel) < 0: self.true_anomaly = math.tau - self.true_anomaly
        self.mean_motion = np.sqrt(self.entity.primary.SGP/self.semi_major_axis**3)
        self.eccentric_anomaly = 2*np.arctan(np.tan(self.true_anomaly*0.5)/np.sqrt((1+self.eccentricity)/(1-self.eccentricity)))
        self.epoch_anomaly = self.eccentric_anomaly-self.eccentricity*np.sin(self.eccentric_anomaly)
        self.epoch_time = timev
        rotation_constants(self)

    def state_to_hyperbolic_elements(centre, timev):
        pass
'''
def elliptical_elements_to_pos(entity, mean_anomaly):
    entity.eccentric_anomaly = brentq(eccentric_anomaly,-0.1,6.3,args=(entity.eccentricity, mean_anomaly),xtol=1e-8)
    entity.true_anomaly = 2*np.arctan2(entity.sqrtp*np.sin(0.5*entity.eccentric_anomaly),entity.sqrtm*np.cos(0.5*entity.eccentric_anomaly))
    entity.rel_dist = entity.semi_major_axis*(1-entity.eccentricity*np.cos(entity.eccentric_anomaly))
    return entity.rel_dist * np.matmul(entity.rotation_matrix,np.array([np.cos(entity.true_anomaly),np.sin(entity.true_anomaly)]))

def elliptical_elements_to_vel(entity):

def state_to_elliptical_elements(self, centre, timev):
    entity.rel_dist = np.linalg.norm(centre.rpos)
    entity.momentum_vec = np.cross(centre.rpos,centre.rvel)
    entity.semi_major_axis = 1/((2/entity.rel_dist)-((np.linalg.norm(centre.rvel)**2)*entity.primary.inverse_SGP))
    entity.sqrta3omu = np.sqrt(entity.primary.inverse_SGP*entity.semi_major_axis**3)
    entity.period = 2*np.pi*entity.sqrta3omu
    entity.inclination = np.arccos(entity.momentum_vec[2]/np.linalg.norm(entity.momentum_vec))
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
    entity.mean_motion = np.sqrt(entity.primary.SGP/entity.semi_major_axis**3)
    entity.eccentric_anomaly = 2*np.arctan(np.tan(entity.true_anomaly*0.5)/np.sqrt((1+entity.eccentricity)/(1-entity.eccentricity)))
    entity.epoch_anomaly = entity.eccentric_anomaly-entity.eccentricity*np.sin(entity.eccentric_anomaly)
    entity.epoch_time = timev
    rotation_constants(entity)
'''
'''
def hyperbolic_elements_to_pos(entity, mean_anomaly):
    entity.hyperbolic_anomaly = brentq(hyperbolic_anomaly,-0.1,6.3,args=(entity.eccentricity, mean_anomaly),xtol=1e-8)
    entity.true_anomaly = 2*np.arctan(np.sqrt((entity.eccentricity+1)/(entity.eccentricity-1))*np.tanh(entity.hyperbolic_anomaly*0.5))
    entity.rel_dist = -entity.semi_major_axis*(1-entity.eccentricity*np.cos(entity.hyperbolic_anomaly))
    plane_position = np.array([np.cos(entity.true_anomaly),np.sin(entity.true_anomaly)])
    return entity.rel_dist * np.matmul(entity.rotation_matrix,plane_position)

def hyperbolic_elements_to_vel(entity):
    plane_velocity = np.array([-np.sin(entity.hyperbolic_anomaly),np.sqrt(entity.omes)*np.cos(entity.hyperbolic_anomaly)])
    #return np.matmul(entity.rotation_matrix,plane_velocity) * np.sqrt(entity.primary_SGP*entity.semi_major_axis) / entity.rel_dist
    return np.matmul(entity.rotation_matrix,plane_velocity) * np.sqrt(entity.primary.SGP*entity.semi_major_axis) / entity.rel_dist

def Bookmatter_state_to_elements(entity, centre, timev):
    entity.momentum_vec = np.cross(centre.rpos,centre.rvel)
    entity.long_ascending = np.atan(-entity.momentum_vec[0]/entity.momentum_vec[1])
    entity.inclination = np.atan(np.sqrt(entity.momentum_vec[0]**2 + entity.momentum_vec[1]**2)/entity.momentum_vec[2])
    entity.LRLv = 0
'''
