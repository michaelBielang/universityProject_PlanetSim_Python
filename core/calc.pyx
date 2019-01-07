"""Module for calculation"""
#import math
import cython

import numpy as np
cimport libc.math as math

# The gravitational constant G
cdef double G = 6.67428e-11

def calc_inital_velocity(body, context):
    """
    Calculates the Initial Velocity of random bodies
    :param body: the current body to calculate
    :param context: the current context
    :return: the velocity
    """
    z = np.array([0.0, 0.0, 1.0])

    # get the center of mass
    pos_mass_centre = sum([b[6] * b[0:3] for b in context.np_bodies if not np.array_equal(b, body)]) \
        / (context.mass_all - body[6])

    # get distance from current body from center
    body_distance = body[0:3] - pos_mass_centre
    body_distance_length = np.sqrt((body_distance*body_distance).sum())

    body_distance_z = np.cross(body_distance, z)
    body_distance_length_z = np.sqrt((body_distance_z*body_distance_z).sum())

    mass_dif = context.mass_all - body[6]
    velocity = (mass_dif / context.mass_all) * \
        math.sqrt(G * context.mass_all / body_distance_length)

    return velocity / body_distance_length_z * body_distance_z


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
def calculate_velocity(double[:] planet, double[:] other):
    """Set velocity based on every planet in the system."""

    # Changed to Memory Views for Cython, no numpy used
    cdef double[3] distance_vector
    cdef double distance_length
    cdef double f_total
    cdef double[3] f_vector
    cdef double[3] return_value

    with nogil:

        distance_vector[0] = other[0] - planet[0]
        distance_vector[1] = other[1] - planet[1]
        distance_vector[2] = other[2] - planet[2]

        # math is ok because we change math to cimport libc.math as math

        distance_length = math.sqrt(
            distance_vector[0]*distance_vector[0] +
            distance_vector[1]*distance_vector[1] +
            distance_vector[2]*distance_vector[2])



        # Only calculate force if bodies not on same position

        # (divide by zero)

        if distance_length != 0:

            # calculate gravity force
            f_total = G * planet[6] * other[6] / (distance_length*distance_length)
            f_vector[0] = (distance_vector[0] / distance_length) * f_total
            f_vector[1] = (distance_vector[1] / distance_length) * f_total
            f_vector[2] = (distance_vector[2] / distance_length) * f_total
            # F=m/a -> a=F/m
            # acc += f_vector/planet[6]

            return_value[0] = f_vector[0] / planet[6]
            return_value[1] = f_vector[1] / planet[6]
            return_value[2] = f_vector[2] / planet[6]

    return np.array(return_value)

