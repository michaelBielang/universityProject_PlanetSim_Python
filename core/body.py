"""Holds variables for the simulation."""
import numpy as np

class Body:
    """Subclass of Turtle representing a gravitationally-acting body.

    Extra attributes:
    mass : mass in kg
    vx, vy: x, y velocities in m/s
    px, py: x, y positions in m
    """
    SCALE_FACTOR = 450 * 10 ** 9

    def __init__(self, name, mass, radius):
        """Initialize Body

        Parameter:
        name(str)
        mass(float)
        position(numpy.array[3-dimensional])
        """
        self.name = name
        self.mass = mass
        self.position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.radius = radius
