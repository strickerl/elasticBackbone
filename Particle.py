# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 03:26:58 2022

@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""


from importlib import reload
import numpy as np

from myEnum import enum
from columns import COLUMN_NAMES, HEADER_COLUMN_NAMES

import Vector
reload(Vector)
from Vector import Vector

import Point
reload(Point)
from Point import Point

import SimulationBox
reload(SimulationBox)
from SimulationBox import SimulationBox


class Particle:
    
    def __init__(self, particle_data_string):
                                                   
        self.particleID = int(particle_data_string[COLUMN_NAMES.PARTICLE_ID])
        self.chemicalType = int(particle_data_string[COLUMN_NAMES.CHEMICAL_TYPE])
        x = float(particle_data_string[COLUMN_NAMES.X])
        y = float(particle_data_string[COLUMN_NAMES.Y])
        z = float(particle_data_string[COLUMN_NAMES.Z])
        self.position = Vector(x, y, z)
        self.radius = float
        self.volume = float(particle_data_string[COLUMN_NAMES.VOLUME])
        self.clusterID = int(particle_data_string[COLUMN_NAMES.CLUSTER_ID])
        self.neighbourCount = int(particle_data_string[COLUMN_NAMES.NEIGHBOUR_COUNT])
        self.neighbourIDs = np.ndarray((self.neighbourCount,), dtype=int)
        
        for neighbourIndex in range(0, self.neighbourCount):
            self.neighbourIDs[neighbourIndex] =    \
            int(particle_data_string[COLUMN_NAMES.FIRST_NEIGHBOUR + neighbourIndex])

        self.index = int
        self.forwardBurningTime  = 0
        self.backwardBurningTime = 0
        self.isBurntByParticleIndex = None


            
    def distanceTo(self, point): 
        #point can be a Point or a Particle  
        
        dx = self.position.x - point.position.x
        dy = self.position.y - point.position.y
        dz = self.position.z - point.position.z
          
        d2 = dx*dx + dy*dy + dz*dz
          
        return d2**0.5      
    


    def isBurnt(self):
        return self.isBurntByParticleIndex != None


    
    def isConnectedThroughBox(self, particle, box = SimulationBox):
      
      dx = self.position.x - particle.position.x
      dy = self.position.y - particle.position.y
      dz = self.position.z - particle.position.z
      
      if (abs(dx) < box.lengthX/2 and
          abs(dy) < box.lengthY/2 and 
          abs(dz) < box.lengthZ/2) : # directly connected inside the box
          return True
      else :  #connected through the periodic boundary
          return False



    def resetBurningStatus(self):
        
        self.isBurntByParticleIndex = None
        


    def setParticleIndex(self,particleIndex):
        
        self.index = particleIndex
        
        
    def setParticleRadius(self,parameters):
        
        self.radius = parameters.radiusMin if self.chemicalType==1 else parameters.radiusMax
        
        
    #Debug/output-related method        
    def display(self):
        
        print('ID: {}'.format(self.particleID))
        print('chemicalType: {}'.format(self.chemicalType))
        print('pos: {} {} {}'.format(self.position.x, self.position.y, self.position.z))
        print('volume: {}'.format(self.volume))
        print('clusterID: {}'.format(self.clusterID))
        print('neighbourCount: {}'.format(self.neighbourCount))
        
        for neighbourIndex in range(0, self.neighbourCount):
            print('{}, '.format(self.neighbours[neighbourIndex]))
             

    #Debug/output-related method
    def printInFile(self,outputFileHandler): 
        
        print(self.position.x,\
              self.position.y,\
              self.position.z,\
              self.chemicalType,\
              self.radius,\
              self.forwardBurningTime,\
              self.backwardBurningTime,\
              self.particleID,\
              file = outputFileHandler)

                 