# Melting curves of ice polymorphs in the vicinity of the liquid-liquid critical point

### Integration of the Clausius-Clapeyron equation 

This folder contains input and output data of simulations employed to calculate melting curves.
We integrated the Clausius-Clapeyron equation as proposed by Kofke, Mol. Phys. 78, 1331–1336 (1993).
The starting (T,P) points for the integration were obtained using the biased coexistence simulations described in ```../BiasedCoexistence```. 

The properties of liquid water and ices along melting curves is analyzed in the Jupyter Notebook ```Analysis.ipynb```.

Each ice polymorph folder ```IceIII```, ```IceIV```, ```IceV```, ```IceVI```, and ```IceXIII``` contains a few folders which are independent run sequences.
We have used the following name convention ```Run-(decrease/increase)-pressure-(individual/auto)```.
Increase/decrease pressure indicates whether pressure was increased or decreased along the coexistence curve from a given starting pressure.
Individual/auto indicates if the integration was performed automatically with simulations of fixed length (auto), or if simulations were performed one by one to manually check for convergence (individual).
The latter option was used in regions of the (T,P) plane in which correlation times are very long. 
For instance, some folders with this naming convention are:
* ```IceV/Run-decrease-pressure-auto```
* ```IceV/Run-decrease-pressure-individual```
* ```IceV/Run-increase-pressure-auto``` 

The auto simulations and the numerical integration were handled by the Python script ```integrate-clausius-clapeyron.py```, for instance, in ```IceV/Run-decrease-pressure-auto/integrate-clausius-clapeyron.py```.
The individual simulations and the numerical integration were handled by the bash script ```next_step.sh``` and the Python script ```next_rk_step.py```, which can be bound for instance in ```IceV/Run-decrease-pressure-individual/next_step.sh``` and ```IceV/Run-decrease-pressure-individual/step-base/next_rk_step.py```.

Calculations for the model TIP4P/Ice can be found in the folder ```TIP4PIce``` and some analysis is done in the Jupyter Notebook ```TIP4PIce/AnalysisTIP4PIce.ipynb```.

The results (TP coexistence lines) can be found in the following files:
* ```IceIII/thermo_condition_iceIII.txt```
* ```IceIV/thermo_condition_iceIV.txt```
* ```IceV/thermo_condition_iceV.txt```
* ```IceVI/thermo_condition_iceVI.txt```
* ```IceXIII/thermo_condition_iceXIII.txt```
and in:
* ```Results/thermo_condition_iceIII.txt```
* ```Results/thermo_condition_iceIV.txt```
* ```Results/thermo_condition_iceV.txt```
* ```Results/thermo_condition_iceVI.txt```
* ```Results/thermo_condition_iceXIII.txt```
* ```Results/thermo_condition_iceV_TIP4PIce.txt```

