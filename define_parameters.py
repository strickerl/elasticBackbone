# -*- coding: utf-8 -*-

"""
Created on Sat Aug 27 03:44:56 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""
from my_enum import enum
from importlib import reload

import Parameters
reload(Parameters)
from Parameters import Parameters


def define_parameters():
    """
    Input
    -----    
      RADIUS_MIN, RADIUS_MAX = FLOAT
          minimum and maximum particle size     
                
      BACKBONE_EXTREMES_FLAG : INT
            the box nodes used to calculate initial and final particles of the 
            burning algorithm are (1): fixed in time or (0): recalculated at each time step.
    
    Returns
    -------
      MyParameters : class
    """    

    PARTICLE_RADIUS_MIN = 0.45      #Small particles (chemicalType = 1)
    PARTICLE_RADIUS_MAX = 0.55      #Large particles (chemicalType = 2)
    
    
    #Choice of box nodes to use to set the backbone start/end points for burning algorithm
    CLOSEST_BOX_NODES      = enum(RECACULATE_EACH_FRAME = 0, CONSTANT_FOR_ALL_TIMES = 1)
    BACKBONE_EXTREMES_FLAG = CLOSEST_BOX_NODES.CONSTANT_FOR_ALL_TIMES   
                     
    
    #If user chooses fixed box nodes, they have to choose which ones

    if  BACKBONE_EXTREMES_FLAG == CLOSEST_BOX_NODES.CONSTANT_FOR_ALL_TIMES :
        
        #     Front:         Back:
        #    3     2        7     6  
        #    x_____x        x_____x
        #    |     |        |     |
        #    |     |        |     |
        #    x_____x        x_____x
        #    0     1        4     5
        NODE_START = 0
        NODE_END   = 6
    else:
        NODE_START = None
        NODE_END   = None        
    
    
    myParameters = Parameters(PARTICLE_RADIUS_MIN,PARTICLE_RADIUS_MAX,\
                              BACKBONE_EXTREMES_FLAG,NODE_START,NODE_END)
    
    return myParameters









                     
  


        
                              