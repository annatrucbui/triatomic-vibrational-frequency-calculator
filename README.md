# Triatomic-vibrational-frequency-calculator
A Python program that takes Gaussian output files for a triatomic at different geometies and return the potenial energy surface and the vibrational frequecies of the normal modes

Program extracts SCF energy calculated from Gaussian file and uses this to generate a PES plot. The equilibrium geometry is then determined. 
Vibrational frequencies can be estimated by fitting a quadratic curve along each normal mode OR calculated by diagonalising the Hessian matrix.

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
2. Matplotlib



## Installation
From source:

	git clone https://github.com/annatrucbui/Triatomic-vibrational-frequency-calculator


## Running the program
After finishing installation, you can run each example simulation as follow:

	python3 VibFreqCalculator.py /pathname


## Usage

Input: directory pathname. Within directory are a set of Gaussian output files

Output: Plot of PES as pdf and values of vibrational frequencies


