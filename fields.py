# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:19:03 2022

    Define fields for input operations from file

@author: Laura Stricker
"""

from my_enum import enum

HEADER_FIELDS = enum(PARTICLE_COUNT=0, 
                     CLUSTER_COUNT=1, 
                     SIZE_X=2, 
                     SIZE_Y=3, 
                     SIZE_Z=4)

FIELDS = enum(PARTICLE_ID=0, 
              CHEMICAL_TYPE=1, 
              X=2, 
              Y=3, 
              Z=4, 
              VOLUME=5, 
              CLUSTER_ID=6, 
              NEIGHBOUR_COUNT=7, 
              NEIGHBOURS=8)