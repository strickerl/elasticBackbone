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
        node1 = Point(self.lengthX,0.,0.)
        node2 = Point(self.lengthX,self.lengthY,0.)
        node3 = Point(0.,self.lengthY,0.)
        node4 = Point(0.,0.,self.lengthZ)
        node5 = Point(self.lengthX,0.,self.lengthZ)
        node6 = Point(self.lengthX,self.lengthY,self.lengthZ)
        node7 = Point(0.,self.lengthY,self.lengthZ)

        
        #     Front:         Back:
        #    7     6        3     2  
        #    x_____x        x_____x
        #    |     |        |     |
        #    |     |        |     |
        #    x_____x        x_____x
        #    4     5        0     1
        
        
        self.nodes = (node0,node1,node2,node3,node4,node5,node6,node7)
        
        
        
    def defineFixedNodesToSetBackboneExtremes(self,parameters):
                     
        self.fixedNodePair[0] = self.nodes[parameters.boxNodeStart]
        self.fixedNodePair[1] = self.nodes[parameters.boxNodeEnd]