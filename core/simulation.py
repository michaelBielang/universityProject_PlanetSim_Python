from core.body import *
import core.calc as calc
import core.context as _context
import numpy as np

from planetensimulation_progr3gr10.core import context


def __initialize():
    bodies = list()
    sun = Body(name="sun", mass=1.989 * 10**15, radius=0.2)
    earth = Body(name="earth", mass=5.972 * 10**9, radius=0.01)
    earth2 = Body(name="earth", mass=5.972 * 10**9, radius=0.01)
    earth3 = Body(name="earth", mass=5.972 * 10**9, radius=0.01)

    c = context.context(sun);
    c.add(sun)
    c.add(earth)
    c.add(earth2)
    c.add(earth3)
    c.init(- 149.6 * 10**3, 149.6 * 10**3)

    return c

def initialize(num_planet):
    sun = Body(name="sun", mass=1.989 * 10 ** 30, radius=0.2)
    c = context.context(sun)
    c.add(sun)
    for i in range(num_planet):
        planet = Body(name="earth", mass=5.972 * 10**24, radius=0.05)
        c.add(planet)

    c.init(- 149.6 * 10**9, 149.6 * 10**9)
    return c

def sim_calc(context, timestep):
    context.update(timestep)


def sim_calc_loop(context,timestep):
    while True:
        sim_calc(context,timestep)