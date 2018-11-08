import numpy as np

# The gravitational constant G
G = 6.67428e-11


def calculate_and_set_new_velocity(subject, bodies, timeStep):
    """Set velocity based on every planet in the system."""
    acc = np.array([0.0, 0.0, 0.0])

    for other in bodies:
        if other is not subject:
            distance_vector = other.position - subject.position
            distance_length = np.sqrt(distance_vector.item(0)**2
                                      + distance_vector.item(1)**2
                                      + distance_vector.item(2)**2)

            # Only calculate force if bodies not on same position (divide by zero)
            if distance_length is not 0.0:
                # calculate gravity force
                f_total = G * subject.mass*other.mass/(distance_length**2)
                f_vector = (distance_vector/distance_length)*f_total

                # F=m/a -> a=F/m
                acc += f_vector/subject.mass

    # velocity += acceleration*timestep
    subject.velocity += acc*timeStep


def calculate_and_set_new_pos(subject, timeStep):
    """Moves planet with current velocity and given timestep."""

    # position += velocity*timestep
    subject.position += subject.velocity*timeStep