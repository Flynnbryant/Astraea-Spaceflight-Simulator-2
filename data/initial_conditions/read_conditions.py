import numpy as np
from mechanics.orbit import *
from mechanics.rotations import *

def read_initial_elements(entity, data, universe):
    elements = data[6].split(',')

    if data[5] == 'elements':
        entity.orbit.semi_major_axis = 1000*sn(elements[11])
        entity.orbit.eccentricity = sn(elements[2])
        entity.orbit.inclination = np.deg2rad(sn(elements[4]))
        entity.orbit.arg_periapsis = np.deg2rad(sn(elements[6]))
        entity.orbit.long_ascending = np.deg2rad(sn(elements[5]))
        entity.orbit.mean_anomaly = np.deg2rad(sn(elements[9]))

    elif data[5] == 'tle':
        pass

    rotation_constants(entity.orbit)
    entity.bodycentre.rpos = entity.orbit.elliptical_elements_to_pos(entity.orbit.mean_anomaly)
    entity.bodycentre.rvel = entity.orbit.elliptical_elements_to_vel()
    entity.orbit.state_to_elements(entity.bodycentre, universe.time)

def read_initial_state(entity, data, universe):
    elements = data[6].split(',')
    entity.bodycentre.rpos = 1000*np.array([sn(elements[2]),sn(elements[3]),sn(elements[4])])
    entity.bodycentre.rvel = 1000*np.array([sn(elements[5]),sn(elements[6]),sn(elements[7])])
    entity.orbit.state_to_elements(entity.bodycentre, universe.time)
    rotation_constants(entity.orbit)

def sn(datastr):
    datalist = datastr.replace(',','').lower().split('e')
    return np.float64(datalist[0])*10**int(datalist[1])
