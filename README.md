# Triatomic-vibrational-frequency-calculator
A Python program that takes Gaussian output files for a triatomic at different geometies and return the potenial energy surface and the vibrational frequecies of the normal modes

Program extracts SCF energy calculated from Gaussian file and uses this to generate a PES plot. The equilibrium geometry is then determined. 
Vibrational frequencies are estimated by fitting a quadratic curve along each normal mode and calculated by diagonalising the Hessian matrix.

The calculation is applied to two examples:
1. H20

2. H2S



## Requirements 

Triatomic-vibrational-frequency-calculator should work on all Linux distributions.
Triatomic-vibrational-frequency-calculator
requires Python 3.x

	sudo apt-get update && sudo apt-get install python3

### The packages required include:

1. NumPy (https://numpy.org/)

2. Matplotlib (https://matplotlib.org/)

3. SciPy (https://www.scipy.org/)


## Installation
From source:

	git clone https://github.com/annatrucbui/Triatomic-vibrational-frequency-calculator


## Running the program
After finishing installation, you can run the program as follow:

	python3 VibFreqCalculator.py


## Usage

Input: directory pathname. Within directory are a set of Gaussian output files. Alternative: also take compressed .tar.bz2 and extract to readable output files.

The program only takes relative path as input. Gaussian outfiles, either compressed on extracted, should be in the same directory as the program.


Outputs: 
1. Potential energy surface plot for a triatomic 

2. Potential energy plot estimate near the equilibrium along 2 normal modes

3. Equilibrium geometry, equilibrium energy, vibrational frequencies

## Examples

Experimental data vs computed data
Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.

<p float="left">
  <img src="https://github.com/annatrucbui/triatomic-vibrational-frequency-calculator/blob/master/PESoutputs/H2O_PES.jpg?raw=true" width="400" />
  <img src="https://github.com/annatrucbui/triatomic-vibrational-frequency-calculator/blob/master/PESoutputs/H2S_PES.jpg?raw=true" width="400" />

</p>





