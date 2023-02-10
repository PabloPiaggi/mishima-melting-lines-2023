import numpy as np

data = np.loadtxt('thermo.out')
lx = np.mean(data[100:,-7])
lz = np.mean(data[100:,-5])
xy = np.mean(data[100:,-4])
xz = np.mean(data[100:,-3])
yz = np.mean(data[100:,-2])

print("fix 4 all deform 1 x final 0.0 {} z final 0.0 {} xy final {} xz final {} yz final {} units box".format(lx,lz,xy,xz,yz))
