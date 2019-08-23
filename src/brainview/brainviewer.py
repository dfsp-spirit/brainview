#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import numpy as np
import brainload as bl
import mayavi.mlab as mlab
import brainview as bv
import brainview.export as bex
import argparse

# To run this in dev mode (in virtual env, pip -e install of brainview active) from REPO_ROOT:
# PYTHONPATH=./src/brainview python src/brainview/brainviewer.py tim -d ~/data/tim_only/

def brainviewer():
    """
    Brain morphometry data viewer.

    A viewer for morphometry data. Supports data from the subject itself and subject data that has been mapped to a common subject like fsaverage.
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="View brain morphometry data.")
    parser.add_argument("subject", help="The subject you want to load. String, a directory under the subjects_dir.")
    parser.add_argument("-d", "--subjects_dir", help="The subjects_dir containing the subject. Defaults to environment variable SUBJECTS_DIR.", default="")
    parser.add_argument("-m", "--measure", help="The measure to load. String, defaults to None (no morphometry data). Examples: 'area' or 'thickness'.", default=None)
    parser.add_argument("-s", "--surface", help="The surface to load. String, defaults to 'white'.", default="white")
    parser.add_argument("-e", "--hemi", help="The hemisphere to load. One of ('both', 'lh, 'rh'). Defaults to 'both'.", default="both", choices=['lh', 'rh', 'both'])
    parser.add_argument("-c", "--common-subject-mode", help="Load data mapped to a common or average subject.", action="store_true")
    parser.add_argument("-a", "--average-subject", help="The common or average subject to use. String, defaults to 'fsaverage'. Ignored unless -c is active.", default="fsaverage")
    parser.add_argument("-f", "--fwhm", help="The smoothing or fwhm setting to use for the common subject measure. String, defaults to '10'. Ignored unless -c is active.", default="10")
    parser.add_argument("-i", "--interactive", help="Display brain plot in an interactive window.", action="store_true")
    parser.add_argument("-o", "--outputfile", help="Output image file name. String, defaults to 'brain_morphometry.png'.", default="brain_morphometry.png")
    parser.add_argument("-n", "--no-clip", help="Do not clip morphometry values.", action="store_true")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity.", action="store_true")
    parser.add_argument("-x", "--mesh-export", help="Mesh export output filename. The file extension should be '.obj' or '.ply' to indicate the output format, otherwise obj is used. Optional, if not given at all, then no mesh will be exported.", default="")
    args = parser.parse_args()

    cfg, cfg_file = bv.get_config()
    verbose = False
    if args.verbose:
        verbose = True
        print("Verbosity turned on.")
        if cfg_file is None:
            print("Using internal default configuration. No config file found at '%s'." % bv.get_default_config_filename())
        else:
            print("Using configuration from file: '%s'" % cfg_file)

    if args.subjects_dir == "":
        subjects_dir = os.getenv('SUBJECTS_DIR')
    else:
        subjects_dir = args.subjects_dir

    subject_id = args.subject
    measure = args.measure
    surface = args.surface
    hemi = args.hemi

    interactive = False
    if args.interactive:
        interactive = True
    mlab.options.offscreen = not interactive

    load_morphometry_data = measure is not None

    if args.common_subject_mode:
        fwhm = args.fwhm
        average_subject = args.average_subject
        if verbose:
            print("Loading data mapped to common subject %s for subject %s from subjects dir '%s': measure %s of surface %s for hemisphere %s at fwhm %s." % (average_subject, subject_id, subjects_dir, measure, surface, hemi, fwhm))
        vert_coords, faces, morphometry_data, meta_data = bl.subject_avg(subject_id, subjects_dir=subjects_dir, measure=measure, surf=surface, hemi=hemi, fwhm=fwhm, average_subject=average_subject, load_morphometry_data=load_morphometry_data)
    else:
        if verbose:
            print("Loading data for subject %s from subjects dir '%s': measure %s of surface %s for hemisphere %s." % (subject_id, subjects_dir, measure, surface, hemi))
        vert_coords, faces, morphometry_data, meta_data = bl.subject(subject_id, subjects_dir=subjects_dir, measure=measure, surf=surface, hemi=hemi, load_morphometry_data=load_morphometry_data)

    if not load_morphometry_data:
        if verbose:
            print("No morphometry data loaded, setting all values to zero.")
        morphometry_data = np.zeros((vert_coords.shape[0],), dtype=float)

    morphometry_data = morphometry_data.astype(float)

    if verbose:
        if hemi == "lh" or hemi == "both":
            print("Loaded lh surface mesh from file '%s'." % meta_data["lh.surf_file"])
            if load_morphometry_data:
                print("Loaded lh morphometry data from file '%s'." % meta_data["lh.morphometry_file"])
        if hemi == "rh" or hemi == "both":
            print("Loaded rh surface from file '%s'." % meta_data["rh.surf_file"])
            if load_morphometry_data:
                print("Loaded rh morphometry data from file '%s'." % meta_data["rh.morphometry_file"])
        print("Loaded mesh consisting of %d vertices and %d faces." % (vert_coords.shape[0], faces.shape[0]))
        if load_morphometry_data:
            print("Loaded morphometry data for %d vertices." % (morphometry_data.shape[0]))

    fig_title = 'Brainviewer: %s: %s of surface %s' % (subject_id, measure, surface)

    if args.mesh_export != "":
        colormap_name = bv.cfg_get('meshexport', 'colormap', 'viridis')
        colormap_adjust_alpha_to = bv.cfg_getint('meshexport', 'colormap_adjust_alpha_to', -1)
        clip_values_export = bv.cfg_getboolean('meshexport', 'clip_values', True)
        if clip_values_export and not args.no_clip:
            clip_values_lower = bv.cfg_getint('meshexport', 'clip_values_lower', 5)
            clip_values_upper = bv.cfg_getint('meshexport', 'clip_values_upper', 95)
            print("Clipping exported values below percentile %d and above %d." % (clip_values_lower, clip_values_upper))
            morphometry_data_for_export = bex.clip_data_at_percentiles(morphometry_data, lower=clip_values_lower, upper=clip_values_upper)
        else:
            morphometry_data_for_export = morphometry_data
        print("Exporting brain mesh to file '%s'..." % args.mesh_export)
        bv.export_mesh_to_file(args.mesh_export, vert_coords, faces, morphometry_data=morphometry_data_for_export, colormap_name=colormap_name, colormap_adjust_alpha_to=colormap_adjust_alpha_to)

    fig = mlab.figure(fig_title, bgcolor=(1, 1, 1), size=(bv.cfg_getint('figure', 'width', 800), bv.cfg_getint('figure', 'height', 600)))
    mesh_args = {'representation': bv.cfg_get('mesh', 'representation', 'surface'), 'colormap': bv.cfg_get('mesh', 'colormap', 'cool')}
    clip_values_live = bv.cfg_getboolean('mesh', 'clip_values', True)
    if clip_values_live and not args.no_clip:
        clip_values_lower = bv.cfg_getint('mesh', 'clip_values_lower', 5)
        clip_values_upper = bv.cfg_getint('mesh', 'clip_values_upper', 95)
        print("Clipping visualized values below percentile %d and above %d." % (clip_values_lower, clip_values_upper))
        morphometry_data_live = bex.clip_data_at_percentiles(morphometry_data, lower=clip_values_lower, upper=clip_values_upper)
    else:
        morphometry_data_live = morphometry_data
    brain_mesh = bv.brain_morphometry_view(fig, vert_coords, faces, morphometry_data_live, **mesh_args)
    print("Saving brain view to image file '%s'..." % (args.outputfile))
    mlab.savefig(args.outputfile)
    if interactive:
        if verbose:
            print("Interactive mode set, displaying brain plot in interactive window.")
        bv.show()

    sys.exit(0)


if __name__ == "__main__":
    brainviewer()
