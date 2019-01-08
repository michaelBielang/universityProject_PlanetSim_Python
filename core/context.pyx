import cython
import os
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
import multiprocessing
import sys
cdef double G = 6.67428e-11
cimport libc.math as math

import numpy as np

from core import calc, taskmanager
from calc cimport calculate_velocity


class context:
    def __init__(self, num_planets):
        self.mass_all = 0.0
        self.context = []
        self.np_bodies = np.zeros((num_planets, 9), dtype=np.float64)
        self.SCALE_FACTOR = 0.0
        self.SCALE_Z = 0.2
        self.TimeStep = 30000
        self.InputQueue = multiprocessing.Queue()
        self.OutputQueue = multiprocessing.Queue()
        self.id_count = 0
        self.cycle_id = 0
        self.connected_workers = 0
        self.exit_notify = False
        self.taskmanager_class = taskmanager.TaskManager()
        if num_planets != 1:
            self.taskmanager_class.startup(self)

    def add(self, i, mass, radius):
        """
        Add a Body to the Context (Universe)
        :param i: the body index in the Array
        :param mass: the mass of the body
        :param radius: the radius of the body
        :return:
        """
        # NP Array is defind like this np_array[0:3] is the x,y,z position,
        # np_arry[3:6] is the Velocity, np_array[6] is the mass, np_arry[7] is the radius, np_array[8] is the ID
        temp = np.zeros(6)
        temp = np.append(temp, mass)
        temp = np.append(temp, radius)
        temp = np.append(temp, self.id_count)
        self.id_count += 1
        self.np_bodies[i] = temp
        self.mass_all = self.__calc_mass_all()

    def init(self, area_min, area_max):
        """
        Set the area_in and area_max defined by the user
        :param area_min:
        :param area_max:
        :return:
        """
        for i in range(1, len(self.np_bodies)):
            self.np_bodies[i][0:3] = np.asarray([np.random.uniform(low=area_min, high=area_max),
                                      np.random.uniform(low=area_min, high=area_max),
                                      np.random.uniform(low=area_min, high=area_max) * self.SCALE_Z])

        for planet in self.np_bodies:
            planet[3:6] = calc.calc_inital_velocity(planet, self)

    def update(self, timeStep):
        """
        Update the Universe by timeStep
        :param timeStep: timeStep of the calculation (should be small, else we have to much miss calculation)
        :return:
        """
        for planet in self.np_bodies:
            for other in self.np_bodies:
                # Removed because its faster to calculate than compare two numpy arrays
                # if np.array_equal(planet,other):
                #    continue
                a = calc.calculate_velocity(planet, other)
                planet[3:6] = planet[3:6] + timeStep * a

        for planet in self.np_bodies:
            """Moves planet with current velocity and given timestep."""
            planet[0:3] += timeStep * planet[3:6]

    def add_body_mass(self, i, mass):
        """
        Add the Body Mass to the NP Array[i]
        :param i: The Position in the NP Array
        :param mass: The Mass to set
        :return:
        """
        body = self.np_bodies[i]
        body[6] = body[6] * mass

    def __calc_mass_all(self):
        """
        Calculate the mass of all Planets
        :return:
        """
        m = 0
        for planet in self.np_bodies:
            m += planet[6]

        return m

    def ExitParralelWorkers(self):
        """
        Exit the Parralel Workers
        :return:
        """
        if(self.executor is None):
            raise ValueError("InitParralelWorkers has to be called befor exiting the Workers")

        self.exit_notify = True
        #for _ in range(self.executor):
        #    self.InputQueue().put(-1)

    def InitParralelWorkers(self, server_ip="localhost"):
        """
        Starts the Workers,
        :param self: Needs a context
        :return: None
        """#

        self.Taskmanager = taskmanager.TaskManager().clientConnect(server_ip)
        self.executor = multiprocessing.Pool()
        for i in range(multiprocessing.cpu_count()):
            p = Process(target=context.ExecutionWorker,args=(server_ip,self.TimeStep,self.exit_notify))
            p.start()
        return True


    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    @staticmethod
    def ExecutionWorker(server_ip,timeStep_to_calc,exit_notify):
        """
        Execution Worker for parralel Calculation of the Acceleration
        :param InputQueue:
        :param OutputQueue:
        :return:
        """

        #print("Execution Worker started with PID: " + str(os.getpid()))

        # Setup Proxy Connect
        Taskmanager = taskmanager.TaskManager().clientConnect(server_ip)
        InputQueue, OutputQueue, data_proxy, cycle_proxy = Taskmanager.get_job_queue(), Taskmanager.get_result_queue(), Taskmanager.get_data(), Taskmanager.get_cycle()

        # Write Info to Master
        worker_info_proxy = Taskmanager.set_worker_info()
        import socket
        hostname = socket.gethostname()

        # ""=""Execution Worker started with PID: " + str(os.getpid()) + "on Host" + hostname

        worker_info_proxy.update({hostname + "/" + str(os.getpid()):(hostname,os.getpid())})

        #
        #test2 = data_proxy.get()
        #data_proxy.set(np.zeros(9,dtype=np.float64))
        #test2 = data_proxy.get()
        #
        cdef double[3] distance_vector = np.zeros(3)
        cdef double distance_length
        cdef double f_total
        cdef int timeStep = timeStep_to_calc
        cdef double[3] f_vector = np.zeros(3)
        #cdef double[3] return_value
        #
        cdef int cycle_id = -1
        cdef int master_cycle = -1
        cdef double[3] calc_acceleration = np.zeros(3)
        cdef double[:] planet = np.zeros(9)
        cdef double[:] other = np.zeros(9)
        #cdef double[3] current_calc
        cdef int planet_count = len(data_proxy.get('p'))
        cdef double[:, :] np_bodies = np.zeros_like(data_proxy.get('p'))
        cdef double[7] np_body = np.zeros(7)
        #cdef planet
        cdef int other_num = 0
        cdef int planet_num = 0
        #np_bodies = 0
        result = 0
        cdef double[3] new_velocity
        new_position = 0
        while True:
            #Check if new Work exists
            planet_num = InputQueue.get()
            if exit_notify is not True:
                #Do work
                # Reduce Network Traffic
                #t1 = time.time()
                master_cycle = cycle_proxy.get('c')
                if master_cycle != cycle_id:
                    np_bodies = data_proxy.get('p')
                    cycle_id = master_cycle
                #t2 = time.time()

                calc_acceleration[0] = 0
                calc_acceleration[1] = 0
                calc_acceleration[2] = 0
                f_vector[0] = 0
                f_vector[1] = 0
                f_vector[2] = 0
                f_total = 0
                #planet[:] = 0



                for other_num in range(planet_count):

                    with nogil:
                        other = np_bodies[other_num]
                        planet = np_bodies[planet_num]

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

                        #print(distance_length)

                        if distance_length != 0:

                            # calculate gravity force
                            f_total = G * planet[6] * other[6] / (distance_length*distance_length)
                            f_vector[0] = (distance_vector[0] / distance_length) * f_total
                            f_vector[1] = (distance_vector[1] / distance_length) * f_total
                            f_vector[2] = (distance_vector[2] / distance_length) * f_total
                            # F=m/a -> a=F/m
                            # acc += f_vector/planet[6]

                        calc_acceleration[0] += f_vector[0] / planet[6]
                        calc_acceleration[1] += f_vector[1] / planet[6]
                        calc_acceleration[2] += f_vector[2] / planet[6]

                        #current_calc = calc.calculate_velocity(planet, other)
                        #calc_acceleration[0] = current_calc[0]
                        #calc_acceleration[1] = current_calc[1]
                        #calc_acceleration[2] = current_calc[2]

                    #new_velocity = planet[3:6] + timeStep * calc_acceleration

                    np_body[3] = planet[3] + timeStep * calc_acceleration[0]
                    np_body[4] = planet[4] + timeStep * calc_acceleration[1]
                    np_body[5] = planet[5] + timeStep * calc_acceleration[2]

                    #new_position = planet[0:3] + new_velocity*timeStep

                    np_body[0] = planet[0] + np_body[3]*timeStep
                    np_body[1] = planet[1] + np_body[4]*timeStep
                    np_body[2] = planet[2] + np_body[5]*timeStep

                    np_body[6] = planet[8]

                #print(np.array(np_body))

                OutputQueue.put(np.array(np_body))
                #InputQueue.task_done()
                #t3 = time.time()

                #print("Get Data" +str(t2-t1))
                #print("Calc Data" +str(t3-t2))
            if exit_notify is True:
                #Exit no Work anymore
                #InputQueue.task_done()
                break

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    def updateWorkers(self):

        self.taskmanager_class.dict_position["p"] = self.np_bodies
        self.taskmanager_class.dict_cycle["c"] = self.cycle_id

        #workers = len(self.taskmanager_class.dict_worker_info)

        #if  workers != self.connected_workers:
        #    self.taskmanager_class.print_worker_info(self.connected_workers,workers)
        #    self.connected_workers = workers

        #print(self.taskmanager_class.dict_worker_info)


        for work in range(self.id_count):
            self.InputQueue.put(work)


        # Reasamble List
        cdef int i = 0
        #cdef current_item

        while i != self.id_count:
            item = self.OutputQueue.get(block=True)
            # Set new Position
            #print(self.np_bodies)
            #print(item)
            self.np_bodies[int(item[6])][0:6] = item[0:6]
            #self.np_bodies[int(item[6])][3:6] = item[3:6]
            i += 1

        ## Join my Workers together
        #self.InputQueue.join()

        #Create a Cycle ID for the worker to see if its the current iteration
        #and not to load the full np array each time
        if self.cycle_id == 1:
            self.cycle_id = 0
        else:
            self.cycle_id = 1

        ## Step is finished
