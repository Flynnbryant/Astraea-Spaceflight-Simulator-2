import time
import numpy as np
from scipy.optimize import brentq
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
        entity.orbit.mean_anomaly = (entity.orbit.epoch_anomaly + (universe.time-entity.orbit.epoch_time)*entity.orbit.mean_motion)%(2*np.pi)
        entity.orbit.eccentric_anomaly = brentq(eccentric_anomaly,-0.1,6.3,args=(entity.orbit.eccentricity, entity.orbit.mean_anomaly),xtol=1e-9)
        arglist = [entity.orbit.sqrtp, entity.orbit.eccentric_anomaly, entity.orbit.sqrtm, entity.orbit.semi_major_axis, entity.orbit.eccentricity, entity.orbit.rotation_matrix]
        entity.orbit.true_anomaly, entity.orbit.rel_dist, entity.barycentre.rpos = faster_elements_to_pos(*arglist) if entity.orbit.eccentricity < 1 else faster_hyperbolic_elements_to_pos(*arglist)

    ''' Using conservation of momentum, calculate the positions of the sun and planets relative to their barycentres '''
    for planet in universe.star.satellites:
        planet.bodycentre.rpos = -planet.bodycentre.inverse_mass*sum((moon.barycentre.rpos * moon.barycentre.mass) for moon in planet.barycentre.satellites)
    universe.star.bodycentre.rpos = -universe.star.bodycentre.inverse_mass*sum((planet.barycentre.rpos * planet.barycentre.mass) for planet in universe.star.barycentre.satellites)
    universe.profile.add('osc')

def rectify(universe, camera):
    for entity in universe.entities:
        entity.barycentre.ppos += entity.barycentre.pvel*universe.timestep
        entity.barycentre.rpos += entity.barycentre.ppos
    universe.star.bodycentre.apos = universe.star.barycentre.apos + universe.star.bodycentre.rpos
    for planet in universe.star.satellites:
        planet.barycentre.apos = planet.barycentre.rpos + planet.primary.apos
        planet.bodycentre.apos = planet.bodycentre.rpos + planet.barycentre.apos
        for moon in planet.satellites:
            moon.bodycentre.apos = moon.barycentre.rpos + moon.primary.apos
    for vessel in universe.vessels:
        vessel.bodycentre.rpos = vessel.barycentre.rpos
        vessel.bodycentre.apos = vessel.barycentre.rpos + vessel.primary.apos
    subtract = -universe.focus_entity.bodycentre.apos
    for entity in universe.entities:
        entity.barycentre.apos += subtract
        entity.bodycentre.apos += subtract
    universe.profile.add('rec')

    universe.refresh_object = universe.bodies[(universe.framecount % universe.bodylength)+1]
    universe.refresh_object.barycentre.rvel = universe.refresh_object.orbit.elliptical_elements_to_vel() + universe.refresh_object.barycentre.pvel
    universe.refresh_object.orbit.state_to_elements(universe.refresh_object.barycentre, universe.time)
    universe.refresh_object.barycentre.pvel = np.array([0.,0.,0.],dtype=np.float64)
    universe.refresh_object.barycentre.ppos = np.array([0.,0.,0.],dtype=np.float64)
    if universe.refresh_object.trace in camera.traces:
        universe.refresh_object.trace.points = np.dot(universe.refresh_object.orbit.rotation_matrix,faster_calculate_trace(universe.refresh_object.orbit.eccentricity, universe.refresh_object.trace.trace_detail, universe.refresh_object.orbit.semi_major_axis, universe.refresh_object.orbit.semi_minor_axis, universe.refresh_object.orbit.periapsis))

    for vessel in universe.vessels:
        #vessel.nodal_precession = universe.timestep*vessel.primary.object.precession_constant*np.cos(vessel.inclination)/(vessel.sqrta3omu*(vessel.semi_major_axis*vessel.omes)**2)
        vessel.barycentre.rvel = (vessel.orbit.elliptical_elements_to_vel() if vessel.orbit.eccentricity <1 else vessel.orbit.hyperbolic_elements_to_vel()) + vessel.barycentre.pvel
        vessel.primary.check_model(universe, vessel)
        vessel.orbit.state_to_elements(vessel.barycentre, universe.time)
        vessel.trace.points = np.dot(vessel.orbit.rotation_matrix,faster_calculate_trace(vessel.orbit.eccentricity, vessel.trace.trace_detail, vessel.orbit.semi_major_axis, vessel.orbit.semi_minor_axis, vessel.orbit.periapsis))
        vessel.barycentre.pvel = np.array([0.,0.,0.],dtype=np.float64)
    universe.profile.add('ref')
