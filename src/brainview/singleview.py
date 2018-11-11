"""
Functions to display morphometry data in 3D on brain surface meshes.

These functions provide a single view.
"""

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
    print "[View] azimuth=%f, elevation=%f, distance=%f" % (view[0], view[1], view[2])


def _get_surface_from_mlab_triangular_mesh(vert_coords, faces, **kwargs):
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


def _get_surface_from_mlab_triangular_mesh_source(vert_coords, faces, morphometry_data, **kwargs):
    """
    Load the data as a surface based on a triangular_mesh_source.

    Load the mesh as an `mlab.pipeline.triangular_mesh_source`. This is inspired by what is done in the _Hemisphere class of PySurfer. It was needed because when I used `mlab.triangular_mesh`, the colors were broken for some meshes.
    """
    kwargs_mesh_source = {'scalars': morphometry_data}
    kwargs_surface = {'colormap': 'cool'}
    x, y, z = st.coords_a2s(vert_coords)
    src_mesh = mlab.pipeline.triangular_mesh_source(x, y, z, faces, **kwargs_mesh_source)
    src_mesh.data.points = vert_coords
    src_mesh.data.cell_data.normals = None
    surf = mlab.pipeline.surface(src_mesh, reset_zoom=True, **kwargs_surface)
    surf.actor.property.backface_culling = True

    # set color LUT manually, see http://docs.enthought.com/mayavi/mayavi/auto/example_custom_colormap.html
    lut = surf.module_manager.scalar_lut_manager.lut.table.to_array()

    # The lut is a 255x4 array, with the columns representing RGBA
    # (red, green, blue, alpha) coded with integers going from 0 to 255.

    # We modify the alpha channel to add a transparency gradient
    lut[:, -1] = np.linspace(0, 255, 256)
    # and finally we put this LUT back in the surface object. We could have
    # added any 255*4 array rather than modifying an existing LUT.
    surf.module_manager.scalar_lut_manager.lut.table = lut
    mlab.draw()


def get_brain_view(vert_coords, faces, morphometry_data, **kwargs):
    """
    Create a mayavi mesh from data.

    Create a mayavi mesh from the vert_coords, faces and morphometry_data. Additional keyword arguments will be passed on to the call to the mlab.triangular_mesh function.

    Parameters
    ----------
    vert_coords: 2D numpy array of shape (n_verts, 3)
        An array of vertex corrdinates. Each vertex position is identified by an x, y, and z coordinate.

    faces: 2D numpy array of shape (n_faces, 3)
        An array of 3-faces, i.e., each face has to consists of 3 vertices. The 3 vertices are indices into the vert_coords array.

    morphometry_data: 1D numpy array of shape (n_verts, )
        Assigns a scalar value to each vertex.

    kwargs: extra keyword arguments
        Will be passed on to the call to the mayavi mesh function.

    Returns
    -------
    surface: mayavi.modules.surface.Surface
        The resulting surface. It gets added to the current scene by default and potentially triggers actions in there (like camera re-orientation), use kwargs to change that behaviour.
    """
    print "min=%f max=%f" % (np.min(morphometry_data), np.max(morphometry_data))
    #return _get_mayavi_mesh(vert_coords, faces, scalars=morphometry_data, **kwargs)
    return _get_surface_from_mlab_triangular_mesh_source(vert_coords, faces, morphometry_data, **kwargs)


def activate_overlay(meta_data):
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


def export_figure(fig_handle, export_file_name_with_extension, silent=False, **kwargs):
    """
    Export the view of the scene to an image file.

    Export the figure identified by the given fig_handle to the file. File must be valid path to a writable location, and the file extension must be one that is supported by `mlab.savefig`.

    Parameters
    ----------
    fig_handle: mlab figure handle
        Handle for the figure

    export_file_name_with_extension: string
        Path to a file, the extension determines the output format. Example: '/tmp/brain.png'

    silent: bool, optional
        Whether to be silent, i.e., NOT print a message to stdout that informs the user of the location where the file was saved. Defaults to False.

    **kwargs: any keyword arguments, optional
        Will be passed on to the call to `mlab.savefig`.

    """
    if not silent:
        print "Exporting scene to file '%s'." % export_file_name_with_extension
    mlab.savefig(export_image_file, figure=fig_handle, **kwargs)


def show():
    """
    Display the currently active mayavi scene in an interactive window.

    Render and display the currently active mayavi scene in an interactive window. This requires a GUI and a working setup of matplotlib with proper backend configuration on the machine. Currently does nothing but to call `mlab.show()`.
    """
    mlab.show()


def _get_brain_multi_view(vert_coords, faces, morphometry_data):
    """
    Experimental, ignore.

    Copy the original mesh, then rotate and translate it to get another view. Fakes a very simple and stupid multi-view in a single view.
    """
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
