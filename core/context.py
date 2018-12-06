import multiprocessing

import numpy as np

from core import calc


class context:
    def __init__(self, num_planets):
        self.mass_all = 0.0
        self.context = []
        self.np_bodies = np.zeros((num_planets, 9), dtype=np.float64)
        self.SCALE_FACTOR = 0.0
        self.TimeStep = 30000
        m = multiprocessing.Manager()
        self.InputQueue = m.JoinableQueue()
        self.OutputQueue = m.Queue()
        self.id_count = 0
        self.partial_list = np.array_split(self.np_bodies,multiprocessing.cpu_count()-1)

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
            pos = np.random.uniform(low=area_min, high=area_max, size=(1, 3))
            planet[0:3] = pos[0]

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

    def InitParralelWorkers(self):
        """
        Starts the Workers,
        :param self: Needs a context
        :return: None
        """

        #Setup Executor pool with number of CPU Cores
        self.executor = multiprocessing.pool.ThreadPool(1)
        for i in range(1):
            self.executor.apply_async(context.ExecutionWorker,args=(self.InputQueue,self.OutputQueue,self.np_bodies,self.TimeStep))


    @staticmethod
    def ExecutionWorker(InputQueue,OutputQueue,np_bodies,timeStep):
        """
        Execution Worker for parralel Calculation of the Acceleration
        :param InputQueue:
        :param OutputQueue:
        :return:
        """
        while True:
            #Check if new Work exists
            Task = InputQueue.get()
            if Task != None:
                #Do work
                for planet in Task:
                    calc_acceleration = 0
                    for other in np_bodies:
                        calc_acceleration += calc.calculate_velocity(planet, other)
                    # Setup Output Array [vx,vy,vz,id]
                    new_acc = np.concatenate(planet[3:6] + timeStep * calc_acceleration,np.array(planet[9]))
                    OutputQueue.put(new_acc)
                    InputQueue.task_done()
            elif Task == 0:
                #Exit no Work anymore
                break

    def updateWorkers(self):

        for work in self.partial_list:
            self.InputQueue.put(work)

        # Join my Workers together
        self.InputQueue.join()

        for _ in range(len(self.np_bodies)):
            # Reasamble List
            item = self.OutputQueue()
            self.np_bodies[item[4]][3:6] = item

        ## Step is finished


