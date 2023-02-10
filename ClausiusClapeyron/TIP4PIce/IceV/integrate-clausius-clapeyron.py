import numpy as np
import subprocess
import os

# variables
thermo_filename = "thermo_condition.txt"
data = np.genfromtxt(thermo_filename)
step_size_pressure = -250  # bar
num_steps = 1
lammps_exe = "/home/ppiaggi/Programs/Lammps/lammps-git-cpu/build9/lmp_della"
exe = "srun -N 1 -n 14 " + lammps_exe + " -screen screen.txt -i "
env_setup="export SLURM_WHOLE=1; export SLURM_OVERLAP=1; "

num_mols_phase1 = 336
num_mols_phase2 = 288

# Read initial data
if data.ndim == 1:
    # Case in which only initial data is in the file
    initial_pressure = data[0]
    initial_temperature = data[1]
elif data.ndim == 2:
    initial_pressure = data[-1, 0]
    initial_temperature = data[-1, 1]
pressure = initial_pressure
temperature = initial_temperature

def slope(my_pressure, my_temperature):
    # Define thermodynamic conditions
    os.system("cp in.thermosettings.base in.thermosettings")
    os.system('sed -i "s/TEMP/{:f}/g" in.thermosettings'.format(my_temperature))
    convert_bar_to_atm = 0.986923
    os.system(
        'sed -i "s/PRESS/{:f}/g" in.thermosettings'.format(
            my_pressure * convert_bar_to_atm
        )
    )
    os.system('sed -i "s/SEED/$RANDOM/g" in.thermosettings')
    # Run two phases
    p1 = subprocess.Popen("cd phase1; " + env_setup + exe + "in.lammps.phase1", shell=True)
    # p1 = subprocess.Popen(["srun","-N","1","-n","14",lammps_exe,"-screen","screen.txt","-i","in.lammps.phase1"], cwd="phase1")
    print("Running p1")
    p2 = subprocess.Popen("cd phase2; " + env_setup + exe + "in.lammps.phase2", shell=True)
    print("Running p2")
    p1.wait()
    p2.wait()
    print("Finished waiting for p1")
    print("Finished waiting for p2")
    # p2 = subprocess.Popen(["srun","-N","1","-n","14",lammps_exe,"-screen","screen.txt","-i","in.lammps.phase2"], cwd="phase2")
    # Back up
    os.system("./back-up.sh")
    # Get data
    data_phase1 = np.genfromtxt("phase1/thermo.phase1")
    data_phase2 = np.genfromtxt("phase2/thermo.phase2")
    ignore1 = int(np.shape(data_phase1)[0] / 4)
    ignore2 = int(np.shape(data_phase2)[0] / 4)
    enthalpy_phase1 = np.mean(data_phase1[ignore1:, :], axis=0)[1] / num_mols_phase1
    enthalpy_phase2 = np.mean(data_phase2[ignore2:, :], axis=0)[1] / num_mols_phase2
    volume_phase1 = np.mean(data_phase1[ignore1:, :], axis=0)[2] / num_mols_phase1
    volume_phase2 = np.mean(data_phase2[ignore2:, :], axis=0)[2] / num_mols_phase2
    os.system(
        "echo kx calculation - temperature {:f} - pressure {:f}".format(
            my_temperature, my_pressure
        )
    )
    os.system(
        "echo Properties phase 1 enthalpy {:f} volume {:f} - phase 2 enthalpy {:f} volume {:f}".format(
            enthalpy_phase1, volume_phase1, enthalpy_phase2, volume_phase2
        )
    )
    conversion_factor_bar_kCalmol_Acube = (6.0221408 / 4.184) * 1e-5
    return (
        my_temperature
        * (volume_phase1 - volume_phase2)
        * conversion_factor_bar_kCalmol_Acube
        / (enthalpy_phase1 - enthalpy_phase2)
    )


for i in range(num_steps):
    os.system(
        "echo This is iteration {:d} - temperature {:f} - pressure {:f}".format(
            i, temperature, pressure
        )
    )
    k1 = slope(pressure, temperature)
    k2 = slope(
        pressure + 0.5 * step_size_pressure, temperature + 0.5 * step_size_pressure * k1
    )
    k3 = slope(
        pressure + 0.5 * step_size_pressure, temperature + 0.5 * step_size_pressure * k2
    )
    k4 = slope(pressure + step_size_pressure, temperature + step_size_pressure * k3)
    new_pressure = pressure + step_size_pressure
    new_temperature = temperature + (1.0 / 6.0) * step_size_pressure * (
        k1 + 2 * k2 + 2 * k3 + k4
    )
    os.system(
        "echo {:f} {:f} >> {:s}".format(new_pressure, new_temperature, thermo_filename)
    )
    pressure = new_pressure
    temperature = new_temperature
