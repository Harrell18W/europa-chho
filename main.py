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
# One astronomical unit in meters
AU = 149597871000
# The gravitational constant
G = 6.67384E-11
# -------------------- Constants End -------------------

# -------------------- Rocket Launch Values -------------------
# The day of launch
launchDay = 72.7
# The angle of the launch, think polar coordinates
launchDir = -4.8
# The angle between the rocket launch vector and the z-axis, think spherical coordinates
phi = 38.7
# The velocity of the rocket after escaping Earth's atmosphere
vInitial = 8501
# -------------------- Rocket Launch Values End -------------------

# -------------------- Rocket Constants -------------------
# The initial distance of the rocket from Earth
rInitial = 5.6*6.4E+06
# Th distance from Jupiter to Europa
orbitalDist = 675088558
# The unit vector in the direction of the rocket's launch
vVec = vec(cos(radians(launchDir)), sin(radians(launchDir)), cos(radians(phi)))
# The vector of the rocket's initial velocity
initRVel = vInitial * vVec
# The vector of the rocket's initial position relative to Earth
rocketPosRel = vVec * rInitial
# The mass of the rocket
Mrocket = 334500
# The mass of the fuel containers
MFCon = 4067 + 21054 + 2316
# The mass of the fuel
MFuel = 42630 + 284089 + 20830
# -------------------- Rocket Constants End -------------------

# -------------------- Scene Effects -------------------
# Change the width of the scene to 1600 pixels
scene.width = 1600
# Change the height of the scene to 800 pixels
scene.height = 900
# -------------------- Scene Effects End -------------------

# -------------------- Functions -------------------
# Find the gravitational force between two objects
def forceOf(planet, otherPlanet):
    global G
    # Find the vector representing the distance between both objects
    r = planet.pos - otherPlanet.pos
    # Find the magnitude of the vector
    rmag = mag(r)
    # Find the unit vector point from one planet to another
    runit = norm(r)
    # Calculate the force between the two objects
    return -(G*planet.mass*otherPlanet.mass)/(rmag**2)*runit

# Update the momentum, velocity, and position values
def updatePlanet(planet, dt):
    # The momentum is incremented by the force times time delta
    planet.momentum += planet.force*dt
    # The velocity is equal to the momentum divided by the mass
    planet.velocity = planet.momentum/planet.mass
    # The pos is incremented by the velocity times time delta
    planet.pos += planet.velocity*dt

# FInd the distance between two objects
def distTo(planet, otherPlanet):
    # Find the vector representing the distance between both objects
    r = planet.pos - otherPlanet.pos
    # Return the magnitude of that vector
    return mag(r)

# Update the line and label from the rocket to Europa
def updateDistLabel():
    # Remove all points from the curve distRtoE 
    distRtoE.clear()
    # Add the rocket's position to the curve
    distRtoE.append(rocket.pos)
    # Add Europa's position to the curve
    distRtoE.append(europa.pos)
    # Create a string with the distance from the rocket to Europa
    diststr = "{:,}".format(round(mag(rocket.pos-europa.pos))) + ' meters'
    # Update the label text with the string 
    distlabel.text = diststr
    # The label position is halfway between the rocket and Europa and half an AU in the y direction
    distpos = rocket.pos - norm(rocket.pos-europa.pos)*mag(rocket.pos-europa.pos)/2 + vector(0, 0.5*AU, 0)
    # Update the label position
    distlabel.pos = distpos
# -------------------- Functions End -------------------

# -------------------- Data Import -------------------
# Load the data.txt file into the variable data in read mode
data = open("data.txt", 'r')
# The planetData list will contain the data for each planet
planetData = []
# The planetNames list will contain the name of each planet
planetNames = []
# Each line contains a planet's name, mass, radius, position, and velocity
for line in data:
    # At the end of each line is '\n' this is removed here
    line = str(line)[:-2]
    # Split the line into a list according to the spaces in the line
    vals = line.split()
    # Reassign the values into variables that make more sense
    varname, mass, rad, posx, posy, posz, velx, vely, velz = vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8]
    # Add the name of the planet to the planetNames array
    planetNames.append(varname)
    # Add the data to a variable called 'planetName'Info
    exec(varname + 'Info = [' + mass + ', ' + rad + ', ' + posx + ', ' + posy + ', ' + posz + ', ' + velx + ', ' + vely + ',' + velz + ']')
    # Add the data to the planetData array
    exec('planetData.append(' + varname + 'Info)')

# Print the list containing the names of all planets in the simulation
print(planetNames)

# Print the planetData list in the format where
# 'planetName'Info = planet data
for i in range(len(planetData)):
    print(list(locals().keys())[list(locals().values()).index(planetData[i])], '=', planetData[i])

# The planets list will contain all the planets
planets = []
# The planetLabels list will contain the labels for all the planets
planetLabels = []

# For each planet:
for i in range(len(planetNames)):
    # Store the planet position in a vector called 'planetName'pos
    exec(planetNames[i] + 'pos = vec(' + planetNames[i] + 'Info[2] , ' + planetNames[i] + 'Info[3], ' + planetNames[i] + 'Info[4])')
    # Store the planet velocity in a vector called 'planetName'vel
    exec(planetNames[i] + 'vel = vec(' + planetNames[i] + 'Info[5] , ' + planetNames[i] + 'Info[6], ' + planetNames[i] + 'Info[7])')
    # Store the planet radius in a variable called R'planetName'
    exec('R' + planetNames[i] + ' = ' + planetNames[i] + 'Info[1]')
    # Store the planet mass in a variable called M'planetName'
    exec('M' + planetNames[i] + ' = ' + planetNames[i] + 'Info[0]')
    # Initialize the planet object in the simulation
    exec(planetNames[i] + ' = sphere(pos=' + planetNames[i] + 'pos, radius=R' + planetNames[i] + ', color=color.green, make_trail=True)')
    # Store the planet mass in the planet instance
    exec(planetNames[i] + '.mass = M' + planetNames[i])
    # Store the initial planet velocity in the planet instance
    exec(planetNames[i] + '.velocity = ' + planetNames[i] + 'vel')
    # Append the planet to the planets list
    exec('planets.append(' + planetNames[i] + ')')

