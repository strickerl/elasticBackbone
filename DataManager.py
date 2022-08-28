# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:00:31 2022

@author: lauram16
"""

from importlib import reload

import particle
reload(particle)
import vector
reload(vector)

from my_enum import enum
from Particle import Particle
from Vector import Vector
from fields import FIELDS, HEADER_FIELDS

import numpy as np



class DataManager:

    def __init__(self):
 
        particle_count = 0
        self.numberOfParticles = -1
        self.particles = np.ndarray((particle_count,), dtype=object)
        
        #TODO: 
        #self.particle_index_lookup = np
        
        
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
        
        self.numberOfParticles = int(header_fields[HEADER_FIELDS.PARTICLE_COUNT])
        self.particles = np.resize(self.particles, self.numberOfParticles)
        
    
    def load_particle_data_by_row(self, file_handle):
        
        # skip header row
        file_handle.seek(0)
        file_handle.readline()
        
        for index in range(0, self.numberOfParticles):
            
            line = file_handle.readline()
            particle_data = line.split()
            
            self.particles[index] = Particle(particle_data)
    
    
    def filter_particles_by_cluster_id(self, clusterId):

        my_filter = lambda p: p.clusterId == clusterId
        
        matches = np.asarray([my_filter(particle) for particle in self.particles])
        indices = np.where(matches == True)[0]
        self.particles = self.particles[indices]
        
    
    def sort_particles_by_particle_id(self):
        
        self.particles = np.asarray(sorted(self.particles, key=lambda particle: particle.particleId))  
    
    
    def find_distance_from_point(self, point):
        
        self.deltas = np.asarray([p.get_distance_from_point(point) for index, p in enumerate(self.particles)])
