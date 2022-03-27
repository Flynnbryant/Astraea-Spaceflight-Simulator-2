import numpy as np
from mechanics.elliptical_elements import *
from mechanics.hyperbolic_elements import *
from mechanics.utilities import *
from mechanics.centres import *

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
        vessel.bodycentre.pvel = new_vector()
