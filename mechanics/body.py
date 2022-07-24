import numpy as np
import time
from mechanics.entity import *
from mechanics.rotations import *
from graphics.trace import *
from graphics.spheroid import *
from graphics.labels import *
from mechanics.centres import *

class Body(Entity):
    def __init__(self, data, universe, focus):
        self.isvessel = False
        self.bodycentre, self.barycentre = create_centres(self, data, universe.grav_constant)
        super().__init__(data, universe, focus)
        mass_scale = 0.0001*np.log10(self.bodycentre.mass)
        self.spheroid = Spheroid(self)

        if self.primary:
            self.primary.satellites.append(self)
            if not self.primary.object.barycentre.complete:
                self.primary.object.barycentre.SGP += self.barycentre.SGP
                self.primary.object.barycentre.mass += self.barycentre.mass
                self.primary.object.barycentre.inverse_SGP = 1/self.primary.object.barycentre.SGP
                self.primary.object.barycentre.inverse_mass = 1/self.primary.object.barycentre.mass
            self.label = EntityLabel(self, width = mass_scale, height = 20*mass_scale)
        else:
            self.label = EntityLabel(self, width = mass_scale, height = 20*mass_scale)
            self.spheroid.render_detail = 16
            universe.star = self
            self.hill                   = np.inf
            self.SOI                    = np.inf
            self.outer_label_distance   = np.inf
            self.inner_label_distance   = 0.

        self.rings = Ring(self) if self.name == 'Saturn' else False
        self.shape_and_orientation(data)

        self.texture = 'Default'
        universe.bodies.append(self)

    def shape_and_orientation(self, data):
        self.rotation_rate = float(data[13])/86400
        self.shift = float(data[12]) + float(data[14]) - 946684800.0*self.rotation_rate
        self.tilt_quaternion, self.axis_vector, self.ECL_to_EQU_matrix, self.EQU_to_ECL_matrix = celestial_to_ecliptic(float(data[10]),float(data[11]))

        self.oblateness = (self.radii[0]-self.radii[2])/self.radii[0]
        self.precession_constant = -(self.radii[0]**2)*(2*self.oblateness-(self.radii[0]**3)*(np.deg2rad(self.rotation_rate)**2)*self.bodycentre.inverse_SGP)/2
