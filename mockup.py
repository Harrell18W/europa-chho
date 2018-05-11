class Planet(object):
    def __init__(self, i):

earthInfo = [mass, radius, posx

planets = [sun, venus, mercury, earth, mars, jupiter, saturn, neptune, uranus, pluto]

dt = 3600 # 1 Hour

for planet in planets:
    planet.force = 0
    for otherPlanet in planets:
        if otherPlanet is not planet:
            planet.force += (G*planet.mass*otherPlanet.mass)/planet.distTo(OtherPlanet)

for planet in planets:
    plane.update(dt)

class Planet(object):
    def distTo(self, other):
        return ((self.x-other.x)**2+(self.y-other.y)**2)
    def update(self, dt):
        self.p += self.force*dt
        self.vel = self.p/self.mass
        self.pos += self.vel*dt

