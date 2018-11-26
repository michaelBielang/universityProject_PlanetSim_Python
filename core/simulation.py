import copy

from core.body import *
import core.calc as calc
import numpy as np
import multiprocessing
from threading import Thread


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

def chunks(l, n):
    # For item i in a range that is a length of l,
    if (n == 1):
        return l
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

def sim_calc(bodies, timestep):

    # Minus current Thread
    free_cores = multiprocessing.cpu_count() -1
    #free_cores = 1 # Just for Profiling
    threads = []
    results = []
    #objects = copy.deepcopy(bodies)
    objects = bodies

    if(free_cores != 1):
        for partial_list in chunks(objects,free_cores):
            threads.append(Thread(target=sim_calc_partitial, args=(partial_list,bodies, 70000,results)))
    else:
        threads.append(Thread(target=sim_calc_partitial, args=(bodies,bodies, 70000,results)))

    for s in threads:
        s.start()

    for thread in threads:
        thread.join()

    for current_cody in range(len(bodies)):
        bodies[current_cody] = results[current_cody]




    #calc.calculate_and_set_new_velocity(body, bodies, timestep)

    #for body in bodies:
    #    calc.calculate_and_set_new_pos(body, timestep)

def sim_calc_partitial(partial_list,bodies,timestep,results):

    for subject in partial_list:
        import cProfile
        results.append(calc.calculate_and_set_new_velocity(subject,bodies,timestep))



