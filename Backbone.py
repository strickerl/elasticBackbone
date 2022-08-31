# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 23:57:04 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""


import numpy as np
import matplotlib.pyplot as plt

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
        self.extremes               = np.ndarray((2,), object = Particle)
        self.linearDistanceExtremes   = float()
        self.allMinPathsParticleCount = int
        self.largestClusterParticleCount = len(particles)
        self.forwardBurnParticleCount = int
        self.forwardBurnParticleCount = int
        

    def calculateLinearDistanceBetweenExtremes(self):
        
        particle1 = self.extremes[0]
        particle2 = self.extremes[1]
        
        self.linearDistanceExtremes = particle1.distanceToParticle(particle2)

        

    def printFileSummary(self,fileHandler):
                
        print("{:6d}".format(self.timeIndex),\
              "{:.2f}".format(self.time),\
              "{:6d}".format(self.minParticleCount),\
              "{:.2f}".format(self.minConnectedPath), \
              "{:6d}".format(self.totalParticleCount),\
              "{:.2f}".format(self.linearDistanceExtremes),\
              "{:6d}".format(self.largestClusterParticleCount),\
               file = fileHandler)



    def checkForErrors(self):
              
       assert self.forwardBurnParticleCount == self.backwardBurnParticleCount,\
           'Min # particles is != in forward and backward burning\n' \
            f'time={self.time}\n'\
            f'forward burning particle # ={self.forwardBurnParticleCount}, \n'\
            f'backward burning particle # = {self.backwardBurnParticleCount}'

       
           

    def getSummaryForwardBurning(self,particles,startParticle,endParticle):

        endParticleIndex = endParticle.index         

        self.forwardBurnParticleCount = particles[endParticleIndex]
        self.minPathParticleCount     = self.forwardBurnParticleCount
        self.minPathLength = self.getMinPathLength(particles,endParticle)



    def getMinPathLength(self,particles,endParticle):
        ''' Sum of inteparticle distances along shortest path connecting backbone extremes
            It is calculated by going backwards, from one particle to its burner
        '''
        
        connectedLength = 0.
        particle = endParticle
    
        while particle.isBurntByParticleIndex != None:
    
            burnerIndex = particle.isBurntByParticleIndex
            burner      = particles[burnerIndex]
        
            dLength = burner.distanceToParticle(particle)
            connectedLength = connectedLength + dLength
    
            particle = burner            



class BackboneAllTimes:
    
    def __init__(self,timeCount):
    
        self.values    = np.zeros(timeCount, dtype=object)
        self.timeCount = timeCount


    def setValuesOneFrame(self,timeIndex):
        
        self.all[timeIndex] = Backbone
        

    def printOnScreen(self):

        timeCount  =  self.timeCount
        time                    = [self.allTimes[timeIndex].time for timeIndex in range(0,timeCount)]        
        nParticleMinBackbone    = [self.allTimes[timeIndex].minParticleCount for timeIndex in range(0,timeCount)] 
        nParticleTotBackbone    = [self.allTimes[timeIndex].totalParticleCount for timeIndex in range(0,timeCount)] 
        nParticleLargestCluster = [self.allTimes[timeIndex].largestClusterParticleCount for timeIndex in range(0,timeCount)] 
        connectedLengthMin      = [self.allTimes[timeIndex].minPathLength for timeIndex in range(0,timeCount)]
        linearDistance          = [self.allTimes[timeIndex].linearDistanceExtremes for timeIndex in range(0,timeCount)]

        ax = plt.figure(1)
        line1, = plt.plot(time, nParticleMinBackbone,'r')
        line2, = plt.plot(time, nParticleTotBackbone,'b')
        plt.xlabel('Time')
        plt.ylabel('Min connected path (P1P2)')
        plt.show()
        line1.set_label('Min # particles')
        line2.set_label('Tot # particles elastic backbone')
        ax.legend()
    
        plt.figure(2)
        plt.plot(time, [nParticleMinBackbone[index]/nParticleLargestCluster[index] for index in range(0,timeCount)])
        plt.xlabel('Time')
        plt.ylabel('Min # particles P1P2/ Tot # particles cluster')
        plt.show()
    
        plt.figure(3)
        plt.plot(time,connectedLengthMin)
        plt.xlabel('Time')
        plt.ylabel('Min connected path P1P2 [Length]')
        plt.show()
    
        plt.figure(4)
        plt.plot(time, [connectedLengthMin[index]/linearDistance[index] for index in range(0,timeCount)])
        plt.xlabel('Time')
        plt.ylabel('Min connected path / linear distance (P1P2) ')
        plt.show()        