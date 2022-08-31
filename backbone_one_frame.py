# -*- coding: utf-8 -*-
"""
Created on Mon May  6 14:20:01 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch

    Routines to calculate elastic backbone for a single particle configuration
    by implementing the burning algorithm described in
        H J Herrmann et al, J. Phys. A: Math. Gen., 17 L261, 1984

"""
import numpy as np
from importlib import reload
from burning_algorithm import forwardBurning
from burning_algorithm import backwardBurning


import Backbone
reload(Backbone)
from Backbone import Backbone

import SimulationBox
reload(SimulationBox)
from SimulationBox import SimulationBox

import Particle
reload(Particle)
from Particle import Particle

import Point
reload(Point)
from Point import Point


def findClosestParticleToPoint(particles,pointP):
    '''Function that finds the minimum distance between pointP (xP,yP,zP) and 
        all particles contained in a list'''  
           
    particleDistancesToPoint = np.asarray([p.distanceToPoint(pointP) for p in particles])
        
    # Get the index (not the ID) of particle with smallest distance to pointP 
    indexClosestParticleToPoint= np.argmin(particleDistancesToPoint )
    
    closestParticleToPoint = particles[indexClosestParticleToPoint]
    
    return closestParticleToPoint




def findBurningAlgorithmExtremes(box,particles,parameters,backbone): 
    '''
    Find the particles P1,P2 to use as initial and final point for the 
    burning algorithm


    Parameters
    ----------
    box : OBJECT(SimulationBox)
    particles : ARRAY of OBJECTS(Particle) = particles of the largest cluster
    parameters: OBJECT(Parameters)    


    Returns
    -------
    backboneExtremeParticles : array(2,OBJECT(Particle))
    '''
    

    box.findNodes()   

    if  parameters.use_constant_box_nodes_for_backbone_extremes:          
        
        #Box can change size but the box node pair reamins constant 
        box.defineFixedNodesToSetBackboneExtremes(parameters)  
        fixedBoxNodes = box.fixedNodePair             

        #Find the closest particles to the two fixed box vertices
        backboneExtremes = np.asarray([findClosestParticleToPoint(particles,node) for node in fixedBoxNodes])
        
    
    else: 

        #Find closer particles to box nodes (one per node)
        closestParticlesToNodes = [findClosestParticleToPoint(particles,node) for node in box.nodes]

        #Find particle pair further apart
        particleDistanceMax = 0.        
        for index1, particle1 in enumerate(closestParticlesToNodes):    
            
            for particle2 in closestParticlesToNodes[index1+1:]:  
                
                particleDistance = particle1.distanceToParticle(particle2)
                
                if particleDistance > particleDistanceMax:
                    particleDistanceMax = particleDistance
                    backboneExtremes    = np.array(particle1,particle2)


    backbone.extremes = backboneExtremes
    backbone.calculateLinearDistanceBetweenExtremes()


 

def calculateBackboneOneFrame(fileNamesIO,time,timeIndex,parameters):
    '''             
    It calculates the elastic backbone for a single particle configuration, 
    corresponding to a single time instant, provided by a .dat file.

    Parameters
    ----------
    nameFilesIO : OBJECT(NameFilesIO)
        it contains names of input/output files and the bare name.
    parameters : OBJECT(Parameter)
    time : FLOAT
    timeIndex : INT
    
    Returns
    -------
     backbone = OBJECT(Backbone)
         summary of general info on backbone for one time instant   
    
    Input file
    ----------    
    File with an instantaneous particle configuration, with the data structure:
        
        Number of particles
        [empty line]
        particleID   particleType   positionX   positionY   positionZ   particleVoronoiVolume   clusterID   numberOfNeighbours   listOfNeighbourIDs(variable length)
        particleID   particleType   positionX   positionY   positionZ   particleVoronoiVolume   clusterID   numberOfNeighbours   listOfNeighbourIDs(variable length)
        ...


    Output file
    -----------    
     .xyz file that can be used as input in the Ovito visualization tool
     and has the following structure:
         
         numberOfParticle
         [empty line]
         positionX   positionY   positionZ  chemicalType   radius  particleForwardBurningTime particleBackwardBurningTime  particleID
         positionX   positionY   positionZ  chemicalType   radius  particleForwardBurningTime particleBackwardBurningTime  particleID
         ...

    '''    
    import DataManager
    reload(DataManager)
    from DataManager import DataManager
    
    from my_enum import enum
    CLUSTER_ID   = enum(LARGEST_CLUSTER = 1)
    
    
    DM = DataManager()
    DM.loadDataFromFile(fileNamesIO.input)

    
    #Retain only particles belonging to largest cluster
    DM.filterParticlesByClusterID(CLUSTER_ID.LARGEST_CLUSTER)
    DM.setParticleRadii(parameters)
    
    #Conversion table: particle ID --> index
    DM.buildParticleIndexFromIDlookup()
    DM.setParticleIndexes()
       
    #Shift box so that origin coincides with min(x,y,z) of particles
    DM.shiftOriginOfAxes()

    
    # CALCULATE ELASTIC BACKBONE
    #---------------------------
    backbone = Backbone(timeIndex,time,DM.particles)
    
    findBurningAlgorithmExtremes(DM.box,DM.particles,parameters,backbone)
    
    #Find backbone length = min # connected particles and min path between extremes
    forwardBurning(DM,backbone)    
    
    #Find whole backbone = all equivalent paths between extremes
    backwardBurning(DM,backbone)
    
    backbone.checkForErrors()


    DM.printXYZFile(DM.particles,fileNamesIO.output)
    
    

    return backbone