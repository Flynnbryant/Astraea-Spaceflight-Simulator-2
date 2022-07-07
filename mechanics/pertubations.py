import time
import numpy as np
from mechanics.orbit import *
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

def perturb_vessels(universe):
    ''' loop through all objects to apply pertubations if the timestep is sufficiently small to be accurate '''
    for vessel in universe.vessels:
        vessel.bodycentre.rpos = vessel.barycentre.rpos
        #vessel.bodycentre.rpos = np.ravel(np.matmul(vessel.primary.object.EQU_to_ECL_matrix,vessel.barycentre.rpos))

        if universe.timestep < 0.01 * vessel.period:

            ''' perturb vessel by its grandparent, if it has one '''
            if vessel.primary.object.primary:
                vesselvec = vessel.primary.object.barycentre.rpos + vessel.bodycentre.rpos
                vessel.bodycentre.pvel += -universe.timestep * vessel.primary.object.primary.SGP*((vesselvec/np.linalg.norm(vesselvec)**3)-(vessel.primary.object.barycentre.rpos/np.linalg.norm(vessel.primary.object.barycentre.rpos)**3))

            ''' perturb vessel by the true position of the primary planet, if orbiting around barycentre '''
            if isinstance(vessel.primary, Barycentre):
                true_vec = vessel.primary.object.bodycentre.rpos-vessel.bodycentre.rpos
                vessel.bodycentre.pvel += universe.timestep*vessel.primary.object.bodycentre.SGP*((true_vec/np.linalg.norm(true_vec)**3) + (vessel.bodycentre.rpos/np.linalg.norm(vessel.bodycentre.rpos)**3))

            ''' perturb vessel by its siblings (other objects orbiting around the same primary object) '''
            for sibling in vessel.primary.object.satellites:
                pvvec = vessel.primary.pv_vec(vessel.bodycentre, sibling)
                pvdis = np.linalg.norm(pvvec)
                vessel.bodycentre.pvel += universe.timestep*sibling.barycentre.SGP*((pvvec/pvdis**3)+vessel.primary.ps_vec(vessel.bodycentre, sibling))
                if pvdis < sibling.SOI:
                    vessel.change_primary(universe, sibling, barycentre=True)

        ''' update vessel true position based on pertubations '''
        vessel.bodycentre.rpos += vessel.bodycentre.pvel*universe.timestep
        vessel.bodycentre.apos = vessel.bodycentre.rpos + vessel.primary.apos
        vessel.nodal_precession = universe.timestep*vessel.primary.object.precession_constant*np.cos(vessel.inclination)/(vessel.sqrta3omu*(vessel.semi_major_axis*vessel.omes)**2)
        #vessel.bodycentre.rpos = np.ravel(np.matmul(vessel.primary.object.ECL_to_EQU_matrix,vessel.bodycentre.rpos.T).T)
        #vessel.bodycentre.rvel = elliptical_elements_to_vel(vessel) + np.ravel(np.matmul(vessel.primary.object.ECL_to_EQU_matrix,vessel.bodycentre.pvel.T).T)
        vessel.bodycentre.rvel = elliptical_elements_to_vel(vessel) + vessel.bodycentre.pvel
        vessel.primary.check_model(universe, vessel)
        state_to_elliptical_elements(vessel, vessel.bodycentre, universe.time)
        vessel.trace.calculate_trace()
        vessel.bodycentre.pvel = np.array([0.,0.,0.],dtype=np.float64)
