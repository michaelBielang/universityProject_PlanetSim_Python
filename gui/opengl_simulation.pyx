"""opengl"""

import sys

import numpy as np

from gui.galaxy_renderer.simulation_constants import END_MESSAGE

__FPS = 60

# __DELTA_ALPHA = 0.01

# def _move_bodies(bodies,bodies_list):
#    """
#    Updates the Position of the Bodies
#    :param bodies: The NP Array for the Pipe
#    :param bodies_list: The Body List deliverd by the Sinmulation
#    :return:
#    """
#    for body_index, body in enumerate(bodies):
#        body[0] = bodies_list[body_index].x
#        body[1] = bodies_list[body_index].y
#        body[2] = bodies_list[body_index].z
#    time.sleep(1/__FPS)


def _move_bodies(bodies, bodies_list, scale, col = False):
    """
    Initialises the needed NP Array for transfering the Position of the
    Bodys over the Pipe
    :param bodies_list: List of Bodies
    :return: The NP Array for Pipe Transport
    """

    if bodies is None:
        # If bodies is not initialised
        if col:
            bodies = np.zeros((bodies_list.__len__(), 8), dtype=np.float64)
        else:
            bodies = np.zeros((bodies_list.__len__(), 4), dtype=np.float64)

    for body_index in range(bodies_list.__len__()):
        bodies[body_index] = np.append(bodies_list[body_index][0:3] / scale,
                                       bodies_list[body_index][7])

    # time.sleep(1/__FPS)
    return bodies


def startup(sim_pipe, context):
    """
    Initialise and continuously update a position list.
    Results are sent through a pipe after each update step

    :param sim_pipe: (multiprocessing.Pipe) Pipe to send results
    :param bodies_list: The Body List deliverd by the Sinmulation
    :return:
    """

    bodies = None

    # Whithout FPS lock
    # import threading
    # thread = threading.Thread(target=s.sim_calc_loop,
    #           args=(bodies_list,70000))
    # thread.daemon = True                            # Daemonize thread
    # thread.start()                                  # Start the execution

    # NP Array is defind like this np_array[0:3] is the x,y,z position,
    # np_arry[3:6] is the Velocity, np_array[7] is the mass, np_arry[8] is the radius

    context.InitParralelWorkers()
    while True:
        if sim_pipe.poll():
            message = sim_pipe.recv()
            if isinstance(message, str) and message == END_MESSAGE:
                print('simulation exiting ...')
                context.ExecutionWorker()
                sys.exit(0)

        #context.update(10000)
        context.updateWorkers()
        # s.sim_calc(bodies_list,70000)

        bodies = _move_bodies(bodies, context.np_bodies, context.SCALE_FACTOR)

        sim_pipe.send(bodies)
