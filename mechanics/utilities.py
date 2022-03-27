import numpy as np

def eccentric_anomaly(E, e, M):
    return E - e*np.sin(E) - M

def hyperbolic_anomaly(H, e, M):
    return e*np.sinh(H) - H - M

def rotation_constants(entity):
   sinw = np.sin(entity.arg_periapsis)
   cosw = np.cos(entity.arg_periapsis)
   sino = np.sin(entity.long_ascending)
   coso = np.cos(entity.long_ascending)
   sini = np.sin(entity.inclination)
   cosi = np.cos(entity.inclination)

   entity.rotation_matrix = np.array([
   [cosw*coso - sinw*cosi*sino, -(sinw*coso + cosw*cosi*sino)],
   [cosw*sino + sinw*cosi*coso, cosw*cosi*coso - sinw*sino],
   [sinw*sini, cosw*sini]])

   entity.omes = 1-entity.eccentricity**2
   entity.sqrtm = np.sqrt(1-entity.eccentricity)
   entity.sqrtp = np.sqrt(1+entity.eccentricity)

def sn(datastr):
    datalist = datastr.replace(',','').lower().split('e')
    return np.float64(datalist[0])*10**int(datalist[1])

def new_vector(data=[0.,0.,0.]):
    return np.array(data,dtype=np.float64)

def major_siblings(body):
    major_siblings = []
    for sibling in body.primary.object.satellites:
        if sibling is not body and sibling.barycentre.mass > 1e20:
            major_siblings.append(sibling)
    return major_siblings
