from numpy import e

mp = float(input("Mass of payload in kg: ")) #payload mass, kg
vf = float(input("Final velocity in m/s: ")) #final velocity, m/s

m0 = 561774 + mp #initial mass, kg
ve = 4860.54 #exhaust velocity, m/s

m1 = m0/e**(vf/ve)

deltam = m0-m1
print("Initial mass (including propellant):", m0, "\nFinal mass:", m1, "\nFuel use:", deltam)