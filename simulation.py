import math

import matplotlib.pyplot as plt

from get_data import get_data


# def start_default_sim_test():
#     planet_earth = planet.planet(5.97 * math.pow(10, 24), "Earth", 1, 0, 1, 2, 0, 2)
#     sun = planet.planet(1.98 * math.pow(10, 30), "Sun", 0, 0, 0, 0, 0, 0)
#     planet_list = [planet_earth, sun]
#     center_of_mass = get_data.get_center_of_mass(planet_list)
#     total_mass = get_data.get_total_mass(planet_list)
#
#     get_data.get_initial_velocity(planet_list)
#     # print(get_data.get_speed_direction(planet_earth, planet_list))


def start_default_sim():
    planet_earth = get_data.planet(5.97 * math.pow(10, 24), "Earth", 1, 0, 1, 2, 0, 2)
    sun = get_data.planet(1.98 * math.pow(10, 30), "Sun", 0, 0, 0, 0, 0, 0)
    planet_list = [planet_earth, sun]
    get_data.get_initial_velocity(planet_list)
    for x in range(0, 100, 1):
        for planet in planet_list:
            print(planet.get_velocity())
            print(planet.get_position())


def plot_test_2():
    plt.setp('ro', 'animated')
    plt.plot([1, 1, 3, 4])
    plt.ylabel('some numbers')
    plt.show()


start_default_sim()
