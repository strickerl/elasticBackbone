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
                                                   
        self.particleID = int(particle_data_string[FIELDS.PARTICLE_ID])
        self.chemicalType = int(particle_data_string[FIELDS.CHEMICAL_TYPE])
        x = float(particle_data_string[FIELDS.X])
        y = float(particle_data_string[FIELDS.Y])
        z = float(particle_data_string[FIELDS.Z])
        self.position = Vector(x, y, z)
        self.volume = float(particle_data_string[FIELDS.VOLUME])
        self.clusterID = int(particle_data_string[FIELDS.CLUSTER_ID])
        self.neighbourCount = int(particle_data_string[FIELDS.NEIGHBOUR_COUNT])
        self.neighboursIds = np.ndarray((self.neighbourCount,), dtype=int)
           
        for neighbourIndex in range(0, self.neighbourCount):
            self.neighboursIds[neighbourIndex] = int(particle_data_string[FIELDS.FIRST_NEIGHBOUR + neighbourIndex])
        
        
    def display(self):
        
        print('ID: {}'.format(self.particleID))
        print('chemicalType: {}'.format(self.chemicalType))
        print('pos: {} {} {}'.format(self.position.x, self.position.y, self.position.z))
        print('volume: {}'.format(self.volume))
        print('clusterID: {}'.format(self.clusterID))
        print('neighbourCount: {}'.format(self.neighbourCount))
        
        for neighbourIndex in range(0, self.neighbourCount):
            print('{}, '.format(self.neighbours[neighbourIndex]))
         
         
    def distanceToPoint(self, point = Point): 
        
        dx = self.position.x - point.x
        dy = self.position.y - point.y
        dz = self.position.z - point.z
        
        d2 = dx*dx + dy*dy + dz*dz
        
        return d2**0.5
 
            
    def distanceToParticle(self, particle): 
          
        dx = self.position.x - particle.position.x
        dy = self.position.y - particle.position.y
        dz = self.position.z - particle.position.z
          
        d2 = dx*dx + dy*dy + dz*dz
          
        return d2**0.5      
        



        
        