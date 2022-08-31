# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 01:31:06 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch

    Subroutines implementing burning algorithm described in
        H J Herrmann et al, J. Phys. A: Math. Gen., 17 L261, 1984
"""

def forwardBurning(DM,backbone):   
    '''
    FIRST BURNING ROUND (FORWARD):
    It finds the length of elastic backbone, i.e. min number of connected particles 
    and min path length between P1-P2 (sum of distances between connected particles)

    Parameters
    ----------
    DM: CLASS(DataManager)
        it includes all particles of largest cluster,box info and 
        conversion lookup from particle ID to index 

    Returns
    -------
    backbone.burningTimeForward: INT
    backbone.minPathLength = FLOAT 
        sum of interparticle distances along min connected path
        
    '''
          
    firstBurntParticle = backbone.extremes[0] #pointers
    lastBurntParticle  = backbone.extremes[1]
    burningTimeIndex = 1;    
    burntParticles = [firstBurntParticle]
    firstBurntParticle.isBurntByParticleIndex = -1   
    firstBurntParticle.forwardBurningTime = burningTimeIndex    

    
    while burntParticles: #Exit condition: when nothing was found to burn
    
        burningTimeIndex = burningTimeIndex + 1      #Burning step; consider it as a time!
    
        burntParticlesAtPreviousTime = burntParticles
        burntParticles = [];
    
        #Loop over particles burnt at previous time
        for particle in burntParticlesAtPreviousTime:
                                                     
            #Loop over neighbours of particle
            for neighbourID in particle.neighbourIDs:
                
                neighbourIndex  = DM.getParticleIndexFromID(neighbourID)            
                neighbour       = DM.particles[neighbourIndex]
                
                #If the link is inside the box or via periodic boundary conditions               
                if neighbour.isConnectedThroughBox(particle, DM.box):
                            
                    if not neighbour.isBurnt(): #if neighbour has not been burnt yet
                    
                        neighbour.forwardBurningTime     = burningTimeIndex
                        neighbour.isBurntByParticleIndex = particle.index
                        burntParticles.append(neighbour) 
                        
                    
    backbone.getSummaryForwardBurning(DM.particles,firstBurntParticle,lastBurntParticle)                
   

#----------------------------------------------------------------------------------

def backwardBurning(DM,backbone):
    '''
    SECOND BURNING ROUND (BACKWARDS)
    It finds the whole elastic backbone,i.e. all equivalent paths connecting points P1,P2
        
    
    Parameters
    ----------
    DM: CLASS(DataManager)
        it includes all particles of largest cluster,box info and 
        conversion lookup from particle ID to index 

    Returns
    -------
    backbone.burningTimeBackward: INT
    backbone.allMinPathsParticleCount = INT
        total # particles on equivalent min paths between extremes 
     '''

    firstBurntParticle = backbone.extremes[1] #pointers
    lastBurntParticle  = backbone.extremes[0]
    burningTimeIndex = 1;    
    burntParticles = [firstBurntParticle]
    firstBurntParticle.backwardBurningTime = burningTimeIndex    
    burntParticleCountTot = 0 
    
    for particle in DM.particles:
        particle.resetBurningStatus()
    
   
    while burntParticles: #Exit condition: when nothing was found to burn
    
        burningTimeIndex = burningTimeIndex + 1      #Burning step; consider it as a time!
    
        burntParticlesAtPreviousTime = burntParticles
        burntParticles = [];
    
        #Loop over particles burnt at previous time
        for particle in burntParticlesAtPreviousTime:
                                                     
            #Loop over neighbours of particle
            for neighbourID in particle.neighbourIDs:
                
                neighbourIndex  = DM.getParticleIndexFromID(neighbourID)            
                neighbour       = DM.particles[neighbourIndex]
                
                #If the link is inside the box or via periodic boundary conditions               
                if neighbour.isConnectedThroughBox(particle, DM.box):                   
                    #if neighbour has not been burnt yet
                    if (not neighbour.isBurnt()) and\
                        (neighbour.forwardBurningTime < particle.forwardBurningTime):                   
                        #if neighbour was burnt before particle in forward burning    
                        neighbour.backwardBurningTime  = burningTimeIndex
                        neighbour.isBurntByParticleIndex = particle.index
                        burntParticles.append(neighbour) 
                        burntParticleCountTot += 1  # Number of all burnt particles
                        
                    
    backbone.getSummaryBackwardBurning(lastBurntParticle,burntParticleCountTot)                