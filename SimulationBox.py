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


        self.lengthX   = float(lengthX)
        self.lengthY   = float(lengthY)
        self.lengthZ   = float(lengthZ)
        self.nodes     = np.zeros(8, dtype=object)
        self.fixedNodePair = np.zeros(2, dtype=object)
    
    
    def findNodes(self):
        
        node0 = Point(0.,0.,0.)
        node1 = Point(self.lx,0.,0.)
        node2 = Point(0.,self.ly,0.)
        node3 = Point(0.,0.,self.lz)
        node4 = Point(self.lx,self.ly,0.)
        node5 = Point(self.lx,0.,self.lz)
        node6 = Point(0.,self.ly,self.lz)
        node7 = Point(self.lx,self.ly,self.lz)
        
        self.nodes = (node0,node1,node2,node3,node4,node5,node6,node7)
        
        
        
    def defineFixedNodesToSetBackboneExtremes(self,parameters):
             
        nodeStart = parameters.boxNodeStart
        nodeEnd   = parameters.boxNodeEnd
        
        self.fixedNodePair = self.nodes(nodeStart,nodeEnd)