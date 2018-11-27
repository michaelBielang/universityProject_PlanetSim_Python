import copy
import configparser

from core.body import *
import core.calc as calc
import numpy as np
import multiprocessing
from threading import Thread


def initialize():
    bodies = list()

    conf = configparser.ConfigParser()
    conf.read("config.ini")
    for section in conf.sections():
        name = conf[section]['name']
        mass = float(conf[section]['mass'])
        radius = float(conf[section]['radius'])
        pos = np.array([float(conf[section]['xPos']), float(conf[section]['yPos']), float(conf[section]['zPos'])])
        vel = np.array([float(conf[section]['xVel']), float(conf[section]['yVel']), float(conf[section]['zVel'])])
        body = Body(name=name, mass=mass, radius=radius, position=pos, velocity=vel)
        bodies.append(body)

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
            threads.append(Thread(target=sim_calc_partitial, args=(partial_list,bodies, timestep,results)))
    else:
        threads.append(Thread(target=sim_calc_partitial, args=(bodies,bodies, timestep,results)))

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



