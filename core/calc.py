"""Module for calculation"""

import numpy as np
import copy
import core.body

# The gravitational constant G
G = 6.67428e-11


def calculate_and_set_new_velocity(subject, bodies, timestep):
    """Set velocity based on every planet in the system."""

    acc = np.zeros(3)

    for other in bodies:
        if other is not subject:
            distance_vector = other.position - subject.position
            distance_length = np.sqrt(distance_vector.item(0)**2
                                      + distance_vector.item(1)**2
                                      + distance_vector.item(2)**2)

            # Only calculate force if bodies not on same position
            # (divide by zero)
            if distance_length is not 0.0:
                # calculate gravity force
                f_total = G * subject.mass*other.mass/(distance_length**2)
                f_vector = (distance_vector/distance_length)*f_total

                # F=m/a -> a=F/m
                acc += f_vector/subject.mass

    subject_return = core.body.Body(subject.name,subject.mass,np.copy(subject.position), subject.velocity,subject.radius)
    #subject_return = copy.deepcopy(subject)

    # velocity += acceleration*timestep
    subject_return.velocity += acc*timestep

    subject_return.position += subject_return.velocity*timestep

    return subject_return
