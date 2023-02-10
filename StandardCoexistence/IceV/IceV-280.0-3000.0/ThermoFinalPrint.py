import ipdb
ist = ipdb.set_trace
import numpy as np
import sys

def blockAvg(data,nblocks=30):
  nframes = data.shape[0]
  nframeblock = nframes/nblocks
  data_block = []
  for block in range(nblocks):
    data_block.append(np.mean(data[block*nframeblock:(block+1)*nframeblock]))
  datmean = np.mean(data_block)
  daterr = np.std(data_block)
  return datmean,daterr

data = np.loadtxt('thermo.sample.out')
avgTime = float(sys.argv[1])
nframes = int(avgTime*1000/(0.0005*1000)) 
U = data[-nframes:,1]*96.487/672.0
V = data[-nframes:,-1]*(6.022*10**23)*((10**-10)**3)/672.0
P = data[-nframes:,-5]*10**5
T = data[-nframes:,4]

Umean,Uerr = blockAvg(U,nblocks=10)
Vmean,Verr = blockAvg(V,nblocks=10)
Pmean,Perr = blockAvg(P,nblocks=10)
Tmean,Terr = blockAvg(T,nblocks=10)
np.savetxt('ThermoFinal.txt',np.column_stack((Tmean,Terr,Pmean,Perr,Vmean,Verr,Umean,Uerr)),header='T (K) err, P (Pa) err, V (m^3/mol) err, U (kJ/mol) err from {} ns of sampling'.format(avgTime))
