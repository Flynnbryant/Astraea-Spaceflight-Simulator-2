import time
import numpy as np
from mechanics.orbit import *
from spacecraft.node import *
from graphics.trace import *
from mechanics.entity import *
from mechanics.body import *
from spacecraft.vessel import *
from mechanics.pertubations import *

def simulation(universe, dt):
    universe.profile.add('buf')
    universe.timestep = (universe.usertime*dt if dt < 0.1 else 0)

    osculating_orbits(universe)
    perturb_bodies(universe)
    perturb_vessels(universe)

    universe.time += universe.timestep
    universe.framecount += 1
    if universe.nodes[0].time < universe.time:
        universe.nodes[0].run(universe)
        universe.nodes.pop(0)
    universe.profile.add('ves')

def osculating_orbits(universe):
    ''' Begin by assuming a perfect elliptical osculating orbit for each object. '''
    for entity in universe.entities[1:]:
        entity.mean_anomaly = (entity.epoch_anomaly + (universe.time-entity.epoch_time)*entity.mean_motion)%(2*np.pi)
        entity.barycentre.rpos = elliptical_elements_to_pos(entity, entity.mean_anomaly) if entity.eccentricity < 1 else hyperbolic_elements_to_pos(entity, entity.mean_anomaly)

    ''' Using conservation of momentum, calculate the positions of the sun and planets relative to their barycentres '''
    for planet in universe.star.satellites:
        planet.bodycentre.rpos = -planet.bodycentre.inverse_mass*sum((moon.barycentre.rpos * moon.barycentre.mass) for moon in planet.barycentre.satellites)
    universe.star.bodycentre.rpos = -universe.star.bodycentre.inverse_mass*sum((planet.barycentre.rpos * planet.barycentre.mass) for planet in universe.star.barycentre.satellites)
    universe.profile.add('osc')
