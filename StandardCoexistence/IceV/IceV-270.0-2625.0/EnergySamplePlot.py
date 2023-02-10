import ipdb
ist = ipdb.set_trace
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import glob
import sys

def set_size(w,h,ax=None):
  if not ax: ax=plt.gca()
  l = ax.figure.subplotpars.left
  r = ax.figure.subplotpars.right
  t = ax.figure.subplotpars.top
  b = ax.figure.subplotpars.bottom
  figw = float(w)/(r-l)
  figh = float(h)/(t-b)
  ax.figure.set_size_inches(figw,figh)

def blockAvg(data,npts=2001):
  nframes = data.shape[0]
  nblocks = int(nframes/npts)
  data_block = []
  for block in range(nblocks):
    data_block.append(np.mean(data[block*npts:(block+1)*npts]))
  datmean = np.mean(data_block)
  daterr = 1.96*np.std(data_block)/np.sqrt(nblocks)
  return datmean,daterr,data_block

plt.rc('font',family='Arial')
plt.rc('font',serif='Arial')
plt.rcParams['font.size'] = 14
lfont = {'fontname':'Arial'}
plt.rcParams['mathtext.fontset'] = 'cm'

colors = ['black','blue','red','magenta','green','orangered','grey','cyan','brown','purple','darkgrey']
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
lines = ['-','--']
symbols = ['o','o','o']

f3 = plt.figure(3,figsize=(3.25,3.25))
ax3 = f3.add_subplot(111)

data = np.loadtxt('thermo.sample.out')
inittime = data[0,0]
U = data[:,1]*96.487/672.0

datman,daterr,dat_block = blockAvg(U,npts=2001)
ax3.plot((data[:,0]-inittime)*0.0005/1000,U,'-',linewidth=0.25,color=colors[3],alpha=0.5)
ax3.plot(0.5+np.arange(len(dat_block)),dat_block,'d',linewidth=0.25,color=colors[3],mec='black')

ax3.tick_params(length=4,width=0.8,labelsize=12,direction='in')#,top='on',right='on')
ax3.tick_params(length=2,width=0.4,direction='in',which='minor')#top='on',right='on',which='minor')
plt.setp(ax3.get_xticklabels(),**lfont)    
plt.setp(ax3.get_yticklabels(),**lfont)    
ax3.set_ylabel(r'$U\ (kJ/mol)$',**lfont)
ax3.set_xlabel(r'Time $(ns)$',**lfont)
#ax3.set_xlim([0,6])
ax3.set_ylim([-1566,-1559])
set_size(2.5,2.0,ax=ax3)
f3.savefig('IceV.U.270.0-2625.0.sample.png',dpi=600,bbox_inches='tight')
plt.close(3)
