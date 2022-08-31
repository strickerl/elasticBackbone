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

from define_parameters import defineParameters
from backbone_one_frame import calculateBackboneOneFrame
from IO_operations import defineIOFileNames
from IO_operations import defineSummaryOutputFileName
from IO_operations import extractInputFileList

import BackboneTimeEvolution
reload(BackboneTimeEvolution)
from BackboneTimeEvolution import BackboneTimeEvolution



parameters = defineParameters()
                                  
#Import data from .dat file inside the folder \Input
baseFolder                     = os.path.dirname(__file__)  #absolute dir the present script is in
[inputFileList,inputFileCount] = extractInputFileList(baseFolder)


summaryOutputFileName  = defineSummaryOutputFileName(baseFolder)
fileSummaryOuputHandle = open(summaryOutputFileName,'w')


#Create instance of class
backboneAllTimes = BackboneTimeEvolution(inputFileCount)

#Loop over time instants
timeIndex = -1
for fileName in inputFileList:     
    timeIndex = timeIndex + 1
    time      = int("".join(filter(str.isdigit, fileName)))  #Extract time from file name
    
    fileNamesIO = defineIOFileNames(baseFolder,fileName)     #For input/output
    print(fileNamesIO.raw)       
    
    backboneOneFrame = calculateBackboneOneFrame(fileNamesIO,time,timeIndex,parameters) 
     
    backboneOneFrame.printFileSummary(fileSummaryOuputHandle)   
    
    backboneAllTimes.values[timeIndex] = backboneOneFrame  

     
fileSummaryOuputHandle.close()                        
backboneAllTimes.printOnScreen()