# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 16:32:12 2020

@author: btb32
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib as mpl
import sys
import math

Const = {'m_u': 1.66054e-27,
         'Hartree': 4.35974e-18}
pathname = "./Gaussian-output-files/H2Ooutfiles/"
#filename = "H2O.r0.70theta70.0.out"

def gemeotry_energy(filename):
    "Take a file and return a tuple (bond length, bond angle, energy)"
    
    
    rthetalist = filename[5:-4].split("theta")
    
    r = float(rthetalist[0])
    theta = float(rthetalist[1])
    
    f = open(pathname + filename, "r")
    for line in f:
        if "SCF Done:" in line:
            energy = float(line.split()[4])
            break # exit from loop once energy is obtained
    f.close()
        
    return r, theta, energy
    
    


bondlengths = []
bondangles = []
energies = []

for filename in os.listdir(pathname):
    if filename.endswith(".out"):
        extractedinfo = gemeotry_energy(filename)
        bondlengths.append(extractedinfo[0])
        bondangles.append(extractedinfo[1])
        energies.append(extractedinfo[2])
        


def plot_potential_energy_surface():
    '''Creates a 3D surface plot of the potential energy surface if given a list of Atoms objects'''
    XX = bondlengths
    YY = bondangles
    ZZ= energies

    ax = plt.axes(projection='3d')
    ax.set_xlabel('r / A')
    ax.set_ylabel('Theta / degrees')
    ax.set_zlabel('Energy / au')
    ax.set_title('Potential Energy Surface of H2O')
    ax.view_init(35,290)
    ax.plot_trisurf(XX, YY, ZZ,cmap=mpl.cm.coolwarm)
    plt.savefig('_PES.pdf')
    plt.show()
    plt.close()
    return None   
        
def equilibrium(energies):
    index_min = np.argmin(energies)
    
    #count = energies.count(energies[index_min])
    #print(count)
    r0 = bondlengths[index_min]
    theta0 = bondangles[index_min]
    return r0, theta0
index_min = np.argmin(energies)    


        
        


