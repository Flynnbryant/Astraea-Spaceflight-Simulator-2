import numpy as np
import statistics
import time

from data.read_conditions import *
from mechanics.orbit import *
from graphics.labels import *
from graphics.trace import *
from mechanics.centres import *

class Entity():
    def __init__(self, data, universe, focus):
        self.name = data[0]
        self.primary = False
        self.radii = 1000*np.array([float(data[7]),float(data[8]),float(data[9])])
        self.mean_radius = statistics.mean(self.radii)
        universe.entities.append(self)
        self.focus_num = len(universe.entities)-2
        self.color = np.array([float(i) for i in (data[4].split(','))])
        self.colorsmall = self.color/255
        self.specific_strength = 1
        self.orbit = Orbit(self)

        if self.name == focus:
            universe.focus = self.focus_num
            universe.focus_entity = self

        for body in universe.bodies:
            if body.name == data[2]:
                self.primary = body.barycentre if data[3] == 'barycentre' else body.bodycentre
                self.barycentre_model = data[3] == 'barycentre'
                read_initial_state(self, data, universe) if data[5] == 'state' else read_initial_elements(self, data, universe)
                self.local_planet = self.primary.object.local_planet if self.primary.object.primary else self
