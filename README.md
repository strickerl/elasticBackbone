# elasticBackbone
Calculate the elastic backbone for a series of files

Purpose
------- 
    This code finds the elastic backbone in a 3D percolating colloidal system evolving in time
    where the particle positions are provided. To this aim, it implements the 'burning algorithm' 
    described in 
        H J Herrmann et al, J. Phys. A: Math. Gen., 17 L261, 1984


Algorithm
----------
    The elastic backbone is the load-bearing structure in a connected percolating colloidal system.
    The code extracts the elastic backbone based on the burning algorithm, using two consecutive
    burning loops. The burning loops require the choice of two points P1,P2 at the furthest
    extremities of the percolation cluster, i.e. the largest cluster. The first burning loop, from 
    P1 to P2, finds the minimum path connecting P1-P2. The second burning loop, from P2 to P1, finds 
    all equivalent paths connecting P2-P1, i.e. all paths with the same number of particles. 
    
    Points P1,P2:
    Ideally the points P1,P2 should belongc to one of the diagonals of the image and be always fixed 
    in time. In reality they will be as close as possible to a diagonal but variable, as the particles 
    move. The user can choose to either keep P1,P2 fixed (same particles) or to recalculate them for
    each particle configuration, i.e. at each time. This is done by setting the flag
      'flagFixedPointsP1P2'   
        1:points P1,P2 are kept constant 
        0:points P1,P2 are recalculated for each configuration
