#!/usr/bin/env python
import os
import numpy as np
import brainload as bl
import mayavi.mlab as mlab
import brainview as bv
import argparse

# To run this in dev mode (in virtual env, pip -e install of brainview active):
# cd REPO_ROOT
# PYTHONPATH=./src/brainview python bin/brainviewer.py --help

def brainviewer():

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="View brains.")
    parser.add_argument("subject", help="The subject you want to load. Directory name in the subjects_dir.")
    parser.add_argument("-d", "--subjects_dir", help="The subjects_dir containing the subject.", default="")
    parser.add_argument("-m", "--measure", help="The measure to load.", default="area")
    parser.add_argument("-s", "--surface", help="The surface to load.", default="white")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity.", action="store_true")
    args = parser.parse_args()

    verbose = False
    if args.verbose:
        verbose = True
        print("Verbosity turned on.")

    if args.subjects_dir == "":
        subjects_dir = os.getenv('SUBJECTS_DIR')
    else:
        subjects_dir = args.subjects_dir

    subject_id = args.subject

    vert_coords, faces, morphometry_data, meta_data = bl.subject(subject_id, subjects_dir=subjects_dir)

    fig = mlab.figure(1, bgcolor=(1, 1, 1), size=(800, 600))
    brain_mesh = sv.get_brain_view(vert_coords, faces, morphometry_data)
    bv.show()


if __name__ == "__main__":
    brainviewer()
