import planet
import math
import numpy as np
from get_data import get_data


def start_default_sim():
    planet_earth = planet.planet(5.97 * math.pow(10, 24), "Earth", 1, 0, 1, 2, 0, 2)
    sun = planet.planet(1.98 * math.pow(10, 30), "Sun", 0, 0, 0, 0, 0, 0)
    planet_list = [planet_earth, sun]
    center_of_mass = get_data.get_center_of_mass(planet_list)
    print("center of mass: " + str(center_of_mass))
    total_mass = get_data.get_total_mass(planet_list)
    print("total mass: " + str(total_mass))
    print(get_data.get_gravitation_force(planet_earth, sun))
    get_data.get_initial_velocity(planet_list)


start_default_sim()
