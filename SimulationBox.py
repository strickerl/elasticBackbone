# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 02:44:37 2022

@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""

import numpy as np
from importlib import reload

import Point
reload(Point)
from Point import Point


class SimulationBox:

    def __init__(self,lengthX,lengthY,lengthZ):


        self.lx   = float(lengthX)
        self.ly   = float(lengthY)
        self.lz   = float(lengthZ)
        self.vertices = np.zeros(8, dtype=object)
        self.fixedVertexPair = np.zeros(2, dtype=object)
    
    
    def findVertices(self):
        
        V1 = Point(0.,0.,0.)
        V2 = Point(self.lx,0.,0.)
        V3 = Point(0.,self.ly,0.)
        V4 = Point(0.,0.,self.lz)
        V5 = Point(self.lx,self.ly,0.)
        V6 = Point(self.lx,0.,self.lz)
        V7 = Point(0.,self.ly,self.lz)
        V8 = Point(self.lx,self.ly,self.lz)
        
        self.vertices = (V1,V2,V3,V4,V5,V6,V7,V8)
        
        
        
    def defineFixedVerticesForBurningAlgorithm(self):
             
        self.fixedVertexPair = self.vertices(0,7)