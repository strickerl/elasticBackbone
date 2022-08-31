# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 14:05:44 2022

@author: Laura Stricker
"""

from myEnum import enum
CLOSEST_BOX_NODES = enum(RECACULATE_EACH_FRAME = 0, CONSTANT_FOR_ALL_TIMES = 1)


class Parameters:
    
    def __init__(self,PARTICLE_RADIUS_MIN,PARTICLE_RADIUS_MAX,\
                 BACKBONE_EXTREMES_FLAG,NODE_START,NODE_END):
        
        self.radiusMin = PARTICLE_RADIUS_MIN
        self.radiusMax = PARTICLE_RADIUS_MAX
        self.backbone_extremes_flag = BACKBONE_EXTREMES_FLAG
        self.boxNodeStart = NODE_START
        self.boxNodeEnd   = NODE_END


    def use_constant_box_nodes_for_backbone_extremes(self):
        '''to know what is currently set'''
        return (self.backbone_extremes_flag == CLOSEST_BOX_NODES.CONSTANT_FOR_ALL_TIMES)