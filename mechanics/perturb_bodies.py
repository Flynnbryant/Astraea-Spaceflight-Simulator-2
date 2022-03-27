import time
import numpy as np
from mechanics.elliptical_elements import *
from mechanics.hyperbolic_elements import *
from mechanics.utilities import *
from mechanics.centres import *

def perturb_bodies(universe):
    ''' loop through all objects to apply pertubations if the timestep is sufficiently small to be accurate'''
    for body in universe.bodies[1:]:
        if universe.timestep < 0.01 * body.period:

            ''' apply pertubations from the sun to the orbit of all moons '''
            if body.primary.object.primary:
                sun_to_moon_vec = body.primary.object.barycentre.rpos + body.barycentre.rpos
                body.barycentre.pvel += universe.timestep*body.primary.object.primary.SGP*((-sun_to_moon_vec/np.linalg.norm(sun_to_moon_vec)**3) - (-body.primary.object.barycentre.rpos/np.linalg.norm(body.primary.object.barycentre.rpos)**3))

            ''' apply pertubations from siblings (other bodies orbiting around the same object) '''
            for sibling in body.major_siblings:
                pvvec = body.primary.pv_vec(body.barycentre, sibling)
                body.barycentre.pvel += universe.timestep*sibling.barycentre.SGP*((pvvec/np.linalg.norm(pvvec)**3)+body.primary.ps_vec(body.barycentre, sibling))

            ''' adjust position due to the pertubations '''
            body.barycentre.ppos += body.barycentre.pvel*universe.timestep
            body.barycentre.rpos += body.barycentre.ppos
    universe.profile.add('per')

    ''' update absolute positions of all objects for rendering '''
    universe.star.bodycentre.apos = universe.star.barycentre.apos + universe.star.bodycentre.rpos
    for planet in universe.star.satellites:
        planet.barycentre.apos = planet.barycentre.rpos + planet.primary.apos
        planet.bodycentre.apos = planet.bodycentre.rpos + planet.barycentre.apos
        for moon in planet.satellites:
            moon.bodycentre.apos = moon.barycentre.rpos + moon.primary.apos

    ''' select a body to rectify the osculating orbit based on pertubations it has recieved since last rectified '''
    universe.refresh_object = universe.bodies[(universe.framecount % universe.bodylength)+1]
    universe.refresh_object.barycentre.rvel = elliptical_elements_to_vel(universe.refresh_object) + universe.refresh_object.barycentre.pvel
    state_to_elliptical_elements(universe.refresh_object, universe.refresh_object.barycentre, universe.time)
    #universe.refresh_object.trace.calculate_trace()
    universe.refresh_object.barycentre.pvel = np.array([0.,0.,0.],dtype=np.float64)
    universe.refresh_object.barycentre.ppos = np.array([0.,0.,0.],dtype=np.float64)
    universe.profile.add('rec')
