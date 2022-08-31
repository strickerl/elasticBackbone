# elasticBackbone
Calculate the elastic backbone for a series of files

Purpose
------- 
    This code finds the elastic backbone in a 3D percolating colloidal system evolving in time
    where the particle positions are provided. To this aim, it implements the 'burning algorithm' 
    described in 
        H J Herrmann et al, J. Phys. A: Math. Gen., 17 L261, 1984
	https://doi.org/10.1088/0305-4470/17/5/008

Algorithm
----------
    The elastic backbone is the load-bearing structure in a connected percolating colloidal system.
    The code extracts the elastic backbone based on the burning algorithm, using two consecutive
    burning loops. The burning loops require the choice of two particless P1,P2 at the furthest
    extremities of the percolation cluster, i.e. the largest cluster. The first burning loop 
    (forward burning), from P1 to P2, finds the minimum path connecting P1-P2. The second burning 
    loop (backward burning), from P2 to P1, finds all equivalent paths connecting P2-P1, i.e. all 
    paths with the same number of particles. 
    
    Choice of particles P1,P2:
    Ideally the particles P1,P2 should belong to one of the diagonals of the image and be always fixed 
    in time. In reality they will be as close as possible to a diagonal but variable, as the particles 
    move. The user can choose to either keep P1,P2 fixed (same particles) or to recalculate them for
    each particle configuration, i.e. at each time. This is done by setting the flag
      'BACKBONE_EXTREMES_FLAG'   
        1:points P1,P2 are calculated as the closest points to a fixed pair of box nodes 
        0:points P1,P2 are calculated as the closest points to a pair of box nodes recalculated at each time


User-defined parameters 
-----------------------
    Parameters are defined by the user inside the file myParameters.config

       PARTICLE_RADIUS_MIN = float : radius of particles with chemicalType = 1
       PARTICLE_RADIUS_MAX = float : radius of particles with chemicalType = 2
       BACKBONE_EXTREMES_FLAG = int :choice of fixed(1)/variable(0) box nodes to set extremes of backbone
       NODE_START = int : fixed box node 1; defined if fixed box nodes to set extremes of backbone
       NODE_END   = int : fxied box node 2; defined if fixed box nodes to set extremes of backbon
 	