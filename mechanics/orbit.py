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

class Orbit:
    def __init__(self, entity):
        self.entity = entity
        self.nodal_precession = 0.

    def elliptical_elements_to_pos(self, mean_anomaly):
        self.eccentric_anomaly = brentq(eccentric_anomaly,-0.1,6.3,args=(self.eccentricity, mean_anomaly),xtol=1e-8)
        self.true_anomaly, self.rel_dist, pos = faster_elements_to_pos(self.sqrtp, self.eccentric_anomaly, self.sqrtm, self.semi_major_axis, self.eccentricity, self.rotation_matrix)
        return pos

    def hyperbolic_elements_to_pos(self, mean_anomaly): #Convert into a njit faster function
        self.hyperbolic_anomaly = brentq(hyperbolic_anomaly,-0.1,6.3,args=(self.eccentricity, mean_anomaly),xtol=1e-8)
        self.true_anomaly = 2*np.arctan(np.sqrt((self.eccentricity+1)/(self.eccentricity-1))*np.tanh(self.hyperbolic_anomaly*0.5))
        self.rel_dist = -self.semi_major_axis*(1-self.eccentricity*np.cos(self.hyperbolic_anomaly))
        plane_position = np.array([np.cos(self.true_anomaly),np.sin(self.true_anomaly)])
        return self.rel_dist * np.matmul(self.rotation_matrix,plane_position)

    def elliptical_elements_to_vel(self):
        plane_velocity = np.array([-np.sin(self.eccentric_anomaly),np.sqrt(self.omes)*np.cos(self.eccentric_anomaly)])
        return np.dot(self.rotation_matrix,plane_velocity) * np.sqrt(self.entity.PP_SGP*self.semi_major_axis) / self.rel_dist

    def hyperbolic_elements_to_vel(self):
        plane_velocity = np.array([-np.sin(self.hyperbolic_anomaly),np.sqrt(self.omes)*np.cos(self.hyperbolic_anomaly)])
        return np.matmul(self.rotation_matrix,plane_velocity) * np.sqrt(self.PP_SGP*self.semi_major_axis) / self.rel_dist

    def state_to_elements(self, centre, timev):
        self.rel_dist = np.linalg.norm(centre.rpos)
        self.momentum_vec = np.cross(centre.rpos,centre.rvel)
        self.semi_major_axis = 1/((2/self.rel_dist)-((np.linalg.norm(centre.rvel)**2)*self.entity.PP_inverse_SGP))
        self.sqrta3omu = np.sqrt(self.entity.PP_inverse_SGP*self.semi_major_axis**3)
        self.period = 2*np.pi*self.sqrta3omu
        self.inclination = np.arccos(self.momentum_vec[2]/np.linalg.norm(self.momentum_vec))
        self.eccentricity_vec = np.cross(centre.rvel,self.momentum_vec)*self.entity.PP_inverse_SGP - centre.rpos/self.rel_dist
        self.eccentricity = np.linalg.norm(self.eccentricity_vec)
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
        self.mean_motion = np.sqrt(self.entity.PP_SGP/self.semi_major_axis**3)
        self.eccentric_anomaly = 2*np.arctan(np.tan(self.true_anomaly*0.5)/np.sqrt((1+self.eccentricity)/(1-self.eccentricity)))
        self.epoch_anomaly = self.eccentric_anomaly-self.eccentricity*np.sin(self.eccentric_anomaly)
        self.epoch_time = timev
        rotation_constants(self)

    def state_to_hyperbolic_elements(self, centre, timev):
        pass
