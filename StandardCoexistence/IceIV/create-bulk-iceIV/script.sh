# This script creates an ice V configuration using GenIce.
# The configuration is converted into a lammps data file
# suitable for DPMD using VMD and ASE.
for i in `seq 1 1`
do
	echo $i
	genice --rep 2 2 2 IV --format g --seed $RANDOM > iceIV.gro
	vmd -dispdev none -e script-vmd.tcl
	python3 script-ase.py
	awk '{if ($2==1) print $1,2,$3,$4,$5; else if ($2==2) print $1,1,$3,$4,$5; else print $0}' iceIV.data > iceIV-${i}.data	
	#rm iceV.data iceV-full.data iceV.gro
done
