# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 23:57:04 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""


import numpy as np
from importlib import reload

import Particle
reload(Particle)
from Particle import Particle


class Backbone:

    def __init__(self,timeIndex,time,particles):


        self.timeIndex              = timeIndex
        self.time                   = time
        self.minPathParticleCount   = int
        self.minPathLength          = float
        self.extremes               = np.ndarray((2,), dtype = object)
        self.linearDistanceExtremes = float()
        self.totalParticleCount = int
        self.largestClusterParticleCount = len(particles)
        self.forwardMinParticleCount  = int
        self.backwardMinParticleCount = int
        

    def calculateLinearDistanceBetweenExtremes(self):
        
        particle1 = self.extremes[0]
        particle2 = self.extremes[1]
        
        self.linearDistanceExtremes = particle1.distanceToParticle(particle2)

        

    def printFileSummary(self,fileHandler):
                
        print("{:6d}".format(self.timeIndex),\
              "{:.2f}".format(self.time),\
              "{:6d}".format(self.minPathParticleCount),\
              "{:.2f}".format(self.minPathLength), \
              "{:6d}".format(self.totalParticleCount),\
              "{:.2f}".format(self.linearDistanceExtremes),\
              "{:6d}".format(self.largestClusterParticleCount),\
               file = fileHandler)



    def checkForErrors(self):
              
       assert self.forwardMinParticleCount == self.backwardMinParticleCount,\
           'Min # particles is != in forward and backward burning\n' \
            f'time={self.time}\n'\
            f'forward burning particle # ={self.forwardMinParticleCount}, \n'\
            f'backward burning particle # = {self.backwardMinParticleCount}'
            
       self.minPathParticleCount  = self.forwardMinParticleCount



    def getSummaryBackwardBurning(self,endParticle,burntParticleCountTot):
     
        self.backwardMinParticleCount = endParticle.backwardBurningTime
        self.totalParticleCount       = burntParticleCountTot
       
           

    def getSummaryForwardBurning(self,particles,startParticle,endParticle):

        self.forwardMinParticleCount = endParticle.forwardBurningTime
        self.getMinPathLength(particles,startParticle,endParticle)



    def getMinPathLength(self,particles,startParticle,endParticle):
        ''' Sum of inteparticle distances along shortest path connecting backbone extremes
            It is calculated by going backwards, from one particle to its burner
        '''
        
        connectedLength = 0.
        particle = endParticle
    
        while particle != startParticle:
        #while particle.isBurntByParticleIndex != None:
    
            burnerIndex = particle.isBurntByParticleIndex
            burner      = particles[burnerIndex]
        
            dLength = burner.distanceToParticle(particle)
            connectedLength = connectedLength + dLength
    
            particle = burner            
            
        self.minPathLength = connectedLength