# Calculate the momentum of each planet
for planet in planets:
    planet.momentum = planet.velocity*planet.mass

# Create labels for each of the planets
for i in range(len(planetNames)):
    # The label text will contain the name of the planet
    exec('pstr = "' + planetNames[i] + '"')
    # The label will be 0.3 AU above the planet and set it's ext
    exec(planetNames[i] + 'label = label(pos=vector(0, 0.3*AU, 0) + ' + planetNames[i] + 'pos , text = pstr)')
    # Add the label to the array of labels
    exec('planetLabels.append(' + planetNames[i] + 'label)')
# -------------------- Data Import End -------------------

# -------------------- Label and Rocket Init -------------------
# Initialize the time label
tstr = "Time: {:.0f} days".format(0)
tlabel = label(pos=vector(0, 20*AU, 0), text=tstr)
# Initialize the simulation status label
launchstr = 'Click to Start'
launchlabel = label(pos=vector(0, -20*AU, 0), text=launchstr)

# The dt is 1 hour, there are 3600 seconds in an hour
dt = 3600
# One day contains 24 hours, or 24*3600 seconds
day = 24*3600
# t is initially zero
t = 0

# The position of the rocket is initially earth's position plus the position of the rocket relative to Earth
rocketpos = earth.pos + rocketPosRel

# Initialize the rocket
rocket = sphere(pos=rocketpos, radius=60, color=color.green, make_trail=True)

# The mass of the rocket is equal to the mass of the body, plus the mass of the fuel containers, plus the mass of the fuel
rocket.mass = Mrocket + MFCon + MFuel

# Initialize the line and label from the rocket to Europa, will not be visible until the rocket launches
distRtoE = curve(pos=[rocket.pos, europa.pos], color=color.red, visible=False)
diststr = str(round(mag(rocket.pos-europa.pos))) + ' meters' 
distpos = rocket.pos - norm(rocket.pos-europa.pos)*mag(rocket.pos-europa.pos)/2 + vec(0, 0.5*AU, 0)
distlabel = label(pos=distpos, text=diststr, visible=False)
# -------------------- Label and Rocket Init End -------------------

# -------------------- Main Loop -------------------
# Arc length of path traveled
distanceTraveled = 0
# Has the rocket launched yet
launched = False

# Will contain the distances from when the rocket is close to jupiter, will be used to find minimum distance to Jupiter
distances = []
# Whether or not the rocket has come close to Jupiter
passed = False

# Main Loop
while True:
    # Limit the rate of glowscript to 168*4 cycles/sec, there are 168 hours in a week, so 4 weeks per second.
    rate(168*4)
    
    # If the simulation has yet to start
    if t == 0:
        # Update the simulation status with the text, "Click to Start"
        launchstr = "Click to Start"
        # Update the text of the simulation status
        launchlabel.text = launchstr
        # Pause the simulation until a click occurs
        scene.waitfor('click')
        # Update the simulation status, saying that it is running
        launchstr = "Running..."
        # Update the text of the simulation status
        launchlabel.text = launchstr

    # The rocket is as close to Jupiter as Europa is.
    if distTo(rocket, jupiter) < orbitalDist:
        # Print the rocket's distance to Jupiter and Europa
        print("The rocket is", '{:,}'.format(round(distTo(rocket, jupiter))), "meters from Jupiter and", '{:,}'.format(round(distTo(rocket, europa))), "meters from Europa")
        # Update the simulation status with the number of days after launch.
        launchstr = "The rocket approaches jupiter after" + str((t/day-launchDay)) + "days. Click to Continue."
        # Update the text of the simulation status
        launchlabel.text = launchstr
        # Pause the simulation until a click occurs
        scene.waitfor('click')
        # Update the simulation status, saying that it is running
        launchstr = "Running..."
        # Update the text of the simulation status
        launchlabel.text = launchstr

    # If the rocket is within 100 billion meters of jupiter
    if distTo(rocket, jupiter) < 100000000000:
        # Append the current distance to the distances array
        distances.append(distTo(rocket, jupiter))
        # Toggle the passed variable
        if not passed:
            passed = True
    # After the rocket has approached jupiter and then left Jupiters proximiter
    if passed and distTo(rocket, jupiter) > 100000000000:
        # Print the closest distance from jupiter to the rocket (The minimum of the distances array)
        print("The rocket came closest to jupiter at", '{:,}'.format(round(sorted(distances)[0])), "meters.")
        # Exit the program
        exit()

    # For each planet in the simulation
    for planet in planets:
        # The force is considered to be initially zero
        planet.force = vec(0, 0, 0)
        # For each planet that is not the current planet
        for otherPlanet in planets:
            if otherPlanet is not planet:
                # Sum up the force of the rest of the planets on the planet
                planet.force += forceOf(planet, otherPlanet)
        # Update position, velocity, and momentum values of the planet
        updatePlanet(planet, dt)
    
    # For each planet label
    for i, label in enumerate(planetLabels):
        # Store the planets position + 0.1AU j hat in a vector called position
        exec('position = vector(0, 0.1*AU, 0) + ' + planetNames[i] + '.pos')
        # Update the position of the label
        label.pos = position

    # If the rocket has launched:
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
