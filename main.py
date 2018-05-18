from datetime import datetime, timedelta
from vpython import *

# Closest Europa Approach:
# launchDay = 72.7
# launchDir = -4.8
# phi = 38.7
# vInitial = 8501
# minDistJ: 502,284,730 Meters
# minDistE: 211,301,384 Meters

# Closest Jupiter Approach:
# launchDay =  
# launchDir = 
# phi = 
# vInitial = 
# minDistJ: 
# minDistE: 

# -------------------- Constants -------------------
AU = 149597871000
G = 6.67384E-11
# -------------------- Constants End -------------------

# -------------------- Rocket Launch Values -------------------
launchDay = 72.7
launchDir = -4.8
phi = 38.7
vInitial = 8501
# -------------------- Rocket Launch Values End -------------------

# -------------------- Rocket Constants -------------------
rInitial = 5.6*6.4E+06
orbitalDist = 675088558
vVec = vec(cos(radians(launchDir)), sin(radians(launchDir)), cos(radians(phi)))
initRVel = vInitial * vVec
rocketPosRel = vVec * rInitial
Mrocket = 334500
MFCon = 4067 + 21054 + 2316
MFuel = 42630 + 284089 + 20830
# -------------------- Rocket Constants End -------------------

# -------------------- Scene Effects -------------------
scene.width = 1600
scene.height = 900
# -------------------- Scene Effects End -------------------

# -------------------- Functions -------------------
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

def distTo(planet, otherPlanet):
    r = planet.pos - otherPlanet.pos
    return mag(r)

def updateDistLabel():
    distRtoE.clear()
    distRtoE.append(rocket.pos)
    distRtoE.append(europa.pos)
    diststr = "{:,}".format(round(mag(rocket.pos-europa.pos))) + ' meters'
    distlabel.text = diststr
    distpos = rocket.pos - norm(rocket.pos-europa.pos)*mag(rocket.pos-europa.pos)/2 + vector(0, 0.5*AU, 0)
    distlabel.pos = distpos

def JOI(dt):
    rocket.force -= rocket.reverseThrust
# -------------------- Functions End -------------------

# -------------------- Data Import -------------------
data = open("data.txt", 'r')
planetData = []
planetNames = []
for line in data:
    line = str(line)[:-2]
    vals = line.split()
    varname, mass, rad, posx, posy, posz, velx, vely, velz = vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8]
    planetNames.append(varname)
    exec(varname + 'Info = [' + mass + ', ' + rad + ', ' + posx + ', ' + posy + ', ' + posz + ', ' + velx + ', ' + vely + ',' + velz + ']')
    exec('planetData.append(' + varname + 'Info)')

print(planetNames)

for i in range(len(planetData)):
    print(list(locals().keys())[list(locals().values()).index(planetData[i])], '=', planetData[i])

planets = []
planetLabels = []

for i in range(len(planetNames)):
    exec(planetNames[i] + 'pos = vec(' + planetNames[i] + 'Info[2] , ' + planetNames[i] + 'Info[3], ' + planetNames[i] + 'Info[4])')
    exec(planetNames[i] + 'vel = vec(' + planetNames[i] + 'Info[5] , ' + planetNames[i] + 'Info[6], ' + planetNames[i] + 'Info[7])')
    exec('R' + planetNames[i] + ' = ' + planetNames[i] + 'Info[1]')
    exec('M' + planetNames[i] + ' = ' + planetNames[i] + 'Info[0]')
    exec(planetNames[i] + ' = sphere(pos=' + planetNames[i] + 'pos, radius=R' + planetNames[i] + ', color=color.green, make_trail=True, retain=1000)')
    exec(planetNames[i] + '.mass = M' + planetNames[i])
    exec(planetNames[i] + '.velocity = ' + planetNames[i] + 'vel')
    exec('planets.append(' + planetNames[i] + ')')
# -------------------- Data Import End -------------------

# -------------------- Label and Rocket Init -------------------
tstr = "Time: {:.0f} days".format(0)
tlabel = label(pos=vector(0, 20*AU, 0), text=tstr)
launchstr = 'Click to Start'
launchlabel = label(pos=vector(0, -20*AU, 0), text=launchstr)

dt = 3600
day = 24*3600
t = 0

rocketpos = earth.pos + rocketPosRel
launched = False

