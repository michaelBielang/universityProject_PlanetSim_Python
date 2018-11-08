import numpy as np


class planet:

    def __init__(self, mass, name, pos_x, pos_y, pos_z, v_x, v_y, v_z):
        self.__mass = mass
        self.__name = name
        self.__position = np.array([pos_x, pos_y, pos_z], np.float64)
        self.__velocity = np.array([v_x, v_y, v_z], np.float64)

    def get_position(self) -> np.array:
        return self.__position

    def get_velocity(self):
        return self.__velocity

    def set_position(self, new_position: np.array):
        self.__position = new_position

    def set_velocity(self, new_velocity: np.array):
        self.__velocity = new_velocity

    def get_mass(self):
        return self.__mass
