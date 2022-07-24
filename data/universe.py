import numpy as np
import time
import csv

from analysis.profile import *
from spacecraft.node import *
from mechanics.body import *
from mechanics.entity import *
from mechanics.pertubations import *
from spacecraft.vessel import *

class Universe:
    def __init__(self, focus, profile):
        self.profile = Profile(profile)
        self.focusinput = focus

    def populate(self):
        self.grav_constant = 6.67430*10**-11    #Universal gravitational constant
        self.c = 299792458                      #Speed of light, in m/s
        self.g = 9.80665                        #Standard gravity, in m/s^2
        self.time = 1640995200                  #Unix time for 2022 Jan 1st 00:00, the simulation start point
        self.framecount = 0
        self.usertime = 1.0
        self.bodies = []
        self.vessels = []
        self.entities = []

        with open('data/initial_conditions/bodies.csv') as file:
            data = list(csv.reader(file))
            for body in data[1:]:
                body = [item.strip() for item in body]
                Body(body, self, self.focusinput)

        with open('data/initial_conditions/vessels.csv') as file:
            data = list(csv.reader(file))
            for vessel in data[1:]:
                vessel = [item.strip() for item in vessel]
                Vessel(vessel, self, self.focusinput)

        self.entitylength = len(self.entities)
        self.bodylength = len(self.bodies)-1

        for entity in self.entities[1:]:
            personal_primary_mass(entity)
            rotation_constants(entity.orbit)
            entity.bodycentre.rpos = entity.orbit.elliptical_elements_to_pos(entity.orbit.mean_anomaly)
            entity.bodycentre.rvel = entity.orbit.elliptical_elements_to_vel()
            entity.orbit.state_to_elements(entity.bodycentre, self.time)
            entity.trace = Trace(entity, 52, True)

        self.star.satellites = self.star.bodycentre.satellites + self.star.barycentre.satellites
        self.star.barycentre_transition = 0.5*self.star.barycentre.satellites[0].orbit.semi_major_axis
        for body in self.bodies[1:]:
            body.satellites = body.bodycentre.satellites + body.barycentre.satellites
            body.barycentre_transition = 0.5*body.barycentre.satellites[0].orbit.semi_major_axis if body.barycentre.satellites   else np.inf
            body.hill = body.orbit.semi_major_axis*(1-body.orbit.eccentricity)*np.cbrt(body.barycentre.mass/(3*body.primary.mass))
            body.SOI = body.orbit.semi_major_axis*(body.barycentre.mass/body.primary.mass)**(0.4)
            body.outer_label_distance = body.orbit.semi_major_axis * np.log10(body.mean_radius)
            body.inner_label_distance = 0.05 * body.outer_label_distance

    def read_initial_elements(self, entity):
        with open(f'data/initial_conditions/horizons_elements/{entity.name}.txt') as file:
            flag = False
            for line in file:
                if flag:
                    elements = line.split(',')
                    break
                elif '$$SOE' in line:
                    flag = True

        entity.orbit.semi_major_axis    = 1000*sn(elements[11])
        entity.orbit.eccentricity       = sn(elements[2])
        entity.orbit.inclination        = np.deg2rad(sn(elements[4]))
        entity.orbit.arg_periapsis      = np.deg2rad(sn(elements[6]))
        entity.orbit.long_ascending     = np.deg2rad(sn(elements[5]))
        entity.orbit.mean_anomaly       = np.deg2rad(sn(elements[9]))

    def read_initial_TLE(self, entity):
        with open(f'data/initial_conditions/spacecraft_TLE/{entity.name}.txt') as file:
            linelist = [line for line in file]

        entity.orbit.semi_major_axis    = np.cbrt(entity.primary.SGP/(float(linelist[2][52:63])*7.2722052166431e-5)**2)
        entity.orbit.eccentricity       = float('0.'+linelist[2][26:33])
        entity.orbit.inclination        = np.deg2rad(float(linelist[2][8:16]))
        entity.orbit.arg_periapsis      = np.deg2rad(float(linelist[2][34:42]))
        entity.orbit.long_ascending     = np.deg2rad(float(linelist[2][17:25]))
        entity.orbit.mean_anomaly       = np.deg2rad(float(linelist[2][43:51]))

def sn(datastr):
    datalist = datastr.replace(',','').lower().split('e')
    return np.float64(datalist[0])*10**int(datalist[1])
