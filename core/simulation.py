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
    for section in conf.sections():
        name = conf[section]['name']
        mass = float(conf[section]['mass'])
        radius = float(conf[section]['radius'])
        pos = np.array([float(conf[section]['xPos']), float(conf[section]['yPos']), float(conf[section]['zPos'])])
        vel = np.array([float(conf[section]['xVel']), float(conf[section]['yVel']), float(conf[section]['zVel'])])
        body = Body(name=name, mass=mass, radius=radius)
        body.position = pos
        body.velocity = vel
        c.add(body)

    c.centre = c.bodies[0]
    return c

def initialize_random(num_planet):
    sun = Body(name="sun", mass=1.989 * 10 ** 30, radius=0.2)
    c = context(sun)
    c.add(sun)
    for i in range(num_planet):
        planet = Body(name="earth", mass=5.972 * 10**24, radius=0.05)
        c.add(planet)

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