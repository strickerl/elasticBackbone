# -*- coding: utf-8 -*-

"""
Created on Sat Aug 27 03:44:56 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""
from myEnum import enum
from importlib import reload

import Parameters
reload(Parameters)
from Parameters import Parameters

import configparser
    

def defineParameters():
    """
        It reads from .config file, where the user defines the parameters

    Structure of .config file
    -------------------------
    [Particle radii] 
    # Min for chemicalType 1, Max for chemicalType2 
    PARTICLE_RADIUS_MIN = float
    PARTICLE_RADIUS_MAX = float
        
    [Box nodes for backbone extremes]   
    # 0: recalculate them at each time; 1: constant for all times
    BACKBONE_EXTREMES_FLAG = int   
                         
    [Fixed box nodes]    
    # If user chooses box nodes constant for all times, they have to choose which ones
    NODE_START = int
    NODE_END   = int   
    
    Returns
    -------
      MyParameters : OBJECT(Parameters)
    """   
    CLOSEST_BOX_NODES   = enum(RECACULATE_EACH_FRAME = 0, CONSTANT_FOR_ALL_TIMES = 1)

    #Box node numeration:
    #    Front:         Back:
    #    7     6        3     2  
    #    x_____x        x_____x
    #    |     |        |     |
    #    |     |        |     |
    #    x_____x        x_____x
    #    4     5        0     1
  
    config = configparser.ConfigParser()
    config.read('myParameters.config')

    paramRadii = config['Particle radii']
    PARTICLE_RADIUS_MIN = float( paramRadii['PARTICLE_RADIUS_MIN'])
    PARTICLE_RADIUS_MAX = float( paramRadii['PARTICLE_RADIUS_MAX'])

    # Choice of box nodes to use to set the backbone start/end points for burning algorithm
    paramBackboneExtremesFlag = config['Box nodes for backbone extremes']   
    BACKBONE_EXTREMES_FLAG = int( paramBackboneExtremesFlag['BACKBONE_EXTREMES_FLAG'])


    # Fixed box nodes
    paramFixedBoxNodes = config['Fixed box nodes']    
    if  BACKBONE_EXTREMES_FLAG == CLOSEST_BOX_NODES.CONSTANT_FOR_ALL_TIMES :     
        NODE_START = int(paramFixedBoxNodes['NODE_START'])
        NODE_END   = int(paramFixedBoxNodes['NODE_END'])
    else:
         NODE_START = None
         NODE_END   = None        

    myParameters = Parameters(PARTICLE_RADIUS_MIN,PARTICLE_RADIUS_MAX,\
                              BACKBONE_EXTREMES_FLAG,NODE_START,NODE_END)
    
    return myParameters