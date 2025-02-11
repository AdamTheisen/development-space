import pandas
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 18})

df = pandas.read_csv('./ship_workshop_ranking.csv', index_col=0)
df.plot.scatter(x='Feasibility', y='Scientific Priority', c='grey', s=100)
for i in df.index:
    va = 'bottom'
    yoff = 0. - 0.085
    xoff = 0
    text = i
    if 'Meteorology' in i or 'Sky Conditions' in i or 'Droplet Number' in i or 'Liquid Water' in i or 'Cloud Optical' in i:
        va = 'top'
        yoff = 0.075
    if 'Turbulence' in i or 'Cloud Optical' in i or 'Cloud Base Heights' in i :
        yoff = 0.025
        xoff = 0 - 0.28
        va = 'top'
    if 'Radiation' in i:
        yoff = 0.025
        xoff = 0 - 0.2
        va = 'top'
    if 'Sky Conditions' in i:
        yoff = 0.085
        xoff = 0.175
        va = 'top'
        text = 'Sky Imagery'
    if 'Ship' in i:
        text = '\n'.join(i.split('/'))
        yoff = 0. - 0.15
      
    plt.text(df.loc[i]['Feasibility'] + xoff, df.loc[i]['Scientific Priority'] + yoff, text, horizontalalignment='center',
             verticalalignment=va, c='grey', fontsize=12)

ax = plt.gca()
ax.set_axisbelow(True)
ax.set_ylim([0.9, 3.25])
ax.set_xlim([0.9, 3.25])
ax.set_xticks(np.arange(1, 3.5, 0.5))
ax.set_yticks(np.arange(1, 3.5, 0.5))
ax.set_aspect('equal', adjustable='box')
plt.grid(c='whitesmoke')
ax.tick_params(axis="both",which='minor', direction="in", length=3)
ax.tick_params(axis="both",which='major', direction="in", length=5)
plt.minorticks_on()
plt.tight_layout()
plt.subplots_adjust(hspace=0, wspace=0)
plt.show()
