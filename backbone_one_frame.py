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
from IO_operations     import read_file
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


def find_closest_particle_to_a_point(particles,pointP):
    '''Function that finds the minimum distance between pointP (xP,yP,zP) and 
        all particles contained in a list'''  
           
    x = [particles[index].x for index in range(0,len(particles))]   
    y = [particles[index].y for index in range(0,len(particles))] 
    z = [particles[index].z for index in range(0,len(particles))] 
    
    xP = pointP.x
    yP = pointP.y
    zP = pointP.z
      
    
    distancesFromP = np.sqrt((x-xP)**2 + (y-yP)**2 + (z-zP)**2) 
    
    # Get the index (not the ID) of smallest element in numpy array 
    indexClosestParticleToPointP= np.argmin(distancesFromP)
    
    
    ClosestParticleToPointP  = particles[indexClosestParticleToPointP]
    
    #return indexClosestParticleToPointP, coordinatesClosestParticleToPointP
    return ClosestParticleToPointP




def find_start_end_points_for_burning_algorithm_P1_P2(Box,particles,FLAG_FIXED_EXTREMES_BACKBONE): 
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
    StartEndParticlesBurningAlgorithm : CLASS
    '''
    
    #Find vertices of 
    Box.findVertices()   


    if  FLAG_FIXED_EXTREMES_BACKBONE == 0:      #P1,P2 recalculated at each time        
        
        #Find the closest particles (of the largest cluster) to the vertices of the box
        closestParticlesToVertices = [find_closest_particle_to_a_point(particles,Point) for Point in Box.vertices]


        lengthDiagonalMax = 0.
        
        for index1, Particle1 in enumerate(closestParticlesToVertices):    
            
            for Particle2 in closestParticlesToVertices[index1+1:]:            
                
                Diagonal = ParticlePair(Particle1,Particle2)
                
                if Diagonal.length > lengthDiagonalMax:
                    lengthDiagonalMax = Diagonal.length
                    StartEndParticlesBurningAlgorithm   = Diagonal

    
    
    else:  #P1,P2 are the closest points to a fixed pair of vertices

        #Box can change size but the vertex pair reamins constant 
        Box.defineFixedVerticesForBurningAlgorithm(Box)  
        fixedVertices = Box.fixedVertexPair             

        #Find the closest particles (of the largest cluster) to the two fixed vertices of the box
        closestParticlesToVertices = [find_closest_particle_to_a_point(particles,point) for point in fixedVertices]
        
        Particle1 = closestParticlesToVertices[0]
        Particle2 = closestParticlesToVertices[1]
        StartEndParticlesBurningAlgorithm = ParticlePair(Particle1,Particle2)
  

    return StartEndParticlesBurningAlgorithm

 

def Shift_origin_of_axes_of_box(x,y,z):
    '''
        Shift all particle coordinates (x,y,z) to that the new origin of the box 
        coincides with min(x),min(y),min(z)

    ''' 
    
    #Define new origin of axes based on particles' positions
    x_min = np.min(x)
    y_min = np.min(y)
    z_min = np.min(z)


    #Shift particle coordinates
    x_shifted = x - x_min
    y_shifted = y - y_min
    z_shifted = z - z_min

    return x_shifted, y_shifted, z_shifted




def calculate_backbone_one_frame(folder,Name_files_IO,time,timeIndex,parameters):
    '''             
    It calculates the elastic backbone for a single particle configuration, 
    corresponding to a single time instant, provided by a .dat file.


    Parameters
    ----------
    folder : STR
        path of the folder containing the code.
    Name_files_IO : CLASS
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
    
    #User-defined parameters
    RADIUS_MIN = parameters[0]
    RADIUS_MAX = parameters[1]
    FLAG_FIXED_EXTREMES_BACKBONE = parameters[2]
    
    
    #Import data from .dat file  
    Box,Npart,IDpart,chemType,x,y,z,radius,vol,Nneighb,IDneighb,ID_to_index =\
        read_file(RADIUS_MIN,RADIUS_MAX,Name_files_IO)
      
    
    #Shift box so that origin coincides with min particle coordinate min(x,y,z)
    x,y,z = Shift_origin_of_axes_of_box(x,y,z)
    
    #Particles = Shift_origin_of_axes_of_box(Particles)
    
   
    # CALCULATE ELASTIC BACKBONE
    #------------------------------
    #Define initial and final points for burning algorithm: P1,P2
    # kk_P1, kk_P2 = Indexes of P1,P2
    StartEndParticles = find_start_end_points_for_burning_algorithm_P1_P2\
                        (Box,particles,FLAG_FIXED_EXTREMES_BACKBONE)
    
    
    #P1,P2 = Find_Points_P1_P2(Box,Particles,flag_fixed_P1P2)

    
    #Burning loop 1: from P1 to P2 
    #   find length of elastic backbone = min N of connected particles and min path P1-P2
    BurningTime,MinN_P1P2,MinPath_P1P2,points = forward_burning\
        (x,y,z,P1,P2,kk_P1,kk_P2,Npart,IDneighb,ID_to_index,Lx_box,Ly_box,Lz_box)    
        
    #resultsLoop1 =  First_burning_loop_from_P1_to_P2(Particles,P1,P2,box)  

    
    #Burning loop 2: from P2 to P1
    #  find the whole elastic backbone, i.e. all equivalent shortest path between P1,P2
    BurningTime_2,MinN_P2P1,N_ElasticBackbone,points_2 = backward_burning\
        (x,y,z,P1,P2,kk_P1,kk_P2,Npart,IDneighb,ID_to_index,Lx_box,Ly_box,Lz_box,points)

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