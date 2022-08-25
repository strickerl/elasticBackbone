# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 21:26:08 2022

@author: Laura Stricker
"""

import os
from importlib import reload

from elastic_backbone_one_frame import calculate_elastic_backbone_one_frame
from IO_operations import define_file_names
from IO_operations import extract_input_file_list

import ElasticBackbone
reload(ElasticBackbone)
from ElasticBackbone import ElasticBackboneTimeEvolution


#Parameters of the simulations 
RADIUS_MIN = 0.45              #Radius of particles of chemicalType = 1
RADIUS_MAX = 0.55              #Radius of particles of chemicalType = 2
FLAG_FIXED_POINTS_P1P2 = 1     #1: points P1,P2 constant; 0: P1,P2 recalculated at each time 

#Import data from .dat file inside the folder \Input
[inputFileList,fileCount,path] = extract_input_file_list()

#Open summary output file
folder             = os.path.dirname(__file__)  #absolute dir the present script is in
fileNameSummary    = 'Summary.dat'
summaryOutputFile  = folder + '/Output/' + fileNameSummary
fileSummaryOuputHandler = open(summaryOutputFile,'w')

#Create instance of class
ElasticBackboneAllTimes = ElasticBackboneTimeEvolution(fileCount)


#Loop over time instants
timeIndex = -1
for fileName in inputFileList:     
    timeIndex = timeIndex + 1
    time      = int("".join(filter(str.isdigit, fileName)))  #Extract time from file name
    
    FilesIO = define_file_names(folder,path,fileName)       #Name of files for input/output
    print(FilesIO.raw)       
    
    ElasticBackboneOneFrame =  calculate_elastic_backbone_one_frame\
                              (path,FilesIO,time,timeIndex,RADIUS_MIN,RADIUS_MAX,FLAG_FIXED_POINTS_P1P2) 
     
    ElasticBackboneOneFrame.printFile(fileSummaryOuputHandler)   
    
    ElasticBackboneAllTimes.all[timeIndex] = ElasticBackboneOneFrame  

     
fileSummaryOuputHandler.close()                        
ElasticBackboneAllTimes.printOnScreen()

