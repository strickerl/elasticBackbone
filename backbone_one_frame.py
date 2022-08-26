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
from IO_operations     import Read_file
from burning_algorithm import First_burning_loop_from_P1_to_P2
from burning_algorithm import Second_burning_loop_from_P2_to_P1


import Backbone
reload(Backbone)
from Backbone import Backbone


def find_closest_particle_to_a_point(x,y,z,P):
    '''Function that finds the minimum distance between pointP (xP,yP,zP) and 
        all points contained in a list'''  
           
    
    xP = P[0]  
    yP = P[1]
    zP = P[2]
      
    distancesFromP = np.sqrt((x-xP)**2 + (y-yP)**2 + (z-zP)**2) 
    
    # Get the indices kk (not the ID) of minimum element in numpy array 
    indexClosestParticleToPointP= np.argmin(distancesFromP)
    
    
    # Get the coordinates of the corresponding point
    #closestParticleToPointP  = Particles[indexClosestParticleToPointP]
    coordinatesClosestParticleToPointP  = \
        [x[indexClosestParticleToPointP],\
         y[indexClosestParticleToPointP],\
         z[indexClosestParticleToPointP]]
    
    
    return indexClosestParticleToPointP, coordinatesClosestParticleToPointP



def Find_Points_P1_P2(Lx_box,Ly_box,Lz_box,x,y,z,FLAG_FIXED_EXTREMES_BACKBONE): 
    '''Purpose
       -------
        Find the points P1,P2 used as initial and final point for the 
        burning algorithm
      
      Returns
      -------
      INT
          kk = index to scan vector containing particles of the largest cluster
          ID = identifier of particle 
    
    '''
    
    #Define vertices of the box 
    V1 = [0.,0.,0.]
    V2 = [Lx_box,0.,0.]
    V3 = [0.,Ly_box,0.]
    V4 = [0.,0.,Lz_box]
    V5 = [Lx_box,Ly_box,0.]
    V6 = [Lx_box,0.,Lz_box]
    V7 = [0.,Ly_box,Lz_box]
    V8 = [Lx_box,Ly_box,Lz_box]
    
    
    
    #Find particles of the largest cluster the closest to the vertices of the box
    closestParticlesToVertices   = [find_closest_particle_to_a_point(x,y,z,point) for point in [V1, V2, V3, V4, V5, V6, V7, V8]]
    
    #Vector with indexes of particles (of largest cluster) closest to the vertices
    indexesClosestParticlesToVertices    = [particle[0] for particle  in closestParticlesToVertices]  
    
    #Vector with coordinates of particles (of largest cluster) closest to the vertices    
    coordsClosestParticlesToVertices  = [particle[1] for particle in closestParticlesToVertices]   
    
        
        
    #Find extremes P1,P2
    if  FLAG_FIXED_EXTREMES_BACKBONE == 0:     #I recalculate them for each particle configuration (time instant)
        
        #Find length of all lines (ideally diagonals) connecting the 8 closest points to cube vertices Vi
        diagonals     = [] 
        i1_diagonal  = [] 
        i2_diagonal  = [] 
        kk1_diagonal = []
        kk2_diagonal = []
        for indexFirstPoint in range(0,7):    
            x1,y1,z1 = coordsClosestParticlesToVertices[indexFirstPoint]
            kk1      = indexesClosestParticlesToVertices[indexFirstPoint]
            for indexSecondPoint in range(indexFirstPoint+1,8):        
                x2,y2,z2 = coordsClosestParticlesToVertices[indexSecondPoint]
                kk2      = indexesClosestParticlesToVertices[indexSecondPoint]
               
                lengthDiagonal = np.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 ) 
                diagonals.append(lengthDiagonal)
                i1_diagonal.append(indexFirstPoint)
                i2_diagonal.append(indexSecondPoint)
                kk1_diagonal.append(kk1)
                kk2_diagonal.append(kk2)
       
           
        #Find the longest "diagonal" and the points that it connects    
        k_DiagMax = np.where(diagonals == np.amax(diagonals))  
        k_DiagMax = int(k_DiagMax[0])  
        iP1       = i1_diagonal[k_DiagMax]
        iP2       = i2_diagonal[k_DiagMax]    
        coordsP1    = coordsClosestParticlesToVertices[iP1]     #Coordinates of point P1
        coordsP2    = coordsClosestParticlesToVertices[iP2]     #Coordinates of point P2
        indexP1     = int(kk1_diagonal[k_DiagMax])       #kk of point P1
        indexP2     = int(kk2_diagonal[k_DiagMax])       #kk of point P2
    
    
    else:   #I keep P1,P2 constant for each configuration (i.e. throughout the whole time evolution)
            #Here I take V1 and V8 as reference points *** NOTE: this can be changed if required

        coordsP1  = coordsClosestParticlesToVertices[0]    #Coordinates of point P1
        coordsP2  = coordsClosestParticlesToVertices[7]    #Coordinates of point P2
        indexP1   = indexesClosestParticlesToVertices[0]       #kk of point P1
        indexP2   = indexesClosestParticlesToVertices[7]       #kk of point P2


    return coordsP1,coordsP2,indexP1,indexP2

 
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




