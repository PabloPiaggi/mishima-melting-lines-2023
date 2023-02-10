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

plt.rc('font',family='Arial')
plt.rc('font',serif='Arial')
plt.rcParams['font.size'] = 14
lfont = {'fontname':'Arial'}
plt.rcParams['mathtext.fontset'] = 'cm'

colors = ['black','blue','red','magenta','green','orangered','grey','cyan','brown','purple','darkgrey']
colors = ['#1f78b4','#33a02c','#e31a1c','#ff7f00','#6a3d9a','#b15928','#a6cee3','#b2df8a','#fb9a99','#fdbf6f','#cab2d6','#ffff99']
lines = ['-','--']
symbols = ['o','o','o']

f1 = plt.figure(1,figsize=(3.25,3.25))
ax1 = f1.add_subplot(111)

data = np.loadtxt('COLVAR')
times = (data[-1,0]-data[-2,0])*np.arange(data.shape[0])
times = 0.25*np.arange(data.shape[0])
inittime = data[0,0]
ax1.plot((times)/1000,data[:,4],'-',linewidth=0.25,color=colors[0],alpha=0.8)

ax1.tick_params(length=4,width=0.8,labelsize=12,direction='in')#,top='on',right='on')
ax1.tick_params(length=2,width=0.4,direction='in',which='minor')#top='on',right='on',which='minor')
plt.setp(ax1.get_xticklabels(),**lfont)    
plt.setp(ax1.get_yticklabels(),**lfont)    
ax1.set_xlabel(r'Time $(ns)$',**lfont)
ax1.set_ylabel(r'$N_{iceV}$',**lfont)
ax1.set_ylim([280,410])
#ax1.set_xlim([0,6])
set_size(2.5,2.0,ax=ax1)
f1.savefig('DPMD.NiceV.260K-2000bar.png',dpi=600,bbox_inches='tight')
plt.close(1)
