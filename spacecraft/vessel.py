from mechanics.entity import *
import numpy as np

class Vessel(Entity):
    def __init__(self, data, universe, focus):
        self.bodycentre = Vesselcentre(self)
        self.barycentre = Blankcentre()
        super().__init__(data, universe, focus)
        self.label = EntityLabel(self, width = 0.008, height = 0.03)
        universe.vessels.append(self)
        self.trace = Trace(self, 52, True)

    def change_primary(self, universe, new_primary, barycentre = True):
        self.primary = new_primary.barycentre if barycentre else new_primary.bodycentre
        self.local_planet = self.primary.object.local_planet

class Vesselcentre():
    def __init__(self, object):
        self.object = object
        self.apos = np.array([0.,0.,0.],dtype=np.float64)
        self.rpos = np.array([0.,0.,0.],dtype=np.float64)
        self.pvel = np.array([0.,0.,0.],dtype=np.float64)

class Blankcentre():
    def __init__(self):
        self.apos = np.array([0.,0.,0.],dtype=np.float64)
