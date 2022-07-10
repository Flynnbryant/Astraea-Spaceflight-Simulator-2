import time
import numpy as np
from mechanics.orbit import *
from mechanics.centres import *
from spacecraft.vessel import *

def perturbations(universe):
    ''' loop through all bodies and vessels, applying pertubations if the timestep is sufficiently small to be more accurate than not considering them '''
    for entity in universe.entities[1:]:
        if universe.timestep < 0.02*entity.period:

            ''' Apply pertubations from its grandparent, if it has one. E.g. sun to moon.'''
            if entity.primary.object.primary:
                grandparent_vec = entity.primary.object.barycentre.rpos + entity.barycentre.rpos #THIS IS INCORRECT FOR BODYCENTRE ORBITS. Check vector algebra taking into account parent bodycentre around parent barycentre.
                entity.barycentre.pvel += universe.timestep*entity.primary.object.primary.SGP*((-grandparent_vec/np.linalg.norm(grandparent_vec)**3) - (-entity.primary.object.barycentre.rpos/np.linalg.norm(entity.primary.object.barycentre.rpos)**3))

            ''' Include a term for notable piblings '''

            ''' Correct for parent error '''
            #if entity.isbarycentric:
            if isinstance(entity.primary, Barycentre) and isinstance(entity, Vessel):
                true_vec = entity.primary.object.bodycentre.rpos-entity.barycentre.rpos
                entity.barycentre.pvel += universe.timestep*entity.primary.object.bodycentre.SGP*((true_vec/np.linalg.norm(true_vec)**3) + (entity.barycentre.rpos/np.linalg.norm(entity.barycentre.rpos)**3))

            ''' Apply pertubations from relevant siblings (bodies orbiting around the same parent) '''
            '''
            for sibling in entity.major_siblings:
                pvvec = 0.
                psvec = 0.
                entity.barycentre.pvel += universe.timestep*sibling.barycentre.SGP*(0)
            '''

            ''' Update true positions due to pertubations '''
            entity.barycentre.ppos += entity.barycentre.pvel*universe.timestep
            entity.barycentre.rpos += entity.barycentre.ppos
    universe.profile.add('per')

'''
# Barycentre
    def pv_vec(self, centre, sibling):
        return sibling.primary.bary_request_pv_vec(centre, sibling)

    def ps_vec(self, centre, sibling):
        return sibling.primary.bary_request_ps_vec(centre, sibling)

    def bary_request_pv_vec(self, centre, sibling):
        return sibling.barycentre.rpos-centre.rpos

    def body_request_pv_vec(self, centre, sibling):
        return sibling.barycentre.rpos-(centre.rpos+centre.object.primary.object.bodycentre.rpos)

    def bary_request_ps_vec(self, centre, sibling):
        return centre.rpos/np.linalg.norm(centre.rpos)**3

    def body_request_ps_vec(self, centre, sibling):
        return -sibling.barycentre.rpos/np.linalg.norm(sibling.barycentre.rpos)**3


# Bodycentre
    def pv_vec(self, centre, sibling):
        return sibling.primary.body_request_pv_vec(centre, sibling)

    def ps_vec(self, centre, sibling):
        return sibling.primary.body_request_ps_vec(centre, sibling)

    def bary_request_pv_vec(self, centre, sibling):
        return centre.object.primary.object.bodycentre.rpos + sibling.barycentre.rpos - centre.rpos

    def body_request_pv_vec(self, centre, sibling):
        return sibling.barycentre.rpos-centre.rpos

    def bary_request_ps_vec(self, centre, sibling):
        return -centre.rpos/np.linalg.norm(centre.rpos)**3

    def body_request_ps_vec(self, centre, sibling):
        return 0.
'''

def rectify(universe, camera):
    universe.refresh_object = universe.bodies[(universe.framecount % universe.bodylength)+1]
    universe.refresh_object.barycentre.rvel = elliptical_elements_to_vel(universe.refresh_object) + universe.refresh_object.barycentre.pvel
    state_to_elliptical_elements(universe.refresh_object, universe.refresh_object.barycentre, universe.time)
    universe.refresh_object.barycentre.pvel = np.array([0.,0.,0.],dtype=np.float64)
    universe.refresh_object.barycentre.ppos = np.array([0.,0.,0.],dtype=np.float64)
    if universe.refresh_object.trace in camera.traces:
        universe.refresh_object.trace.calculate_trace()
        universe.refresh_object.label.regenerate_label()

    for vessel in universe.vessels:
        #vessel.nodal_precession = universe.timestep*vessel.primary.object.precession_constant*np.cos(vessel.inclination)/(vessel.sqrta3omu*(vessel.semi_major_axis*vessel.omes)**2)
        vessel.bodycentre.rvel = elliptical_elements_to_vel(vessel) + vessel.barycentre.pvel
        vessel.primary.check_model(universe, vessel)
        state_to_elliptical_elements(vessel, vessel.bodycentre, universe.time)
        vessel.trace.calculate_trace()
        vessel.barycentre.pvel = np.array([0.,0.,0.],dtype=np.float64)
    universe.profile.add('ret')
