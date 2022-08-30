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

from define_parameters import define_parameters
from backbone_one_frame import calculate_backbone_one_frame
from IO_operations import define_file_names
from IO_operations import extract_input_file_list

import Backbone
reload(Backbone)
from Backbone import BackboneTimeEvolution



parameters = define_parameters()
                                  
#Import data from .dat file inside the folder \Input
[inputFileList,fileCount,path] = extract_input_file_list()

#Open summary output file
folder             = os.path.dirname(__file__)  #absolute dir the present script is in
fileNameSummary    = 'Summary.dat'
summaryOutputFile  = folder + '/Output/' + fileNameSummary
fileSummaryOuputHandler = open(summaryOutputFile,'w')

#Create instance of class
backboneAllTimes = BackboneTimeEvolution(fileCount)


#Loop over time instants
timeIndex = -1
for fileName in inputFileList:     
    timeIndex = timeIndex + 1
    time      = int("".join(filter(str.isdigit, fileName)))  #Extract time from file name
    
    filesIO = define_file_names(folder,path,fileName)        #For input/output
    print(filesIO.raw)       
    
    backboneOneFrame = calculate_backbone_one_frame(path,filesIO,time,timeIndex,parameters) 
     
    backboneOneFrame.printFile(fileSummaryOuputHandler)   
    
    backboneAllTimes.values[timeIndex] = backboneOneFrame  

     
fileSummaryOuputHandler.close()                        
backboneAllTimes.printOnScreen()