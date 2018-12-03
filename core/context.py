import multiprocessing

import numpy as np

from core import calc


class context:
    def __init__(self, num_planets):
        self.mass_all = 0.0
        self.context = []
        self.np_bodies = np.zeros((num_planets, 8), dtype=np.float64)
        self.SCALE_FACTOR = 0.0
        self.TimeStep = 30000
        self.InputQueue = multiprocessing.JoinableQueue()
        self.OutputQueue = multiprocessing.Queue()

    def add(self, i, mass, radius):
        """
        Add a Body to the Context (Universe)
        :param i: the body index in the Array
        :param mass: the mass of the body
        :param radius: the radius of the body
        :return:
        """
        # NP Array is defind like this np_array[0:3] is the x,y,z position,
        # np_arry[3:6] is the Velocity, np_array[6] is the mass, np_arry[7] is the radius
        temp = np.append(np.zeros(3), np.zeros(3))
        temp = np.append(temp, mass)
        temp = np.append(temp, radius)
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
    self.executor = multiprocessing.Pool(multiprocessing.cpu_count())
    for i in range(multiprocessing.cpu_count()):
        self.executor.apply(ExecutionWorker,args=(self.InputQueue,self.OutputQueue,self.np_bodies))


@staticmethod
def ExecutionWorker(InputQueue,OutputQueue,np_bodies):
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
                OutputQueue.put(calc_acceleration)
                InputQueue.task_done()
        elif Task == 0:
         #Exit no Work anymore
         break

def updateWorkers(self):
    for work in self.partial_list:
        self.InputQueue.put()

    # Join my Workers together
    self.InputQueue.join()
    
    for output in self.OutputQueue:
        # Reasamble List
        test = 0;

    ## Step is finished


