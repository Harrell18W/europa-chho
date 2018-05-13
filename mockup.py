from math import sqrt

def magnitude(x, y):
    return sqrt(x**2 + y**2)

class Vec(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mag = magnitude(x, y)
    def __add__(self, otherVector):
        self.x += otherVector.x
        self.y += otherVector.y
        self.updateMag()
    def __sub__(self, otherVector):
        self.x -= otherVector.x
        self.y -= otherVector.y
        self.updateMag()
    def updateMag(self):
        self.mag = magnitude(self.x, self.y)

class Planet(object):
    def __init__(self, info):
        self.mass = info[0]
        self.radius = info[1]
        self.pos = Vec(info[3], info[4])
        self.vel = Vec(info[4], info[5])
        self.p = self.mass * self.vel.mag
    def distTo(self, other):
        return ((self.pos.x-other.pos.x)**2+(self.pos.y-other.pos.y)**2)
    def update(self, dt):
        self.p += self.force*dt
        self.vel = self.p/self.mass
        self.pos += self.vel*dt

planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

dt = 3600 # 1 Hour

for planet in planets:
    planet.force = 0
    for otherPlanet in planets:
        if otherPlanet is not planet:
            planet.force += (G*planet.mass*otherPlanet.mass)/planet.distTo(OtherPlanet)

for planet in planets:
    planet.update(dt)