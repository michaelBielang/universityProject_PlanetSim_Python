import math

import numpy as np
import scipy.constants
from numpy import linalg as LA

from get_data.planet import planet


# ok test
def get_center_of_mass(planets: list):
    """ returns the location of the center of mass"""

    rs = np.array([0.0, 0.0, 0.0], np.float64)

    for planet in planets:
        rs += planet.get_position() * planet.get_mass()

    # rs = 1/M sum m*r
    rs = [rs / get_total_mass(planets)]
    return rs


def get_total_mass(planets: list):
    M = 0.0
    for planet in planets:
        M += planet.get_mass()
    return M


def get_gravitation_force(planet_1: planet, planet_2: planet):
    """
          m1*m2
    G * --------- (r2-r1)
        |r2 - r1|³
    """
    G = scipy.constants.gravitational_constant
    m1 = planet_1.get_mass()
    m2 = planet_2.get_mass()
    zaehler = m1 * m2

    r2_minus_r1 = np.absolute(planet_2.get_position() - planet_1.get_position())
    nenner = math.pow(np.linalg.norm(r2_minus_r1), 3)

    part_1 = G * zaehler / nenner

    return np.array(part_1 * r2_minus_r1)


def get_initial_velocity(planets: list):
    """"get initial velocity"""
    total_mass = get_total_mass(planets)

    for planet in planets:
        speed = get_speed(planet, planets, total_mass)

        speed_direction = get_speed_direction(planet, planets)

        # todo unsicher ob das so hinhaut
        """  
                   (ri - ri,rs)  x z
        v = |v|*  -----------------
                   |(ri - ri,rs) x z |
        """
        planet.set_velocity([speed_direction[0] * speed, speed_direction[1] * speed, speed_direction[2] * speed])


def get_speed_direction(planet: planet, planets):
    """"
    https://de.serlo.org/mathe/geometrie/analytische-geometrie/methoden-vektorrechnung/vektorprodukt/vektor-kreuzprodukt

     v    (ri - ri,rs)  x z
    -- =  -----------------
    |v|   |(ri - ri,rs) x z |

    """

    z = [0, 0, 1]
    # (ri - ri,rs)
    position_center_of_mass_com_and_planet = get_ri_minus_rirs(planet, planets)

    #  |(ri - ri,rs) |
    abs_pos_mass = get_skalar_produkt(position_center_of_mass_com_and_planet)

    zeahler = np.cross(position_center_of_mass_com_and_planet, z)
    nenner = LA.norm(np.cross(abs_pos_mass, z))

    np.divide(zeahler, nenner)
    result = np.division(zeahler, nenner)
    return result


def get_speed(planet: planet, planets: list, total_mass: float):
    """ |v| = (M-mi) / M * sqrt(GM/r)  mit r = | ri-rsi |"""

    M = total_mass
    m = planet.get_mass()
    G = scipy.constants.gravitational_constant
    r = get_skalar_produkt(get_ri_minus_rirs(planet, planets))
    return (M - m) / M * math.sqrt((G * M) / r)


def get_skalar_produkt(array: np.array):
    """
    | (ri - ri,rs) |
    Betrag von Vektor = sqrt(x²+y²+z²)
    """

    variable_x = math.pow(array[0], 2)
    variable_y = math.pow(array[1], 2)
    variable_z = math.pow(array[2], 2)
    # Betrag der Vektoren
    # https://de.serlo.org/mathe/geometrie/analytische-geometrie/methoden-vektorrechnung/skalarprodukt/skalarprodukt
    return math.sqrt(variable_x + variable_y + variable_z)


def get_ri_minus_rirs(planet: planet, planets: list):
    """
    (ri - ri,rs)
     Masseschwerpunkt zwischen Masseschwerpunkt und Planet
     """

    return planet.get_position() - get_center_of_mass(planets)
