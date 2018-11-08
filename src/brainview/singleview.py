"""
Functions to display morphometry data in 3D on brain surface meshes.

These functions provide a single view.
"""

import mayavi.mlab as mlab
import numpy as np
import brainload as bl
import brainload.spatial as st


def _print_mlab_view():
    '''See http://docs.enthought.com/mayavi/mayavi/auto/mlab_camera.html#view for details.'''
    view = mlab.view()
    print "[View] azimuth=%f, elevation=%f, distance=%f" % (view[0], view[1], view[2])


def _get_mayavi_mesh(vert_coords, faces, **kwargs):
    """
    Creates a mayavi mesh from the vert_coords and faces. All extra arguments are passed to the mlab.triangular_mesh call.

    Returns
    -------
    surface: mayavi.modules.surface.Surface

    Examples
    --------
    my_mesh = _get_mayavi_mesh(vert_coords, faces, scalars=morphometry_data, color=(1, 0, 0))
    """
    x, y, z = st.coords_a2s(vert_coords)
    mayavi_mesh = mlab.triangular_mesh(x, y, z, faces, **kwargs)
    return mayavi_mesh


def get_brain_view(vert_coords, faces, morphometry_data, **kwargs):
    """
    Convenience wrapper around _get_mayavi_mesh. Creates a mayavi mesh from the vert_coords, faces and morphometry_data.

    Returns
    -------
    surface: mayavi.modules.surface.Surface
    """
    print "min=%d max=%d" % (np.min(morphometry_data), np.max(morphometry_data))
    return _get_mayavi_mesh(vert_coords, faces, scalars=morphometry_data, **kwargs)


def activate_overlay(meta_data):
    """
    Displays various information from the given meta_data dictionary in the view of the currently active mlab figure.
    """
    mlab.colorbar()
    mlab.title('Brain of subject ' + meta_data.get('subject_id', '?'), size=0.4)
    mlab.text(0.1, 0.5, meta_data.get('surf', ''), color=(1.0, 0.0, 0.0), width=0.05) # width should be scaled by the number of characters
    mlab.text(0.1, 0.55, meta_data.get('measure', ''), color=(1.0, 0.0, 0.0), width=0.05)


def export_figure(fig_handle, export_file_name_with_extension, silent=False, **kwargs):
    """
    Exports the figure identified by the given fig_handle to the file. File must be valid path to a writable location, and the file extension must be one that is supported by mlab.savefig.
    """
    if not silent:
        print "Exporting scene to file '%s'." % export_file_name_with_extension
        mlab.savefig(export_image_file, figure=fig_handle, **kwargs)


def show():
    """
    Renders and displays the currently active mayavi scene in an interactive window.
    This requires a GUI and a working setup of matplotlib with proper backend configuration on the machine.
    """
    mlab.show()


def get_brain_multi_view(vert_coords, faces, morphometry_data):
    mesh_center = get_brain_view(vert_coords, faces, morphometry_data)
    x, y, z = st.coords_a2s(vert_coords)

    # Create lateral view
    x1, y1, z1 = st.rotate_3D_coordinates_around_axes(x, y, z, deg2rad(90), 0, 0);
    mayavi_mesh_m1 = mlab.triangular_mesh(x1, y1, z1, faces, scalars=morphometry_data, color=(1, 0, 0))
    _print_mlab_view()

    x2, y2, z2 = st.rotate_3D_coordinates_around_axes(x, y, z, deg2rad(90), 0, 0);
    x2, y2, z2 = st.scale_3D_coordinates(x2, y2, z2, 1.5)
    # = rotate_3D_coordinates_around_axes(x, y, z, rotx, roty, rotz)
    # = scale_3D_coordinates(x, y, z, x_scale_factor, y_scale_factor=None, z_scale_factor=None)
    # = mirror_3D_coordinates_at_axis(x, y, z, axis, mirror_at_axis_coordinate=None)
    # = point_mirror_3D_coordinates(x, y, z, point_x, point_y, point_z):
    x2, y2, z2 = st.translate_3D_coordinates_along_axes(x, y, z, 200, 0, 0)
    mayavi_mesh_m2 = mlab.triangular_mesh(x2, y2, z2, faces, scalars=morphometry_data, color=(0, 0, 1))
    _print_mlab_view()
