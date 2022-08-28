# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:24:11 2022

@author: Laura Stricker
"""

def enum(**enums):
    return type('Enum', (), enums)