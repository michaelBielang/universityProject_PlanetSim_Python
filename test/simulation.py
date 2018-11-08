from core.body import *
import core.calc as calc
import matplotlib.pyplot as plt

# time between calculations in seconds
timestep=700000

bodies = list()
sun = Body(name="sun", mass=1.989 * 10**30,
           position=np.array([0.0, 0.0, 0.0]),
           velocity=np.array([0.0, 0.0, 0.0]))
earth = Body(name="earth", mass=5.972 * 10**24,
             position=np.array([- 149.6 * 10**9, 0.0, 0.0]),
             velocity=np.array([0.0, 29800.0, 0.0]))

bodies.append(sun)
bodies.append(earth)


# plotXList = list()
# plotYList = list()
# plotXList.append(sun.position.item(0))
# plotYList.append(sun.position.item(1))
# plotXList.append(earth.position.item(0))
# plotYList.append(earth.position.item(1))
# counter = 0

while True:
    for body in bodies:
        calc.calculate_and_set_new_velocity(body, bodies, timestep)

    for body in bodies:
        calc.calculate_and_set_new_pos(body, timestep)

    # plotXList.append(bodies[1].position.item(0))
    # plotYList.append(bodies[1].position.item(1))
    #
    # counter += 1

    # if counter >= 100:
    #     i=1
    #     plt.plot(plotXList[0], plotYList[0], 'ro')
    #     while i<len(plotXList):
    #         plt.plot(plotXList[i], plotYList[i], 'yo')
    #         i += 1
    #     plt.axis('equal')
    #     plt.show()
    #     counter=0
