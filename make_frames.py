#!/usr/bin/env python
from sys import argv
from glob import glob
import pynbody as pyn
import numpy as np
import matplotlib.pyplot as plt

basename = 'merger'
n_snaps = 250

if __name__ == "__main__":
    for i in range(n_snaps):
        print(f"Processing Frame {i+1} of {n_snaps}")
        snap = pyn.load(f'{argv[1]}/{basename}.{i+1:05d}')
        plt.clf()
        plt.plot(snap.s['x'][snap.s['tform'] == 1], snap.s['y'][snap.s['tform'] == 1], 'c,', alpha=0.2)
        plt.plot(snap.s['x'][snap.s['tform'] == 0], snap.s['y'][snap.s['tform'] == 0], 'y,', alpha=0.05)
        plt.ylim(-150, 150)
        plt.xlim(-150, 150)
        plt.gca().set_facecolor('black')
        plt.gca().set_aspect('equal')
        plt.gcf().set_facecolor('black')
        plt.savefig(f'images/im{i:05d}.png', dpi=200)
