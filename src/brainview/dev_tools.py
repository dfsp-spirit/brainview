"""
Brainview development functions for debugging.
"""
from __future__ import print_function
import numpy as np
import brainload as bl
import brainload.spatial as st
import mayavi.mlab as mlab


def _print_mlab_view():
    """
    Print the camera properties in the current mlab view.

    See http://docs.enthought.com/mayavi/mayavi/auto/mlab_camera.html#view for details.
    """
    view = mlab.view()
    print("[View] azimuth=%f, elevation=%f, distance=%f" % (view[0], view[1], view[2]))


def _print_data_description(vert_coords, faces, morphometry_data, print_tag="[data]"):
    print("%s #verts=%d #faces=%d" % (print_tag, vert_coords.shape[0], faces.shape[0]))
    print("%s morphometry_data: length=%d min=%f max=%f" % (print_tag, len(morphometry_data), np.min(morphometry_data), np.max(morphometry_data)))


def _activate_overlay(meta_data):
    """
    Display a very simple meta_data overlay in the current view.

    Display various information from the given meta_data dictionary in the view of the currently active mlab figure.

    Parameters
    ----------
    meta_data: dictionary
        A dictionary with meta_data that has been created manually or received from a braibload function when loading the subject data. The entries 'subject_id', 'surf', and 'measure' or accessed to create the overlay text.
    """
    mlab.colorbar()
    mlab.title('Brain of subject ' + meta_data.get('subject_id', '?'), size=0.4)
    mlab.text(0.1, 0.5, meta_data.get('surf', ''), color=(1.0, 0.0, 0.0), width=0.05) # width should be scaled by the number of characters
    mlab.text(0.1, 0.55, meta_data.get('measure', ''), color=(1.0, 0.0, 0.0), width=0.05)
