import configparser

import random

import numpy as np

from core.context import context


def update_scale_factor(c):
    maxdistance = 0.0
    for body in c.np_bodies:
        if maxdistance < distance_between_two(c.np_bodies[0], body):
            maxdistance = distance_between_two(c.np_bodies[0], body)
    c.SCALE_FACTOR = maxdistance


def distance_between_two(body1, body2):
    distance_vector = body2[0:3] - body1[0:3]
    distance_length = np.sqrt(distance_vector[0]**2 + distance_vector[1]**2 +
                              distance_vector[2]**2)
    return distance_length


def initialize():
    conf = configparser.ConfigParser()
    conf.read("config.ini")
    i = 0
    name = list()
    mass = list()
    radius = list()
    pos = list()
    vel = list()
    for section in conf.sections():
        name.append(conf[section]['name'])
        mass.append(float(conf[section]['mass']))
        radius.append(0.02)  # float(conf[section]['radius']))
        pos.append(
            np.array([
                float(conf[section]['xPos']),
                float(conf[section]['yPos']),
                float(conf[section]['zPos'])
            ]))
        vel.append(
            np.array([
                float(conf[section]['xVel']),
                float(conf[section]['yVel']),
                float(conf[section]['zVel'])
            ]))

        i += 1

    c = context(i)
    i = 0
    while i < len(name):
        c.add(i, mass=mass[i], radius=radius[i])
        c.np_bodies[i][0:3] = pos[i]
        c.np_bodies[i][3:6] = vel[i]
        i += 1
    c.centre = c.np_bodies[0]
    update_scale_factor(c)
    return c


def initialize_random(num_planet, area_min, area_max, mass_max):
    """
    Initialize the Random Universe
    :param num_planet:  The num of planets specified by the user
    :param area_min:  The area_min specified by the user
    :param area_max:  The area_max specified by the user
    :param mass_max:  The mass_max specified by the user
    :return: Returns the context
    """
    c = context(num_planet + 1)
    c.add(i=0, mass=1.989 * 10**30, radius=0.2)  # Sonne
    for i in range(1, num_planet + 1):
        c.add(
            i=i,
            mass=random.uniform(1, mass_max),
            radius=random.uniform(0.02, 0.1))

    c.init(area_min, area_max)  # - 149.6 * 10**9, 149.6 * 10**9)
    update_scale_factor(c)
    return c
