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
        
    # Get the index (not the ID) of smallest element in numpy array 
    indexClosestParticleToPoint= np.argmin(particleDistancesToPoint )
    
    closestParticleToPoint = particles[indexClosestParticleToPoint]
    
    return closestParticleToPoint




def find_start_end_particles_for_burning_algorithm(box,particles,parameters): 
    '''
    Find the particles P1,P2 to use as initial and final point for the 
    burning algorithm


    Parameters
    ----------
    Box : CLASS(SimulationBox)
    
    particles : LIST of CLASSES(Particle)
        
    FLAG_FIXED_EXTREMES_BACKBONE : INT
        vertices of simulation box used to calculate start/end points for burning algorithm are
        1:  always the same  0: recalculated at each time 

    Returns
    -------
    backboneExtremeParticles : CLASS
    '''
    

    box.findNodes()   
    

    if  parameters.use_constant_box_nodes_for_backbone_extremes:          
        
        #Box can change size but the box node pair reamins constant 
        box.defineFixedNodesToSetBackboneExtremes(box,parameters)  
        fixedBoxNodes = box.fixedNodePair             

        #Find the closest particles (of the largest cluster) to the two fixed box vertices
        backboneExtremes = np.asarray([find_closest_particle_to_point(particles,node) for node in fixedBoxNodes])
        
    
    
    else: 

        #Find closer particles (of the largest cluster) to box nodes (one per node)
        closestParticlesToNodes = [find_closest_particle_to_point(particles,node) for node in box.nodes]

        #Find the largest distance between particles close to box nodes
        particleDistanceMax = 0.
        
        for index1, particle1 in enumerate(closestParticlesToNodes):    
            
            for particle2 in closestParticlesToNodes[index1+1:]:  
                
                particleDistance = particle1.distanceToParticle(particle2)
                
                if particleDistance > particleDistanceMax:
                    particleDistanceMax = particleDistance
                    backboneExtremes    = np.array(particle1,particle2)


    return backboneExtremes

 

def calculate_backbone_one_frame(folder,fileNamesIO,time,timeIndex,parameters):
    '''             
    It calculates the elastic backbone for a single particle configuration, 
    corresponding to a single time instant, provided by a .dat file.


    Parameters
    ----------
    folder : STR
        path of the folder containing the code.
    nameFilesIO : CLASS
        it contains names of input and output files and the bare name.
    parameters : LIST
    

    Returns
    -------
     CLASS(Backbone)
         BackboneOneFrame = summary of info on backbone for one time instant   
    
    Input
    -----    
    File with an instantaneous particle configuration, with the data structure:
        
        Number of particles
        [empty line]
        particleID   particleType   positionX   positionY   positionZ   paricleVolume   clusterID   numberOfNeighbours   listOfNeighbourIDs (variable length)
        ...

    Output
    -------    
     This code an output .dat file that can be used as input in the 
     Ovito visualization tool and has the following structure:
         
         Number of particles
         [empty line]
         positionX   positionY   positionZ  chemicalType   particleRadius  particleBurningTimeInLoop1 particleBurningTimeInLoop2  particleID
         ....

    '''    
    
    import DataManager
    reload(DataManager)
    from DataManager import DataManager
    
    
    #User-defined parameters
    RADIUS_MIN = parameters[0]
    RADIUS_MAX = parameters[1]
    FLAG_FIXED_EXTREMES_BACKBONE = parameters[2]
    
    
    DM = DataManager()
    DM.load_data_from_simulation_file(fileNamesIO.input)

      
    #Shift box so that origin coincides with min(x,y,z) of particles
    DM.shift_origin_of_axes()

    
   
    # CALCULATE ELASTIC BACKBONE
    #------------------------------
    #Define initial and final points for burning algorithm: P1,P2
    # kk_P1, kk_P2 = Indexes of P1,P2
    backboneExtremes = find_start_end_particles_for_burning_algorithm\
                       (box,particles,parameters)
    
    
    #Burning loop 1: from P1 to P2 
    #   find length of elastic backbone = min N of connected particles and min path P1-P2
    BurningTime,MinN_P1P2,MinPath_P1P2,forwardBurningTimes = forward_burning\
        (DM,particles,backboneExtremes,box)    
        
    #resultsLoop1 =  First_burning_loop_from_P1_to_P2(Particles,P1,P2,box)  

    
    #Burning loop 2: from P2 to P1
    #  find the whole elastic backbone, i.e. all equivalent shortest path between P1,P2
    BurningTime_2,MinN_P2P1,N_ElasticBackbone,points_2 = backward_burning\
        (particles,backboneExtremeParticles,ID_to_index,box,forwardBurningTimes)

    #resultsLoop2 = Second_burning_loop_from_P2_to_P1(Particles,P1,P2,box,resultsLoop1)

    
    #Check that Min N particles is the same in loop 1 and loop 2
    assert MinN_P1P2 ==  MinN_P2P1,'Min N particles is != in loop 1 and loop 2\n' \
         f'time={time}:  Min N loop 1 ={MinN_P1P2}, Min N loop 2 = {MinN_P2P1}'


    #CALCULATE LINEAR DISTANCE BETWEEN POINTS P1,P2
    #Coordinates of points P1,P2
    xP1 = P1[0]
    yP1 = P1[1]
    zP1 = P1[2]
    xP2 = P2[0]
    yP2 = P2[1]
    zP2 = P2[2]
    dist_P1P2 = np.sqrt((xP1-xP2)**2 + (yP1-yP2)**2 + (zP1-zP2)**2) 
      
     
    #OUTPUT
    f_out = open(Name_files_IO.output,'w')
    print(Npart,file = f_out)
    print(file = f_out)
    for i in range(0,Npart):
         print(x[i],y[i],z[i],chemType[i],radius[i],points[i],points_2[i],IDpart[i],file = f_out)
    f_out.close()
    
    
    BackboneOneFrame = Backbone(timeIndex,time,MinN_P2P1,MinPath_P1P2,\
                                N_ElasticBackbone,dist_P1P2,Npart)
    
    
    
    
    
    return BackboneOneFrame