def calculate_backbone_one_frame(folder,Name_files_IO,time,timeIndex,\
                                 RADIUS_MIN,RADIUS_MAX,FLAG_FIXED_POINTS_P1P2):
    '''             
    It calculates the elastic backbone for a single particle configuration, 
    corresponding to a single time instant, provided by a .dat file.


    Parameters
    ----------
    folder : STR
        path of the folder containing the code.
    Name_files_IO : CLASS
        it contains names of input and output files and the bare name.
    RADIUS_MIN,RADIUS_MAX : FLOAT
        minimum and maximum particle size.
    FLAG_FIXED_EXTREMES_BACKBONE : INT
        flag telling if the initial and final points of the burning algorithm are
        (1): fixed in time
        (0): recalculated at each time step.


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
    
    #Import data from .dat file  
    Lx_box,Ly_box,Lz_box,\
        Npart,IDpart,chemType,x,y,z,radius,vol,Nneighb,IDneighb,ID_to_index =\
        Read_file(RADIUS_MIN,RADIUS_MAX,Name_files_IO)
      
    
    #Shift box so that origin coincides with min particle coordinate min(x,y,z)
    x,y,z = Shift_origin_of_axes_of_box(x,y,z)
    
    #Particles = Shift_origin_of_axes_of_box(Particles)
    
   
    # CALCULATE ELASTIC BACKBONE
    #------------------------------
    #Define initial and final points for burning algorithm: P1,P2
    # kk_P1, kk_P2 = Indexes of P1,P2
    P1,P2,kk_P1,kk_P2 = Find_Points_P1_P2(Lx_box,Ly_box,Lz_box,x,y,z,FLAG_FIXED_POINTS_P1P2)
    
    #P1,P2 = Find_Points_P1_P2(Box,Particles,flag_fixed_P1P2)

    
    #Burning loop 1: from P1 to P2 
    #   find length of elastic backbone = min N of connected particles and min path P1-P2
    BurningTime,MinN_P1P2,MinPath_P1P2,points = First_burning_loop_from_P1_to_P2\
        (x,y,z,P1,P2,kk_P1,kk_P2,Npart,IDneighb,ID_to_index,Lx_box,Ly_box,Lz_box)    
        
    #resultsLoop1 =  First_burning_loop_from_P1_to_P2(Particles,P1,P2,box)  

    
    #Burning loop 2: from P2 to P1
    #  find the whole elastic backbone, i.e. all equivalent shortest path between P1,P2
    BurningTime_2,MinN_P2P1,N_ElasticBackbone,points_2 = Second_burning_loop_from_P2_to_P1\
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