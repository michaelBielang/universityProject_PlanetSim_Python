from core import calc
import numpy as np


class context:
    def __init__(self, num_planets):
        self.mass_all = 0.0
        self.context = []
        self.np_bodies = np.zeros((num_planets, 8), dtype=np.float64)

    def add(self, i, mass, radius):
        # NP Array is defind like this np_array[0:3] is the x,y,z position,
        # np_arry[3:6] is the Velocity, np_array[7] is the mass, np_arry[8] is the radius
        temp = np.append(np.zeros(3),np.zeros(3))
        temp = np.append(temp, mass)
        temp = np.append(temp, radius)
        self.np_bodies[i] = temp
        self.mass_all = self.__calc_mass_all()


    def init(self, area_min, area_max):
        for planet in self.np_bodies:
            pos = np.random.uniform(low=area_min, high=area_max, size=(1, 3))
            planet[0:3] = pos[0]

        for planet in self.np_bodies:
            planet[3:6] = calc.calc_inital_velocity(planet, self)


    def update(self, timeStep):
        for planet in self.np_bodies:
            for other in self.np_bodies:
                if np.array_equal(planet,other):
                    continue
                a = calc.calculate_velocity(planet, other)
                planet[3:6]= planet[3:6] +  (a * timeStep)

        for planet in self.np_bodies:
            """Moves planet with current velocity and given timestep."""
            planet[0:3] += timeStep * planet[3:6]

    def add_body_mass(self, i, mass):
        body = self.np_bodies[i]
        body[7] = body[7] * mass


    def __calc_mass_all(self):
        m = 0
        for planet in self.np_bodies:
            m += planet[7]

        return m