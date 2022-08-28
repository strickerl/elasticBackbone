# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 03:26:58 2022

@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""


from importlib import reload
import numpy as np
from my_enum import enum
from fields import FIELDS, HEADER_FIELDS

import Vector
reload(Vector)
from Vector import Vector

import Point
reload(Point)
from Point import Point



class Particle:
    
    def __init__(self, particle_data_string):
                                                   
        self.particleId = int(particle_data_string[FIELDS.PARTICLE_ID])
        self.chemicalType = int(particle_data_string[FIELDS.CHEMICAL_TYPE])
        x = float(particle_data_string[FIELDS.X])
        y = float(particle_data_string[FIELDS.Y])
        z = float(particle_data_string[FIELDS.Z])
        self.position = Vector(x, y, z)
        self.volume = float(particle_data_string[FIELDS.VOLUME])
        self.clusterId = int(particle_data_string[FIELDS.CLUSTER_ID])
        self.neighbourCount = int(particle_data_string[FIELDS.NEIGHBOUR_COUNT])
        self.neighbours = np.ndarray((self.neighbourCount,), dtype=int)
           
        for neighbourIndex in range(0, self.neighbourCount):
            self.neighbours[neighbourIndex] = int(particle_data_string[FIELDS.NEIGHBOURS + neighbourIndex])
        
        
    def display(self):
        
        print('ID: {}'.format(self.particleId))
        print('chemicalType: {}'.format(self.chemicalType))
        print('pos: {} {} {}'.format(self.position.x, self.position.y, self.position.z))
        print('volume: {}'.format(self.volume))
        print('clusterID: {}'.format(self.clusterId))
        print('neighbourCount: {}'.format(self.neighbourCount))
        
        for neighbourIndex in range(0, self.neighbourCount):
            print('{}, '.format(self.neighbours[neighbourIndex]))
         
         
    def get_distance_from_point(self, point): 
        
        dx = self.position.x - point.x
        dy = self.position.y - point.y
        dz = self.position.z - point.z
        
        d2 = dx*dx + dy*dy + dz*dz
        
        return d2**0.5
 
    

class ParticlePair:

    def __init__(self,Particle1,Particle2):


        self.particle1 = Particle1(dtype = object)
        self.particle2 = Particle2(dtype = object)
        self.distance  = float() 
        
        
    def calculateDistance(self,Particle1,Particle2): 
        
        x1 = Particle1.position.x
        y1 = Particle1.position.y
        z1 = Particle1.position.z
        x2 = Particle2.position.x
        y2 = Particle2.position.y
        z2 = Particle2.position.z       
        
        self.distance  = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2) 
        
        
        
# class AllParticlesOneInstant:
    
#     def __init__(self,particlesDataFrame):


#         self.count = len(particlesDataFrame)
#         self.x            = np.array(particlesDataFrame['x'])
#         self.y            = np.array(particlesDataFrame['y'])
#         self.z            = np.array(particlesDataFrame['z'])
#         self.radius       = np.array(particlesDataFrame['radius'])
#         self.particleID   = np.array(particlesDataFrame['IDparticle'])
#         self.volume       = np.array(particlesDataFrame['volume'])
#         self.chemicalType = np.array(particlesDataFrame['chemicalType'])
#         self.NumberOfNeighbours  = np.array(particlesDataFrame['N_neighbours'])
        
        