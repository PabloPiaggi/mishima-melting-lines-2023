# Melting curves of ice polymorphs in the vicinity of the liquid-liquid critical point

### Standard coexistence simulations

We performed standard coexistence simulations of ice IV and ice V to validate the results obtained with biased coexistence and the integration of the Clausius-Clapeyron equation.
Results are shown in folders ```IceIV``` and ```IceV```.
The subfolders correspond to simulations at different thermodynamic conditions.
The naming convention is ```Ice(IV/V)/Ice(IV/V)-TEMP-PRESS``` where TEMP and PRESS are the temperature in K and the pressure in bar used for the simulation.
For instance,
* ```IceV/IceV-260.0-2500.0```
* ```IceIV/IceIV-250.0-3500.0/```

There is also a ```BASE``` subfolder which was replicated to create folders for simulations at different thermodynamic conditions.
Inside the ```BASE``` folder we found the input files for the simulations:
* ```BoxDimensions.py``` - Obtain equilibrium bulk ice box geometry at a given T,P
* ```iceIV-1-equil.data``` - Intial ice IV bulk structure in LAMMPS data format
* ```in.boxdimensions``` - Equilibrium box dimensions written by ```BoxDimensions.py```
* ```in.lammps.equil``` - LAMMPS input for bulk equilibration
* ```in.lammps.init``` - LAMMPS input for interface equilibration
* ```in.lammps.sample``` - LAMMPS input for production run (sample)
* ```in.thermosettings``` - Thermodynamic conditions read by LAMMPS
* ```run.init.qs``` - SLURM input script
* ```run.sample.qs``` - SLURM input script
* ```water.data.interface``` - Interfacial configuration in LAMMPS data format

