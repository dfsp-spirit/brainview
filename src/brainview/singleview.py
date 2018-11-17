"""
Functions to display morphometry data, labels and annotations in 3D on brain surface meshes.

These functions provide a single view, i.e., the scene is visible from a single camera perspective.
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


def _print_data_description(vert_coords, faces, morphometry_data, print_tag="[data]"):
    print "%s #verts=%d #faces=%d" % (print_tag, vert_coords.shape[0], faces.shape[0])
    print "%s morphometry_data: length=%d min=%f max=%f" % (print_tag, len(morphometry_data), np.min(morphometry_data), np.max(morphometry_data))


def brain_label_view(fig, vert_coords, faces, verts_in_label):
    """
    View the vertices which are part of a label.

    View the vertices which are part of a label. A label is a nothing but a set of vertices.

    Parameters
    ----------
    fig: figure handle
        The figure the surface should be added to

    vert_coords: 2D numpy array of shape (n_verts, 3)
        An array of vertex corrdinates. Each vertex position is identified by an x, y, and z coordinate.

    faces: 2D numpy array of shape (n_faces, 3)
        An array of 3-faces, i.e., each face has to consists of 3 vertices. The 3 vertices are indices into the vert_coords array.

    verts_in_label: ndarray, shape (m_vertices,)
        An array containing the indices of all vertices which are part of the label. All other vertices are assumed not to be part of the label.

    Returns
    -------
    surface: mayavi.modules.surface.Surface
        The resulting surface. It gets added to the current scene by default and potentially triggers actions in there (like camera re-orientation), use kwargs to change that behaviour.

    Examples
    --------
    Load a label file using brainload and visualize it on the surface mesh of a subject:

    >>> import brainload as bl; import brainview as bv; import os
    >>> subjects_dir = os.getenv('SUBJECTS_DIR')   # or whatever
    >>> subject = 'subject1'
    >>> vert_coords, faces, morphometry_data, morphometry_meta_data = bl.subject(subject, subjects_dir=subjects_dir, load_morphometry_data=False)      # load mesh
    >>> verts_in_label, label_meta_data = bl.label(subject, subjects_dir, 'Medial_wall', meta_data=morphometry_meta_data)                               # load label
    >>> fig = mlab.figure('Some title', bgcolor=(1, 1, 1), size=(800, 600))             # create figure and scene
    >>> surface = bv.brain_label_view(fig, vert_coords, faces, verts_in_label)          # create an mlab mesh and add it to the scene
    >>> bv.show()                                                                       # open figure in interactive window

    This will get you a view of the labels on the brain mesh of the subject.
    """
    num_verts = vert_coords.shape[0]
    num_verts_in_label = len(verts_in_label)
    # create fake morphometry data from the label: set all values for vertices in the label to 1.0, the rest to 0.0
    label_map = np.zeros((num_verts), dtype=float)
    label_map[verts_in_label] = 1.0
    return brain_morphometry_view(fig, vert_coords, faces, label_map)


def _brain_atlas_view_simple(fig, vert_coords, faces, vertex_labels, label_names):
    """
    View the vertices which are part of an annotation, usually a brain atlas.

    View the vertices which are part of an annotation, usually a brain atlas. An atlas consists of several sets of vertices, each of which is assigned a color and a label. This simple version just assigns random colors to each set, ignoring the given color list.

    Parameters
    ----------
    fig: figure handle
        The figure the surface should be added to

    vert_coords: 2D numpy array of shape (n_verts, 3)
        An array of vertex corrdinates. Each vertex position is identified by an x, y, and z coordinate.

    faces: 2D numpy array of shape (n_faces, 3)
        An array of 3-faces, i.e., each face has to consists of 3 vertices. The 3 vertices are indices into the vert_coords array.

    vertex_labels: ndarray, shape (n_vertices,)
        An array containing the index (for each vertex) into the label_colors and label_names datastructures to retrieve the color and name. If some vertex has no annotation, -1 must be set for it.False.)

    label_names: list of strings
       The names of the labels. The length of the list is n_labels.

    Returns
    -------
    surface: mayavi.modules.surface.Surface
        The resulting surface. It gets added to the current scene by default and potentially triggers actions in there (like camera re-orientation), use kwargs to change that behaviour.
    """
    num_verts = vert_coords.shape[0]
    num_labels = len(label_names)
    # create fake morphometry data from the label: set all values for vertices in the label to 1.0, the rest to 0.0
    label_map = np.zeros((num_verts), dtype=float)
    for idx, value in enumerate(label_names):
        label_map[vertex_labels == idx] = (idx + 1.0)
    return brain_morphometry_view(fig, vert_coords, faces, label_map)


def brain_atlas_view(fig, vert_coords, faces, vertex_labels, label_colors, label_names):
    """
    View the vertices which are part of an annotation using the annotation colors.

    View the vertices which are part of an annotation, usually a brain atlas. An atlas consists of several sets of vertices, each of which is assigned a color and a label. This version uses the color list.

    Parameters
    ----------
    fig: figure handle
        The figure the surface should be added to

    vert_coords: 2D numpy array of shape (n_verts, 3)
        An array of vertex corrdinates. Each vertex position is identified by an x, y, and z coordinate.

    faces: 2D numpy array of shape (n_faces, 3)
        An array of 3-faces, i.e., each face has to consists of 3 vertices. The 3 vertices are indices into the vert_coords array.

    vertex_labels: ndarray, shape (n_vertices,)
        An array containing the index (for each vertex) into the label_colors and label_names datastructures to retrieve the color and name. If some vertex has no annotation, -1 must be set for it.False.)

    label_colors: ndarray, shape (n_labels, 4)
        RGBT + label id colortable array. The first 4 values encode the label color: RGB is red, green, blue as usual, from 0 to 255 per value. T is the transparency, which is defined as 255 - alpha. If the array has more than 4 entries, all others are ignored.

    label_names: list of strings
       The names of the labels. The length of the list is n_labels.

    Returns
    -------
    surface: mayavi.modules.surface.Surface
        The resulting surface. It gets added to the current scene by default and potentially triggers actions in there (like camera re-orientation), use kwargs to change that behaviour.

    Examples
    --------
    Load an annotation file using brainload and visualize it on the surface mesh of a subject. In this case, we are loading the cortical parcellation based on the Desikan atlas:

    >>> import brainload as bl; import brainview as bv; import os
    >>> subjects_dir = os.getenv('SUBJECTS_DIR')   # or whatever
    >>> subject = 'subject1'
    >>> vert_coords, faces, morphometry_data, morphometry_meta_data = bl.subject(subject, subjects_dir=subjects_dir, load_morphometry_data=False)      # load mesh
    >>> vertex_labels, label_colors, label_names, atlas_meta_data = bl.annot(subject, subjects_dir, 'aparc')                 # load annotation
    >>> fig = mlab.figure('Some title', bgcolor=(1, 1, 1), size=(800, 600))                                     # create figure and scene
    >>> surface = bv.brain_atlas_view(fig, vert_coords, faces, vertex_labels, label_colors, label_names)     # create an mlab mesh and add it to the scene
    >>> bv.show()                                                                                               # open figure in interactive window

    This will get you a view of the annotation on the brain mesh of the subject.
    """
    num_verts = vert_coords.shape[0]
    num_labels = len(label_names)
    label_map = np.zeros((num_verts), dtype=float)
    lut = np.ones((num_labels, 4), dtype=int)       # create color lookup table
    for idx, value in enumerate(label_names):
        label_map[vertex_labels == idx] = (idx + 1.0)
        lut[idx, 0:3] = label_colors[idx][0:3]      # Set RGB values.
        lut[idx, 3] = 255 - label_colors[idx][3]    # Set alpha channel: this is stored as a transparency in the source data, so we convert it to alpha.
    surf = brain_morphometry_view(fig, vert_coords, faces, label_map)

    lut_manager = surf.module_manager.scalar_lut_manager
    lut_manager.lut.table = lut         # use our lut

    fig.render()
    mlab.draw()


def brain_morphometry_view(fig, vert_coords, faces, morphometry_data, **kwargs):
    """
    Create a surface from the mesh and morphometry data.

    Create an mlab surface from the vert_coords, faces and morphometry_data. Additional keyword arguments will be passed on to the call to the `mlab.triangular_mesh` function.

    Parameters
    ----------
    fig: figure handle
        The figure the surface should be added to

    vert_coords: 2D numpy array of shape (n_verts, 3)
        An array of vertex corrdinates. Each vertex position is identified by an x, y, and z coordinate.

    faces: 2D numpy array of shape (n_faces, 3)
        An array of 3-faces, i.e., each face has to consists of 3 vertices. The 3 vertices are indices into the vert_coords array.

    morphometry_data: 1D numpy array of shape (n_verts, )
        Assigns a scalar value to each vertex.

    kwargs: extra keyword arguments
        Will be passed on to the call to the `mlab.triangular_mesh` function from Mayavi.

    Returns
    -------
    surface: mayavi.modules.surface.Surface
        The resulting surface. It gets added to the current scene by default and potentially triggers actions in there (like camera re-orientation), use kwargs to change that behaviour.

    Examples
    --------
    Load cortical thickness data for a subject and visualize it:

    >>> import brainload as bl; import brainview as bv; import os
    >>> subjects_dir = os.getenv('SUBJECTS_DIR')   # or whatever
    >>> subject = 'subject1'
    >>> vert_coords, faces, morphometry_data, morphometry_meta_data = bl.subject(subject, subjects_dir=subjects_dir, measure='thickness')      # load mesh and morphometry data
    >>> fig = mlab.figure('Some title', bgcolor=(1, 1, 1), size=(800, 600))                                     # create figure and scene
    >>> surface = bv.brain_morphometry_view(fig, vert_coords, faces, vertex_labels, morphometry_data)        # create an mlab mesh and add it to the scene
    >>> bv.show()                                                                                               # open figure in interactive window

    This will get you a view of the morphometry data on the brain mesh of the subject.
    """
    morphometry_data = morphometry_data.astype(float)
    return _get_surface_from_mlab_triangular_mesh(vert_coords, faces, scalars=morphometry_data, **kwargs)


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

    Examples
    --------
    Export a figure to a PNG file in the current working directory:

    >>> fig = ...
    >>> bv.export_figure('brain.png', figure=fig)
    """
    if not silent:
        print "Exporting scene to file '%s'." % export_file_name_with_extension
    mlab.savefig(export_image_file, figure=fig_handle, **kwargs)


def show():
    """
    Display the currently active Mayavi scene in an interactive window.

    Render and display the currently active mayavi scene in an interactive window. This requires a GUI and a working setup of matplotlib with proper backend configuration on the machine. Currently does nothing but to call `mlab.show()`.

    Examples
    --------
    >>> ...
    >>> fig = mlab.figure('Some title', bgcolor=(1, 1, 1), size=(800, 600))     # create a figure
    >>> surface = bv.brain_label_view(fig, vert_coords, faces, verts_in_label)  # add something to the current scene, optional
    >>> bv.show()
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
