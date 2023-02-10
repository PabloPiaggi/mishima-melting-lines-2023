import numpy as np
import subprocess
import os

#####################################
# Variables
#####################################

thermo_filename="thermo_condition.txt"
data=np.genfromtxt("../" + thermo_filename)
step_size_pressure=-250 # bar
num_mols_phase1=336
num_mols_phase2=192

#####################################
# Read initial data
#####################################

if (data.ndim==1):
	# Case in which only initial data is in the file
	initial_pressure=data[0]
	initial_temperature=data[1]
elif (data.ndim==2):
	initial_pressure=data[-1,0]
	initial_temperature=data[-1,1]
pressure=initial_pressure
temperature=initial_temperature

#####################################
# Define functions
#####################################

def create_simulation_folder(folder,my_temperature,my_pressure):
    os.system("mkdir " + folder)
    os.system("cp -r ../phase1 " + folder + "/.")
    os.system("cp -r ../phase2 " + folder + "/.")
    os.system("cp ../in.thermosettings.base " + folder + "/in.thermosettings")
    os.system('sed -i "s/TEMP/{:f}/g" '.format(my_temperature) + folder + '/in.thermosettings')
    os.system('sed -i "s/PRESS/{:f}/g" '.format(my_pressure) + folder + '/in.thermosettings')
    os.system('sed -i "s/SEED/$RANDOM/g" ' + folder + '/in.thermosettings')
    os.system('echo {:f} {:f} >> {:s}'.format(my_pressure,my_temperature,folder + "/" + thermo_filename))
    # Copy last configuration from previous run
    if (int(folder)>0):
        prev_folder=str(int(folder)-1)
        os.system('cp ' + prev_folder + '/phase1/water.data.final.phase1 ' + folder + '/phase1/water.data.phase1')
        os.system('cp ' + prev_folder + '/phase2/water.data.final.phase2 ' + folder + '/phase2/water.data.phase2')
        print("   Copied succesfully last configuration from previous folder " + prev_folder + " to new folder " + folder) 
    else:
        print("   Check if last configuration from previous RK iteration is needed") 
    print("   Preparing folder " + folder + " with pressure and temperature ",my_pressure,my_temperature)

def slope(folder):
    print("   Calculating slope for folder " + folder)
    # Get temperature and pressure
    thermo_filename=folder + "/thermo_condition.txt"
    thermo_data=np.genfromtxt(thermo_filename)
    my_pressure=thermo_data[0]
    my_temperature=thermo_data[1]
    # Get data
    data_phase1=np.genfromtxt(folder + "/phase1/thermo.phase1")
    data_phase2=np.genfromtxt(folder + "/phase2/thermo.phase2")
    ignore1=int(np.shape(data_phase1)[0]/2)
    ignore2=int(np.shape(data_phase2)[0]/2)
    enthalpy_phase1=np.mean(data_phase1[ignore1:,:],axis=0)[1]/num_mols_phase1
    enthalpy_phase2=np.mean(data_phase2[ignore2:,:],axis=0)[1]/num_mols_phase2
    volume_phase1=np.mean(data_phase1[ignore1:,:],axis=0)[2]/num_mols_phase1
    volume_phase2=np.mean(data_phase2[ignore2:,:],axis=0)[2]/num_mols_phase2
    print('      Temperature {:f} - pressure {:f}'.format(my_temperature,my_pressure))
    print("      Properties phase 1 enthalpy {:f} volume {:f} - phase 2 enthalpy {:f} volume {:f}".format(enthalpy_phase1,volume_phase1,enthalpy_phase2,volume_phase2))
    conversion_factor_bar_eV_Acube=6.241509e-7
    return my_temperature*(volume_phase1-volume_phase2)*conversion_factor_bar_eV_Acube/(enthalpy_phase1-enthalpy_phase2)

#####################################
# Create folders
#####################################

if (not(os.path.isdir("0"))): # Step 0
    print("Step 0")
    my_pressure=pressure
    my_temperature=temperature
    create_simulation_folder("0",my_temperature,my_pressure)
elif (not(os.path.isdir("1"))): # Step 1
    print("Step 1")
    k1=slope("0")
    my_pressure=pressure+0.5*step_size_pressure
    my_temperature=temperature+0.5*step_size_pressure*k1
    create_simulation_folder("1",my_temperature,my_pressure)
elif (not(os.path.isdir("2"))): # Step 2
    print("Step 2")
    k2=slope("1")
    my_pressure=pressure+0.5*step_size_pressure
    my_temperature=temperature+0.5*step_size_pressure*k2
    create_simulation_folder("2",my_temperature,my_pressure)
elif (not(os.path.isdir("3"))): # Step 3
    print("Step 3")
    k3=slope("2")
    my_pressure=pressure+step_size_pressure
    my_temperature=temperature+step_size_pressure*k3
    create_simulation_folder("3",my_temperature,my_pressure)
else: # Nothing to be done
    print("All steps finished - writing results to file ../" + str(thermo_filename))
    k1=slope("0")
    k2=slope("1")
    k3=slope("2")
    k4=slope("3")
    new_pressure=pressure+step_size_pressure
    new_temperature=temperature+(1./6.)*step_size_pressure*(k1+2*k2+2*k3+k4)
    print("   New pressure and temperature ",new_pressure,new_temperature)
    os.system('echo {:f} {:f} >> {:s}'.format(new_pressure,new_temperature,"../" + thermo_filename))


