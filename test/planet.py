import numpy as np


class planet:

    def __init__(self, mass, name, pos_x, pos_y, pos_z, v_x, v_y, v_z):
        self.mass = mass
        self.name = name
        self.position = np.array(pos_x, pos_y, pos_z)
        self.velocity = np.array(v_x, v_y, v_z)

    def get_position(self):
        return np.array(self.position)

    def get_velocity(self):
        return self.velocity

    def set_position(self, new_position):
        self.position = new_position

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def get_mass(self):
        return self.mass