rocket = sphere(pos=rocketpos, radius=60, color=color.green, make_trail=True)

rocket.mass = Mrocket + MFCon + MFuel
rocket.reverseThrust = 99200

distRtoE = curve(pos=[rocket.pos, europa.pos], color=color.red, visible=False)
diststr = str(round(mag(rocket.pos-europa.pos))) + ' meters'
distpos = rocket.pos - norm(rocket.pos-europa.pos)*mag(rocket.pos-europa.pos)/2
distlabel = label(pos=distpos, text=diststr, visible=False)

for planet in planets:
    planet.momentum = planet.velocity*planet.mass

for i in range(len(planetNames)):
    exec('pstr = "' + planetNames[i] + '"')
    exec(planetNames[i] + 'label = label(pos=vector(0, 0.3*AU, 0) + ' + planetNames[i] + 'pos , text = pstr)')
    exec('planetLabels.append(' + planetNames[i] + 'label)')
# -------------------- Label and Rocket Init End -------------------

# -------------------- Main Loop -------------------
distanceTraveled = 0

distances = []
passed = False

while True:
    rate(168*4)
    
    if t == 0:
        launchstr = "Click to Start"
        launchlabel.text = launchstr
        scene.waitfor('click')
        launchstr = "Running..."
        launchlabel.text = launchstr

    if distTo(rocket, jupiter) < orbitalDist:
        print("The rocket is", '{:,}'.format(round(distTo(rocket, jupiter))), "meters from Jupiter and", '{:,}'.format(round(distTo(rocket, europa))), "meters from Europa")
        launchstr = "The rocket approaches jupiter after" + str((t/day-launchDay)) + "days. Click to Continue."
        launchlabel.text = launchstr
        scene.waitfor('click')
        launchstr = "Running..."
        launchlabel.text = launchstr
    
    if distTo(rocket, jupiter) < orbitalDist:

        print("The rocket is", distTo(rocket, jupiter), "meters from jupiter", ((t/day-launchDay)), "days after launch")

    if distTo(rocket, jupiter) < 100000000000:
        distances.append(distTo(rocket, jupiter))
        if not passed:
            passed = True
    if passed and distTo(rocket, jupiter) > 100000000000:
        print("The rocket came closest to jupiter at", '{:,}'.format(round(sorted(distances)[0])), "meters.")
        exit()

    for planet in planets:
        planet.force = vec(0, 0, 0)
        for otherPlanet in planets:
            if otherPlanet is not planet:
                planet.force += forceOf(planet, otherPlanet)
        updatePlanet(planet, dt)
    
    for i, label in enumerate(planetLabels):
        exec('position = vector(0, 0.1*AU, 0) + ' + planetNames[i] + '.pos')
        label.pos = position

    if launched:
        rocket.force = vec(0, 0, 0)
        # Sum up the force of all the planets on the rocket.
        for planet in planets:
            rocket.force += forceOf(rocket, planet)
        # Update the position, velocity, and momentum values for the rocket
        updatePlanet(rocket, dt)
        # Calculate the arc length of the path taken to Europa
        distanceTraveled += mag(rocket.velocity*dt)
        # Update the line and label showing the distance from the rocket to Europa
        updateDistLabel()
    else:
        # If the rocket has not launched yet, keep its position constant relative to Earth
        rocket.pos = earth.pos + rocketPosRel

    # If it is within half a day of the specified launch day, consider the rocket launched.
    if abs(t/day - launchDay) < 0.5:
        # Toggle, only run this code once
        if not launched:
            # The rocket has launched
            launched = True
            # Lock the camera to the rocket
            scene.camera.follow(rocket)
            # Begin updating the line and label showing the distance from the rocket to Europa
            updateDistLabel()
            # Make the line and label visible
            distlabel.visible = True
            distRtoE.visible = True
            # Output that the rocket has launched.
            print("The rocket has launched on", datetime(2020, 3, 20)+timedelta(t/day))
            rocket.pos = earth.pos + rocketPosRel
            rocket.momentum = initRVel*rocket.mass + earth.velocity*rocket.mass
            rocket.velocity = rocket.momentum/rocket.mass
    
    # Update the time value by increment dt and update time label
    t += dt
    tstr = "Time: {:0f} days".format(t/day)
    tlabel.text = tstr
# -------------------- Main Loop End -------------------

    
