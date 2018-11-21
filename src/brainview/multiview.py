"""
Functions to display morphometry data, labels and annotations in 3D on brain surface meshes.

These functions provide multi view, i.e., the scene is visible from different camera perspectives.
"""

import numpy as np
import brainload as bl
import brainload.spatial as st
import mayavi.mlab as mlab
import brainview as bv
import brainview.dev_tools as dt


def multi_view(fig, vert_coords, faces, morphometry_data):
    """
    Experimental, ignore.

    Copy the original mesh, then rotate and translate it to get another view. Fakes a very simple and stupid multi-view in a single view.
    """
    mesh_in_central_position = bv.brain_morphometry_view(fig, vert_coords, faces, morphometry_data)
    x, y, z = st.coords_a2s(vert_coords)

    # Create lateral view
    x1, y1, z1 = st.rotate_3D_coordinates_around_axes(x, y, z, st.deg2rad(90), 0, 0);
    mayavi_mesh_m1 = mlab.triangular_mesh(x1, y1, z1, faces, scalars=morphometry_data, color=(1, 0, 0))
    dt._print_mlab_view()

    x2, y2, z2 = st.rotate_3D_coordinates_around_axes(x, y, z, st.deg2rad(90), 0, 0);
    x2, y2, z2 = st.scale_3D_coordinates(x2, y2, z2, 1.5)
    # = rotate_3D_coordinates_around_axes(x, y, z, rotx, roty, rotz)
    # = scale_3D_coordinates(x, y, z, x_scale_factor, y_scale_factor=None, z_scale_factor=None)
    # = mirror_3D_coordinates_at_axis(x, y, z, axis, mirror_at_axis_coordinate=None)
    # = point_mirror_3D_coordinates(x, y, z, point_x, point_y, point_z):
    x2, y2, z2 = st.translate_3D_coordinates_along_axes(x, y, z, 200, 0, 0)
    mayavi_mesh_m2 = mlab.triangular_mesh(x2, y2, z2, faces, scalars=morphometry_data, color=(0, 0, 1))
    dt._print_mlab_view()
    meshes = [mayavi_mesh_m1, mayavi_mesh_m2]
    return meshes
