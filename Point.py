# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 03:09:28 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch
"""

from importlib import reload

import Vector
reload(Vector)
from Vector import Vector


class Point:

    def __init__(self,coordinateX,coordinateY,coordinateZ):

        self.position = Vector(coordinateX, coordinateY, coordinateZ)