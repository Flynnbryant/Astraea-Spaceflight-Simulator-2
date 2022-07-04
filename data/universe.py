import numpy as np
import time
import csv

from graphics.labels import *

from analysis.profile import *
from spacecraft.node import *
from mechanics.body import *
from mechanics.entity import *
from spacecraft.vessel import *
from mechanics.utilities import *

class Universe:
    def __init__(self, focus, profiler):
        self.profile = Profile(profiler)
        self.focusinput = focus

    def populate(self):
        self.nodes = [Node(False,253399708800)]
        self.grav_constant = 6.67430*10**-11
        self.c = 299792458
        self.time = 1640995200 #Unix time for 2022 Jan 1st 00:00, the simulation start point
        self.framecount = 0
        self.usertime = 1.0
        self.bodies = []
        self.vessels = []
        self.entities = []

        with open(f'data/full.csv') as f:
            data = list(csv.reader(f))
            for entity in data[1:]:
                Body(entity, self, self.focusinput) if entity[1] == 'body' else Vessel(entity, self, self.focusinput)
            #initialise_entities()
            #configure_masses()
            #generate_orbits()

        self.entitylength = len(self.entities)-1
        self.bodylength = len(self.bodies)-1

        self.star.satellites = self.star.bodycentre.satellites + self.star.barycentre.satellites
        self.star.neg_inv_mass = -1/(self.star.bodycentre.mass*sum(planet.barycentre.mass for planet in self.star.satellites))
        self.star.barycentre_transition = 0.5*self.star.barycentre.satellites[0].semi_major_axis

        for body in self.bodies[1:]:
            body.satellites = body.bodycentre.satellites + body.barycentre.satellites
            body.barycentre_transition = 0.5*body.barycentre.satellites[0].semi_major_axis if body.barycentre.satellites else 0.
            body.orbital_environment(self)
