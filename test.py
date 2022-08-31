# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 02:09:09 2022

@author: lauram16
"""
from importlib import reload
import numpy as np
from my_enum import enum

# PARTICLE_COUNT = 2

import Vector
reload(Vector)
from Vector import Vector

import Point
reload(Point)
from Point import Point


class Particle:
    
    def __init__(self,x,y,z):
                                                   
        x = float(x)
        y = float(y)
        z = float(z)
        self.position = Vector(x, y, z)
        
        
                
    def distance_to(self, pointOrParticle): 
         
        if isinstance(pointOrParticle,Particle):
             otherPosition = pointOrParticle.position
        else:
            otherPosition = pointOrParticle
             
            
        dx = self.position.x - otherPosition.x
        dy = self.position.y - otherPosition.y
        dz = self.position.z - otherPosition.z
          
        d2 = dx*dx + dy*dy + dz*dz
         
            
        return d2**0.5   

    def distance_to_Point(self, point : Point):
        
        return self.distance_to(point)





class AllParticles:

        
    def __init__(self,particle1,particle2):
                                   
        self.tot = np.ndarray((2,), dtype=object)
        self.tot[0] = particle1
        self.tot[1] = particle2

        
        
p1 = Particle(1.,2.,3.)
p2 = Particle(10.,20.,30.)
particles = AllParticles(p1,p2)
        

ciccio = []

ciccio.append(particles.tot[0])
ciccio.append(particles.tot[0])
ciccio[0].x = 101
ciccio[1].x = 200
print(ciccio[0].x)
print(particles.tot[0].x)


# # getXValues = lambda p : p.x
# # xAll = np.array([getXValues(particle) for particle in particles.tot])
# # particleXmax  = np.max(xAll)


# # xAll = lambda particles : [p.x for p in particles.tot]
# # particleXmax  = np.max(xAll(particles))


# xAll = [particle.x for particle in particles.tot]
# particleXmax  = np.max(xAll)


# for particle in particles.tot:
#     particle.x = particle.x - 1
#     particle.y = particle.y - 1
#     particle.z = particle.z - 1
    
# xAllNew = [particle.x for particle in particles.tot]
# particleXmaxNew  = np.max(xAllNew)






