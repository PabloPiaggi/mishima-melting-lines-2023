import numpy as np
import matplotlib.pyplot as plt
import MDAnalysis
import freud
import ipdb
ist = ipdb.set_trace

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
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
lines = ['-','--']
symbols = ['o','o','o']

f3 = plt.figure(3,figsize=(3.25,3.25))
ax3 = f3.add_subplot(111)

step=1
ql = freud.order.Steinhardt(l=4,average=True,wl=False)
reader = MDAnalysis.coordinates.LAMMPS.DumpReader("water.lammps-dump",format='LAMMPSDUMP',timeunit='ps')
n_frames=sum(1 for e in reader[::step])
n_solid_molecules=np.zeros(n_frames)
counter=0
ql_all = []
for frame in reader[::step]:
    ts = MDAnalysis.coordinates.base.Timestep(frame.positions[::3,:].shape[0])
    ts.positions=frame.positions[::3,:]
    ts.dimensions=frame.dimensions
    ql.compute(ts, {'r_max':3.05}) #,reset=False)
    #print(ql.ql)
    ql_all.append(ql.ql)
    n_solid_molecules[counter]=ql.ql[ql.ql>0.26].shape[0]
    print(n_solid_molecules[counter])
    counter += 1
#plt.plot(np.arange(n_frames),n_solid_molecules)
#plt.show()

hist,bins = np.histogram(ql_all,bins=50,range=(0.05,0.45))
binmid = (bins[1:]+bins[:-1])/2.0

plt.plot(binmid,hist)
#plt.show()
ax3.tick_params(length=4,width=0.8,labelsize=12,direction='in')#,top='on',right='on')
ax3.tick_params(length=2,width=0.4,direction='in',which='minor')#top='on',right='on',which='minor')
plt.setp(ax3.get_xticklabels(),**lfont)    
plt.setp(ax3.get_yticklabels(),**lfont)    
ax3.set_ylabel(r'Count',**lfont)
ax3.set_xlabel(r'$q_4$',**lfont)
#ax3.set_xlim([0,6])
#ax3.set_ylim([-1570,-1550])
set_size(2.5,2.0,ax=ax3)
f3.savefig('IceV.240.0-2500.0.q4hist.png',dpi=600,bbox_inches='tight')
plt.close(3)
