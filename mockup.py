class Planet(object):
    def __init__(self, i):

sun = [1.989110e30, 6.9550810e6, -1.318179998275412E+06, 4.010555758878363E+05, -4.493504117531995E-03, -1.503318013232030E-02]
mercury = [3.302210e23, 2.439710e3, 4.183977317411777E+07, -4.422147843777118E+07, 2.534767960872066E+01, 3.616526476323813E+01]
venus = [4.868510e24, 6.051810e3, -8.208050566798364E+07, -7.152072408769740E+07, 2.303847371249511E+01, -2.633317430531520E+01]

planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

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