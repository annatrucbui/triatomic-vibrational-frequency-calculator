
"""
Created on Sat Oct 24 16:32:12 2020


Generate 
1. potential energy surface plot for a triatomic 
2. potential energy plot estimate near the equilibrium along 2 normal modes
3. equilibrium geometry, equilibrium energy, vibrational frequencies

Usage: $python3 VibFreqCalculator.py path/to/outputfiles/

if none specified, ./H2Ooutfiles


@author: btb32
"""
import vfc_functions as vfc
import tarfile



def main():
    
    print('\nWelcome to Vibrational Frequency Calculator! \n')
    print("Example format: H2Ooutfiles or extractedfiles/H20outfiles or H20outfiles.tar.bz2")
    

    try:
        dirname = input("Please enter directory name containing Gaussian out files: ")
        
        if "tar" in dirname:
            tar = tarfile.open(dirname)
            tar.extractall("./extractedfiles")
            tar.close()
            pathname = "./extractedfiles/" + dirname[:-8] +"/"
            PES_dict = vfc.dictionary_PES(pathname)
        else:
            pathname = "./" + dirname + "/"
            PES_dict = vfc.dictionary_PES(pathname) 
            
        name = dirname[0:3]
 
    except FileNotFoundError:
        print("\nFile is not found so automatically select H2O file")
        pathname = "./H2Ooutfiles/"
        name = "H2O"
        PES_dict = vfc.dictionary_PES(pathname)
    except:
        print("\nFile not correct type so automatically select H20 file")
        pathname = "./H2Ooutfiles/"
        name = "H2O"
        PES_dict = vfc.dictionary_PES(pathname)

    
    vfc.plot_PES(PES_dict, name)


    r_eq, theta_eq = vfc.get_equilibrium_geometry(PES_dict)
    
    print("\nOptimum geometry:")
    print(" bondlength =" + str(r_eq) + " Angstroms")
    print(" bond angle = " + str(theta_eq) + " degrees")
    
    print("\nFitting curve around minimum along r:")
    
    errorlimit_r = 0.05
    for i in range(10):
        try:
            k_r, k_r_err = vfc.fit_curve_nm(PES_dict, "r", 10-i, False)
            fractionerror = k_r_err/k_r
            if fractionerror < errorlimit_r:
                print(" Error in fitting:" + str(round(fractionerror*100,1)) +"%")
                print(" Number of points used: " + str((10-i)*2+1))
                vfc.fit_curve_nm(PES_dict, "r", 10-i, True, name)
                break
        except KeyError:
            pass
        
            
    print("\nFitting curve around minimum along theta:") 
    errorlimit_theta = 0.02
    for i in range(10):
        try:
            k_theta, k_theta_err = vfc.fit_curve_nm(PES_dict, "theta", 10-i, False)
            fractionerror = k_theta_err/k_theta
            if k_theta_err/k_theta < errorlimit_theta:
                print(" Error in fitting:" + str(round(fractionerror*100,1)) +"%")
                print(" Number of points used: " + str((10-i)*2+1))
                vfc.fit_curve_nm(PES_dict, "theta", 10-i, True, name)
                break
        except KeyError:
            pass

    
 
    
    print('\nVibrational frequencies by curve fitting:')
 
    sym, bend = vfc.calculate_vib_frequencies(k_r, k_theta, r_eq, theta_eq)
    sym_err, bend_err = vfc.calculate_vib_frequencies(k_r_err, k_theta_err, r_eq, theta_eq)
    
    print(" Symmetric stretch: " + str(round(sym,2)) + " \u00B1 " + str(round(sym_err,2)) + " cm\u207B\u00B9")
    print(" Bending: " + str(round(bend,2)) + " \u00B1 " + str(round(bend_err,2)) + " cm\u207B\u00B9")
    
    
    
    print("\nVibrational frequencies by diagonalising Hessian:")
    
    k_r_H, k_theta_H = vfc.Hessian(PES_dict)
    sym_H, bend_H = vfc.calculate_vib_frequencies(k_r_H, k_theta_H, r_eq, theta_eq)
    
    print(" Symmetric stretch: " + str(round(sym_H,2)) + " cm\u207B\u00B9")
    print(" Bending: " + str(round(bend_H,2)) +  " cm\u207B\u00B9")
    


 
if __name__ == '__main__':
    main()

