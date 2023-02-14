# Melting curves of ice polymorphs in the vicinity of the liquid-liquid critical point

### Biased coexistence simulations

This folder contains input and ouput data for biased coexistence simulations for IceIII, IceIV, IceV, and IceXIII.
These simulations were used to compute melting points for the different polymorphs.
The melting points were then used as starting points for the integration of the Clausius-Clapyron equation (see ```../ClausiusClapeyron```).

The code to generate Figure 3 from the paper can be found in the Jupyter Notebook ```Analysis.ipynb```.

Each ice polymorph folder ```IceIII```, ```IceIV```, ```IceV```, and ```IceXIII``` contains three folders, for instance:
* ```IceIII/1-distributions```: Distributions of environment similarity CV in the liquid and in the ice polymorph
* ```IceIII/2-create-interface-and-equilibrate```: Creation and equilibration of configuration with interface
* ```IceIII/3-production```: Production runs - biased simulations

The analysis of the simulations is performed in the Jupyter Notebooks:
* ```IceIII/3-production/Analysis.ipynb```
* ```IceIV/3-production/Analysis.ipynb```
* ```IceV/3-production/Analysis.ipynb```
* ```IceXIII/3-production/Analysis.ipynb```
for each different polymorph.
This analysis involves the calculation of free energy surfaces and chemical potentials as a function of temperature and pressure.
