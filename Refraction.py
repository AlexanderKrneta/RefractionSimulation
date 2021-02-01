# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:26:02 2021

@author: Alexa
"""
import pygame
from vec import vec
from ray import ray
pygame.init()
screen = pygame.display.set_mode([2560, 1440])
  

class refraction_sim():
    c = 50
    def __init__(self, function, rays, timeStep):
        self.function, self.dt = function, timeStep
        self.activeRays = rays
    def take_step(self):
        #print(len(self.activeRays))
        nextRays = []
        for dray in self.activeRays: # For every active ray, create the next rays
            for newRay in dray.interact(refraction_sim.c, self.dt, self.function): # For every created ray
                nextRays.append(newRay) # append it to the 'NextRays' list
        self.activeRays = nextRays # Update the 'activeRays' to the nextRays
        for dray in self.activeRays: # Time to draw the path the ray 
            color, start, end = dray.draw()
            pygame.draw.line(screen, color, start, end, 2)
        
#f = lambda v: 3-2*math.sin(.01*(v.x))
#f = lambda v: 5 - ((v.x - 600)**2 + (v.y - 600)**2)/200000
f = lambda v: 1 + 0.001*v.x
rays = []
for i in range(0,3):
    rays.append(ray(vec(100,100), vec(1,1), 600+10*i, 1))
    
    
atmos = refraction_sim(f, rays, 1)


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



