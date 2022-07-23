import numpy as np
from mechanics.body import *

def sn(datastr):
    datalist = datastr.replace(',','').lower().split('e')
    return np.float64(datalist[0])*10**int(datalist[1])

def create_centres(object, data, grav_constant):
    if data[8] == 'Mass':
        mass = sn(data[9])
        SGP = mass*grav_constant
        return Bodycentre(object, mass, SGP), Barycentre(object, mass, SGP, complete=False)

    elif data[8] == 'False':
        SGP = np.float64(data[9])*1e9
        mass = SGP/grav_constant
        return Bodycentre(object, mass, SGP), Barycentre(object, mass, SGP, complete=False)
    else:
        bary_SGP = np.float64(data[8])*1e9
        body_SGP = np.float64(data[9])*1e9
        bary_mass = bary_SGP/grav_constant
        body_mass = body_SGP/grav_constant
        return Bodycentre(object, body_mass, body_SGP), Barycentre(object, bary_mass, bary_SGP, complete=True)

def personal_primary_mass(object):
    if isinstance(object.primary,Barycentre) and not object.isvessel:
        object.PP_mass          = object.primary.mass   - object.barycentre.mass
        object.PP_SGP           = object.primary.SGP    - object.barycentre.SGP
    else:
        object.PP_mass          = object.primary.mass
        object.PP_SGP           = object.primary.SGP
    object.PP_inverse_mass  = 1/object.PP_mass
    object.PP_inverse_SGP   = 1/object.PP_SGP

class Centre():
    def __init__(self, object, mass, SGP):
        self.apos = np.array([0.,0.,0.],dtype=np.float64)
        self.rpos = np.array([0.,0.,0.],dtype=np.float64)
        self.object = object
        self.satellites = []
        self.mass = mass
        self.inverse_mass = 1/mass
        self.SGP = SGP
        self.inverse_SGP = 1/SGP

class Barycentre(Centre):
    def __init__(self, object, mass, SGP, complete=False):
        super().__init__(object, mass, SGP)
        self.complete=complete
        self.ppos = np.array([0.,0.,0.],dtype=np.float64)
        self.pvel = np.array([0.,0.,0.],dtype=np.float64)

    def check_model(self, universe, vessel):
        if vessel.orbit.periapsis < self.object.barycentre_transition:
            vessel.change_primary(universe, vessel.primary.object, barycentre=False)
        elif vessel.orbit.rel_dist > vessel.primary.object.SOI:
            vessel.change_primary(universe, vessel.primary.object.primary.object, barycentre=False)
        elif vessel.orbit.rel_dist < vessel.primary.object.mean_radius:
            vessel.collision(universe, vessel)

class Bodycentre(Centre):
    def __init__(self, object, mass, SGP):
        super().__init__(object ,mass, SGP)

    def check_model(self, universe, vessel):
        if vessel.orbit.periapsis > self.object.barycentre_transition:
            vessel.change_primary(universe, vessel.primary.object, barycentre=True)
        elif vessel.orbit.rel_dist < vessel.primary.object.mean_radius:
            vessel.collision(universe, vessel)

class Vesselcentre():
    def __init__(self, object):
        self.object = object
        self.apos = np.array([0.,0.,0.],dtype=np.float64)
        self.rpos = np.array([0.,0.,0.],dtype=np.float64)
        self.pvel = np.array([0.,0.,0.],dtype=np.float64)

class Blankcentre():
    def __init__(self, object):
        self.object = object
        self.apos = np.array([0.,0.,0.],dtype=np.float64)
        self.pvel = np.array([0.,0.,0.],dtype=np.float64)
        self.ppos = np.array([0.,0.,0.],dtype=np.float64)
