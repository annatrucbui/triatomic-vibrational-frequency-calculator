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
import scipy.optimize as optimize


Const = {'m_u': 1.66054e-27,
         'Hartree': 4.35974e-18}

pathname = "./Gaussian-output-files/H2Ooutfiles/"
name = "H2O"
def get_gemeotry_energy(filename):
    """Take an output file from Gaussian and return r, theta and energy.
    
    filename: str
    r: H-X bond length
    theta: H-X-H bond angle
    Returns: tuple (r, theta, energy)
    """
    
    rthetalist = filename[5:-4].split("theta") # Extract r and theta from filename
    
    r = float(rthetalist[0])
    theta = float(rthetalist[1])
    
    
    f = open(pathname + filename, "r") # Extract energy by parsing 
    for line in f:
        if "SCF Done:" in line:
            energy = float(line.split()[4])
            break # exit from loop once energy is obtained
    f.close()
        
    return r, theta, energy
    
    
    
def dictionary_PES(pathname):
    """Take a pathname containing output files and return a dictionary relating geometry to energy.
    
    Returns: dictionary with keys as tuples (r, theta) and values as energies"""
    
    PES_dict = {} # Create empty dictionary
    
    for filename in os.listdir(pathname):
        if filename.endswith(".out"):
            r, theta, energy = get_gemeotry_energy(filename)
            PES_dict[(r, theta)] = energy
            
    return PES_dict
            
        


def plot_PES(PES_dict, name):
    """Takes a dictionary of geometry and energy and creates a 3D surface plot of the potential energy surface"""
    
    # https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
    
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # Make data
    r = []
    theta = []
    for geometry in PES_dict.keys():
        r.append(geometry[0])
        theta.append(geometry[1])
        
    x = np.arange(min(r), max(r) + 0.05, 0.05) 
    y = np.arange(min(theta), max(theta) + 1, 1) 
    
    X, Y = np.meshgrid(x, y)
    Z = np.ndarray(X.shape)
    
    for i in range(len(y)):
        for j in range(len(x)):
            Z[i][j] = PES_dict[(round(X[i][j], 2), round(Y[i][j], 1))]
        
    # Plot the surface.
    ax.view_init(35,290)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_xlabel("X-H bond legnth/ Å")
    ax.set_ylabel("H-X-H bong angle/ degrees")
    ax.set_zlabel("Energy/ Hartrees")
    ax.set_title("Potential Energy Surface for " + name)
    

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.6, aspect=5)
    plt.savefig(name + '_PES.png')
    plt.show()
    plt.close()
    
    return None   
        

def get_equilibrium_geometry(PES_dict):
    """Takes a dictionary of geometry and energy and returns the geometry with the minimum energy
    
    Returns: tuple (r, theta)
    """
    
    return min(PES_dict, key=PES_dict.get)


def select_data_to_fit(PES_dict, number_points):
    "Returns meshgrid of region of r and theta suitable for fitting"
    
    r_0, theta_0 = get_equilibrium_geometry(PES_dict)
    energy_0 = PES_dict[(r_0, theta_0)]
    
    x = np.arange(r_0 - 0.05*number_points, r_0 + 0.05*(number_points+1), 0.05)
    y = np.arange(theta_0 - 1*number_points, theta_0 + 1*(number_points+1), 1)
    X, Y = np.meshgrid(x, y)
    return X, Y
    

def fit_PES(PES_dict):
    "Return a quadratic fit for PES"
    number_points = 3
    r_0, theta_0 = get_equilibrium_geometry(PES_dict)
    energy_0 = PES_dict[(r_0, theta_0)]
 
    
    x = np.arange(r_0 - 0.05*number_points, r_0 + 0.05*(number_points+1), 0.05)
    y = np.arange(theta_0 - 1*number_points, theta_0 + 1*(number_points+1), 1)
    X, Y = np.meshgrid(x, y)
    
    
    
    def PESfit(data, k_r, k_theta):  # https://stackoverflow.com/questions/15413217/fitting-3d-points-python
        r, theta = data
    
        return energy_0 + 0.5*k_r*((r - r_0)**2) +  0.5*k_theta*((theta - theta_0)**2)
    
    
    Energy = np.ndarray(X.shape)
    for i in range(len(y)):
        for j in range(len(x)):
            Energy[i][j] = PES_dict[(round(X[i][j], 2), round(Y[i][j], 1))]
            
   
    xdata = np.vstack((X.ravel(), Y.ravel()))

    params, pcov = optimize.curve_fit(PESfit, xdata, Energy.ravel(), bounds=(0, np.inf))  
    print(params, pcov)
    
    return params

        
        
    

def main():
    pathname = "./Gaussian-output-files/H2Ooutfiles/"
    name = "H2O"
    #filename = "H2O.r0.70theta70.0.out"
    PES_dict = dictionary_PES(pathname)
    plot_PES(PES_dict, name)
    print(get_equilibrium_geometry(PES_dict))
    k_r, k_theta = fit_PES(PES_dict)
    x_eq, y_eq = get_equilibrium_geometry(PES_dict)
    
    vib_freq1 = math.sqrt(k_r*Const['Hartree']*1e20
                      / (2*Const['m_u'])
                      )\
        / (2*math.pi*3e10)
    vib_freq2 = math.sqrt(2*k_theta*Const['Hartree']*360*360
                      / (x_eq*x_eq*1e-20*0.5*Const['m_u'])
                      )\
        / (2*math.pi*3e10)   
   

 

    
    print('Vibrational frequencies of normal modes:')
 
    print('Symmetric stretching mode: %.2f cm^-1' % (vib_freq1))
    print('Bending mode: %.2f cm^-1' % (vib_freq2))
    
 
if __name__ == '__main__':
    main()
  