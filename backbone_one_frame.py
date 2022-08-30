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
from burning_algorithm import forward_burning
from burning_algorithm import backward_burning


import Backbone
reload(Backbone)
from Backbone import Backbone

import SimulationBox
reload(SimulationBox)
from SimulationBox import SimulationBox

import Particle
reload(Particle)
from Particle import Particle, ParticlePair

import Point
reload(Point)
from Point import Point


def find_closest_particle_to_point(particles,pointP):
    '''Function that finds the minimum distance between pointP (xP,yP,zP) and 
        all particles contained in a list'''  
           
    particleDistancesToPoint = np.asarray([p.get_distance_from_point(pointP) for p in particles])
        
    # Get the index (not the ID) of particle with smallest distance to pointP 
    indexClosestParticleToPoint= np.argmin(particleDistancesToPoint )
    
    closestParticleToPoint = particles[indexClosestParticleToPoint]
    
    return closestParticleToPoint




def find_start_end_particles_for_burning_algorithm(box,particles,parameters,backbone): 
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
        box.defineFixedNodesToSetBackboneExtremes(box,parameters)  
        fixedBoxNodes = box.fixedNodePair             

        #Find the closest particles to the two fixed box vertices
        backboneExtremes = np.asarray([find_closest_particle_to_point(particles,node) for node in fixedBoxNodes])
        
    
    else: 

        #Find closer particles to box nodes (one per node)
        closestParticlesToNodes = [find_closest_particle_to_point(particles,node) for node in box.nodes]

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


 

def calculate_backbone_one_frame(fileNamesIO,time,timeIndex,parameters):
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
    DM.load_data_from_simulation_file(fileNamesIO.input)
    
    
    #Retain only particles belonging to largest cluster
    DM.filter_particles_by_cluster_ID(CLUSTER_ID.LARGEST_CLUSTER)
    
    #Conversion table: particle ID --> index
    DM.set_particle_index_from_ID_lookup()
       
    #Shift box so that origin coincides with min(x,y,z) of particles
    DM.shift_origin_of_axes()

    
    # CALCULATE ELASTIC BACKBONE
    #---------------------------
    backbone = Backbone(timeIndex,time)
    
    find_start_end_particles_for_burning_algorithm(DM.box,DM.particles,parameters,backbone)
    
    
    #Find backbone length = min # connected particles and min path between extremes
    forward_burning(DM.particles,DM.box,backbone)    
    
    #Find whole backbone = all equivalent paths between extremes
    backward_burning(DM.particles,DM.box,backbone)
    
    backbone.checkForErrors()


    DM.printXYZFile(DM.particles,fileNamesIO.output)
    
    

    return backbone