import configparser
from core.body import *
import core.calc as calc
import numpy as np
from core.context import context


def initialize():
    bodies = list()

    c = context()
    conf = configparser.ConfigParser()
    conf.read("config.ini")
    i = 0
    for section in conf.sections():
        name = conf[section]['name']
        mass = float(conf[section]['mass'])
        radius = float(conf[section]['radius'])
        pos = np.array([float(conf[section]['xPos']), float(conf[section]['yPos']), float(conf[section]['zPos'])])
        vel = np.array([float(conf[section]['xVel']), float(conf[section]['yVel']), float(conf[section]['zVel'])])
        c.add(i, mass=mass, radius=radius)
        c.np_bodies[i][0:3] = pos
        c.np_bodies[i][3:6] = vel
        i += 1

    c.centre = c.bodies[0]
    return c

def initialize_random(num_planet):

    c = context(num_planet + 1)
    c.add(i=0, mass=1.989 * 10 ** 30, radius=0.2) # Sonne
    for i in range(1,num_planet+1):
        c.add(i=i, mass=5.972 * 10**24, radius=0.05)

    c.init(- 149.6 * 10**9, 149.6 * 10**9)
    return c


def sim_calc(bodies, timestep):
    for body in bodies:
        calc.calculate_and_set_new_velocity(body, bodies, timestep)

def sim_calc(context, timestep):
    context.update(timestep)


def sim_calc_loop(context,timestep):
    while True:
        sim_calc(context,timestep)