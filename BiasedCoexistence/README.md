# Melting curves of ice polymorphs in the vicinity of the liquid-liquid critical point

### Biased coexistence simulations

This folder contains input and ouput data for biased coexistence simulations for IceIII, IceIV, IceV, and IceXIII.
These simulations were used to compute melting points for the different polymorphs.
The melting points were then used as starting points for the integration of the Clausius-Clapyron equation (see ```../ClausiusClapeyron```).

The code to generate Figure 3 from the paper can be found in the Jupyter Notebook ```Analysis.ipynb```.

Each ice polymorph folder ```IceIII```, ```IceIV```, ```IceV```, and ```IceXIII``` contains three subfolders, for instance:
* ```IceIII/1-distributions```: Distributions of environment similarity CV in the liquid and in the ice polymorph
* ```IceIII/2-create-interface-and-equilibrate```: Creation and equilibration of configuration with interface
* ```IceIII/3-production```: Production runs - biased simulations

which correspond to 3 steps to be performed sequentally. I describe these subfolders in greater detail below.

In subfolders ```1-distributions``` we calculate the distributions of the order parameter, the environment similarity CV, for liquid water and ice at a given T,P.
The objective of this step is to find the best possible SIGMA value of the ENVIRONMENTSIMILARITY action in PLUMED, which is the one that minimizes the overlap between the distributions for liquid water and ice.
To do this, we need a simulation of the liquid and ice which are found in folders such as,
* ```IceIII/1-distributions/3000bar-295K/Liquid```
* ```IceIII/1-distributions/3000bar-295K/IceIII```

From these simulations we obtain a trajectory in dcd format which can be read by the PLUMED driver.
The PLUMED input files and the script to compute the ENVIRONMENTSIMILARITY action for different SIGMA values is found, for example, in ```IceIII/1-distributions/3000bar-295K/CalculateOptimalSigma```.
This folder contains the ```script.sh``` to compute the overlap for different SIGMA values, ```script.py``` to compute the overlap between distributions, the ```results.txt```with the result of sigma vs overlap, and the folders ```IceIII``` and ```Liquid``` with the PLUMED input and dcd trajectories.

The subfolder ```2-create-interface-and-equilibrate``` contains the LAMMPS input file to create and equilibrate the interfacial configuartion.

The subfolder ```3-production``` contains a ```BASE``` directory with input files which is replicated to perform simulations at different T,P.
```BASE``` contains the input files:
* ```BoxDimensions.py```: Python script to get equilibrium box dimensions 
* ```bulk.lmp```: LAMMPS input file to equilibrate bulk ice
* ```env*.pdb```: Environments for ENVIRONMENTSIMILARITY PLUMED action
* ```equil.lmp```: LAMMPS input file to equilibrate the interface (after executing bulk.lmp)
* ```iceIII.data```: Ice III bulk configuration in LAMMPS data format.
* ```in.*```: LAMMPS supplementary input files (included in the base input scripts)
* ```job.sh```: SLURM script
* ```plumed.dat```: PLUMED input file
* ```Restart.lmp```: LAMMPS input file to restart production runs
* ```start.lmp```: LAMMPS input file for production runs
* ```water.data.interface```: Interfacial configuration in LAMMPS data format


Finally, the analysis of the simulations is performed in the Jupyter Notebooks:
* ```IceIII/3-production/Analysis.ipynb```
* ```IceIV/3-production/Analysis.ipynb```
* ```IceV/3-production/Analysis.ipynb```
* ```IceXIII/3-production/Analysis.ipynb```

for each different polymorph.
This analysis involves the calculation of free energy surfaces and chemical potentials as a function of temperature and pressure.

