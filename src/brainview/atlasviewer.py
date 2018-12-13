#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import numpy as np
import brainload as bl
import mayavi.mlab as mlab
import brainview as bv
import argparse

# To run this in dev mode (in virtual env, pip -e install of brainview active) from REPO_ROOT:
# PYTHONPATH=./src/brainview python src/brainview/atlasviewer.py tim label Median_wall -d ~/data/tim_only/ -i
# PYTHONPATH=./src/brainview python src/brainview/atlasviewer.py tim atlas aparc -d ~/data/tim_only/ -i

def atlasviewer():
    """
    Brain atlas data viewer.

    A viewer for brain atlas and label data. Typically used to inspect cortical parcellation results.
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="View brain label data or brain annotation / atlas  data.")
    parser.add_argument("subject", help="The subject you want to load. String, a directory under the subjects_dir.")
    parser.add_argument("mode", help="The mode. One of ('atlas', 'label').")
    parser.add_argument("data", help="The data to load from the label dub dir of the subject, without the ?h part and the file extensions. If mode is 'atlas', something like 'aparc'. If mode is 'label', something like 'cortex'.")
    parser.add_argument("-s", "--surface", help="The surface to load. String, defaults to 'white'.", default="white")
    parser.add_argument("-d", "--subjects_dir", help="The subjects_dir containing the subject. Defaults to environment variable SUBJECTS_DIR.", default="")
    parser.add_argument("-e", "--hemi", help="The hemisphere to load. One of ('both', 'lh, 'rh'). Defaults to 'both'.", default="both", choices=['lh', 'rh', 'both'])
    parser.add_argument("-i", "--interactive", help="Display brain plot in an interactive window.", action="store_true")
    parser.add_argument("-o", "--outputfile", help="Output image file name. String, defaults to 'brain_<mode>.png'.", default=None)
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
    mode = args.mode
    outputfile = args.outputfile
    if outputfile is None:
        if mode == "label":
            outputfile = "brain_label.png"
        else:
            outputfile = "brain_atlas.png"

    surface = args.surface
    hemi = args.hemi
    data = args.data

    interactive = False
    if args.interactive:
        interactive = True
    mlab.options.offscreen = not interactive

    vert_coords, faces, morphometry_data, morphometry_meta_data = bl.subject(subject_id, subjects_dir=subjects_dir, surf=surface, hemi=hemi, load_morphometry_data=False)
    fig_title = 'Atlasviewer: %s: %s on surface %s' % (subject_id, data, surface)
    cfg, cfg_file = bv.get_config()
    fig = mlab.figure(fig_title, bgcolor=(1, 1, 1), size=(bv.cfg_getint('figure', 'width', 800), bv.cfg_getint('figure', 'height', 600)))

    if mode == 'atlas':
        if verbose:
            print("Loading atlas %s for subject %s from subjects dir %s: displaying on surface %s for hemisphere %s." % (data, subject_id, subjects_dir, surface, hemi))
        vertex_labels, label_colors, label_names, atlas_meta_data = bl.annot(subject_id, subjects_dir, data, hemi=hemi, orig_ids=False)
        brain_mesh = bv.brain_atlas_view(fig, vert_coords, faces, vertex_labels, label_colors, label_names)
    else:
        if verbose:
            print("Loading label %s for subject %s from subjects dir %s: displaying on surface %s for hemisphere %s." % (data, subject_id, subjects_dir, surface, hemi))
        verts_in_label, label_meta_data = bl.label(subject_id, subjects_dir, data, hemi=hemi, meta_data=morphometry_meta_data)
        brain_mesh = bv.brain_label_view(fig, vert_coords, faces, verts_in_label)


    print("Saving brain view to file '%s'..." % (outputfile))
    mlab.savefig(outputfile)
    if interactive:
        if verbose:
            print("Interactive mode set, displaying brain plot in interactive window.")
        bv.show()

    sys.exit(0)


if __name__ == "__main__":
    atlasviewer()
