import numpy as np

# The gravitational constant G
G = 6.67428e-11

def CalculateAndSetNewVelocity(subject, allPlanets, timeStep):
    """Set velocity based on every planet in the system."""
    a_X = 0.0
    a_Y = 0.0
    a_Z = 0.0

    for other in allPlanets:
        if other is not self:
            dx = (other.pos_X-self.pos_X)
            dy = (other.pos_Y-self.pos_Y)
            dz = (other.pos_Z-self.pos_Z)
            d = np.sqrt(dx**2 + dy**2 + dz**2)

            #Nur wenn die Körper nicht an selber Position sind
            if d is not 0.0:
                #Gravitationskraft berechnen
                F = G * self.mass*other.mass/(d**2)
                F_X = (dx/d)*F
                F_Y = (dy/d)*F
                F_Z = (dz/d)*F

                #F=m/a -> a=F/m
                a_X += F_X/self.mass
                a_Y += F_Y/self.mass
                a_Z += F_Z/self.mass

    #Geschwindigkeit += Beschleunigung*Zeitschritt
    self.vel_X += a_X*timeStep
    self.vel_Y += a_Y*timeStep
    self.vel_Z += a_Z*timeStep

    #Position += Geschwindigkeit*Zeitschritt
def CalculateAndSetNewPos(self, timeStep):
    """Moves planet with current velocity and given timestep."""
    self.pos_X += self.vel_X*timeStep
    self.pos_Y += self.vel_Y*timeStep
    self.pos_Z += self.vel_Z*timeStep