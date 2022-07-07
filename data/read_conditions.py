import numpy as np
from mechanics.orbit import *
from mechanics.rotations import *

def read_initial_elements(entity, data, universe):
    elements = data[6].split(',')

    if data[5] == 'elements':
        entity.semi_major_axis = 1000*sn(elements[11])
        entity.eccentricity = sn(elements[2])
        entity.inclination = np.deg2rad(sn(elements[4]))
        entity.arg_periapsis = np.deg2rad(sn(elements[6]))
        entity.long_ascending = np.deg2rad(sn(elements[5]))
        entity.mean_anomaly = np.deg2rad(sn(elements[9]))

    elif data[5] == 'tle':
        pass

    rotation_constants(entity)
    entity.bodycentre.rpos = elliptical_elements_to_pos(entity, entity.mean_anomaly)
    entity.bodycentre.rvel = elliptical_elements_to_vel(entity)
    state_to_elliptical_elements(entity, entity.bodycentre, universe.time)

def read_initial_state(entity, data, universe):
    elements = data[6].split(',')
    entity.bodycentre.rpos = 1000*np.array([sn(elements[2]),sn(elements[3]),sn(elements[4])])
    entity.bodycentre.rvel = 1000*np.array([sn(elements[5]),sn(elements[6]),sn(elements[7])])
    state_to_elliptical_elements(entity, entity.bodycentre, universe.time)
    rotation_constants(entity)

def sn(datastr):
    datalist = datastr.replace(',','').lower().split('e')
    return np.float64(datalist[0])*10**int(datalist[1])
