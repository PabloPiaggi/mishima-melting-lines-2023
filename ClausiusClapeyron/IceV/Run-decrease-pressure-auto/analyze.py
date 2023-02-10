import numpy as np
import subprocess
import os

# variables
num_mols_phase1=336
num_mols_phase2=336

os.system("echo '# temperature pressure enthalpy_phase1 volume_phase1 enthalpy_phase2 volume_phase2'")
for i in range(0,28):
	# Get data
	data_phase1=np.genfromtxt("bck." + str(i) + "/phase1/thermo.phase1")
	data_phase2=np.genfromtxt("bck." + str(i) + "/phase2/thermo.phase2")
	ignore1=int(np.shape(data_phase1)[0]/2)
	ignore2=int(np.shape(data_phase2)[0]/2)
	enthalpy_phase1=np.mean(data_phase1[ignore1:,:],axis=0)[1]/num_mols_phase1
	enthalpy_phase2=np.mean(data_phase2[ignore2:,:],axis=0)[1]/num_mols_phase2
	volume_phase1=np.mean(data_phase1[ignore1:,:],axis=0)[2]/num_mols_phase1
	volume_phase2=np.mean(data_phase2[ignore2:,:],axis=0)[2]/num_mols_phase2
	my_temperature=float(os.popen("grep 'temperature equal' bck." + str(i) + "/in.thermosettings | awk '{print $4}'").read())
	my_pressure=float(os.popen("grep 'pressure equal' bck." + str(i) + "/in.thermosettings | awk '{print $4}'").read())
	os.system("echo {:f} {:f} {:f} {:f} {:f} {:f}".format(my_temperature,my_pressure,enthalpy_phase1,volume_phase1,enthalpy_phase2,volume_phase2))
