# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 03:30:39 2022

@author: Laura Stricker
"""

from importlib import reload
import numpy as np
import matplotlib.pyplot as plt

import Vector
reload(Vector)
from Vector import Vector

import Point
reload(Point)
from Point import Point

import Backbone
reload(Backbone)
from Backbone import Backbone

import SimulationBox
reload(SimulationBox)
from SimulationBox import SimulationBox



class BackboneTimeEvolution:

    
    def __init__(self,timeCount):
    
        self.values    = np.zeros(timeCount, dtype=object)
        self.timeCount = timeCount



    def setValuesOneFrame(self,timeIndex):
        
        self.values[timeIndex] = Backbone

        

    def printOnScreen(self):

        time                    = np.asarray([backbone.time                   for backbone in self.values])   
        nParticleMinBackbone    = np.asarray([backbone.minPathParticleCount   for backbone in self.values]) 
        nParticleTotBackbone    = np.asarray([backbone.totalParticleCount     for backbone in self.values]) 
        nParticleLargestCluster = np.asarray([backbone.largestClusterParticleCount for backbone in self.values]) 
        connectedLengthMin      = np.asarray([backbone.minPathLength          for backbone in self.values])
        linearDistance          = np.asarray([backbone.linearDistanceExtremes for backbone in self.values])

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
        plt.plot(time, nParticleMinBackbone/nParticleLargestCluster)
        plt.xlabel('Time')
        plt.ylabel('Min # particles P1P2/ Tot # particles cluster')
        plt.show()
    
        plt.figure(3)
        plt.plot(time, connectedLengthMin)
        plt.xlabel('Time')
        plt.ylabel('Min connected path P1P2 [Length]')
        plt.show()
    
        plt.figure(4)
        plt.plot(time, connectedLengthMin/linearDistance)
        plt.xlabel('Time')
        plt.ylabel('Min connected path / linear distance (P1P2) ')
        plt.show()        