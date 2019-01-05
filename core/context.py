import os
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
import multiprocessing
import sys

import numpy as np

from core import calc, taskmanager


class context:
    def __init__(self, num_planets):
        self.mass_all = 0.0
        self.context = []
        self.np_bodies = np.zeros((num_planets, 9), dtype=np.float64)
        self.SCALE_FACTOR = 0.0
        self.TimeStep = 30000
        self.InputQueue = multiprocessing.JoinableQueue()
        self.OutputQueue = multiprocessing.Queue()
        self.id_count = 0
        self.cycle_id = 0
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
        for planet in self.np_bodies:
            planet[0:2] = np.random.uniform(low=area_min, high=area_max, size=(1,2))[0]
            planet[2:2] = np.random.uniform(-0.000000000001, 0.000000000001)

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


    @staticmethod
    def ExecutionWorker(server_ip,timeStep,exit_notify):
        """
        Execution Worker for parralel Calculation of the Acceleration
        :param InputQueue:
        :param OutputQueue:
        :return:
        """

        print("Execution Worker starteded with PID: " + str(os.getpid()))

        # Setup Proxy Connect

        Taskmanager = taskmanager.TaskManager().clientConnect(server_ip)
        InputQueue, OutputQueue, np_bodies_proxy, cycle_id_proxy = Taskmanager.get_job_queue(), Taskmanager.get_result_queue(), Taskmanager.get_np_bodies(), Taskmanager.get_cycle_id()

        #

        #test = np_bodies_proxy._getvalue().get()
        #test2 = np_bodies_proxy.get()
        #np_bodies_proxy.set(np.zeros(9,dtype=np.float64))
        #test2 = np_bodies_proxy.get()
        cycle_id = -1
        #np_bodies = 0
        #result = 0
        #new_velocity = 0
        #new_position = 0
        #cdef int calc_acceleration = 0
        while True:
            #Check if new Work exists
            planet = InputQueue.get()
            if planet is not None and exit_notify is not True:
                #Do work
                # Reduce Network Traffic
                if(cycle_id_proxy.get()) != cycle_id:
                 np_bodies = np_bodies_proxy.get()
                 cycle_id = cycle_id_proxy.get()
                calc_acceleration = 0
                for other in np_bodies:
                    calc_acceleration += calc.calculate_velocity(np_bodies[planet], other)
                new_velocity = np_bodies[planet][3:6] + timeStep * calc_acceleration
                new_position = np_bodies[planet][0:3] + new_velocity*timeStep
                result = np.append(new_position,new_velocity)
                result = np.append(result,np_bodies[planet][8])
                OutputQueue.put(result)
                InputQueue.task_done()
            if exit_notify is True:
                #Exit no Work anymore
                #InputQueue.task_done()
                break

    def updateWorkers(self):

        #self.Taskmanager.get_np_bodies().set(self.np_bodies)
        #self.Taskmanager.get_cycle_id().set(self.cycle_id)
        # Set Index as Work
        for work in range(self.id_count):
            self.InputQueue.put(work)

        # Join my Workers together
        #self.Taskmanager.joinQueue()

        self.InputQueue.join()

        for _ in range(self.id_count):
            # Reasamble List
            item = self.OutputQueue.get()
            # Set new Position
            self.np_bodies[int(item[6])][0:3] = item[0:3]
            self.np_bodies[int(item[6])][3:6] = item[3:6]

        #Create a Cycle ID for the worker to see if its the current iteration
        #and not to load the full np array each time
        if self.cycle_id == 1:
            self.cycle_id = 0
        else:
            self.cycle_id = 1

        #self.taskmanager_class.context = self
        #self.taskmanager_class.set_np_bodies(self.np_bodies)
        #self.taskmanager_class.np_bodies.set_cycle_id(self.cycle_id)
        #test = self.Taskmanager
        #self.taskmanager_class.np_bodies.set(self.np_bodies)
        #self.taskmanager_class.cycle_id.set(self.cycle_id)
        self.Taskmanager.get_np_bodies().set(self.np_bodies)
        self.Taskmanager.get_cycle_id().set(self.cycle_id)


        ## Step is finished