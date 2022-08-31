# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:00:31 2022
@author: Laura Stricker laura.stricker@mat.ethz.ch

    Operations on the whole particle configuration for a time instant (frame)
"""

from importlib import reload
import numpy as np

from myEnum import enum
from columns import COLUMN_NAMES, HEADER_COLUMN_NAMES

import Particle
reload(Particle)
from Particle import Particle

import Vector
reload(Vector)
from Vector import Vector

import SimulationBox
reload(SimulationBox)
from SimulationBox import SimulationBox



class DataManager:

    def __init__(self):
 
        particle_count = 0
        self.particleCount = int
        self.particles = np.ndarray((particle_count,), dtype=object)
        self.box = object 
        self.particleIndexFromIDlookup = -np.ones(particle_count,dtype=int)
        
        
    def buildParticleIndexFromIDlookup(self):
           
         particleIDmax  = np.max([p.particleID for p in self.particles])
         
         self.particleIndexFromIDlookup = -np.ones(particleIDmax + 1, dtype=int)  
         
         #The line ID of the lookup array contains the value of the corresponding particle index    
         for particleIndex in range(0,self.particleCount):
              particleID = self.particles[particleIndex].particleID
              self.particleIndexFromIDlookup[particleID] = particleIndex     
                    
        
        
    def filterParticlesByClusterID(self, clusterID):

        myFilter = lambda p: p.clusterID == clusterID
        
        matches = np.asarray([myFilter(particle) for particle in self.particles])
        indices = np.where(matches == True)[0]
        self.particles = self.particles[indices]
        self.particleCount = len(self.particles)
    
   
    
    def findDistancesFromPoint(self, point):
        
        self.distances = np.asarray([p.distanceToPoint(point) for index, p in enumerate(self.particles)])        
        
        
        
    def loadDataFromFile(self, fname):
        
        try:
            file_handle = open(fname, 'r')
        
            self.readHeaderFromSimulationFile(file_handle)
            self.loadParticleDataByRow(file_handle)
        
            file_handle.close()
        
        except:
            print('Failed to open: {}'.format(fname))
        #else:
        #    print('Successfully loaded {}'.format(fname))
        
        
                
    def loadParticleDataByRow(self, fileHandle):
           
           # skip header row
           fileHandle.seek(0)
           fileHandle.readline()
           
           for index in range(0, self.particleCount):
               
               line = fileHandle.readline()
               particleData = line.split()
               
               self.particles[index] = Particle(particleData)
          
        
    
    def getParticleIndexFromID(self,particleID):
        return self.particleIndexFromIDlookup[particleID]

     
              

    def readHeaderFromSimulationFile(self, fileHandle):
        
        line = fileHandle.readline()
        headerColumnNames = line.split()
        
        particleCount = headerColumnNames[HEADER_COLUMN_NAMES.PARTICLE_COUNT]
        lengthX = headerColumnNames[HEADER_COLUMN_NAMES.BOX_SIZE_X]
        lengthY = headerColumnNames[HEADER_COLUMN_NAMES.BOX_SIZE_Y]
        lengthZ = headerColumnNames[HEADER_COLUMN_NAMES.BOX_SIZE_Z]
        
        self.particleCount = int(particleCount)
        self.box = SimulationBox(float(lengthX),float(lengthY),float(lengthZ))
        self.particles = np.resize(self.particles, self.particleCount)
              
    
    
    def setParticleIndexes(self):
            
        for particleIndex, particle in enumerate(self.particles):
            particle.setParticleIndex(particleIndex)
    
    
    
    def setParticleRadii(self,parameters):
        
        for particle in self.particles:
            particle.setParticleRadius(parameters)

    
    
    def shiftOriginOfAxes(self):
        '''
            Shift all particle coordinates (x,y,z) so that the new origin of axes 
            coincides with min(x),min(y),min(z)
        ''' 
        #New origin of axes based on particles' positions
        xMin = np.min([particle.position.x for particle in self.particles])
        yMin = np.min([particle.position.y for particle in self.particles])
        zMin = np.min([particle.position.z for particle in self.particles])
               
        #Shift particle coordinates
        for particle in self.particles:
            particle.position.x = particle.position.x - xMin
            particle.position.y = particle.position.y - yMin
            particle.position.z = particle.position.z - zMin
            
            
    #Debug/output files        
    def printXYZFile(self, particles, outputFileName):

        outputFileHandle = open(outputFileName,'w')             

        print(self.particleCount,file = outputFileHandle) #Particle number
        print(file = outputFileHandle)                         #Empty line
        for particle in particles:
           particle.printInFile(outputFileHandle)
           
        outputFileHandle.close()
   