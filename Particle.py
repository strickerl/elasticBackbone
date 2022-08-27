# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 03:26:58 2022

@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""


from importlib import reload
import numpy as np


import Point
reload(Point)
from Point import Point


class Particle:

    def __init__(self,positionX,positionY,positionZ,radius,index,ID):


        self.x   = float(positionX)
        self.y   = float(positionY)
        self.z   = float(positionZ)
        self.radius = float(radius)
        self.index  = int(index)
        self.ID     = int(ID)




class ParticlePair:

    def __init__(self,Particle1,Particle2):


        self.particle1 = Particle1(dtype = object)
        self.particle2 = Particle2(dtype = object)
        self.distance  = float() 
        
        
    def calculateDistance(self,Particle1,Particle2): 
        
        x1 = Particle1.x
        y1 = Particle1.y
        z1 = Particle1.z
        x2 = Particle2.x
        y2 = Particle2.y
        z2 = Particle2.z       
        
        self.distance  = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2) 
        
        
        
class AllParticlesOneInstant:
    
    def __init__(self,particlesDataFrame):


        self.count = len(particlesDataFrame)
        self.x            = np.array(particlesDataFrame['x'])
        self.y            = np.array(particlesDataFrame['y'])
        self.z            = np.array(particlesDataFrame['z'])
        self.radius       = np.array(particlesDataFrame['radius'])
        self.particleID   = np.array(particlesDataFrame['IDparticle'])
        self.volume       = np.array(particlesDataFrame['volume'])
        self.chemicalType = np.array(particlesDataFrame['chemicalType'])
        self.NumberOfNeighbours  = np.array(particlesDataFrame['N_neighbours'])
        
        
        #I could create an array of objects Particle instead but then I will not be able to use the 
        # vectorial operations on np.array! 
        #OR I could use just lists for all these and still be able to use np.array
        #I would need a way to extract from the class of all particles all the .x
        