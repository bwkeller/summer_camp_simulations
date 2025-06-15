#!/usr/bin/env python
from sys import argv
import numpy as np
import pynbody as pyn
from pytipsy import rtipsy, wtipsy

nbulge = 65536

if __name__ == "__main__":
    if(len(argv) < 3):
        print('usage: make_IC.py theta phi')
        exit(1)
    theta = float(argv[1])
    phi = float(argv[2])
    d0 = 200 #kpc
    v0 = 200 #km/s
    v0 /= 20.7403
    h,g,d,s = rtipsy('mw.tipsy')
    h_new = h.copy()
    h_new['n'] *= 2 
    h_new['ndark'] = 0
    h_new['nstar'] = 2*h['ndark']
    g_new = {}
    d_new = {}
    s_new = {}
    for k in d.keys():
        s_new[k] = np.tile(d[k], 2)
    # set up star properties
    s_new['tform'] = np.ones(s_new['mass'].shape)
    s_new['tform'][:nbulge] -= 1
    s_new['tform'][h['ndark']:h['ndark']+nbulge] -= 1
    s_new['metals'] = np.zeros(s_new['mass'].shape)

    # rotate the second disk
    snap = pyn.snapshot.new(star=h['ndark'])
    snap['x'] = d['x']
    snap['y'] = d['y']
    snap['z'] = d['z']
    snap['vx'] = d['vx']
    snap['vy'] = d['vy']
    snap['vz'] = d['vz']
    snap.rotate_x(theta)
    snap.rotate_z(phi)
    s_new['x'][:h['ndark']] = snap['x']
    s_new['y'][:h['ndark']] = snap['y']
    s_new['z'][:h['ndark']] = snap['z']
    s_new['vx'][:h['ndark']] = snap['vx']
    s_new['vy'][:h['ndark']] = snap['vy']
    s_new['vz'][:h['ndark']] = snap['vz']

    # offset the second disk
    s_new['x'][:h['ndark']] += d0/2
    s_new['x'][h['ndark']:] -= d0/2
    s_new['vx'][:h['ndark']] -= v0/2
    s_new['vx'][h['ndark']:] += v0/2
    s_new['vy'][:h['ndark']] -= 1
    s_new['vy'][h['ndark']:] += 1
    s_new['vz'][:h['ndark']] -= 1
    s_new['vz'][h['ndark']:] += 1
    wtipsy('merger.tipsy', h_new, g_new, d_new, s_new, STANDARD=True)
