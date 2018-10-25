import numpy as np
from numpy import linalg as LA
import math
import scipy.constants


def get_center_of_mass(planets):
    """ returns the location of the center of mass"""

    mass_position = [0.0, 0.0, 0.0]

    for planet in planets:
        mass_position += [position * planet.get_mass() for position in planet.get_position()]

    # rs = 1/M sum m*r
    mass_position = [position * (1 / get_total_mass(planets)) for position in mass_position]
    return mass_position


def get_total_mass(planets):
    M = 0.0
    for planet in planets:
        M += planet.get_mass()
    return M


def get_gravitation_force(planet_1, planet_2):
    """
          m1*m2
    G * --------- (r2-r1)
        |r2 - r1|³
    """
    G = scipy.constants.gravitational_constant
    m1 = planet_1.getMass()
    m2 = planet_2.getMass()
    zaehler = m1 * m2

    x = planet_1.get_position()[0] - planet_2.get_position()[0]
    y = planet_1.get_position()[0] - planet_2.get_position()[0]
    z = planet_1.get_position()[0] - planet_2.get_position()[0]
    nenner = math.pow(get_pos_mass_abs([x, y, z]), 3)

    part_1 = G * zaehler / nenner

    # todo check ob korrekt. Was wenn pos p2 > pos p1 dann wäre x negativ?
    return [x * part_1, y * part_1, z * part_1]


def get_initial_velocity(planet, planets):
    """"get initial velocity"""

    speed = get_speed(planet, planets)

    speed_direction = get_speed_direction(planet, planets)

    # todo unsicher ob das so hinhaut
    """  
               (ri - ri,rs)  x z
    v = |v|*  -----------------
               |(ri - ri,rs) x z |
    """
    v = [speed_direction[0] * speed, speed_direction[1] * speed, speed_direction[2] * speed]


def get_speed_direction(planet, planets):
    """"
    https://de.serlo.org/mathe/geometrie/analytische-geometrie/methoden-vektorrechnung/vektorprodukt/vektor-kreuzprodukt

     v    (ri - ri,rs)  x z
    -- =  -----------------
    |v|   |(ri - ri,rs) x z |

    """

    z = [0, 0, 1]
    # (ri - ri,rs)
    position_center_of_mass_com_and_planet = get_r(planet, planets)

    #  |(ri - ri,rs) |
    abs_pos_mass = get_pos_mass_abs(position_center_of_mass_com_and_planet)

    zeahler = np.cross(position_center_of_mass_com_and_planet, z)
    nenner = LA.norm(np.cross(abs_pos_mass, z))

    np.divide(zeahler, nenner)
    result = np.division(zeahler, nenner)
    return result


def get_speed(planet, planets):
    """ |v| = (M-mi) / M * sqrt(GM/r)  mit r = | ri-rsi |"""

    M = get_total_mass(planets)
    m = planet.get_mass()
    G = scipy.constants.gravitational_constant
    r = get_pos_mass_abs(get_r(planet, planets))
    return (M - m) / M * math.sqrt((G * M) / r)


def get_pos_mass_abs(position_center_of_mass_com_and_planet):
    """
    | (ri - ri,rs) |
    Betrag von Vektor = sqrt(x²+y²+z²)
    """

    variable_x = math.pow(position_center_of_mass_com_and_planet[0], 2)
    variable_y = math.pow(position_center_of_mass_com_and_planet[1], 2)
    variable_z = math.pow(position_center_of_mass_com_and_planet[2], 2)
    # Betrag der Vektoren
    # https://de.serlo.org/mathe/geometrie/analytische-geometrie/methoden-vektorrechnung/skalarprodukt/skalarprodukt
    return math.sqrt(variable_x + variable_y + variable_z)


def get_r(planet, planets):
    """
    (ri - ri,rs)
     Masseschwerpunkt zwischen Masseschwerpunkt und Planet
     """
    counter = 0
    position_center_of_mass_com_and_planet = [0, 0, 0]
    for position_center_of_mass in get_center_of_mass(planets):
        position_center_of_mass_com_and_planet[counter] = position_center_of_mass - (
                position_center_of_mass + planet.get_position()[counter])
        counter += 1
    return position_center_of_mass_com_and_planet
