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
        self.forwardBurning        = object(BurningRound)
        self.backwardBurning       = object(BurningRound)
        

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
       
       particleCountForward = self.forwardBurning.particleCount
       particleCountBackward = self.backwardBurning.particleCount
       
       assert particleCountForward == particleCountBackward,\
           'Min # particles is != in forward and backward burning\n' \
            f'time={self.time}\n'\
            f'forward burning particle # ={particleCountForward}, \n'\
            f'backward burning particle # = {particleCountBackward}'



class BurningRound:
    
    def __init__(self,particleCount):

        self.particleCount = particleCount




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