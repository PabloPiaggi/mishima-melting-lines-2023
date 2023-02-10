import numpy as np
import subprocess
import os

# variables
thermo_filename="thermo_condition.txt"
data=np.genfromtxt(thermo_filename)
step_size_pressure=500 # bar
num_steps=3
lammps_exe="/home/ppiaggi/Programs/DeepMD/lammps2/src/lmp_mpi"
exe="srun -N 1 -n 4 " + lammps_exe + " -screen screen.txt -i "
num_mols_phase1=1024
num_mols_phase2=1024

# Read initial data
if (data.ndim==1):
	# Case in which only initial data is in the file
	initial_pressure=data[0]
	initial_temperature=data[1]
elif (data.ndim==2):
	initial_pressure=data[-1,0]
	initial_temperature=data[-1,1]
pressure=initial_pressure
temperature=initial_temperature

def slope(my_pressure,my_temperature):
	# Define thermodynamic conditions
	os.system('cp in.thermosettings.base in.thermosettings')
	os.system('sed -i "s/TEMP/{:f}/g" in.thermosettings'.format(my_temperature))
	os.system('sed -i "s/PRESS/{:f}/g" in.thermosettings'.format(my_pressure))
	os.system('sed -i "s/SEED/$RANDOM/g" in.thermosettings')
	# Run two phases
	p1 = subprocess.Popen("cd phase1; " + exe + "in.lammps.phase1",shell=True)
	p2 = subprocess.Popen("cd phase2; " + exe + "in.lammps.phase2",shell=True)
	p1.wait()
	p2.wait()
	# Get data
	data_phase1=np.genfromtxt("phase1/thermo.phase1")
	data_phase2=np.genfromtxt("phase2/thermo.phase2")
	enthalpy_phase1=np.mean(data_phase1,axis=0)[1]/num_mols_phase1
	enthalpy_phase2=np.mean(data_phase2,axis=0)[1]/num_mols_phase2
	volume_phase1=np.mean(data_phase1,axis=0)[2]/num_mols_phase1
	volume_phase2=np.mean(data_phase2,axis=0)[2]/num_mols_phase2
	os.system("echo kx calculation - temperature {:f} - pressure {:f}".format(my_temperature,my_pressure))
	os.system("echo Properties phase 1 enthalpy {:f} volume {:f} - phase 2 enthalpy {:f} volume {:f}".format(enthalpy_phase1,volume_phase1,enthalpy_phase2,volume_phase2))
	conversion_factor_bar_eV_Acube=6.241509e-7
	return my_temperature*(volume_phase1-volume_phase2)*conversion_factor_bar_eV_Acube/(enthalpy_phase1-enthalpy_phase2)

for i in range(num_steps):
	os.system("echo This is iteration {:d} - temperature {:f} - pressure {:f}".format(i,temperature,pressure))
	k1=slope(pressure,temperature)
	k2=slope(pressure+0.5*step_size_pressure,temperature+0.5*step_size_pressure*k1)
	k3=slope(pressure+0.5*step_size_pressure,temperature+0.5*step_size_pressure*k2)
	k4=slope(pressure+step_size_pressure,temperature+step_size_pressure*k3)
	new_pressure=pressure+step_size_pressure
	new_temperature=temperature+(1./6.)*step_size_pressure*(k1+2*k2+2*k3+k4)
	os.system('echo {:f} {:f} >> {:s}'.format(new_pressure,new_temperature,thermo_filename))
	pressure=new_pressure
	temperature=new_temperature
