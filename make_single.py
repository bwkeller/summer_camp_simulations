#!/usr/bin/env python
from sys import argv
import numpy as np
import pynbody as pyn
from pytipsy import rtipsy, wtipsy

nbulge = 65536

if __name__ == "__main__":
    if(len(argv) < 2):
        print('usage: make_single.py velocity_dispersion')
        exit(1)
    factor = float(argv[1])/20.7403
    h,g,d,s = rtipsy('mw.tipsy')
    h_new = h.copy()
    h_new['ndark'] = 0
    h_new['nstar'] = h['ndark']
    g_new = {}
    d_new = {}
    s_new = {}
    for k in d.keys():
        s_new[k] = d[k]
    # set up star properties
    s_new['tform'] = np.ones(s_new['mass'].shape)
    s_new['tform'][:nbulge] -= 1
    s_new['metals'] = np.zeros(s_new['mass'].shape)

    # Introduce velocity noise
    s_new['vx'] = np.random.normal(loc=s_new['vx'], scale=factor/np.sqrt(3))
    s_new['vy'] = np.random.normal(loc=s_new['vy'], scale=factor/np.sqrt(3))
    s_new['vz'] = np.random.normal(loc=s_new['vz'], scale=factor/np.sqrt(3))

    wtipsy('single.tipsy', h_new, g_new, d_new, s_new, STANDARD=True)
