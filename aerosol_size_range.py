import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

fig, ax = plt.subplots(figsize=(10,5))
bar3 = ax.barh(0, left=5, width=375, label='mSEMS', color='lightblue')
bar1 = ax.barh(1, left=10, width=490, label='SMPS', color='lightblue')
bar2 = ax.barh(2, left=60, width=940, label='UHSAS', color='lightblue')
bar12 = ax.barh(3, left=100, width=3000, label='PCASP', color='lightblue')
bar11 = ax.barh(4, left=130, width=3000, label='POPS', color='lightblue')
bar31 = ax.barh(5, left=150, width=3000, label='mSEMS', color='lightblue')
bar3 = ax.barh(6, left=250, width=34750, label='OPC', color='lightblue')
bar4 = ax.barh(7, left=500, width=19500, label='APS', color='lightblue')
ax.set_ylim([-0.5, 8])
plt.tick_params(axis='both', left=False, top=False, right=False, labelleft=False, labeltop=False, labelright=False)
ax.spines[['left', 'right', 'top']].set_visible(False)

ax.xaxis.grid(which='major', color='k')

ax.set_xscale('log')
plt.xticks([10, 100, 1000, 10000, 35000])
ax.set_xticklabels(['10', '100', '1,000', '10,000', '35,000'])
ax.set_xlabel('Particle Size (nm)')
plt.savefig('./images/particle_size_background.png', transparent=True)
