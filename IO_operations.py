# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 16:35:29 2022
@author: Laura Stricker, laura.stricker@mat.ethz.ch

        Input/output operations

"""

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import make_dataclass



def natural_sort(l): 
    '''Sort alphanumeric list'''

    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)



def define_file_names(folder,path,file_name):
    '''Define name of input and output files, given the path'''    


    input_filename = path + file_name
    
    #Extract raw name, without .dat extension
    raw_filename = file_name[0:len(file_name)-4]
    
    #Define name of output file
    output_filename = folder + '/Output/' + raw_filename + '.xyz'
        
    
    #Create class with name of files
    Name_files = make_dataclass('Name_files', ['input', 'output', 'raw'])
    
    #Create and return instance of class Name_files
    return Name_files(input_filename, output_filename, raw_filename)



def extract_input_file_list():
    '''
       Define list of input files with particle data, contained inside folder
       .\input
    '''   

    folder        = os.path.dirname(__file__)  #absolute dir the present script is in
    path          = folder + r'/Input/'


    #List of files inside 'path'
    files = os.listdir(path)

    #Open files with the string ('keyword') in the name
    keyword     = "cluster_atoms"
    list_files_atoms = [name_file for name_file in files if keyword in name_file]
    nfiles      = len(list_files_atoms)
    list_files_atoms = natural_sort(list_files_atoms)      


    return list_files_atoms,nfiles,path




def Read_file(rMin,rMax,Name_files):

    '''Read files
    
    Input
    -----
    
    
    Output
    ------
    int
        Npart
        
    float    
        Lx_box,Ly_box,Lz_box,
                 
    list (int)    
        IDpart   = identifiers of particles
        chemType = type of particles (large/small)
        Nneighb  = number of neighbours of particles
        
    list (float)    
        x,y,z  = position of particle centers
        radius = radii of particles
        vol    = Voronoi volumes of particles
        
        IDneighb,ID_to_index
    
    '''
       
    #Read general info on the first line of configuration file:
    #  Number of clusters    Box length x    Box length y    Box length z    
    #-----------------------------------------------------------------------------
    inputfile  = open(Name_files.input,'r')
    first_line = inputfile.readline()
    line_list = first_line.split()            #Convert string into array of numbers
    map_object = map(float, line_list)
    list_of_numbers = list(map_object)
    Npart  = int(list_of_numbers[0])          #Number of particles
    Nclust = int(list_of_numbers[1])          #Number of clusters
    Lx_box = list_of_numbers[2]               #Length x of the box
    Ly_box = list_of_numbers[3]               #Length y of the box
    Lz_box = list_of_numbers[4]               #Length z of the box 
       
       
    #Read file into a data frame
    df = pd.read_fwf(inputfile, header=None, infer_nrows=Npart)      
    inputfile.close()
    
    # Npart  = df.iloc[0,0]       #Number of particles
    # Nclust = df.iloc[0,1]       #Number of clusters
    # Lx_box = df.iloc[0,2]       #Length x of the box
    # Ly_box = df.iloc[0,3]       #Length y of the box
    # Lz_box = df.iloc[0,4]    
    
    # df_particles = df[df["Index"] > 0]
    # df_particles_largest_cluster = df[df["IDcluster"] == 1]
      
        
    # Name of columns in the dataframe
    namesCol = ["IDparticle", "chemicalType", "x", "y", "z", "volume", "IDcluster", "N_neighbours"]
    myDict = {i : namesCol[i] for i in range(0,8)}
    df = df.rename(columns=myDict)
    

    
    #Load data from file
    df_particlesLargestCluster = df[df["IDcluster"] == 1]
    particleID   = list(df_particlesLargestCluster['IDparticle'])
    chemicalType = list(df_particlesLargestCluster['chemicalType'])
    x            = list(df_particlesLargestCluster['x'])
    y            = list(df_particlesLargestCluster['y'])
    z            = list(df_particlesLargestCluster['z'])
    volume       = list(df_particlesLargestCluster['volume'])
    NumberOfNeighbours  = list(df_particlesLargestCluster['N_neighbours'])

    particleNumber    = len(df_particlesLargestCluster)    #Number of particles


    #List of list of neighbours of particles belonging to the largest cluster
    neighbourIDs = [ df_particlesLargestCluster.iloc[index,8:].dropna().astype('int64').tolist() \
                     for index in range(0,particleNumber) ]

           
    #Create vector with radii of particles of largest cluster
    radius = [rMin if chemicalType[particleIndex] == 1 else rMax \
              for particleIndex in range(0,particleNumber)]  # list comprehension
    
    
    #Conversion ID to index
    particleIDToIndex = Create_conversion_table_from_particle_ID_to_index\
                        (particleID,df_particlesLargestCluster)
    
    
    
    return Lx_box,Ly_box,Lz_box,\
           particleNumber,particleID,chemicalType,x,y,z,radius,volume,\
           NumberOfNeighbours,neighbourIDs,particleIDToIndex




def Create_conversion_table_from_particle_ID_to_index(particleIDs,df_particlesLargestCluster):
    '''

     
    Identifier ID (=number) of particle is assigned based on the list of all
    particles, including those that do not belong to the largest cluster
    In the conversion table, each line ID contains the index of the particle 
    in the lists with the info on the largest cluster only. The lines of the 
    corresponding to particles not belonging to the largest cluster 
    are filled with -1
    '''   
    
    
    #Max ID of particles
    particleIDMax  = df_particlesLargestCluster["IDparticle"].max() 
    
    #Number of particles
    particleNumber = len(df_particlesLargestCluster)    
    
    
    #The line ID contains the value of the corresponding index
    particleIDToIndex = [-1]*(particleIDMax + 1)      
    for particleIndex in range(0,particleNumber):
         row = particleIDs[particleIndex]
         particleIDToIndex[row] = particleIndex      
         
    particleIDToIndex  = list(map(int,particleIDToIndex))   
    
    
    
    return particleIDToIndex





def Plot_results(time,MinN_P1P2,N_ElBackbone,Ntot,MinPath_P1P2,dist_P1P2):
    '''Plot figures'''
      
    
    ax = plt.figure(1)
    line1, = plt.plot(time,MinN_P1P2,'r')
    line2, = plt.plot(time,N_ElBackbone,'b')
    plt.xlabel('time')
    plt.ylabel('Min path (P1P2)')
    plt.show()
    line1.set_label('N particles min P1P2')
    line2.set_label('N particles elastic backbone')
    ax.legend()

    plt.figure(2)
    plt.plot(time,np.array(MinN_P1P2)/np.array(Ntot))
    plt.xlabel('time')
    plt.ylabel('Min N between P1P2/ Ntot')
    plt.show()

    plt.figure(3)
    plt.plot(time,MinPath_P1P2)
    plt.xlabel('time')
    plt.ylabel('Min path (P1P2) [Length]')
    plt.show()

    plt.figure(4)
    plt.plot(time,np.array(MinPath_P1P2)/np.array(dist_P1P2))
    plt.xlabel('time')
    plt.ylabel('Min path / dist (P1P2) ')
    plt.show()

    return