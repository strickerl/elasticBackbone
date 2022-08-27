# -*- coding: utf-8 -*-

"""
Created on Sat Aug 27 03:44:56 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""


def define_parameters():


    """
    Returns
    -------
    PARAMETERS : LIST
    
      RADIUS_MIN, RADIUS_MAX = minimum and maximum particle size     
            
      FLAG_FIXED_EXTREMES_BACKBONE : INT
            flag telling if the initial and final points of the burning algorithm are
            (1): fixed in time
            (0): recalculated at each time step.

    """

    
    RADIUS_MIN = 0.45                 #Radius of small particles (chemicalType = 1)
    RADIUS_MAX = 0.55                 #Radius of large particles (chemicalType = 2)
    FLAG_FIXED_EXTREMES_BACKBONE = 1  #1:extremes for burning algorithm constant
                                      #0:recalculated at each time

    #Which pair of vertices is used if FLAG_FIXED_EXTREMES_BACKBONE == 1
    # is defined in Box.fixedVerticesForBurningAlgorithm. The box can change size, 
    # therefore the actual vertices are recalculated at each time 

            
    return [RADIUS_MIN, RADIUS_MAX, FLAG_FIXED_EXTREMES_BACKBONE]             
                                      
  
                        
  


        
                              