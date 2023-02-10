import ase.io
conf=ase.io.read('iceIV-full.data',format='lammps-data',style='full')
ase.io.write('iceIV.data',conf, format='lammps-data')
quit()
