# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 14:05:44 2022
@author: Laura Stricker laura.stricker@mat.ethz.ch
"""

from myEnum import enum
CLOSEST_BOX_NODES = enum(RECACULATE_EACH_FRAME = 0, CONSTANT_FOR_ALL_TIMES = 1)


class Parameters:
    
    def __init__(self,particleRadiusMin,particleRadiusMax,backboneExtremesFlag,\
                      nodeStart,nodeEnd):
        
        self.radiusMin = particleRadiusMin
        self.radiusMax = particleRadiusMax
        self.backbone_extremes_flag = backboneExtremesFlag
        self.boxNodeStart = nodeStart
        self.boxNodeEnd   = nodeEnd


    def useConstantBoxNodesForBackboneExtremes(self):
        '''to know what is currently set'''
        return (self.backbone_extremes_flag == CLOSEST_BOX_NODES.CONSTANT_FOR_ALL_TIMES)