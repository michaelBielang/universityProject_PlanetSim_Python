from core.body import *
import core.calc as calc


def initialize():
    bodies = list()
    sun = Body(name="sun", mass=1.989 * 10**30, radius=0.2,
               position=np.array([0.0, 0.0, 0.0]),
               velocity=np.array([0.0, 0.0, 0.0]))
    earth = Body(name="earth", mass=5.972 * 10**24,
                 position=np.array([- 149.6 * 10**9, 0.0, 0.0]), radius=0.1,
                 velocity=np.array([0.0, 29800.0, 0.0]))
    earth2 = Body(name="earth", mass=5.972 * 10**24,
                  position=np.array([- 100.6 * 10**9, 0.0, 0.0]), radius=0.1,
                  velocity=np.array([0.0, 26800.0, 0.0]))
    earth3 = Body(name="earth", mass=5.972 * 10**24,
                  position=np.array([145.6 * 10**9, 0.0, 0.0]), radius=0.1,
                  velocity=np.array([0.0, 29800.0, 0.0]))
    bodies.append(sun)
    bodies.append(earth)
    bodies.append(earth2)
    bodies.append(earth3)

    return bodies


def sim_calc(bodies, timestep):
    for body in bodies:
        calc.calculate_and_set_new_velocity(body, bodies, timestep)

    for body in bodies:
        calc.calculate_and_set_new_pos(body, timestep)

def sim_calc_loop(bodies,timestep):
    while True:
        sim_calc(bodies,timestep)