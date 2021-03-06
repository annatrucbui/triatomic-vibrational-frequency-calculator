"""
Vibrational frequecy calculator functions

The functions in this file include
    get_geometry_energy
    dictionary_PES
    plot_PES
    get_equilibrium_geometry
    fit_curve_nm
    calculate_vib_frequencies
    second_der
    Hessian
    
These are used in the main program in VibFreqCalculator.py

@author: btb32

"""

import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"

import math
import scipy.optimize as optimize


def get_gemeotry_energy(pathname, filename):
    """Take an output file from Gaussian and return r, theta and energy.
    pathname: STR directory containing output files
    filename: STR each output filename

    Returns: TUPLE (r, theta, energy)
    r: FLOAT H-X bond length,  in Angstrom
    theta: FLOAT H-X-H bond angle, in degree
    energy: FLOAT, in Hartree
    
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
    """Take a STR pathname containing output files
    
    Returns: DICT with keys as tuples (r, theta) and values as energies"""
    
    PES_dict = {} # Create empty dictionary
    
    for filename in os.listdir(pathname):
        if filename.endswith(".out"):
            r, theta, energy = get_gemeotry_energy(pathname, filename)
            PES_dict[(r, theta)] = energy
            
    return PES_dict
            
        


def plot_PES(PES_dict, name="triatomic"):
    """Takes a DICT of geometry and energy and creates a 3D surface plot of the potential energy surface
    PES_dict: DICT {(r, theta):energy}
    name: STR for title of the plot
    
    Returns: None
    """
    
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
    surf = ax.plot_surface(X, Y, Z, cmap=plt.get_cmap('hot') , linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_xlabel("X-H bond length / Å", fontsize=12)
    ax.set_ylabel("H-X-H bong angle / degrees",  fontsize=12)
    ax.set_zlabel("Energy / Hartrees", fontsize=12)
    ax.set_title("Potential Energy Surface for " + name, fontsize=18)
    

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.6, aspect=5)
    plt.savefig("PESoutputs/" + name + '_PES.pdf')
    plt.show()
    plt.close()
    
    return None   
        

def get_equilibrium_geometry(PES_dict):
    """Takes a DICT of geometry and energy and returns the geometry with the minimum energy
    
    Returns: TUPLE (r, theta)
    r: FLOAT equilibrium H-X bond length,  in Angstrom
    theta: FLOAT equilibrium H-X-H bond angle, in degree
    """
    
    return min(PES_dict, key=PES_dict.get)

    
    
        

def fit_curve_nm(PES_dict, degree_of_freedom, number_points, toplot, name="triatomic"):
    """Return a quadratic fit for the normal mode
    using scipy.optimize.curve_fit that ses non-linear least squares to fit a function to data. 
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
    
    Energies near the minimum along each normal mode are fitted to a quadratic function.
    
    PES_dict: DICT {(r, theta):energy}
    degree_of_freedom: STR "r" or "theta"
    number_points: INT number of points away from of the equilibrium (to each side) used in optimisation
    toplot: BOOL 
    name: STR name of molecule
    
    Save plot to a pdf file in ./PESoutputs/
    Returns: TUPLE (k,kerr)
    k: FLOAT force constant 
    kerr: FLOAT standard deviation error
    
    """
    
    r_0, theta_0 = get_equilibrium_geometry(PES_dict)
    energy_0 = PES_dict[(r_0, theta_0)]
    
    r = np.arange(r_0 - 0.05*number_points, r_0 + 0.05*(number_points+1), 0.05)
    theta = np.arange(theta_0 - 1*number_points, theta_0 + 1*(number_points+1), 1)
    
    if degree_of_freedom == "r":
        x_0 = r_0
        x = r
        Energy = np.ndarray(x.shape)
        for i in range(len(x)):
            Energy[i] = PES_dict[(round(x[i], 2), theta_0)]
            
    elif degree_of_freedom == "theta":
        x_0 = theta_0
        x = theta  
        Energy = np.ndarray(x.shape)
        for i in range(len(x)):
            Energy[i] = PES_dict[r_0, round(x[i],1)]
    
    def PESfit(x, k): 
        return energy_0 + 0.5*k*((x - x_0)**2) 
    
    
    #fitting the quadratic with least squared method
    #p =np.polyfit(x,Energy,2)
    
    params, pcov = optimize.curve_fit(PESfit, x, Energy , bounds=(0, np.inf))  
    kerr = np.sqrt(np.diag(pcov))[0] # one standard deviation errors on the parameters
    k = float(params[0])
     
    if toplot == True:
        if degree_of_freedom == "r":
            xfit=np.arange(r_0 - 0.05*number_points, r_0 + 0.05*(number_points+1), 0.005)
            unit = "Å"
        else: 
            xfit=np.arange(theta_0 - 1*number_points, theta_0 + 1*(number_points+1), 0.005)
            unit = "degree"
            
        yfit = energy_0 + 0.5*k*((xfit - x_0)**2)
       
        #yfit=np.polyval(p,xfit)
        
        plt.scatter(x, Energy, color='red', marker='+')
        plt.plot(xfit, yfit)
        
        #yerr = (0.38088/2) 
        #plt.errorbar(x, Energy, yerr=yerr, fmt='k.')  # Data
        
        plt.title('Potential energy along ' + degree_of_freedom + " for " + name)
        plt.xlabel(str(degree_of_freedom) + " / " + unit)
        plt.ylabel('Energy / Hartrees')
        plt.savefig("PESoutputs/" + name +"_curve_fitting_along_" + degree_of_freedom +".pdf")
        plt.show()
        plt.close()
    
    return k, kerr




def calculate_vib_frequencies(k_r, k_theta, x_eq, y_eq):
    """Return the vibrational frequencies from given force constants

    k_r : FLOAT force constant when r = x_eq, in Hartree/(Angstrom)^2
    k_theta : FLOAT force constant when  theta = y_eq, in Hartree/(degree)^2
    x_eq : FLOAT equilibrium bond length, in Angstrom
    y_eq : FLOAT equilibrium bond angle, in degree

    Returns TUPLE(symm_stretch, bend)
    symm_stretch : FLOAT strething frequency in wavenumber
    bend : FLOAT strething frequency in wavenumber

    """
    
    Hartree = 4.35974465054*(10**(-18))
    Degree = 0.0174533
    m_p = 1.6726219*(10**-27)
    Angstrom = 10**-10
    c = 29979245800

    
    k_r_ = k_r*Hartree*(Angstrom**-2)
        
    k_theta_ = k_theta*Hartree*(Degree**-2)
    
    symm_stretch = (1/(2*np.pi*c))*math.sqrt(k_r_/(2*m_p))
    bend = (1/(2*np.pi*c))*math.sqrt(k_theta_/(((x_eq*Angstrom)**2)*(0.5*m_p)))
    
    return symm_stretch, bend
        


def second_der(x,y, PES_dict):
    """Return the crude estimate second derivatives at equilibrium.
    Using finite difference method (second-order central)
    https://en.wikipedia.org/wiki/Finite_difference
    
    x: STR "r" or "theta"
    y: STR "r" or "theta"
    PES_dict: DICT {(r, theta):energy}

    Returns
    value: FLOAT second derivative"

    """
    r_0, theta_0 = get_equilibrium_geometry(PES_dict)
    def E(x, y):
        E = PES_dict[(round(x,1),round(y,1))]
        return E
    if x == y and x == "r":
        dr = 0.15
        value = (E(r_0 + dr, theta_0) - 2*E(r_0,theta_0) + E(r_0-dr,theta_0)) / (dr**2)
        
    elif x == y and x == "theta":
        dtheta = 1
        value = (E(r_0, theta_0+dtheta) - 2*E(r_0,theta_0) + E(r_0,theta_0-dtheta)) / (dtheta**2)
    elif x != y:
        dr = 0.05
        dtheta = 1
        value = (E(r_0-dr, theta_0-dtheta) + E(r_0+dr, theta_0+dtheta) - E(r_0+dr, theta_0-dtheta) - E(r_0-dr, theta_0+dtheta)) / (4*dr*dtheta)

    return value

def Hessian(PES_dict):
    """Return force constants along r and theta from crude estimate of the Hessian
    PES_dict:
    
    Returns: TUPLE(k_r, k_theta)
    k_r : FLOAT force constant when r = x_eq, in Hartree/(Angstrom)^2
    k_theta : FLOAT force constant when  theta = y_eq, in Hartree/(degree)^2
    """
    
    r_0, theta_0 = get_equilibrium_geometry(PES_dict)
    H = np.zeros((2,2))
    
    H[0][0] = second_der("r", "r", PES_dict)
    H[0][1] = second_der("r", "theta", PES_dict)
    H[1][0] = second_der("theta", "r", PES_dict)
    H[1][1] = second_der("theta", "theta", PES_dict)


    evals, evecs = np.linalg.eig(H)
    evallist = np.round(sorted(evals),10)

    
    return evallist[1], evallist[0]
    
    
    





    
    
  