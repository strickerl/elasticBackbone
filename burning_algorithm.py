# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 01:31:06 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch

    Subroutines implementing burning algorithm described in
        H J Herrmann et al, J. Phys. A: Math. Gen., 17 L261, 1984
"""

import numpy as np



def First_burning_loop_from_P1_to_P2(x,y,z,P1,P2,kk_P1,kk_P2,Npart,IDneighb,ID_to_index,Lx_box,Ly_box,Lz_box):
    '''
    FIRST BURNING LOOP, FROM P1 TO P2:
    It finds the length of elastic backbone, i.e. min number of connected particles 
    and min path length between P1-P2 (sum of distances between connected particles)


    Parameters
    ----------
    x,y,z : FLOAT
        coordinates of centre of particles.
    P1 : LIST(FLOAT)[2]
        coordinates of initial point of loop 1, P1.
    P2 : LIST(FLOAT)[2]
        coordinates of final point of loop 2, P2.
    kk_P1, kk_P2 : INT
        indexes of points P1,P2.
    Npart : INT
        number of particles in main cluster.
    Npart : INT
        Number of particles of the largest cluster.
    IDneighb : LIST[Npart] OF LISTS(INT)[variable lengths]
        each row kk contains the neighbours of the particle kk
    ID_to_index : LIST(INT)
        conversion table from IDparticles to index kk. Each row ID contains the
        corresponding index kk
    Lx_box,Ly_box,Lz_box : FLOAT
        length of box sides


    Returns
    -------
    BurningTime : INT
        total time to burn from point P1 to point P2.
    MinN_P1P2 : INT
        minimum number of points connecting P1-P2.
    points : LIST(INT)[Npart]
        burning time of particles in the first loop from P1 to P2.
    '''
    
    #Initialize
    burningTimes     = [0]*Npart
    burnt            = [0]*Npart
    kk_BurningSource = [0]*Npart
    burningTimeIndex = 1;     #Counter of burning step
    
    #Starting point of the burning loop (P1)
    kk0 = kk_P1         #Index of starting particle in the array of the large cluster
    burningTimes[kk0] = burningTimeIndex    #Array where, for each point kk, I store the value of the time where it was burnt
    burnt[kk0]  = 1 
    
    #'Present points' of previous time it-1
    kk_PtsPrev = [int(kk0)]
    n_PtsPrev  = 1 
    
    
    
    #LOOP 1:burning forwards
    #---------------------------
    flag_exit = 0;
    while flag_exit == 0:
    
        burningTimeIndex = burningTimeIndex + 1      #Burning step; consider it as a time!
    
        #Vector where I keep track of particles I try to burn at the present burning time instant
        burntNow = [0]*Npart
    
        #Initialize list of neighbours of the present points, at instant it 
        kk_newPts = list();
    
        for jj in range(0,n_PtsPrev):
        
            #Select one point from those classified as neighbours during the previous burning time 
            kk     = kk_PtsPrev[jj]
            x_Prev = x[kk]    
            y_Prev = y[kk] 
            z_Prev = z[kk] 
           
            #Indexes of neighbours, i.e. particles connected to particle ID  
            ID_connect = IDneighb[kk]
            N_connect  = len(ID_connect)   #Number of particles connected to particle ID
           
           
            #Mark neighbouring pixels
            for ii in range(0,N_connect):
           
                IDN = ID_connect[ii]
                kkN = ID_to_index[IDN]
                xN  = x[kkN]
                yN  = y[kkN]    
                zN  = z[kkN]
               
               
                #Check if the link is inside the box or via the boundary conditions
                #I want to exclude the latter case
                #--------------------------------------------------------------------------------------------
                # Note: the list of neighbours provided for each particle can include 
                #   particles on the opposite side of the box, if it originates from 
                #   simulations with periodic boundary conditions (PBC) were accounted for. 
                #   PBC do not make sense for the calculation of the elastic backbone. 
                #   The content of the box without PBC is still a representative part of the whole system.
                #--------------------------------------------------------------------------------------------
                if  abs(x_Prev - xN)>Lx_box/2. or  abs(y_Prev - yN)>Ly_box/2. or abs(z_Prev - zN)>Lz_box/2.:
                    flag_connect_viaBoundary = 1
                else:
                    flag_connect_viaBoundary = 0
             
               
                #If pixel is not already burnt either from present time or previous times  
                # AND the considered connection is through the inside of the box             
                if flag_connect_viaBoundary == 0:    #If the connection is inside the box
                   
                    if burnt[kkN] == 0:          #If it has not burnt yet, I burn it    
                        burningTimes[kkN]   = burningTimeIndex       #Value of time instant when the point N is burning
                        burnt[kkN]    = 1        #Flag signaling that the point has now burnt
                        burntNow[kkN] = 1        #Flag that says that this point was burnt at the present time step   
                        kk_newPts.append(kkN)        #I add point N to the list of the new 'present points'
                        kk_BurningSource[kkN] = kk   #Index kk of point who burnt IDN (i.e.index kkN) 
                      
                            
           
        kk_PtsPrev = kk_newPts   
        n_PtsPrev = len(kk_PtsPrev)
       
        #Exit condition: when nothing new can be found
        if n_PtsPrev == 0:
           flag_exit = 1
       
        
    #---------------------------------------------------------------------------- 
    #Find BURNING TIME and MINIMUM PATH between P1 and P2    
    BurningTimeOfPointP2  = np.max(burningTimes) 
    MinN_P1P2             = burningTimes[kk_P2]
    
    
    #Calculate MIN PATH P1-P2 
    #  = sum of inteparticle distances along shortest path connecting P1,P2
    MinPath_P1P2 = 0
    kk           = kk_P2     #Index of starting particle in the array of the large cluster  
    
    for ii  in range(0,MinN_P1P2):
        
        kk_Burner = kk_BurningSource[kk]  #Index of point that burnt point kk
        
        xP  = x[kk]
        yP  = y[kk]
        zP  = z[kk]
        
        xN  = x[kk_Burner]
        yN  = y[kk_Burner]
        zN  = z[kk_Burner]
        
        dist   = np.sqrt((xP-xN)**2 + (yP-yN)**2 + (zP-zN)**2) 
           
        MinPath_P1P2 = MinPath_P1P2 + dist
    
        kk = kk_Burner
    

    return BurningTimeOfPointP2, MinN_P1P2, MinPath_P1P2, burningTimes

#----------------------------------------------------------------------------------

def Second_burning_loop_from_P2_to_P1\
    (x,y,z,P1,P2,kk_P1,kk_P2,Npart,IDneighb,ID_to_index,Lx_box,Ly_box,Lz_box,points):
    '''
    SECOND BURNING LOOP, from P2 to P1:
    It finds the whole elastic backbone,i.e. all equivalent paths connecting points P1,P2
        
    
    Parameters
    ----------
    x,y,z : FLOAT
        position x,y,z of center
    P1 : LIST(FLOAT)[2]
        Coordinates x,y of final point of second burning loop.
    P2 : LIST(FLOAT)[2]
        Coordinates x,y of initial point of second burning loop.
    kk_P1,kk_P2 : INT
        Indexes of P1,P2
    Npart : INT
        Number of particles of the largest cluster.
    IDneighb : LIST[Npart] OF LISTS(INT)[variable lengths]
        Each row kk contains the neighbours of the particle kk
    ID_to_index : LIST(INT)
        conversion table from IDparticles to index kk. Each row ID contains the
        corresponding index kk
    Lx_box,Ly_box,Lz_box : FLOAT
        Length of box sides
    points : LIST(INT)[Npart]
        Burning time of particles in the first loop from P1 to P2.

    Returns
    -------
    BurningTime_2 : INT
        total time to burn from point P2 to point P1.
    MinN_P2P1 : INT
        minimum number of points connecting P2-P1.
    N_ElasticBackbone : INT
        total number of particles belonging to elastic backbone
    points_2 : LIST(INT)[Npart]
        burning time of particles in the second loop from P1 to P2.

    '''


    #Initialize
    points_2    = [0]*Npart
    burnt_2     = [0]*Npart
    it = 1;     #Counter of burning step
    
    #Starting point (now P2)
    kk0 = kk_P2         #Index of starting particle in the array of the largest cluster
    points_2[kk0] = it  
    burnt_2[kk0]  = 1
    
    #Initialize points burnt at the previous 'time'
    kk_PtsPrev = [int(kk0)]
    n_PtsPrev  = 1 
    
    
    
    #LOOP 2: burning backwards
    flag_exit = 0;
    while (flag_exit == 0):
     
        it = it + 1;                #Burning step; consider it as a time 
       
        #New points to burn that we are finding at instant it (=neighbours of present points) 
        kk_newPts = [];
    
        #Loop over points classified as 'neighbour points' at the previous time step
        for jj in range(0,n_PtsPrev):
        
            #Select one point from those classified as neighbours in the previous time step 
            kk     = kk_PtsPrev[jj]
            x_Prev = x[kk]    
            y_Prev = y[kk] 
            z_Prev = z[kk] 
           
            #Indexes of neighbours, i.e. particles connected to particle ID  
            ID_connect = IDneighb[kk]
            N_connect  = len(ID_connect)   #Number of particles connected to ID
     
          
            #Mark neighbouring pixels of ID
            for ii in range(0,N_connect):
           
                IDN = ID_connect[ii]
                kkN = ID_to_index[IDN]
                xN  = x[kkN]
                yN  = y[kkN]    
                zN  = z[kkN]
               
                #Check if the link is inside the box or via the boundary conditions
                #I want to exclude the latter case
                if  abs(x_Prev - xN)>Lx_box/2. or  abs(y_Prev - yN)>Ly_box/2. or abs(z_Prev - zN)>Lz_box/2.:
                    flag_connect_viaBoundary = 1
                else:
                    flag_connect_viaBoundary = 0
               
    
              
                #If particle kkN (that I am trying to burn from particle kk) is not already burnt (in loop 2) 
                #  AND the connection between kk and kkN is inside box and not through the periodic boundaries
                #  AND if in loop 1 kkN was burnt before kk (i.e kkN is not a 'branch') 
                if flag_connect_viaBoundary == 0:    #If connection is inside box
                   
                    if burnt_2[kkN] == 0 and points[kkN]<points[kk]:
                        points_2[kkN]   = it       #Value of time instant when the point is burning
                        burnt_2[kkN]    = 1        #Flag signaling that the point has burnt
                        kk_newPts.append(kkN)
    
    
    
        kk_PtsPrev = kk_newPts   
        n_PtsPrev = len(kk_PtsPrev)
       
        #Exit condition: when nothing new can be found
        if n_PtsPrev == 0:
           flag_exit = 1
                       
    
    BurningTime_2 = np.max(points_2)      
    MinN_P2P1     = points_2[kk_P1]            #Min number of particles connecting P2-P1
    N_ElasticBackbone = np.sum(burnt_2)
    
    
    return BurningTime_2,MinN_P2P1,N_ElasticBackbone,points_2
