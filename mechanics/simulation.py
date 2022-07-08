import time
import numpy as np
from mechanics.orbit import *
from spacecraft.node import *
from graphics.trace import *
from mechanics.entity import *
from mechanics.body import *
from spacecraft.vessel import *
from mechanics.pertubations import *

def simulation(universe, camera, dt):
    universe.profile.add('buf')
    universe.timestep = (universe.usertime*dt if dt < 0.2 else 0)

    osculating_orbits(universe)
    perturbations(universe)
    recenter(universe)
    rectify(universe,camera)

    universe.time += universe.timestep
    universe.framecount += 1
    for vessel in universe.vessels:
        if vessel.nodes[0].time < universe.time:
            vessel.nodes[0].run(universe)
            vessel.nodes.pop(0)

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

def recenter(universe):
    universe.star.bodycentre.apos = universe.star.barycentre.apos + universe.star.bodycentre.rpos
    for planet in universe.star.satellites:
        planet.barycentre.apos = planet.barycentre.rpos + planet.primary.apos
        planet.bodycentre.apos = planet.bodycentre.rpos + planet.barycentre.apos
        for moon in planet.satellites:
            moon.bodycentre.apos = moon.barycentre.rpos + moon.primary.apos
    #for body in universe.bodies[1:]:
    #    body.barycentre.apos = body.barycentre.rpos + body.primary.apos
    #    body.bodycentre.apos = body.bodycentre.rpos + body.barycentre.apos
    for vessel in universe.vessels:
        vessel.bodycentre.rpos = vessel.barycentre.rpos
        vessel.bodycentre.apos = vessel.barycentre.rpos + vessel.primary.apos
    subtract = -universe.focus_entity.bodycentre.apos
    for entity in universe.entities:
        entity.bodycentre.apos += subtract
        entity.barycentre.apos += subtract
    universe.profile.add('ree')
