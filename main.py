# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 21:26:08 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch

Project name: Local and global structures in 3D binary colloidal glasses

    This code calculates the elastic backbone of a series of particles 
    configurations by implementing the burning algorithm described in
          H J Herrmann et al, J. Phys. A: Math. Gen., 17 L261, 1984
            
"""

import os
from importlib import reload

from defineParameters import defineParameters
from backboneOneFrame import calculateBackboneOneFrame
from IOoperations import defineIOFileNames
from IOoperations import defineSummaryOutputFileName
from IOoperations import extractInputFileList

import BackboneTimeEvolution
reload(BackboneTimeEvolution)
from BackboneTimeEvolution import BackboneTimeEvolution



parameters = defineParameters()
                                  
#Import data from .dat file inside the folder \Input
baseFolder                     = os.path.dirname(__file__)  #absolute dir the present script is in
[inputFileList,inputFileCount] = extractInputFileList(baseFolder)


summaryOutputFileName  = defineSummaryOutputFileName(baseFolder)
fileSummaryOuputHandle = open(summaryOutputFileName,'w')

backboneAllTimes = BackboneTimeEvolution(inputFileCount)


for frameTimeIndex, fileNameOneFrame in enumerate(inputFileList):     
    
    frameTime      = int("".join(filter(str.isdigit, fileNameOneFrame)))  #Extract time from file name    
    fileNamesOneFrameIO = defineIOFileNames(baseFolder,fileNameOneFrame)  #For input/output
    print(fileNamesOneFrameIO.raw)       
    
    backboneOneFrame = calculateBackboneOneFrame(fileNamesOneFrameIO,frameTime,frameTimeIndex,parameters) 
     
    backboneOneFrame.printFileSummary(fileSummaryOuputHandle)   
    
    backboneAllTimes.values[frameTimeIndex] = backboneOneFrame  

     
fileSummaryOuputHandle.close()                        
backboneAllTimes.printOnScreen()