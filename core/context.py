from core import calc
import numpy as np


class context:
    def __init__(self, centre=None):
        self.bodies = []
        self.mass_all = 0.0
        self.centre = centre
        self.context = []

    def add(self, body):
        self.bodies.append(body)
        self.mass_all = self.__calc_mass_all()

    def remove(self, body):
        self.bodies.remove(body)
        self.mass_all = self.__calc_mass_all()

    def init(self, area_min, area_max):
        for planet in self.bodies:
            pos = np.random.uniform(low=area_min, high=area_max, size=(1, 3))
            planet.position = pos[0]
            print(planet.position)

        for planet in self.bodies:
            planet.velocity = calc.calc_inital_velocity(planet, self)


    def update(self, timeStep):
        for planet in self.np_array:
            for other in self.np_array:
                if np.array_equal(planet,other):
                    continue
                a = calc.calculate_velocity(planet, other)
                planet.velocity += timeStep * a

        for planet in self.np_array:
            """Moves planet with current velocity and given timestep."""
            planet[0:3] += timeStep * planet[3:6]

    def add_body_mass(self, _body, mass):
        body = self.bodies[_body]
        body.mass = body.mass * mass


    def __calc_mass_all(self):
        m = 0
        for b in self.bodies:
            m += b.mass

        return m