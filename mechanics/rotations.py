import numpy as np

def celestial_to_ecliptic(RA, DEC):
    '''
    Inputs:
    * RA and DEC (degrees) - Right ascension and declination coordinates in the
        celestial coordinate system of a given object's axis of rotation. The
        celestial coordinate system is based on the Earth's equator such that
        Earth's rotational axis is at RA undefined and DEC 90 degrees.

    Outputs:
    * tilt_quaternion - An angle and corresponding vector in the ecliptic
        coordinate system required to rotate an object's pole from its default
        position to the correct orientation.

    * axis_vector - The unit vector in the ecliptic coordinate system parallel
        to the object's axis of rotation, about which the object will spin.

    * ECL_to_EQU_matrix - A rotation matrix to convert relative coordinates in
        the ecliptic plane into relative coordinates in the object's equatorial
        plane.

    * EQU_to_ECL_matrix - A rotation matrix to convert relative coordinates in
        the object's equatorial plane into relative coordinates in the ecliptic
        plane.

    Additional Information:
    * Obliquity - The angle between the +z axis of the celestial coordinate
        system and the +z axis of the ecliptic coordinate system. The +x axes
        for both these two systems are equal.
    * CEL_to_ECL_matrix - A rotation matrix to convert coordinates in the
        celestial sphere into the ecliptic coordinate system. When this function
        is considering the Earth, this will be the same as EQU_to_ECL_matrix.
    '''

    Obliquity = np.deg2rad(23.44)
    CEL_to_ECL_matrix = np.matrix([
    [1, 0, 0],
    [0, np.cos(Obliquity), -np.sin(Obliquity)],
    [0, np.sin(Obliquity), np.cos(Obliquity)]])

    RA = np.deg2rad(RA)
    DEC = np.deg2rad(DEC)

    celestial_vec = np.array([np.cos(RA)*np.cos(DEC),np.sin(RA)*np.cos(DEC),np.sin(DEC)])
    axis_vector = np.squeeze(np.asarray(np.dot(celestial_vec,CEL_to_ECL_matrix)))

    default = np.array([0.,0.,1.])
    tilt_vector = np.cross(default,axis_vector)
    tilt_vector /= np.linalg.norm(tilt_vector)
    tilt_angle_rad = np.arccos(np.dot(default,axis_vector)/(np.linalg.norm(default)*np.linalg.norm(axis_vector)))
    tilt_quaternion = tilt_vector.tolist()
    tilt_quaternion.insert(0,np.rad2deg(tilt_angle_rad))

    ECL_to_EQU_matrix = quaternion_rotation_matrix(tilt_angle_rad, tilt_vector)
    EQU_to_ECL_matrix = quaternion_rotation_matrix(tilt_angle_rad, tilt_vector*-1)

    return tilt_quaternion, axis_vector, ECL_to_EQU_matrix, EQU_to_ECL_matrix

def quaternion_rotation_matrix(angle, vec):
    '''
    Calculates and returns a rotation matrix to transform coordinates between frames of reference.

    Inputs:
        * angle (radians) - the angle to rotate the coordinate system by.

        * vec (unit) - the axis of rotation about which to rotate the coordinate system.

    Outputs:
        * rotation_matrix - A transofmration matrix that can be used in matrix multiplication
            to convert coordinates between two frames of reference.
    '''
    cosa = np.cos(angle)
    sina = np.sin(angle)
    omcos = 1-cosa

    rotation_matrix = np.matrix([
    [cosa+omcos*vec[0]**2, omcos*vec[0]*vec[1]-vec[2]*sina, omcos*vec[0]*vec[2]+vec[1]*sina],
    [omcos*vec[0]*vec[1]+vec[2]*sina, cosa+omcos*vec[1]**2, omcos*vec[1]*vec[2]-vec[0]*sina],
    [omcos*vec[0]*vec[2]-vec[1]*sina, omcos*vec[1]*vec[2]+vec[0]*sina, cosa+omcos*vec[2]**2]])

    return rotation_matrix

def rotation_constants(orbit):
    sinw = np.sin(orbit.arg_periapsis)
    cosw = np.cos(orbit.arg_periapsis)
    sino = np.sin(orbit.long_ascending)
    coso = np.cos(orbit.long_ascending)
    sini = np.sin(orbit.inclination)
    cosi = np.cos(orbit.inclination)

    orbit.rotation_matrix = np.array([
    [cosw*coso - sinw*cosi*sino, -(sinw*coso + cosw*cosi*sino)],
    [cosw*sino + sinw*cosi*coso, cosw*cosi*coso - sinw*sino],
    [sinw*sini, cosw*sini]])

    orbit.omes = 1-orbit.eccentricity**2
    orbit.sqrtm = np.sqrt(1-orbit.eccentricity)
    orbit.sqrtp = np.sqrt(1+orbit.eccentricity)
