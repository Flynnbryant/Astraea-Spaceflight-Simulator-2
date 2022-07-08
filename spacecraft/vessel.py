from mechanics.entity import *
from spacecraft.node import *
from mechanics.centres import *
import numpy as np

class Vessel(Entity):
    def __init__(self, data, universe, focus):
        self.nodes = [Node(False,253399708800)]
        self.bodycentre = Vesselcentre(self)
        self.barycentre = Blankcentre(self)
        super().__init__(data, universe, focus)
        self.label = EntityLabel(self, width = 0.008, height = 0.03)
        universe.vessels.append(self)
        self.trace = Trace(self, 52, True)

    def change_primary(self, universe, new_primary, barycentre = True):
        self.primary = new_primary.barycentre if barycentre else new_primary.bodycentre
        self.local_planet = self.primary.object.local_planet
