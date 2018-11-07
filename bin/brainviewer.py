#!/usr/bin/env python
import os
import numpy as np
import brainload as bl
import mayavi.mlab as mlab
import brainview as bv
import argparse

# To run this in dev mode (in virtual env, pip -e install of brainview active) from REPO_ROOT:
# PYTHONPATH=./src/brainview python bin/brainviewer.py tim -d ~/data/tim_only/

def brainviewer():

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="View brains.")
    parser.add_argument("subject", help="The subject you want to load. String, a directory under the subjects_dir.")
    parser.add_argument("-d", "--subjects_dir", help="The subjects_dir containing the subject. Defaults to environment variable SUBJECTS_DIR.", default="")
    parser.add_argument("-m", "--measure", help="The measure to load. String, defaults to 'area'. ", default="area")
    parser.add_argument("-s", "--surface", help="The surface to load. String, defaults to 'white'.", default="white")
    parser.add_argument("-e", "--hemi", help="The hemisphere to load. One of ('both', 'lh, 'rh'). Defaults to 'both'.", default="both")
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
    measure = args.measure
    surface = args.surface
    hemi = args.hemi

    if verbose:
        print("Loading data for subject %s from subjects dir %s: measure %s of surface %s for hemisphere %s." % (subject_id, subjects_dir, measure, surface, hemi))

    vert_coords, faces, morphometry_data, meta_data = bl.subject(subject_id, subjects_dir=subjects_dir, measure=measure, surf=surface, hemi=hemi)

    if verbose:
        if hemi == "lh" or hemi == "both":
            print("Loaded lh surface mesh from file '%s'." % meta_data["lh.surf_file"])
            print("Loaded lh morphometry data from file '%s'." % meta_data["lh.morphometry_file"])
        if hemi == "rh" or hemi == "both":
            print("Loaded rh surface from file '%s'." % meta_data["rh.surf_file"])
            print("Loaded rh morphometry data from file '%s'." % meta_data["rh.morphometry_file"])
        print "Loaded mesh consisting of %d vertices and %d faces. Loaded morphometry data for %d vertices." % (vert_coords.shape[0], faces.shape[0], morphometry_data.shape[0])

    fig_title = 'Brainviewer: %s: %s of surface %s' % (subject_id, measure, surface)
    fig = mlab.figure(fig_title, bgcolor=(1, 1, 1), size=(800, 600))
    brain_mesh = bv.get_brain_view(vert_coords, faces, morphometry_data)
    bv.show()


if __name__ == "__main__":
    brainviewer()
