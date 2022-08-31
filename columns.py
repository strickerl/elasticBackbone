# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:19:03 2022
@author: Laura Stricker
    Define name of columns in the input files
"""
from myEnum import enum


HEADER_COLUMN_NAMES = enum(PARTICLE_COUNT=0, 
                           CLUSTER_COUNT=1, 
                           BOX_SIZE_X=2, 
                           BOX_SIZE_Y=3, 
                           BOX_SIZE_Z=4)

COLUMN_NAMES = enum(PARTICLE_ID=0, 
                CHEMICAL_TYPE=1, 
                X=2, 
                Y=3, 
                Z=4, 
                VOLUME=5, 
                CLUSTER_ID=6, 
                NEIGHBOUR_COUNT=7, 
                FIRST_NEIGHBOUR=8)