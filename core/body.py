import numpy as np


class Body:
    """Subclass of Turtle representing a gravitationally-acting body.

    Extra attributes:
    mass : mass in kg
    vx, vy: x, y velocities in m/s
    px, py: x, y positions in m
    """

    def __init__(self, name, mass, position, velocity):
        """Initialize Body

        Parameter:
        name(str)
        mass(float)
        position(numpy.array[3-dimensional])
        velocity(numpy.array[3-dimensional])
        """
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity

