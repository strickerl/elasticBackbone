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
from IO_operations import defineFileNames
from IO_operations import extractInputFileList

import Backbone
reload(Backbone)
from Backbone import BackboneTimeEvolution



parameters = defineParameters()
                                  
#Import data from .dat file inside the folder \Input
[inputFileList,fileCount,path] = extractInputFileList()

#Open summary output file
folder             = os.path.dirname(__file__)  #absolute dir the present script is in
fileNameSummary    = 'Summary.dat'
summaryOutputFile  = folder + '/Output/' + fileNameSummary
fileSummaryOuputHandle = open(summaryOutputFile,'w')

#Create instance of class
backboneAllTimes = BackboneTimeEvolution(fileCount)


#Loop over time instants
timeIndex = -1
for fileName in inputFileList:     
    timeIndex = timeIndex + 1
    time      = int("".join(filter(str.isdigit, fileName)))  #Extract time from file name
    
    filesIO = defineFileNames(folder,path,fileName)        #For input/output
    print(filesIO.raw)       
    
    backboneOneFrame = calculateBackboneOneFrame(path,filesIO,time,timeIndex,parameters) 
     
    backboneOneFrame.printFile(fileSummaryOuputHandle)   
    
    backboneAllTimes.values[timeIndex] = backboneOneFrame  

     
fileSummaryOuputHandle.close()                        
backboneAllTimes.printOnScreen()