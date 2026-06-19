#!/usr/bin/env python
import argparse
import numpy as np
import pynbody as pyn
from pytipsy import rtipsy, wtipsy
from util import setup_rundir

nbulge = 65536

if __name__ == "__main__":
    # 1. Set up the argument parser with help text and boundaries
    parser = argparse.ArgumentParser(
        description="Build initial conditions for an isolated galaxy with added velocity dispersion.",
        epilog="Example: ./make_single.py 50"
    )

    # Required positional arguments (the angles)
    parser.add_argument("sigma", type=float,
                        help="Random velocity dispersion (in km/s)")

    # Optional arguments 
    parser.add_argument("--name", type=str, default="single",
                        help="Unique name for this experiment directory and files [Default: single]")

    args = parser.parse_parser_args() if hasattr(parser, 'parse_parser_args') else parser.parse_args()

    factor = float(args.sigma)/20.7403
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

    setup_rundir(args.name, h_new, g_new, d_new, s_new)
