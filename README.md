# Melting curves of ice polymorphs in the vicinity of the liquid-liquid critical point

### Authors: Pablo M. Piaggi, Thomas E. Gartner III, Roberto Car, Pablo G. Debenedetti

[![plumID:23.004](https://www.plumed-nest.org/eggs/23/004/badge.svg)](https://www.plumed-nest.org/eggs/23/004/)
[![DataSpace](https://img.shields.io/badge/DataSpace-88435%2Fdsp01gt54kr255-orange)](https://doi.org/10.34770/pbja-we49)

Analysis and input files to reproduce simulations of manuscript "Melting curves of ice polymorphs in the vicinity of the liquid-liquid critical point" by Piaggi, Gartner, Car, and Debenedetti.

#### Description of folder contents:
* ```BiasedCoexistence```: Input and output files of biased coexistence simulations used to compute melting points for ices III, IV, V, and XIII 
* ```ClausiusClapeyron```: Scripts to integrate the Clausius-Clapeyron equation, and input and output files of simulations for ices III, IV, V, VI, and XIII.
* ```DataLLT```: Data of liquid-liquid transition in our model
* ```DeepPotentialModel```: DeePMD model used in our simulations
* ```ExperimentalResultsDigitized```: Digitezed experimental data on the melting curves of polymorphs for light and heavy water
* ```LandauFreeEnergies```: Landau model used to construct the schematic free energy surfaces shown in Figure 1 of the paper
* ```StandardCoexistence```: Standard coexistence simulations for ices IV and V.

More information is provided in the files README.md within each folder.

#### Analysis is done in the following Jupyter Notebooks:
* ```./BiasedCoexistence/Analysis.ipynb``` - Description: Results of melting curves from biased coexistence simulations for all ice polymorphs
* ```./BiasedCoexistence/IceXIII/3-production/Analysis.ipynb``` - Description: Results of biased coexistence simulations for ice XIII
* ```./BiasedCoexistence/IceIV/3-production/256molecules/Analysis.ipynb``` - Description: Results of biased coexistence simulations for ice IV 256 molecules
* ```./BiasedCoexistence/IceIV/3-production/2048molecules/Analysis.ipynb``` - Description: Results of biased coexistence simulations for ice IV 2048 molecules
* ```./BiasedCoexistence/IceV/3-production/Analysis.ipynb``` - Description: Results of biased coexistence simulations for ice V
* ```./BiasedCoexistence/IceIII/3-production/Analysis.ipynb``` - Description: Results of biased coexistence simulations for ice III
* ```./ClausiusClapeyron/Analysis.ipynb``` - Description: Properties of liquid water and ices along melting curves using data from the integration of the Clausius-Clapeyron eqn
* ```./ClausiusClapeyron/TIP4PIce/AnalysisTIP4PIce.ipynb``` - Description: Melting curve of ice V within the TIP4P/Ice model from integration of the Clausius-Clapeyron eqn
* ```./LandauFreeEnergies/Analysis.ipynb``` - Description: Schematic of free energy curves from Landau's theory

#### Software needed to reproduce the simulations: 

Simulations were performed using the following codes:
* LAMMPS (15 Apr 2020)
* DeePMD-kit v1.0.2-1-g6aee326-dirty - source brach: r1.0 - source commit: 6aee326
* PLUMED 2.8.0-dev (git: 54560ef-dirty)

Jupyter notebooks require the following packages:
* Python 3.10.4 (main, Mar 31 2022, 08:41:55) [GCC 7.5.0]
* Matplotlib 3.5.3
* Numpy 1.22.4
* Scipy 1.7.3

Please e-mail me if you have trouble reproducing the results.
