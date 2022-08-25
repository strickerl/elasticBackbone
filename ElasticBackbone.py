# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 23:57:04 2022

@author: Laura Stricker
"""


import numpy as np
import matplotlib.pyplot as plt


class ElasticBackbone:


    def __init__(self):
    
        
        self.timeIndex           = int
        self.time                = float
        self.minParticleCount    = int
        self.minConnectedPath    = float
        self.totalParticleCount  = int
        self.linearDistanceExtremes      = float          
        self.largestClusterParticleCount = int   
        #self.pathToFile = pathToFile



    def setValues(self,timeIndex,time,minParticleCount,minPathLength,\
                  totalParticleCount,largestClusterParticleCount,linearDistanceExtremes):

        self.timeIndex          = timeIndex
        self.time               = time
        self.minParticleCount   = minParticleCount
        self.minConnectedPath   = minPathLength
        self.totalParticleCount = totalParticleCount
        self.linearDistanceExtremes      = linearDistanceExtremes
        self.largestClusterParticleCount = largestClusterParticleCount


            
    def printFile(self,fileHandler):
                
        print("{:.2f}".format(self.time),\
              "{:6d}".format(self.minParticleCount),\
              "{:.2f}".format(self.minPathLength), \
              "{:6d}".format(self.totalParticleCount),\
              "{:.2f}".format(self.linearDistanceExtremes),\
              "{:6d}".format(self.largestClusterParticleCount),\
                file = fileHandler)
        



class ElasticBackboneTimeEvolution:
    
    
    def __init__(self,timeCount):
    
        self.all       = np.zeros(timeCount, dtype=object)
        self.timeCount = timeCount


    def setValuesOneFrame(self,timeIndex):
        
        self.all[timeIndex] = ElasticBackbone
        


    def printOnScreen(self):

        timeCount  =  self.timeCount
        time                    = [self.all[index].time for index in range(0,timeCount)]        
        nParticleMinBackbone    = [self.all[index].minParticleCount for index in range(0,timeCount)] 
        nParticleTotBackbone    = [self.all[index].totalParticleCount for index in range(0,timeCount)] 
        nParticleLargestCluster = [self.all[index].largestClusterParticleCount for index in range(0,timeCount)] 
        connectedLengthMin      = [self.all[index].minPathLength for index in range(0,timeCount)]
        linearDistance          = [self.all[index].linearDistanceExtremes for index in range(0,timeCount)]


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
        
        
        
        
        