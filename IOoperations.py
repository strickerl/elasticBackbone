# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 16:35:29 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch

        Input/output operations

"""

import os
import re
from importlib import reload
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import make_dataclass

import SimulationBox
reload(SimulationBox)
from SimulationBox import SimulationBox


def naturalSort(myList): 
    '''Sort alphanumeric list'''

    convert         = lambda text: int(text) if text.isdigit() else text.lower()
    alphanumericKey = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(myList, key = alphanumericKey)



def defineIOFileNames(baseFolder,fileName):
    '''Define name of input and output files, given the path'''    


    #Extract raw name, without .dat extension
    rawFileName = fileName[0:len(fileName)-4]

    inputFileName  = baseFolder + '/Input/'  + fileName    
    outputFileName = baseFolder + '/Output/' + rawFileName + '.xyz'
        
    
    #Create class with name of files
    fileNames = make_dataclass('fileNames', ['input', 'output', 'raw'])
    
    #Create and return instance of class Name_files
    return fileNames(inputFileName, outputFileName, rawFileName)



def defineSummaryOutputFileName(baseFolder):
  
    fileNameSummary        = 'summary.dat'
    summaryOutputFileName  = baseFolder + '/Output/' + fileNameSummary
    
    os.makedirs(os.path.dirname(summaryOutputFileName), exist_ok=True)

    return summaryOutputFileName
    


def extractInputFileList(baseFolder):
    '''
       Define list of input files with particle data, contained inside folder
       .\input
    '''   

    path          = baseFolder + r'/Input/'

    #List of files inside 'path'
    files = os.listdir(path)

    #Open files with the string ('keyword') in the name
    keyword           = "cluster_atoms"
    particleFileList  = [fileName for fileName in files if keyword in fileName]
    particleFileList  = naturalSort(particleFileList)      
    fileCount         = len(particleFileList)

    return particleFileList, fileCount