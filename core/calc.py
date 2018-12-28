"""Module for calculation"""
import math

import numpy as np

# The gravitational constant G
G = 6.67428e-11

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


def calculate_velocity(planet, other):
    """Set velocity based on every planet in the system."""

    distance_vector = other[0:3] - planet[0:3]
    distance_length = math.sqrt(
        math.pow(distance_vector[0], 2) + math.pow(distance_vector[1], 2) +
        math.pow(distance_vector[2], 2))

    # Only calculate force if bodies not on same position
    # (divide by zero)
    if distance_length != 0:
        # calculate gravity force
        f_total = G * planet[6] * other[6] / (distance_length**2)
        f_vector = (distance_vector / distance_length) * f_total

        # F=m/a -> a=F/m
        # acc += f_vector/planet[6]
        return f_vector / planet[6]

    return 0
