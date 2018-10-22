import numpy as np
from numpy import linalg as LA


def get_center_of_mass(planets):
    """ returns the location of the center of mass"""

    # total Mass
    M = 0.0
    mass_position = [0.0, 0.0, 0.0]

    for planet in planets:
        mass_position += [position * planet.get_mass() for position in planet.get_position()]
        M += planet.get_mass()

    # rs = 1/M sum m*r
    mass_position = [position * (1 / M) for position in mass_position]
    return mass_position


def get_initial_velocity(planet, planets):
    """"get initial velocity"""

    # | ri - ri,rs | x z
    #  -----------------
    # |(ri - ri,rs) x z |

    # pos planet - pos center of mass
    cleaned_pos_betrag = [0, 0, 0]
    cleaned_post = [0, 0, 0]
    z = [0, 0, 1]
    counter = 0
    for position_center_of_mass in get_center_of_mass(planets):
        # für den Zähler
        cleaned_pos_betrag[counter] = abs(
            position_center_of_mass - (position_center_of_mass + planet.get_position()[counter]))
        # für den Nenner
        cleaned_post[counter] = cleaned_pos_betrag[counter] = (
                position_center_of_mass - (position_center_of_mass + planet.get_position()[counter]))
        counter += 1

        zeahler = np.cross(cleaned_pos_betrag, z)
        nenner = LA.norm(np.cross(cleaned_post, z))

        result = np.division(zeahler, nenner)

    ## todo
