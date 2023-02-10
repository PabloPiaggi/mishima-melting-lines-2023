import numpy as np

data = np.loadtxt('thermo.bulk.out')
ly = np.mean(data[100:,-6])
lz = np.mean(data[100:,-5])
xy = np.mean(data[100:,-4])
xz = np.mean(data[100:,-3])
yz = np.mean(data[100:,-2])

print("fix 4 all deform 1 y final 0.0 {} z final 0.0 {} xy final {} xz final {} yz final {} units box".format(ly,lz,xy,xz,yz))
