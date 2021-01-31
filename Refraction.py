# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:26:02 2021

@author: Alexa
"""
import math
import pygame
pygame.init()
screen = pygame.display.set_mode([2560, 1440])


class vec():
    def __init__(self, x, y, z = 0):
        self.x, self.y, self.z = x, y, z
    def __mul__(self, s):
        return vec(s * self.x, s * self.y, s * self.z)
    def __rmul__(self, s):
        return self * s
    def __truediv__(self, s):
        return self * (1 / s)
    def __add__(self, v):
        return vec(self.x + v.x, self.y + v.y, self.z + v.z)
    def __radd__(self, v):
        return self + v
    def __sub__(self, v):
        return self + v * -1
    def __rsub__(self, v):
        return v + self * -1
    def __pow__(self, v): # Dot product '**'
        return self.x*v.x + self.y*v.y + self.z*v.z
    def __mod__(self, v): # Cross product '%'
        return vec(self.y*v.z - self.z*v.y, 
                   self.z*v.x - self.x*v.z, 
                   self.x*v.y - self.y*v.x)
    def __floordiv__(self, n): # Magnatude '//'
        return math.sqrt(self ** self)
    def __xor__(self, n): # Normalize the vector '^'
        return self / (self//1)
    def __str__(self):
        return "< " + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + " >"
    def __rshift__(self, v): # Cosine between 2 vectors
        return self**v/((self//1)*(v//1))
    def __lshift__(self, v): # Sine between 2 vectors
        return (self%v//1)/((self//1)*(v//1))
    
    
class ray():
    h = 0.0001
    def __init__(self, position, direction, wavelength, intensity):
        self.position, self.direction, self.wavelength, self.intensity = position, direction^1, wavelength, intensity
        self.lastPosition = self.position
        self.color = self.get_color(self.wavelength)
        self.normal = vec(0, 0)
    def interact(self, speed, timeStep, function):
        createdRays = [] # Create an array to store solution rays
        self.get_gradient(function) # Aquire the normal of the boundry at the given position
        if self.normal ** self.direction < 0: # Make sure the angle between the normal a direction vector is not > 90
            self.normal = self.normal * -1 # If it is greater than 90, have the normal face the opposite direction
        n1 = self.getIoR(self.position, function) # Get the IoR at the current position ** Note that This is at 633 nm
        n2 = (n1 + self.getIoR(self.position + self.direction*speed*timeStep, function)) / 2 # Get average if continued in same direction
        #R = self.reflectance(n1, n2) # Get the value of Reflectance for ray
        R = 0
        #print(R)
        # Create reflected ray 
        #createdRays.append(self.reflect(R * self.intensity)) # Add the reflected ray to the createdRays
        #createdRays[0].take_step(function, speed, timeStep) # Have the reflected ray continue for the timestep
        #if R == 1: # If the reflectance is 1, that means no ray was transmitted
        #    return createdRays # Return the reflected ray
        # Create a refracted ray
        createdRays.append(self.refract(n1, n2, (1-R)*self.intensity)) # Add the refracted ray to the createdRays
        createdRays[0].take_step(function, speed, timeStep) # Have the refracted ray continue for the timestep
        return createdRays # Return the new ray(s)
    def reflect(self, newIntensity):
        newDirection = self.direction - ((2 * (self.direction**self.normal)) * self.normal) # Determine the new direction given normal
        return ray(self.position, newDirection^1, self.wavelength, newIntensity) # Return a reflected ray of new Intensity
    def getIoR(self, position, function):
            n = function(position) # Get the IoR for a red beam ## Note that the /1000000 is to turn sqr nm to sqr um
            nL = (((0.1331443408*n - 0.13329)**2)/(self.wavelength * self.wavelength / 1000000)) + n # Get the wave dependent IoR
            return nL    
    def get_gradient(self, function):
        self.normal = vec((function(self.position + vec(ray.h,0)) - function(self.position))/ray.h,
                            (function(self.position + vec(0,ray.h)) - function(self.position))/ray.h)^1
    def refract(self, n1, n2, newIntensity):
        NxS1 = self.normal%self.direction # Normal cross Direction
        N1oN2 = n1 / n2 # Save the division
        S2 = N1oN2*(self.normal%NxS1) - self.normal * math.sqrt(1 - N1oN2*N1oN2*(NxS1**NxS1)) # Refraction formula
        return ray(self.position, (S2^1)*-1, self.wavelength, newIntensity)
    def take_step(self, function, speed, timeStep):
        # First, undertand that the the IoR at the start point is different than the end point
        # So lets say that the ray travels through a medium with an IoR of the average of these 2 values
        n1 = function(self.position) # Get the current IoR
        temp_pos = self.position + (speed / n1 * timeStep) * self.direction # Get the position the ray would be
        n2 = function(temp_pos) # Get the IoR at this new position
        nAvg = (n1 + n2)/2 # Average the IoR's
        self.lastPosition = self.position # Save the current Pos as the lastPos before the step ## This will be used for drawing the rays
        self.position += (speed / nAvg * timeStep) * self.direction # Update the position with the avg IoF
    def reflectance(self, n1, n2):
        cosx = self.direction >> self.normal
        sinx = self.direction << self.normal
        try:
            sqrtShit = math.sqrt(1 - (n2 * sinx / n1)**2)
        except ValueError:
            return 1
        Rs = ((n2*cosx - n1*sqrtShit) / (n2*cosx + n1*sqrtShit))**2
        Rp = ((n2*sqrtShit - n1*cosx) / (n2*sqrtShit + n1*cosx))**2
        R = (Rs + Rp) / 2
        return R
    def get_color(self, L):
        r, b, g = 0, 0, 0
        if 420 <= L < 440:
            r =  -5.3*L + 2332
            b = 255
        elif 440 <= L < 490:
            g = 5.1*L -2244
            b = 255
        elif 490 <= L < 510:
            g = 255
            b = -12.75*L + 6502.5
        elif 510 <= L < 580:
            r = (51 * L / 2 - 13005) / 7
            g = 255
        elif 580 <= L < 645:
            r = 255
            g = (-51*L + 32895)/13
        elif 645 <= L <= 700:
            r = 255
        return [r, g, b]
    def draw(self):
        #print(self.color)
        return [round(self.color[0]*self.intensity), round(self.color[1]*self.intensity), round(self.color[2]*self.intensity)], [self.lastPosition.x, self.lastPosition.y], [self.position.x, self.position.y]

class refraction_sim():
    c = 10
    def __init__(self, function, rays, timeStep):
        self.function, self.dt = function, timeStep
        self.activeRays = rays
    def take_step(self):
        #print(len(self.activeRays))
        nextRays = []
        for ray in self.activeRays: # For every active ray, create the next rays
            for newRay in ray.interact(refraction_sim.c, self.dt, self.function): # For every created ray
                nextRays.append(newRay) # append it to the 'NextRays' list
        self.activeRays = nextRays # Update the 'activeRays' to the nextRays
        for ray in self.activeRays: # Time to draw the path the ray 
            color, start, end = ray.draw()
            pygame.draw.line(screen, color, start, end, 2)
        
f = lambda v: 3-2*math.sin(.01*(v.x))
#f = lambda v: 5 - ((v.x - 600)**2 + (v.y - 600)**2)/200000
rays = []
for i in range(0,38000):
    rays.append(ray(vec(-100,00), vec(10,1), 420+.01*i, 1))
    
    
atmos = refraction_sim(f, rays, .1)


screen.fill((0,0,0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    atmos.take_step()
    pygame.display.flip()
    #pygame.time.wait(1000)
pygame.quit()



