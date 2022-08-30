# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:00:31 2022

@author: Laura Stricker
"""

from importlib import reload
import numpy as np

from my_enum import enum
from fields import FIELDS, HEADER_FIELDS

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
        self.numberOfParticles = -1
        self.particles = np.ndarray((particle_count,), dtype=object)
        self.box = object 
        self.particle_index_from_ID_lookup = int
        
        
        
    def load_data_from_simulation_file(self, fname):
        
        try:
            file_handle = open(fname, 'r')
        
            self.read_header_from_simulation_file(file_handle)
            self.load_particle_data_by_row(file_handle)
        
            file_handle.close()
        
        except:
            print('Failed to open: {}'.format(fname))
        else:
            print('Successfully loaded {}'.format(fname))
        
                
        
        
    def read_header_from_simulation_file(self, file_handle):
        
        line = file_handle.readline()
        header_fields = line.split()
        
        particleCount = header_fields[HEADER_FIELDS.PARTICLE_COUNT]
        lengthX = header_fields[HEADER_FIELDS.BOX_SIZE_X]
        lengthY = header_fields[HEADER_FIELDS.BOX_SIZE_Y]
        lengthZ = header_fields[HEADER_FIELDS.BOX_SIZE_Z]
        
        self.particleCount = int(particleCount)
        self.box = SimulationBox(float(lengthX),float(lengthY),float(lengthZ))
        self.particles = np.resize(self.particles, self.numberOfParticles)
        
    
    
    def load_particle_data_by_row(self, file_handle):
        
        # skip header row
        file_handle.seek(0)
        file_handle.readline()
        
        for index in range(0, self.particleCount):
            
            line = file_handle.readline()
            particle_data = line.split()
            
            self.particles[index] = Particle(particle_data)
    
    
    
    def filter_particles_by_cluster_ID(self, clusterID):

        my_filter = lambda p: p.clusterID == clusterID
        
        matches = np.asarray([my_filter(particle) for particle in self.particles])
        indices = np.where(matches == True)[0]
        self.particles = self.particles[indices]
        self.numberOfParticles = len(self.particles)
    
   
    
    def set_particle_index_from_ID_lookup(self):
           
         particleIDmax  = np.max([p.particleID for p in self.particles])
         
         self.particleIDToIndexLookup = -np.ones(particleIDmax)  
         
         #The line ID of the lookup array contains the value of the corresponding particle index    
         for particleIndex in range(0,self.particleCount):
              particleID = self.particles[particleIndex].particleID
              self.particleIDToIndexLookup[particleID] = particleIndex      
              
    
    
    def shift_origin_of_axes(self):
        '''
            Shift all particle coordinates (x,y,z) so that the new origin of axes 
            coincides with min(x),min(y),min(z)
        ''' 
        #New origin of axes based on particles' positions
        xMin = np.min([particle.x for particle in self.particles])
        yMin = np.min([particle.y for particle in self.particles])
        zMin = np.min([particle.z for particle in self.particles])
               
        #Shift particle coordinates
        for particle in self.particles:
            particle.x = particle.x - xMin
            particle.y = particle.y - yMin
            particle.z = particle.z - zMin

    
    
    def find_distances_from_point(self, point):
        
        self.distances = np.asarray([p.get_distance_from_point(point) for index, p in enumerate(self.particles)])



    def printXYZFile(self, particles, outputFileName):

        outputFileHandler = open(outputFileName,'w')             

        print(particles.particleCount,file = outputFileHandler) #Particle number
        print(file = outputFileHandler)                         #Empty line
        for particle in particles:
           particle.printOnFile(outputFileHandler)

        outputFileHandler.close()

