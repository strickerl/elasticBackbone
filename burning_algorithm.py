# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 01:31:06 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch

    Subroutines implementing burning algorithm described in
        H J Herrmann et al, J. Phys. A: Math. Gen., 17 L261, 1984
"""

import numpy as np




def forward_burning(DM,backbone):   
    '''
    FIRST BURNING LOOP (FORWARD):
    It finds the length of elastic backbone, i.e. min number of connected particles 
    and min path length between P1-P2 (sum of distances between connected particles)

    Parameters
    ----------
    DM: CLASS(DataManager)
        it includes all particles of largest cluster,box info and 
        conversion lookup from particle ID to index 

    Returns
    -------
    particles.burningTimeForward: INT
        burning time in forward loop
           
    '''
          
    firstBurntParticle = backbone.extremes[0] #pointers
    lastBurntParticle  = backbone.extremes[1]


    #Initialize
    burningTimeIndex = 1;    
    burntParticles = [firstBurntParticle]
    firstBurntParticle.forwardBurningTime = burningTimeIndex    
    
    while not burntParticles: #Exit condition: when nothing was found to burn
    
        burningTimeIndex = burningTimeIndex + 1      #Burning step; consider it as a time!
    
        burntParticlesAtPreviousTime = burntParticles
        burntParticles = [];
    
        #Loop over particles burnt at previous time
        for particle in burntParticlesAtPreviousTime:
                                                     
            #Loop over neighbours of particle
            for neighbourID in particle.neighbourIDs:
                
                neighbourIndex  = DM.getParticleIndexFromID[neighbourID]            
                neighbour       = DM.particles[neighbourIndex]
                
                #If the link is inside the box or via periodic boundary conditions               
                if neighbour.isConnectedThroughBox(particle, DM.box):
                            
                    if not neighbour.isBurnt(): #if neighbour has not been burnt yet
                    
                        neighbour.forwardBurningTime   = burningTimeIndex
                        neighbour.burntByParticleIndex = particle.index
                        burntParticles.append(neighbour) 
                    
                    
    backbone.getSummaryForwardBurning\
             (DM.particles,backbone,firstBurntParticle,lastBurntParticle)                
   

#----------------------------------------------------------------------------------

def backward_burning\
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
