from mechanics.entity import *
import numpy as np

class Vessel(Entity):
    def __init__(self, data, universe, focus):
        self.bodycentre = Vesselcentre(self)
        self.barycentre = Blankcentre()
        super().__init__(data, universe, focus)
        self.labelbatch = LabelBatch()
        self.label = EntityLabel(self, width = 0.008, height = 0.03, labelbatch = self.labelbatch)
        universe.vessels.append(self)
        self.trace = Trace(self, 52, True)

    def change_primary(self, universe, new_primary, barycentre = True):
        self.primary = new_primary.barycentre if barycentre else new_primary.bodycentre
        self.local_planet = self.primary.object.local_planet

class Vesselcentre():
    def __init__(self, object):
        self.object = object
        self.apos = new_vector()
        self.rpos = new_vector()
        self.pvel = new_vector()

class Blankcentre():
    def __init__(self):
        self.apos = new_vector()
