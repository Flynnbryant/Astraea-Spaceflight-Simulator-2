import numpy as np

def create_centres(object, mass, grav_constant):
    SGP = mass*grav_constant
    return Bodycentre(object, mass, SGP), Barycentre(object, mass, SGP)

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

    def sibling_collisions(self, universe, vessel):
        for sibling in self.object.satellites:
            if False:
            #if pvdis < sibling.SOI:
                entity.change_primary(universe, sibling, barycentre=True)

class Barycentre(Centre):
    def __init__(self, object, mass, SGP):
        super().__init__(object, mass, SGP)
        self.ppos = np.array([0.,0.,0.],dtype=np.float64)
        self.pvel = np.array([0.,0.,0.],dtype=np.float64)

    def check_model(self, universe, vessel):
        self.sibling_collisions(universe, vessel)
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
        self.sibling_collisions(universe, vessel)
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
