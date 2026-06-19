#!/usr/bin/env python
from sys import argv
from glob import glob
import pynbody as pyn
import numpy as np
import matplotlib.pyplot as plt

basename = 'galaxy'
n_snaps = 300

if __name__ == "__main__":
    for i in range(n_snaps):
        print(f"Processing Frame {i+1} of {n_snaps}")
        snap = pyn.load(f'{argv[1]}/{basename}.{i+1:05d}')
        plt.clf()
        young = snap.s[snap.s['tform'] == 1]
        old = snap.s[snap.s['tform'] == 0]
        com = np.mean(snap['pos'], axis=0)
        snap['pos'] -= com
        plt.plot(young['x'][np.argsort(young['z'])], young['y'][np.argsort(young['z'])], 'c,', alpha=0.2)
        plt.plot(old['x'][np.argsort(old['z'])], old['y'][np.argsort(old['z'])], 'y,', alpha=0.05)
        plt.ylim(-150, 150)
        plt.xlim(-150, 150)
        plt.gca().set_facecolor('black')
        plt.gca().set_aspect('equal')
        plt.gcf().set_facecolor('black')
        plt.figtext(0.8, 0.9, f'{int(snap.properties["time"].in_units("Myr"))} Myr', color='white')
        plt.savefig(f'images/im{i:05d}.png', dpi=200)
