import numpy as np
import statistics
import time

from mechanics.orbit import *
from graphics.labels import *
from graphics.trace import *
from mechanics.centres import *

class Entity():
    def __init__(self, data, universe, focus, radii=True):
        self.name = data[0]
        self.primary = False
        self.radii = 1000*np.array([float(data[5]),float(data[6]),float(data[7])] if radii else [0.01,0.01,0.01])
        self.mean_radius = statistics.mean(self.radii)
        universe.entities.append(self)
        self.focus_num = len(universe.entities)-1
        self.color = np.array([float(i) for i in (data[3].split(','))])
        self.colorsmall = self.color/255
        self.specific_strength = 1
        self.orbit = Orbit(self)

        if self.name == focus:
            universe.focus = self.focus_num
            universe.focus_entity = self

        for body in universe.bodies:
            if body.name == data[1]:
                self.primary = body.barycentre if data[2] == 'bary' else body.bodycentre
                self.barycentric = data[2] == 'bary'
                if data[4] == 'elements':
                    universe.read_initial_elements(self)
                elif data[4] == 'TLE':
                    universe.read_initial_TLE(self)
                self.local_planet = self.primary.object.local_planet if self.primary.object.primary else self
