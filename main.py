from vpython import *

AU = 149597871000
G = 6.67384E-11

scene.width = 1600
scene.height = 900

def keyInput(evt):
    s = evt.key
    if s == 'esc':
        scene.waitfor('keydown')

scene.bind('keydown', keyInput)

def forceOf(planet, otherPlanet):
    global G
    r = planet.pos - otherPlanet.pos
    rmag = mag(r)
    runit = norm(r)
    return -(G*planet.mass*otherPlanet.mass)/(rmag**2)*runit

def updatePlanet(planet, dt):
    planet.momentum += planet.force*dt
    planet.velocity = planet.momentum/planet.mass
    planet.pos += planet.velocity*dt

data = open("data.txt", 'r')
planetData = []
planetNames = []
for line in data:
    line = str(line)[:-2]
    vals = line.split()
    varname, mass, rad, posx, posy, posz, velx, vely, velz = vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8]
    planetNames.append(varname)
    comm = varname + 'Info = [' + mass + ', ' + rad + ', ' + posx + ', ' + posy + ', ' + posz + ', ' + velx + ', ' + vely + ',' + velz + ']'
    exec(comm)
    comm = 'planetData.append(' + varname + 'Info)'
    exec(comm)

print(planetNames)

for i in range(len(planetData)):
    print(list(locals().keys())[list(locals().values()).index(planetData[i])], '=', planetData[i])

planets = []
planetLabels = []

for i in range(len(planetNames)):
    comm = planetNames[i] + 'pos = vec(' + planetNames[i] + 'Info[2] , ' + planetNames[i] + 'Info[3], ' + planetNames[i] + 'Info[4])'
    exec(comm)
    comm = planetNames[i] + 'vel = vec(' + planetNames[i] + 'Info[5] , ' + planetNames[i] + 'Info[6], ' + planetNames[i] + 'Info[7])'
    exec(comm)
    comm = 'R' + planetNames[i] + ' = ' + planetNames[i] + 'Info[1]'
    exec(comm)
    comm = 'M' + planetNames[i] + ' = ' + planetNames[i] + 'Info[0]'
    exec(comm)

    comm = planetNames[i] + ' = sphere(pos=' + planetNames[i] + 'pos, radius=R' + planetNames[i] + ', color=color.green, make_trail=True, retain=1000)'
    exec(comm)
    
    comm = planetNames[i] + '.mass = M' + planetNames[i]
    exec(comm)

    comm = planetNames[i] + '.velocity = ' + planetNames[i] + 'vel'
    exec(comm)

    comm = 'planets.append(' + planetNames[i] + ')'
    exec(comm)

tstr = "Time: {:.0f} days".format(0)
tlabel = label(pos=vector(0, 20*AU, 0), text=tstr)
launchstr = 'Click to Start'
launchlabel=label(pos=vector(0, -20*AU, 0), text=launchstr)

dt = 3600
day = 24*3600
t = 0

for planet in planets:
    planet.momentum = planet.velocity*planet.mass

for i in range(len(planetNames)):
    comm = 'pstr = "' + planetNames[i] + '"'
    exec(comm)

    comm = planetNames[i] + 'label = label(pos=vector(0, 1.2*R' + planetNames[i] + ', 0) + ' + planetNames[i] + 'pos , text = pstr)'
    exec(comm)

    comm = 'planetLabels.append(' + planetNames[i] + 'label)'
    exec(comm)

while True:

    if t == 0:
        launchstr = "Click to Start"
        launchlabel.text = launchstr
        scene.waitfor('click')
        launchstr = "Running..."
        launchlabel.text = launchstr

    for planet in planets:
        planet.force = vec(0, 0, 0)
        for otherPlanet in planets:
            if otherPlanet is not planet:
                planet.force += forceOf(planet, otherPlanet)
        updatePlanet(planet, dt)
    
    for i, label in enumerate(planetLabels):
        comm = 'position = vector(0, 1.2*R' + planetNames[i] + ', 0) + ' + planetNames[i] + '.pos'
        exec(comm)
        #print(position)
        
        label.pos = position

    t += dt
    tstr = "Time: {:0f} days".format(t/day)
    tlabel.text = tstr


    
