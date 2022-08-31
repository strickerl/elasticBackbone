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
  
    fileNameSummary        = 'Summary.dat'
    summaryOutputFileName  = baseFolder + '/Output/' + fileNameSummary

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




def Plot_results(time,MinN_P1P2,N_ElBackbone,Ntot,MinPath_P1P2,dist_P1P2):
    '''Plot figures'''
      
    
    ax = plt.figure(1)
    line1, = plt.plot(time,MinN_P1P2,'r')
    line2, = plt.plot(time,N_ElBackbone,'b')
    plt.xlabel('time')
    plt.ylabel('Min path (P1P2)')
    plt.show()
    line1.set_label('N particles min P1P2')
    line2.set_label('N particles elastic backbone')
    ax.legend()

    plt.figure(2)
    plt.plot(time,np.array(MinN_P1P2)/np.array(Ntot))
    plt.xlabel('time')
    plt.ylabel('Min N between P1P2/ Ntot')
    plt.show()

    plt.figure(3)
    plt.plot(time,MinPath_P1P2)
    plt.xlabel('time')
    plt.ylabel('Min path (P1P2) [Length]')
    plt.show()

    plt.figure(4)
    plt.plot(time,np.array(MinPath_P1P2)/np.array(dist_P1P2))
    plt.xlabel('time')
    plt.ylabel('Min path / dist (P1P2) ')
    plt.show()

    return